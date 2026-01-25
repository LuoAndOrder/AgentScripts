# Flexibility

Source: https://rust-lang.github.io/api-guidelines/

## Functions expose intermediate results to avoid duplicate work (C-INTERMEDIATE)

Many functions that answer a question also compute interesting related data. If
this data is potentially of interest to the client, consider exposing it in the
API.

### Examples from the standard library

- Vec::binary_searchdoes not return aboolof whether the value was
found, nor anOption<usize>of the index at which the value was maybe found.
Instead it returns information about the index if found, and also the index at
which the value would need to be inserted if not found.
Vec::binary_searchdoes not return aboolof whether the value was
found, nor anOption<usize>of the index at which the value was maybe found.
Instead it returns information about the index if found, and also the index at
which the value would need to be inserted if not found.

- String::from_utf8may fail if the input bytes are not UTF-8. In the error
case it returns an intermediate result that exposes the byte offset up to
which the input was valid UTF-8, as well as handing back ownership of the
input bytes.
String::from_utf8may fail if the input bytes are not UTF-8. In the error
case it returns an intermediate result that exposes the byte offset up to
which the input was valid UTF-8, as well as handing back ownership of the
input bytes.

- HashMap::insertreturns anOption<T>that returns the preexisting value
for a given key, if any. For cases where the user wants to recover this value
having it returned by the insert operation avoids the user having to do a second
hash table lookup.
HashMap::insertreturns anOption<T>that returns the preexisting value
for a given key, if any. For cases where the user wants to recover this value
having it returned by the insert operation avoids the user having to do a second
hash table lookup.

## Caller decides where to copy and place data (C-CALLER-CONTROL)

If a function requires ownership of an argument, it should take ownership of the
argument rather than borrowing and cloning the argument.

```rust

#![allow(unused)]
fn main() {
// Prefer this:
fn foo(b: Bar) {
    /* use b as owned, directly */
}

// Over this:
fn foo(b: &Bar) {
    let b = b.clone();
    /* use b as owned after cloning */
}
}
```

```rust

#![allow(unused)]
fn main() {
// Prefer this:
fn foo(b: Bar) {
    /* use b as owned, directly */
}

// Over this:
fn foo(b: &Bar) {
    let b = b.clone();
    /* use b as owned after cloning */
}
}
```

If a functiondoes notrequire ownership of an argument, it should take a
shared or exclusive borrow of the argument rather than taking ownership and
dropping the argument.

```rust

#![allow(unused)]
fn main() {
// Prefer this:
fn foo(b: &Bar) {
    /* use b as borrowed */
}

// Over this:
fn foo(b: Bar) {
    /* use b as borrowed, it is implicitly dropped before function returns */
}
}
```

```rust

#![allow(unused)]
fn main() {
// Prefer this:
fn foo(b: &Bar) {
    /* use b as borrowed */
}

// Over this:
fn foo(b: Bar) {
    /* use b as borrowed, it is implicitly dropped before function returns */
}
}
```

TheCopytrait should only be used as a bound when absolutely needed, not as a
way of signaling that copies should be cheap to make.

## Functions minimize assumptions about parameters by using generics (C-GENERIC)

The fewer assumptions a function makes about its inputs, the more widely usable
it becomes.

Prefer

```rust

#![allow(unused)]
fn main() {
fn foo<I: IntoIterator<Item = i64>>(iter: I) { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
fn foo<I: IntoIterator<Item = i64>>(iter: I) { /* ... */ }
}
```

over any of

```rust

#![allow(unused)]
fn main() {
fn foo(c: &[i64]) { /* ... */ }
fn foo(c: &Vec<i64>) { /* ... */ }
fn foo(c: &SomeOtherCollection<i64>) { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
fn foo(c: &[i64]) { /* ... */ }
fn foo(c: &Vec<i64>) { /* ... */ }
fn foo(c: &SomeOtherCollection<i64>) { /* ... */ }
}
```

if the function only needs to iterate over the data.

More generally, consider using generics to pinpoint the assumptions a function
needs to make about its arguments.

### Advantages of generics

- Reusability. Generic functions can be applied to an open-ended collection of
types, while giving a clear contract for the functionality those types must
provide.
Reusability. Generic functions can be applied to an open-ended collection of
types, while giving a clear contract for the functionality those types must
provide.

- Static dispatch and optimization. Each use of a generic function is
specialized ("monomorphized") to the particular types implementing the trait
bounds, which means that (1) invocations of trait methods are static, direct
calls to the implementation and (2) the compiler can inline and otherwise
optimize these calls.
Static dispatch and optimization. Each use of a generic function is
specialized ("monomorphized") to the particular types implementing the trait
bounds, which means that (1) invocations of trait methods are static, direct
calls to the implementation and (2) the compiler can inline and otherwise
optimize these calls.

