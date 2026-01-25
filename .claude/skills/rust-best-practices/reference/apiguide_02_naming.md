# Naming

Source: https://rust-lang.github.io/api-guidelines/

## Casing conforms to RFC 430 (C-CASE)

Basic Rust naming conventions are described inRFC 430.

In general, Rust tends to useUpperCamelCasefor "type-level" constructs (types and
traits) andsnake_casefor "value-level" constructs. More precisely:

InUpperCamelCase, acronyms and contractions of compound words count as one word: useUuidrather thanUUID,Usizerather thanUSizeorStdinrather thanStdIn. Insnake_case, acronyms and contractions are lower-cased:is_xid_start.

Insnake_caseorSCREAMING_SNAKE_CASE, a "word" should never consist of a
single letter unless it is the last "word". So, we havebtree_maprather thanb_tree_map, butPI_2rather thanPI2.

Crate names should not use-rsor-rustas a suffix or prefix. Every crate
is Rust! It serves no purpose to remind users of this constantly.

### Examples from the standard library

The whole standard library. This guideline should be easy!

## Ad-hoc conversions followas_,to_,into_conventions (C-CONV)

Conversions should be provided as methods, with names prefixed as follows:

For example:

- str::as_bytes()gives a view of astras a slice of UTF-8 bytes, which
is free. The input is a borrowed&strand the output is a borrowed&[u8].
- Path::to_strperforms an expensive UTF-8 check on the bytes of an
operating system path. The input and output are both borrowed. It would not be
correct to call thisas_strbecause this method has nontrivial cost at
runtime.
- str::to_lowercase()produces the Unicode-correct lowercase equivalent of astr, which involves iterating through characters of the string and may
require memory allocation. The input is a borrowed&strand the output is an
ownedString.
- f64::to_radians()converts a floating point quantity from degrees to
radians. The input isf64. Passing a reference&f64is not warranted
becausef64is cheap to copy. Calling the functioninto_radianswould be
misleading because the input is not consumed.
- String::into_bytes()extracts the underlyingVec<u8>of aString,
which is free. It takes ownership of aStringand returns an ownedVec<u8>.
- BufReader::into_inner()takes ownership of a buffered reader and extracts
out the underlying reader, which is free. Data in the buffer is discarded.
- BufWriter::into_inner()takes ownership of a buffered writer and extracts
out the underlying writer, which requires a potentially expensive flush of any
buffered data.
Conversions prefixedas_andinto_typicallydecrease abstraction, either
exposing a view into the underlying representation (as) or deconstructing data
into its underlying representation (into). Conversions prefixedto_, on the
other hand, typically stay at the same level of abstraction but do some work to
change from one representation to another.

When a type wraps a single value to associate it with higher-level semantics,
access to the wrapped value should be provided by aninto_inner()method. This
applies to wrappers that provide buffering likeBufReader, encoding or
decoding likeGzDecoder, atomic access likeAtomicBool, or any similar
semantics.

If themutqualifier in the name of a conversion method constitutes part of
the return type, it should appear as it would appear in the type. For exampleVec::as_mut_slicereturns a mut slice; it does what it says. This name is
preferred overas_slice_mut.

```rust

#![allow(unused)]
fn main() {
// Return type is a mut slice.
fn as_mut_slice(&mut self) -> &mut [T];
}
```

```rust

#![allow(unused)]
fn main() {
// Return type is a mut slice.
fn as_mut_slice(&mut self) -> &mut [T];
}
```

- Result::as_ref
- RefCell::as_ptr
- slice::to_vec
- Option::into_iter

## Getter names follow Rust convention (C-GETTER)

With a few exceptions, theget_prefix is not used for getters in Rust code.

```rust

#![allow(unused)]
fn main() {
pub struct S {
    first: First,
    second: Second,
}

impl S {
    // Not get_first.
    pub fn first(&self) -> &First {
        &self.first
    }

    // Not get_first_mut, get_mut_first, or mut_first.
    pub fn first_mut(&mut self) -> &mut First {
        &mut self.first
    }
}
}
```

```rust

#![allow(unused)]
fn main() {
pub struct S {
    first: First,
    second: Second,
}

impl S {
    // Not get_first.
    pub fn first(&self) -> &First {
        &self.first
    }

    // Not get_first_mut, get_mut_first, or mut_first.
    pub fn first_mut(&mut self) -> &mut First {
        &mut self.first
    }
}
}
```

Thegetnaming is used only when there is a single and obvious thing that
could reasonably be gotten by a getter. For exampleCell::getaccesses the
content of aCell.

For getters that do runtime validation such as bounds checking, consider adding
unsafe_uncheckedvariants. Typically those will have the following
signatures.

```rust

#![allow(unused)]
fn main() {
fn get(&self, index: K) -> Option<&V>;
fn get_mut(&mut self, index: K) -> Option<&mut V>;
unsafe fn get_unchecked(&self, index: K) -> &V;
unsafe fn get_unchecked_mut(&mut self, index: K) -> &mut V;
}
```

