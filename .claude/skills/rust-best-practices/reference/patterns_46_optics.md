# Functional Optics

Source: https://rust-unofficial.github.io/patterns/

# Functional Language Optics

Optics is a type of API design that is common to functional languages. This is a
pure functional concept that is not frequently used in Rust.

Nevertheless, exploring the concept may be helpful to understand other patterns
in Rust APIs, such asvisitors. They also
have niche use cases.

This is quite a large topic, and would require actual books on language design
to fully get into its abilities. However their applicability in Rust is much
simpler.

To explain the relevant parts of the concept, theSerde-API will be used as an
example, as it is one that is difficult for many to understand from simply the
API documentation.

In the process, different specific patterns, called Optics, will be covered.
These areThe Iso,The Poly Iso, andThe Prism.

## An API Example: Serde

Trying to understand the waySerdeworks by only reading the API is a
challenge, especially the first time. Consider theDeserializertrait,
implemented by any library which parses a new data format:

```rust
pub trait Deserializer<'de>: Sized {
    type Error: Error;

    fn deserialize_any<V>(self, visitor: V) -> Result<V::Value, Self::Error>
    where
        V: Visitor<'de>;

    fn deserialize_bool<V>(self, visitor: V) -> Result<V::Value, Self::Error>
    where
        V: Visitor<'de>;

    // remainder omitted
}
```

And here’s the definition of theVisitortrait passed in generically:

```rust
pub trait Visitor<'de>: Sized {
    type Value;

    fn visit_bool<E>(self, v: bool) -> Result<Self::Value, E>
    where
        E: Error;

    fn visit_u64<E>(self, v: u64) -> Result<Self::Value, E>
    where
        E: Error;

    fn visit_str<E>(self, v: &str) -> Result<Self::Value, E>
    where
        E: Error;

    // remainder omitted
}
```

There is a lot of type erasure going on here, with multiple levels of associated
types being passed back and forth.

But what is the big picture? Why not just have theVisitorreturn the pieces
the caller needs in a streaming API, and call it a day? Why all the extra
pieces?

One way to understand it is to look at a functional languages concept calledoptics.

This is a way to do composition of behavior and proprieties that is designed to
facilitate patterns common to Rust: failure, type transformation, etc.1

The Rust language does not have very good support for these directly. However,
they appear in the design of the language itself, and their concepts can help to
understand some of Rust’s APIs. As a result, this attempts to explain the
concepts with the way Rust does it.

This will perhaps shed light on what those APIs are achieving: specific
properties of composability.

## Basic Optics

### The Iso

The Iso is a value transformer between two types. It is extremely simple, but a
conceptually important building block.

As an example, suppose that we have a custom Hash table structure used as a
concordance for a document.2It uses strings for keys (words) and a list of
indexes for values (file offsets, for instance).

A key feature is the ability to serialize this format to disk. A “quick and
dirty” approach would be to implement a conversion to and from a string in JSON
format. (Errors are ignored for the time being, they will be handled later.)

To write it in a normal form expected by functional language users:

```text
case class ConcordanceSerDe {
  serialize: Concordance -> String
  deserialize: String -> Concordance
}
```

The Iso is thus a pair of functions which convert values of different types:serializeanddeserialize.

A straightforward implementation:

```rust
#![allow(unused)]
fn main() {
use std::collections::HashMap;

struct Concordance {
    keys: HashMap<String, usize>,
    value_table: Vec<(usize, usize)>,
}

struct ConcordanceSerde {}

impl ConcordanceSerde {
    fn serialize(value: Concordance) -> String {
        todo!()
    }
    // invalid concordances are empty
    fn deserialize(value: String) -> Concordance {
        todo!()
    }
}
}
```

This may seem rather silly. In Rust, this type of behavior is typically done
with traits. After all, the standard library hasFromStrandToStringin it.

But that is where our next subject comes in: Poly Isos.

### Poly Isos

The previous example was simply converting between values of two fixed types.
This next block builds upon it with generics, and is more interesting.

Poly Isos allow an operation to be generic over any type while returning a
single type.

This brings us closer to parsing. Consider what a basic parser would do ignoring
error cases. Again, this is its normal form:

```text
case class Serde[T] {
    deserialize(String) -> T
    serialize(T) -> String
}
```

Here we have our first generic, the typeTbeing converted.

In Rust, this could be implemented with a pair of traits in the standard
library:FromStrandToString. The Rust version even handles errors:

```rust
pub trait FromStr: Sized {
    type Err;

    fn from_str(s: &str) -> Result<Self, Self::Err>;
}

pub trait ToString {
    fn to_string(&self) -> String;
}
```