- Inline layout. If astructandenumtype is generic over some type
parameterT, values of typeTwill be laid out inline in thestruct/enum, without any indirection.
Inline layout. If astructandenumtype is generic over some type
parameterT, values of typeTwill be laid out inline in thestruct/enum, without any indirection.

- Inference. Since the type parameters to generic functions can usually be
inferred, generic functions can help cut down on verbosity in code where
explicit conversions or other method calls would usually be necessary.
Inference. Since the type parameters to generic functions can usually be
inferred, generic functions can help cut down on verbosity in code where
explicit conversions or other method calls would usually be necessary.

- Precise types. Because generics give anameto the specific type
implementing a trait, it is possible to be precise about places where that
exact type is required or produced. For example, a function#![allow(unused)]fn main() {fn binary<T: Trait>(x: T, y: T) -> T}is guaranteed to consume and produce elements of exactly the same typeT; it
cannot be invoked with parameters of different types that both implementTrait.
Precise types. Because generics give anameto the specific type
implementing a trait, it is possible to be precise about places where that
exact type is required or produced. For example, a function

```rust

#![allow(unused)]
fn main() {
fn binary<T: Trait>(x: T, y: T) -> T
}
```

```rust

#![allow(unused)]
fn main() {
fn binary<T: Trait>(x: T, y: T) -> T
}
```

is guaranteed to consume and produce elements of exactly the same typeT; it
cannot be invoked with parameters of different types that both implementTrait.

### Disadvantages of generics

- Code size. Specializing generic functions means that the function body is
duplicated. The increase in code size must be weighed against the performance
benefits of static dispatch.
Code size. Specializing generic functions means that the function body is
duplicated. The increase in code size must be weighed against the performance
benefits of static dispatch.

- Homogeneous types. This is the other side of the "precise types" coin: ifTis a type parameter, it stands for asingleactual type. So for example
aVec<T>contains elements of a single concrete type (and, indeed, the
vector representation is specialized to lay these out in line). Sometimes
heterogeneous collections are useful; seetrait objects.
Homogeneous types. This is the other side of the "precise types" coin: ifTis a type parameter, it stands for asingleactual type. So for example
aVec<T>contains elements of a single concrete type (and, indeed, the
vector representation is specialized to lay these out in line). Sometimes
heterogeneous collections are useful; seetrait objects.

- Signature verbosity. Heavy use of generics can make it more difficult to
read and understand a function's signature.
Signature verbosity. Heavy use of generics can make it more difficult to
read and understand a function's signature.

### Examples from the standard library

- std::fs::File::opentakes an argument of generic typeAsRef<Path>. This
allows files to be opened conveniently from a string literal"f.txt", aPath, anOsString, and a few other types.

## Traits are object-safe if they may be useful as a trait object (C-OBJECT)

Trait objects have some significant limitations: methods invoked through a trait
object cannot use generics, and cannot useSelfexcept in receiver position.

When designing a trait, decide early on whether the trait will be used as an
object or as a bound on generics.

If a trait is meant to be used as an object, its methods should take and return
trait objects rather than use generics.

Awhereclause ofSelf: Sizedmay be used to exclude specific methods from
the trait's object. The following trait is not object-safe due to the generic
method.

```rust

#![allow(unused)]
fn main() {
trait MyTrait {
    fn object_safe(&self, i: i32);

    fn not_object_safe<T>(&self, t: T);
}
}
```

```rust

#![allow(unused)]
fn main() {
trait MyTrait {
    fn object_safe(&self, i: i32);

    fn not_object_safe<T>(&self, t: T);
}
}
```

Adding a requirement ofSelf: Sizedto the generic method excludes it from the
trait object and makes the trait object-safe.

```rust

#![allow(unused)]
fn main() {
trait MyTrait {
    fn object_safe(&self, i: i32);

    fn not_object_safe<T>(&self, t: T) where Self: Sized;
}
}
```

```rust

#![allow(unused)]
fn main() {
trait MyTrait {
    fn object_safe(&self, i: i32);

    fn not_object_safe<T>(&self, t: T) where Self: Sized;
}
}
```

### Advantages of trait objects

- Heterogeneity. When you need it, you really need it.
- Code size. Unlike generics, trait objects do not generate specialized
(monomorphized) versions of code, which can greatly reduce code size.

### Disadvantages of trait objects

- No generic methods. Trait objects cannot currently provide generic methods.
- Dynamic dispatch and fat pointers. Trait objects inherently involve
indirection and vtable dispatch, which can carry a performance penalty.
- No Self. Except for the method receiver argument, methods on trait objects
cannot use theSelftype.

### Examples from the standard library

- Theio::Readandio::Writetraits are often used as objects.
- TheIteratortrait has several generic methods marked withwhere Self: Sizedto retain the ability to useIteratoras an object.
