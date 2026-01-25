# Future Proofing

Source: https://rust-lang.github.io/api-guidelines/

# Future proofing

## Sealed traits protect against downstream implementations (C-SEALED)

Some traits are only meant to be implemented within the crate that defines them.
In such cases, we can retain the ability to make changes to the trait in a
non-breaking way by using the sealed trait pattern.

```rust

#![allow(unused)]
fn main() {
/// This trait is sealed and cannot be implemented for types outside this crate.
pub trait TheTrait: private::Sealed {
    // Zero or more methods that the user is allowed to call.
    fn ...();

    // Zero or more private methods, not allowed for user to call.
    #[doc(hidden)]
    fn ...();
}

// Implement for some types.
impl TheTrait for usize {
    /* ... */
}

mod private {
    pub trait Sealed {}

    // Implement for those same types, but no others.
    impl Sealed for usize {}
}
}
```

```rust

#![allow(unused)]
fn main() {
/// This trait is sealed and cannot be implemented for types outside this crate.
pub trait TheTrait: private::Sealed {
    // Zero or more methods that the user is allowed to call.
    fn ...();

    // Zero or more private methods, not allowed for user to call.
    #[doc(hidden)]
    fn ...();
}

// Implement for some types.
impl TheTrait for usize {
    /* ... */
}

mod private {
    pub trait Sealed {}

    // Implement for those same types, but no others.
    impl Sealed for usize {}
}
}
```

The empty privateSealedsupertrait cannot be named by downstream crates, so
we are guaranteed that implementations ofSealed(and thereforeTheTrait)
only exist in the current crate. We are free to add methods toTheTraitin a
non-breaking release even though that would ordinarily be a breaking change for
traits that are not sealed. Also we are free to change the signature of methods
that are not publicly documented.

Note that removing a public method or changing the signature of a public method
in a sealed trait are still breaking changes.

To avoid frustrated users trying to implement the trait, it should be documented
in rustdoc that the trait is sealed and not meant to be implemented outside of
the current crate.

### Examples

- serde_json::value::Index
- byteorder::ByteOrder

## Structs have private fields (C-STRUCT-PRIVATE)

Making a field public is a strong commitment: it pins down a representation
choice,andprevents the type from providing any validation or maintaining any
invariants on the contents of the field, since clients can mutate it arbitrarily.

Public fields are most appropriate forstructtypes in the C spirit: compound,
passive data structures. Otherwise, consider providing getter/setter methods and
hiding fields instead.

## Newtypes encapsulate implementation details (C-NEWTYPE-HIDE)

A newtype can be used to hide representation details while making precise
promises to the client.

For example, consider a functionmy_transformthat returns a compound iterator
type.

```rust

#![allow(unused)]
fn main() {
use std::iter::{Enumerate, Skip};

pub fn my_transform<I: Iterator>(input: I) -> Enumerate<Skip<I>> {
    input.skip(3).enumerate()
}
}
```

```rust

#![allow(unused)]
fn main() {
use std::iter::{Enumerate, Skip};

pub fn my_transform<I: Iterator>(input: I) -> Enumerate<Skip<I>> {
    input.skip(3).enumerate()
}
}
```

We wish to hide this type from the client, so that the client's view of the
return type is roughlyIterator<Item = (usize, T)>. We can do so using the
newtype pattern:

```rust

#![allow(unused)]
fn main() {
use std::iter::{Enumerate, Skip};

pub struct MyTransformResult<I>(Enumerate<Skip<I>>);

impl<I: Iterator> Iterator for MyTransformResult<I> {
    type Item = (usize, I::Item);

    fn next(&mut self) -> Option<Self::Item> {
        self.0.next()
    }
}

pub fn my_transform<I: Iterator>(input: I) -> MyTransformResult<I> {
    MyTransformResult(input.skip(3).enumerate())
}
}
```

```rust

#![allow(unused)]
fn main() {
use std::iter::{Enumerate, Skip};

pub struct MyTransformResult<I>(Enumerate<Skip<I>>);

impl<I: Iterator> Iterator for MyTransformResult<I> {
    type Item = (usize, I::Item);

    fn next(&mut self) -> Option<Self::Item> {
        self.0.next()
    }
}

pub fn my_transform<I: Iterator>(input: I) -> MyTransformResult<I> {
    MyTransformResult(input.skip(3).enumerate())
}
}
```