Unlike the Iso, the Poly Iso allows application of multiple types, and returns
them generically. This is what you would want for a basic string parser.

At first glance, this seems like a good option for writing a parser. Let’s see
it in action:

```rust
use anyhow;

use std::str::FromStr;

struct TestStruct {
    a: usize,
    b: String,
}

impl FromStr for TestStruct {
    type Err = anyhow::Error;
    fn from_str(s: &str) -> Result<TestStruct, Self::Err> {
        todo!()
    }
}

impl ToString for TestStruct {
    fn to_string(&self) -> String {
        todo!()
    }
}

fn main() {
    let a = TestStruct {
        a: 5,
        b: "hello".to_string(),
    };
    println!("Our Test Struct as JSON: {}", a.to_string());
}
```

That seems quite logical. However, there are two problems with this.

First,to_stringdoes not indicate to API users, “this is JSON.” Every type
would need to agree on a JSON representation, and many of the types in the Rust
standard library already don’t. Using this is a poor fit. This can easily be
resolved with our own trait.

But there is a second, subtler problem: scaling.

When every type writesto_stringby hand, this works. But if every single
person who wants their type to be serializable has to write a bunch of code –
and possibly different JSON libraries – to do it themselves, it will turn into
a mess very quickly!

The answer is one of Serde’s two key innovations: an independent data model to
represent Rust data in structures common to data serialization languages. The
result is that it can use Rust’s code generation abilities to create an
intermediary conversion type it calls aVisitor.

This means, in normal form (again, skipping error handling for simplicity):

```text
case class Serde[T] {
    deserialize: Visitor[T] -> T
    serialize: T -> Visitor[T]
}

case class Visitor[T] {
    toJson: Visitor[T] -> String
    fromJson: String -> Visitor[T]
}
```

The result is one Poly Iso and one Iso (respectively). Both of these can be
implemented with traits:

```rust
#![allow(unused)]
fn main() {
trait Serde {
    type V;
    fn deserialize(visitor: Self::V) -> Self;
    fn serialize(self) -> Self::V;
}

trait Visitor {
    fn to_json(self) -> String;
    fn from_json(json: String) -> Self;
}
}
```

Because there is a uniform set of rules to transform Rust structures to the
independent form, it is even possible to have code generation creating theVisitorassociated with typeT:

```rust
#[derive(Default, Serde)] // the "Serde" derive creates the trait impl block
struct TestStruct {
    a: usize,
    b: String,
}

// user writes this macro to generate an associated visitor type
generate_visitor!(TestStruct);
```

But let’s actually try that approach.

```rust
fn main() {
    let a = TestStruct { a: 5, b: "hello".to_string() };
    let a_data = a.serialize().to_json();
    println!("Our Test Struct as JSON: {a_data}");
    let b = TestStruct::deserialize(
        generated_visitor_for!(TestStruct)::from_json(a_data));
}
```

It turns out that the conversion isn’t symmetric after all! On paper it is, but
with the auto-generated code the name of the actual type necessary to convert
all the way fromStringis hidden. We’d need some kind ofgenerated_visitor_for!macro to obtain the type name.

It’s wonky, but it works… until we get to the elephant in the room.

The only format currently supported is JSON. How would we support more formats?

The current design requires completely re-writing all of the code generation and
creating a new Serde trait. That is quite terrible and not extensible at all!

In order to solve that, we need something more powerful.

## Prism

To take format into account, we need something in normal form like this:

```text
case class Serde[T, F] {
    serialize: T, F -> String
    deserialize: String, F -> Result[T, Error]
}
```

This construct is called a Prism. It is “one level higher” in generics than Poly
Isos (in this case, the “intersecting” type F is the key).

Unfortunately becauseVisitoris a trait (since each incarnation requires its
own custom code), this would require a kind of generic type boundary that Rust
does not support.

Fortunately, we still have thatVisitortype from before. What is theVisitordoing? It is attempting to allow each data structure to define the way
it is itself parsed.

Well what if we could add one more interface for the generic format? Then theVisitoris just an implementation detail, and it would “bridge” the two APIs.

In normal form:

```text
case class Serde[T] {
    serialize: F -> String
    deserialize F, String -> Result[T, Error]
}

case class VisitorForT {
    build: F, String -> Result[T, Error]
    decompose: F, T -> String
}

case class SerdeFormat[T, V] {
    toString: T, V -> String
    fromString: V, String -> Result[T, Error]
}
```

And what do you know, a pair of Poly Isos at the bottom which can be implemented
as traits!

Thus we have the Serde API:

