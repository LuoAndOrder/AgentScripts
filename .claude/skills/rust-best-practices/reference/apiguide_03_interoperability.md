# Interoperability

Source: https://rust-lang.github.io/api-guidelines/

## Types eagerly implement common traits (C-COMMON-TRAITS)

Rust's trait system does not alloworphans: roughly, everyimplmust live
either in the crate that defines the trait or the implementing type.
Consequently, crates that define new types should eagerly implement all
applicable, common traits.

To see why, consider the following situation:

- Cratestddefines traitDisplay.
- Crateurldefines typeUrl, without implementingDisplay.
- Cratewebappimports from bothstdandurl,
There is no way forwebappto addDisplaytoUrl, since it defines
neither. (Note: the newtype pattern can provide an efficient, but inconvenient
workaround.)

The most important common traits to implement fromstdare:

- Copy
- Clone
- Eq
- PartialEq
- Ord
- PartialOrd
- Hash
- Debug
- Display
- Default
Note that it is common and expected for types to implement bothDefaultand an emptynewconstructor.newis the constructor
convention in Rust, and users expect it to exist, so if it is
reasonable for the basic constructor to take no arguments, then it
should, even if it is functionally identical todefault.

## Conversions use the standard traitsFrom,AsRef,AsMut(C-CONV-TRAITS)

The following conversion traits should be implemented where it makes sense:

- From
- TryFrom
- AsRef
- AsMut
The following conversion traits should never be implemented:

- Into
- TryInto
These traits have a blanket impl based onFromandTryFrom. Implement those
instead.

### Examples from the standard library

- From<u16>is implemented foru32because a smaller integer can always be
converted to a bigger integer.
- From<u32>isnotimplemented foru16because the conversion may not be
possible if the integer is too big.
- TryFrom<u32>is implemented foru16and returns an error if the integer is
too big to fit inu16.
- From<Ipv6Addr>is implemented forIpAddr, which is a type that can
represent both v4 and v6 IP addresses.

## Collections implementFromIteratorandExtend(C-COLLECT)

FromIteratorandExtendenable collections to be used conveniently with
the following iterator methods:

- Iterator::collect
- Iterator::partition
- Iterator::unzip
FromIteratoris for creating a new collection containing items from an
iterator, andExtendis for adding items from an iterator onto an existing
collection.

### Examples from the standard library

- Vec<T>implements bothFromIterator<T>andExtend<T>.

## Data structures implement Serde'sSerialize,Deserialize(C-SERDE)

Types that play the role of a data structure should implementSerializeandDeserialize.

There is a continuum of types between things that are clearly a data structure
and things that are clearly not, with gray area in between.LinkedHashMapandIpAddrare data structures. It would be completely reasonable for
somebody to want to read in aLinkedHashMaporIpAddrfrom a JSON file, or
send one over IPC to another process.LittleEndianis not a data structure.
It is a marker used by thebyteordercrate to optimize at compile time for
bytes in a particular order, and in fact an instance ofLittleEndiancan never
exist at runtime. So these are clear-cut examples; the #rust or #serde IRC
channels can help assess more ambiguous cases if necessary.

If a crate does not already depend on Serde for other reasons, it may wish to
gate Serde impls behind a Cargo cfg. This way downstream libraries only need to
pay the cost of compiling Serde if they need those impls to exist.

For consistency with other Serde-based libraries, the name of the Cargo cfg
should be simply"serde". Do not use a different name for the cfg like"serde_impls"or"serde_serialization".

The canonical implementation looks like this when not using derive:

```toml
[dependencies]
serde = { version = "1.0", optional = true }
```

```rust

#![allow(unused)]
fn main() {
pub struct T { /* ... */ }

#[cfg(feature = "serde")]
impl Serialize for T { /* ... */ }

#[cfg(feature = "serde")]
impl<'de> Deserialize<'de> for T { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
pub struct T { /* ... */ }

#[cfg(feature = "serde")]
impl Serialize for T { /* ... */ }

#[cfg(feature = "serde")]
impl<'de> Deserialize<'de> for T { /* ... */ }
}
```

And when using derive:

```toml
[dependencies]
serde = { version = "1.0", optional = true, features = ["derive"] }
```

```rust

#![allow(unused)]
fn main() {
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub struct T { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub struct T { /* ... */ }
}
```

## Types areSendandSyncwhere possible (C-SEND-SYNC)

SendandSyncare automatically implemented when the compiler determines
it is appropriate.

In types that manipulate raw pointers, be vigilant that theSendandSyncstatus of your type accurately reflects its thread safety characteristics. Tests
like the following can help catch unintentional regressions in whether the type
implementsSendorSync.

```rust

#![allow(unused)]
fn main() {
#[test]
fn test_send() {
    fn assert_send<T: Send>() {}
    assert_send::<MyStrangeType>();
}

#[test]
fn test_sync() {
    fn assert_sync<T: Sync>() {}
    assert_sync::<MyStrangeType>();
}
}
```