```rust

#![allow(unused)]
fn main() {
fn get(&self, index: K) -> Option<&V>;
fn get_mut(&mut self, index: K) -> Option<&mut V>;
unsafe fn get_unchecked(&self, index: K) -> &V;
unsafe fn get_unchecked_mut(&mut self, index: K) -> &mut V;
}
```

The difference between getters and conversions (C-CONV) can be subtle
and is not always clear-cut. For exampleTempDir::pathcan be understood as
a getter for the filesystem path of the temporary directory, whileTempDir::into_pathis a conversion that transfers responsibility for
deleting the temporary directory to the caller. Sincepathis a getter, it
would not be correct to call itget_pathoras_path.

### Examples from the standard library

- std::io::Cursor::get_mut
- std::pin::Pin::get_mut
- std::sync::PoisonError::get_mut
- std::sync::atomic::AtomicBool::get_mut
- std::collections::hash_map::OccupiedEntry::get_mut
- <[T]>::get_unchecked

## Methods on collections that produce iterators followiter,iter_mut,into_iter(C-ITER)

PerRFC 199.

For a container with elements of typeU, iterator methods should be named:

```rust

#![allow(unused)]
fn main() {
fn iter(&self) -> Iter             // Iter implements Iterator<Item = &U>
fn iter_mut(&mut self) -> IterMut  // IterMut implements Iterator<Item = &mut U>
fn into_iter(self) -> IntoIter     // IntoIter implements Iterator<Item = U>
}
```

```rust

#![allow(unused)]
fn main() {
fn iter(&self) -> Iter             // Iter implements Iterator<Item = &U>
fn iter_mut(&mut self) -> IterMut  // IterMut implements Iterator<Item = &mut U>
fn into_iter(self) -> IntoIter     // IntoIter implements Iterator<Item = U>
}
```

This guideline applies to data structures that are conceptually homogeneous
collections. As a counterexample, thestrtype is slice of bytes that are
guaranteed to be valid UTF-8. This is conceptually more nuanced than a
homogeneous collection so rather than providing theiter/iter_mut/into_itergroup of iterator methods, it providesstr::bytesto iterate as bytes andstr::charsto iterate as chars.

This guideline applies to methods only, not functions. For examplepercent_encodefrom theurlcrate returns an iterator over percent-encoded
string fragments. There would be no clarity to be had by using aniter/iter_mut/into_iterconvention.

### Examples from the standard library

- Vec::iter
- Vec::iter_mut
- Vec::into_iter
- BTreeMap::iter
- BTreeMap::iter_mut

## Iterator type names match the methods that produce them (C-ITER-TY)

A method calledinto_iter()should return a type calledIntoIterand
similarly for all other methods that return iterators.

This guideline applies chiefly to methods, but often makes sense for functions
as well. For example thepercent_encodefunction from theurlcrate
returns an iterator type calledPercentEncode.

These type names make the most sense when prefixed with their owning module, for
examplevec::IntoIter.

### Examples from the standard library

- Vec::iterreturnsIter
- Vec::iter_mutreturnsIterMut
- Vec::into_iterreturnsIntoIter
- BTreeMap::keysreturnsKeys
- BTreeMap::valuesreturnsValues

## Feature names are free of placeholder words (C-FEATURE)

Do not include words in the name of aCargo featurethat convey zero meaning,
as inuse-abcorwith-abc. Name the featureabcdirectly.

This arises most commonly for crates that have an optional dependency on the
Rust standard library. The canonical way to do this correctly is:

```toml
# In Cargo.toml

[features]
default = ["std"]
std = []
```

```rust

#![allow(unused)]
fn main() {
// In lib.rs
#![no_std]

#[cfg(feature = "std")]
extern crate std;
}
```

```rust

#![allow(unused)]
fn main() {
// In lib.rs
#![no_std]

#[cfg(feature = "std")]
extern crate std;
}
```

Do not call the featureuse-stdorwith-stdor any creative name that is notstd. This naming convention aligns with the naming of implicit features
inferred by Cargo for optional dependencies. Consider cratexwith optional
dependencies on Serde and on the Rust standard library:

```toml
[package]
name = "x"
version = "0.1.0"

[features]
std = ["serde/std"]

[dependencies]
serde = { version = "1.0", optional = true }
```

When we depend onx, we can enable the optional Serde dependency withfeatures = ["serde"]. Similarly we can enable the optional standard library
dependency withfeatures = ["std"]. The implicit feature inferred by Cargo for
the optional dependency is calledserde, notuse-serdeorwith-serde, so
we like for explicit features to behave the same way.

As a related note, Cargo requires that features are additive so a feature named
negatively likeno-abcis practically never correct.

## Names use a consistent word order (C-WORD-ORDER)

Here are some error types from the standard library:

- JoinPathsError
- ParseBoolError
- ParseCharError
- ParseFloatError
- ParseIntError
- RecvTimeoutError
- StripPrefixError
All of these use verb-object-error word order. If we were adding an error to
represent an address failing to parse, for consistency we would want to name it
in verb-object-error order likeParseAddrErrorrather thanAddrParseError.

The particular choice of word order is not important, but pay attention to
consistency within the crate and consistency with similar functionality in the
standard library.
