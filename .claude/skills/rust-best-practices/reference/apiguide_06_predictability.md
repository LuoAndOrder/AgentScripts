# Predictability

Source: https://rust-lang.github.io/api-guidelines/

## Smart pointers do not add inherent methods (C-SMART-PTR)

For example, this is why theBox::into_rawfunction is defined the way it
is.

```rust

#![allow(unused)]
fn main() {
impl<T> Box<T> where T: ?Sized {
    fn into_raw(b: Box<T>) -> *mut T { /* ... */ }
}

let boxed_str: Box<str> = /* ... */;
let ptr = Box::into_raw(boxed_str);
}
```

```rust

#![allow(unused)]
fn main() {
impl<T> Box<T> where T: ?Sized {
    fn into_raw(b: Box<T>) -> *mut T { /* ... */ }
}

let boxed_str: Box<str> = /* ... */;
let ptr = Box::into_raw(boxed_str);
}
```

If this were defined as an inherent method instead, it would be confusing at the
call site whether the method being called is a method onBox<T>or a method onT.

```rust

#![allow(unused)]
fn main() {
impl<T> Box<T> where T: ?Sized {
    // Do not do this.
    fn into_raw(self) -> *mut T { /* ... */ }
}

let boxed_str: Box<str> = /* ... */;

// This is a method on str accessed through the smart pointer Deref impl.
boxed_str.chars()

// This is a method on Box<str>...?
boxed_str.into_raw()
}
```

```rust

#![allow(unused)]
fn main() {
impl<T> Box<T> where T: ?Sized {
    // Do not do this.
    fn into_raw(self) -> *mut T { /* ... */ }
}

let boxed_str: Box<str> = /* ... */;

// This is a method on str accessed through the smart pointer Deref impl.
boxed_str.chars()

// This is a method on Box<str>...?
boxed_str.into_raw()
}
```

## Conversions live on the most specific type involved (C-CONV-SPECIFIC)

When in doubt, preferto_/as_/into_tofrom_, because they are more
ergonomic to use (and can be chained with other methods).

For many conversions between two types, one of the types is clearly more
"specific": it provides some additional invariant or interpretation that is not
present in the other type. For example,stris more specific than&[u8],
since it is a UTF-8 encoded sequence of bytes.

Conversions should live with the more specific of the involved types. Thus,strprovides both theas_bytesmethod and thefrom_utf8constructor
for converting to and from&[u8]values. Besides being intuitive, this
convention avoids polluting concrete types like&[u8]with endless conversion
methods.

## Functions with a clear receiver are methods (C-METHOD)

Prefer

```rust

#![allow(unused)]
fn main() {
impl Foo {
    pub fn frob(&self, w: widget) { /* ... */ }
}
}
```

```rust

#![allow(unused)]
fn main() {
impl Foo {
    pub fn frob(&self, w: widget) { /* ... */ }
}
}
```

over

```rust

#![allow(unused)]
fn main() {
pub fn frob(foo: &Foo, w: widget) { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
pub fn frob(foo: &Foo, w: widget) { /* ... */ }
}
```

for any operation that is clearly associated with a particular type.

Methods have numerous advantages over functions:

- They do not need to be imported or qualified to be used: all you need is a
value of the appropriate type.
- Their invocation performs autoborrowing (including mutable borrows).
- They make it easy to answer the question "what can I do with a value of typeT" (especially when using rustdoc).
- They provideselfnotation, which is more concise and often more clearly
conveys ownership distinctions.

## Functions do not take out-parameters (C-NO-OUT)

Prefer

```rust

#![allow(unused)]
fn main() {
fn foo() -> (Bar, Bar)
}
```

```rust

#![allow(unused)]
fn main() {
fn foo() -> (Bar, Bar)
}
```

over

```rust

#![allow(unused)]
fn main() {
fn foo(output: &mut Bar) -> Bar
}
```

```rust

#![allow(unused)]
fn main() {
fn foo(output: &mut Bar) -> Bar
}
```

for returning multipleBarvalues.