Aside from simplifying the signature, this use of newtypes allows us to promise
less to the client. The client does not knowhowthe result iterator is
constructed or represented, which means the representation can change in the
future without breaking client code.

Rust 1.26 also introduces theimpl Traitfeature, which is more concise
than the newtype pattern but with some additional trade offs, namely withimpl Traityou are limited in what you can express.  For example, returning an
iterator that implsDebugorCloneor some combination of the other iterator
extension traits can be problematic.  In summaryimpl Traitas a return type
is probably great for internal APIs and may even be appropriate for public APIs,
but probably not in all cases.  See the"impl Traitfor returning complex
types with ease"section of the Edition Guide for more details.

```rust

#![allow(unused)]
fn main() {
pub fn my_transform<I: Iterator>(input: I) -> impl Iterator<Item = (usize, I::Item)> {
    input.skip(3).enumerate()
}
}
```

```rust

#![allow(unused)]
fn main() {
pub fn my_transform<I: Iterator>(input: I) -> impl Iterator<Item = (usize, I::Item)> {
    input.skip(3).enumerate()
}
}
```

## Data structures do not duplicate derived trait bounds (C-STRUCT-BOUNDS)

Generic data structures should not use trait bounds that can be derived or do
not otherwise add semantic value. Each trait in thederiveattribute will be
expanded into a separateimplblock that only applies to generic arguments
that implement that trait.

```rust

#![allow(unused)]
fn main() {
// Prefer this:
#[derive(Clone, Debug, PartialEq)]
struct Good<T> { /* ... */ }

// Over this:
#[derive(Clone, Debug, PartialEq)]
struct Bad<T: Clone + Debug + PartialEq> { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
// Prefer this:
#[derive(Clone, Debug, PartialEq)]
struct Good<T> { /* ... */ }

// Over this:
#[derive(Clone, Debug, PartialEq)]
struct Bad<T: Clone + Debug + PartialEq> { /* ... */ }
}
```

Duplicating derived traits as bounds onBadis unnecessary and a
backwards-compatibiliity hazard. To illustrate this point, consider derivingPartialOrdon the structures in the previous example:

```rust

#![allow(unused)]
fn main() {
// Non-breaking change:
#[derive(Clone, Debug, PartialEq, PartialOrd)]
struct Good<T> { /* ... */ }

// Breaking change:
#[derive(Clone, Debug, PartialEq, PartialOrd)]
struct Bad<T: Clone + Debug + PartialEq + PartialOrd> { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
// Non-breaking change:
#[derive(Clone, Debug, PartialEq, PartialOrd)]
struct Good<T> { /* ... */ }

// Breaking change:
#[derive(Clone, Debug, PartialEq, PartialOrd)]
struct Bad<T: Clone + Debug + PartialEq + PartialOrd> { /* ... */ }
}
```

Generally speaking, adding a trait bound to a data structure is a breaking
change because every consumer of that structure will need to start satisfying
the additional bound. Deriving more traits from the standard library using thederiveattribute is not a breaking change.

The following traits should never be used in bounds on data structures:

- Clone
- PartialEq
- PartialOrd
- Debug
- Display
- Default
- Error
- Serialize
- Deserialize
- DeserializeOwned
There is a grey area around other non-derivable trait bounds that are not
strictly required by the structure definition, likeReadorWrite. They may
communicate the intended behavior of the type better in its definition but also
limits future extensibility. Including semantically useful trait bounds on data
structures is still less problematic than including derivable traits as bounds.

### Exceptions

There are three exceptions where trait bounds on structures are required:

- The data structure refers to an associated type on the trait.
- The bound is?Sized.
- The data structure has aDropimpl that requires trait bounds.
Rust currently requires all trait bounds on theDropimpl are also present
on the data structure.

### Examples from the standard library

- std::borrow::Cowrefers to an associated type on theBorrowtrait.
- std::boxed::Boxopts out of the implicitSizedbound.
- std::io::BufWriterrequires a trait bound in itsDropimpl.