- Each type to be serialized implementsDeserializeorSerialize,
equivalent to theSerdeclass
- They get a type (well two, one for each direction) implementing theVisitortrait, which is usually (but not always) done through code generated by a
derive macro. This contains the logic to construct or destruct between the
data type and the format of the Serde data model.
- The type implementing theDeserializertrait handles all details specific
to the format, being “driven by” theVisitor.
This splitting and Rust type erasure is really to achieve a Prism through
indirection.

You can see it on theDeserializertrait

```rust
pub trait Deserializer<'de>: Sized {
    type Error: Error;

    fn deserialize_any<V>(self, visitor: V) -> Result<V::Value, Self::Error>
    where
        V: Visitor<'de>;

    fn deserialize_bool<V>(self, visitor: V) -> Result<V::Value, Self::Error>
    where
        V: Visitor<'de>;

    // remainder omitted
}
```

And the visitor:

```rust
pub trait Visitor<'de>: Sized {
    type Value;

    fn visit_bool<E>(self, v: bool) -> Result<Self::Value, E>
    where
        E: Error;

    fn visit_u64<E>(self, v: u64) -> Result<Self::Value, E>
    where
        E: Error;

    fn visit_str<E>(self, v: &str) -> Result<Self::Value, E>
    where
        E: Error;

    // remainder omitted
}
```

And the traitDeserializeimplemented by the macros:

```rust
pub trait Deserialize<'de>: Sized {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>;
}
```

This has been abstract, so let’s look at a concrete example.

How does actual Serde deserialize a bit of JSON intostruct Concordancefrom
earlier?

- The user would call a library function to deserialize the data. This would
create aDeserializerbased on the JSON format.
- Based on the fields in the struct, aVisitorwould be created (more on that
in a moment) which knows how to create each type in a generic data model that
was needed to represent it:Vec(list),u64andString.
- The deserializer would make calls to theVisitoras it parsed items.
- TheVisitorwould indicate if the items found were expected, and if not,
raise an error to indicate deserialization has failed.
For our very simple structure above, the expected pattern would be:

- Begin visiting a map (Serde’s equivalent toHashMapor JSON’s
dictionary).
- Visit a string key called “keys”.
- Begin visiting a map value.
- For each item, visit a string key then an integer value.
- Visit the end of the map.
- Store the map into thekeysfield of the data structure.
- Visit a string key called “value_table”.
- Begin visiting a list value.
- For each item, visit an integer.
- Visit the end of the list
- Store the list into thevalue_tablefield.
- Visit the end of the map.
But what determines which “observation” pattern is expected?

A functional programming language would be able to use currying to create
reflection of each type based on the type itself. Rust does not support that, so
every single type would need to have its own code written based on its fields
and their properties.

Serdesolves this usability challenge with a derive macro:

```rust
use serde::Deserialize;

#[derive(Deserialize)]
struct IdRecord {
    name: String,
    customer_id: String,
}
```

That macro simply generates an impl block causing the struct to implement a
trait calledDeserialize.

This is the function that determines how to create the struct itself. Code is
generated based on the struct’s fields. When the parsing library is called - in
our example, a JSON parsing library - it creates aDeserializerand callsType::deserializewith it as a parameter.

Thedeserializecode will then create aVisitorwhich will have its calls
“refracted” by theDeserializer. If everything goes well, eventually thatVisitorwill construct a value corresponding to the type being parsed and
return it.

For a complete example, see theSerdedocumentation.

The result is that types to be deserialized only implement the “top layer” of
the API, and file formats only need to implement the “bottom layer”. Each piece
can then “just work” with the rest of the ecosystem, since generic types will
bridge them.

In conclusion, Rust’s generic-inspired type system can bring it close to these
concepts and use their power, as shown in this API design. But it may also need
procedural macros to create bridges for its generics.

If you are interested in learning more about this topic, please check the
following section.

## See Also

- lens-rs cratefor a pre-built lenses
implementation, with a cleaner interface than these examples
- Serdeitself, which makes these concepts intuitive for end
users (i.e. defining the structs) without needing to understand the details
- luminanceis a crate for drawing
computer graphics that uses similar API design, including procedural macros to
create full prisms for buffers of different pixel types that remain generic
- An Article about Lenses in Scalathat is very readable even without Scala expertise.
- Paper: Profunctor Optics: Modular Data
Accessors
- Musliis a library which attempts to use a
similar structure with a different approach, e.g. doing away with the visitor
- School of Haskell: A Little Lens Starter Tutorial↩
School of Haskell: A Little Lens Starter Tutorial↩

- Concordance on Wikipedia↩
Concordance on Wikipedia↩