Compound return types like tuples and structs are efficiently compiled and do
not require heap allocation. If a function needs to return multiple values, it
should do so via one of these types.

The primary exception: sometimes a function is meant to modify data that the
caller already owns, for example to re-use a buffer:

```rust

#![allow(unused)]
fn main() {
fn read(&mut self, buf: &mut [u8]) -> io::Result<usize>
}
```

```rust

#![allow(unused)]
fn main() {
fn read(&mut self, buf: &mut [u8]) -> io::Result<usize>
}
```

## Operator overloads are unsurprising (C-OVERLOAD)

Operators with built in syntax (*,|, and so on) can be provided for a type
by implementing the traits instd::ops. These operators come with strong
expectations: implementMulonly for an operation that bears some resemblance
to multiplication (and shares the expected properties, e.g. associativity), and
so on for the other traits.

## Only smart pointers implementDerefandDerefMut(C-DEREF)

TheDereftraits are used implicitly by the compiler in many circumstances,
and interact with method resolution. The relevant rules are designed
specifically to accommodate smart pointers, and so the traits should be used
only for that purpose.

### Examples from the standard library

- Box<T>
- Stringis a smart
pointer tostr
- Rc<T>
- Arc<T>
- Cow<'a, T>

## Constructors are static, inherent methods (C-CTOR)

In Rust, "constructors" are just a convention. There are a variety of
conventions around constructor naming, and the distinctions are often
subtle.

A constructor in its most basic form is anewmethod with no arguments.

```rust

#![allow(unused)]
fn main() {
impl<T> Example<T> {
    pub fn new() -> Example<T> { /* ... */ }
}
}
```

```rust

#![allow(unused)]
fn main() {
impl<T> Example<T> {
    pub fn new() -> Example<T> { /* ... */ }
}
}
```

Constructors are static (noself) inherent methods for the type that they
construct. Combined with the practice of fully importing type names, this
convention leads to informative but concise construction:

```rust

#![allow(unused)]
fn main() {
use example::Example;

// Construct a new Example.
let ex = Example::new();
}
```

```rust

#![allow(unused)]
fn main() {
use example::Example;

// Construct a new Example.
let ex = Example::new();
}
```

The namenewshould generally be used for the primary method of instantiating
a type. Sometimes it takes no arguments, as in the examples above. Sometimes it
does take arguments, likeBox::newwhich is passed the value to place in theBox.

Some types' constructors, most notably I/O resource types, use distinct naming
conventions for their constructors, as inFile::open,Mmap::open,TcpStream::connect, andUdpSocket::bind. In these cases names are chosen
as appropriate for the domain.

Often there are multiple ways to construct a type. It's common in these cases
for secondary constructors to be suffixed_with_foo, as inMmap::open_with_offset. If your type has a multiplicity of construction
options though, consider the builder pattern (C-BUILDER) instead.

Some constructors are "conversion constructors", methods that create a new type
from an existing value of a different type. These typically have names beginning
withfrom_as instd::io::Error::from_raw_os_error. Note also though theFromtrait (C-CONV-TRAITS), which is quite similar. There are three
distinctions between afrom_-prefixed conversion constructor and aFrom<T>impl.

- Afrom_constructor can be unsafe; aFromimpl cannot. One example of this
isBox::from_raw.
- Afrom_constructor can accept additional arguments to disambiguate the
meaning of the source data, as inu64::from_str_radix.
- AFromimpl is only appropriate when the source data type is sufficient to
determine the encoding of the output data type. When the input is just a bag
of bits like inu64::from_beorString::from_utf8, the conversion
constructor name is able to identify their meaning.
Note that it is common and expected for types to implement bothDefaultand anewconstructor. For types that have both, they should have the same behavior.
Either one may be implemented in terms of the other.

### Examples from the standard library

- std::io::Error::newis the commonly used constructor for an IO error.
- std::io::Error::from_raw_os_erroris a conversion constructor
based on an error code received from the operating system.
- Box::newcreates a new container type, taking a single argument.
- File::openopens a file resource.
- Mmap::open_with_offsetopens a memory-mapped file, with additional options.