```rust

#![allow(unused)]
fn main() {
#[test]
fn test_send() {
    fn assert_send<T: Send>() {}
    assert_send::<MyStrangeType>();
}

#[test]
fn test_sync() {
    fn assert_sync<T: Sync>() {}
    assert_sync::<MyStrangeType>();
}
}
```

## Error types are meaningful and well-behaved (C-GOOD-ERR)

An error type is any typeEused in aResult<T, E>returned by any public
function of your crate. Error types should always implement thestd::error::Errortrait which is the mechanism by which error handling
libraries likeerror-chainabstract over different types of errors, and
which allows the error to be used as thesource()of another error.

Additionally, error types should implement theSendandSynctraits. An
error that is notSendcannot be returned by a thread run withthread::spawn. An error that is notSynccannot be passed across threads
using anArc. These are common requirements for basic error handling in a
multithreaded application.

SendandSyncare also important for being able to package a custom error
into an IO error usingstd::io::Error::new, which requires a trait bound ofError + Send + Sync.

One place to be vigilant about this guideline is in functions that return Error
trait objects, for examplereqwest::Error::get_ref. TypicallyError + Send + Sync + 'staticwill be the most useful for callers. The addition of'staticallows the trait object to be used withError::downcast_ref.

Never use()as an error type, even where there is no useful additional
information for the error to carry.

- ()does not implementErrorso it cannot be used with error handling
libraries likeerror-chain.
- ()does not implementDisplayso a user would need to write an error
message of their own if they want to fail because of the error.
- ()has an unhelpfulDebugrepresentation for users that decide tounwrap()the error.
- It would not be semantically meaningful for a downstream library to implementFrom<()>for their error type, so()as an error type cannot be used with
the?operator.
Instead, define a meaningful error type specific to your crate or to the
individual function. Provide appropriateErrorandDisplayimpls. If there
is no useful information for the error to carry, it can be implemented as a unit
struct.

```rust

#![allow(unused)]
fn main() {
use std::error::Error;
use std::fmt::Display;

// Instead of this...
fn do_the_thing() -> Result<Wow, ()>

// Prefer this...
fn do_the_thing() -> Result<Wow, DoError>

#[derive(Debug)]
struct DoError;

impl Display for DoError { /* ... */ }
impl Error for DoError { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
use std::error::Error;
use std::fmt::Display;

// Instead of this...
fn do_the_thing() -> Result<Wow, ()>

// Prefer this...
fn do_the_thing() -> Result<Wow, DoError>

#[derive(Debug)]
struct DoError;

impl Display for DoError { /* ... */ }
impl Error for DoError { /* ... */ }
}
```

The error message given by theDisplayrepresentation of an error type should
be lowercase without trailing punctuation, and typically concise.

Error::description()should not be implemented. It has been deprecated and users should
always useDisplayinstead ofdescription()to print the error.

### Examples from the standard library

- ParseBoolErroris returned when failing to parse a bool from a string.

### Examples of error messages

- "unexpected end of file"
- "provided string was not `true` or `false`"
- "invalid IP address syntax"
- "second time provided was later than self"
- "invalid UTF-8 sequence of {} bytes from index {}"
- "environment variable was not valid unicode: {:?}"

## Binary number types provideHex,Octal,Binaryformatting (C-NUM-FMT)

- std::fmt::UpperHex
- std::fmt::LowerHex
- std::fmt::Octal
- std::fmt::Binary
These traits control the representation of a type under the{:X},{:x},{:o}, and{:b}format specifiers.

Implement these traits for any number type on which you would consider doing
bitwise manipulations like|or&. This is especially appropriate for
bitflag types. Numeric quantity types likestruct Nanoseconds(u64)probably do
not need these.

## Generic reader/writer functions takeR: ReadandW: Writeby value (C-RW-VALUE)

The standard library contains these two impls:

```rust

#![allow(unused)]
fn main() {
impl<'a, R: Read + ?Sized> Read for &'a mut R { /* ... */ }

impl<'a, W: Write + ?Sized> Write for &'a mut W { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
impl<'a, R: Read + ?Sized> Read for &'a mut R { /* ... */ }

impl<'a, W: Write + ?Sized> Write for &'a mut W { /* ... */ }
}
```

That means any function that acceptsR: ReadorW: Writegeneric parameters
by value can be called with a mut reference if necessary.

In the documentation of such functions, briefly remind users that a mut
reference can be passed. New Rust users often struggle with this. They may have
opened a file and want to read multiple pieces of data out of it, but the
function to read one piece consumes the reader by value, so they are stuck. The
solution would be to leverage one of the above impls and pass&mut finstead
offas the reader parameter.

### Examples

- flate2::read::GzDecoder::new
- flate2::write::GzEncoder::new
- serde_json::from_reader
- serde_json::to_writer
