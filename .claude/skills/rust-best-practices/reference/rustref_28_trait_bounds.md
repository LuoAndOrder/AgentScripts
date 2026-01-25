# Trait and Lifetime Bounds

Source: https://doc.rust-lang.org/reference/

# Trait and lifetime bounds

SyntaxTypeParamBoundsâTypeParamBound(+TypeParamBound)*+?

TypeParamBoundâLifetime|TraitBound|UseBound

TraitBoundâÂ Â Â Â Â Â (?|ForLifetimes)?TypePathÂ Â Â Â |((?|ForLifetimes)?TypePath)

LifetimeBoundsâ (Lifetime+)*Lifetime?

LifetimeâÂ Â Â Â Â ÂLIFETIME_OR_LABELÂ Â Â Â |'staticÂ Â Â Â |'_

UseBoundâuseUseBoundGenericArgs

UseBoundGenericArgsâÂ Â Â Â Â Â<>Â Â Â Â |<(UseBoundGenericArg,)*UseBoundGenericArg,?>

UseBoundGenericArgâÂ Â Â Â Â ÂLifetimeÂ Â Â Â |IDENTIFIERÂ Â Â Â |Self

Show Railroad

Traitand lifetime bounds provide a way forgeneric itemsto
restrict which types and lifetimes are used as their parameters. Bounds can be
provided on any type in awhere clause. There are also shorter forms for
certain common cases:

- Bounds written after declaring ageneric parameter:fn f<A: Copy>() {}is the same asfn f<A>() where A: Copy {}.
- In trait declarations assupertraits:trait Circle : Shape {}is
equivalent totrait Circle where Self : Shape {}.
- In trait declarations as bounds onassociated types:trait A { type B: Copy; }is equivalent totrait A where Self::B: Copy { type B; }.
Bounds on an item must be satisfied when using the item. When type checking and
borrow checking a generic item, the bounds can be used to determine that a
trait is implemented for a type. For example, givenTy: Trait

- In the body of a generic function, methods fromTraitcan be called onTyvalues. Likewise associated constants on theTraitcan be used.
- Associated types fromTraitcan be used.
- Generic functions and types with aT: Traitbounds can be used withTybeing used forT.

```rust
#![allow(unused)]
fn main() {
type Surface = i32;
trait Shape {
    fn draw(&self, surface: Surface);
    fn name() -> &'static str;
}

fn draw_twice<T: Shape>(surface: Surface, sh: T) {
    sh.draw(surface);           // Can call method because T: Shape
    sh.draw(surface);
}

fn copy_and_draw_twice<T: Copy>(surface: Surface, sh: T) where T: Shape {
    let shape_copy = sh;        // doesn't move sh because T: Copy
    draw_twice(surface, sh);    // Can use generic function because T: Shape
}

struct Figure<S: Shape>(S, S);

fn name_figure<U: Shape>(
    figure: Figure<U>,          // Type Figure<U> is well-formed because U: Shape
) {
    println!(
        "Figure of two {}",
        U::name(),              // Can use associated function
    );
}
}
```

```rust
#![allow(unused)]
fn main() {
type Surface = i32;
trait Shape {
    fn draw(&self, surface: Surface);
    fn name() -> &'static str;
}

fn draw_twice<T: Shape>(surface: Surface, sh: T) {
    sh.draw(surface);           // Can call method because T: Shape
    sh.draw(surface);
}

fn copy_and_draw_twice<T: Copy>(surface: Surface, sh: T) where T: Shape {
    let shape_copy = sh;        // doesn't move sh because T: Copy
    draw_twice(surface, sh);    // Can use generic function because T: Shape
}

struct Figure<S: Shape>(S, S);

fn name_figure<U: Shape>(
    figure: Figure<U>,          // Type Figure<U> is well-formed because U: Shape
) {
    println!(
        "Figure of two {}",
        U::name(),              // Can use associated function
    );
}
}
```

Bounds that donât use the itemâs parameters orhigher-ranked lifetimesare checked when the item is defined.
It is an error for such a bound to be false.

Copy,Clone, andSizedbounds are also checked for certain generic types when using the item, even if the use does not provide a concrete type.
It is an error to haveCopyorCloneas a bound on a mutable reference,trait object, orslice.
It is an error to haveSizedas a bound on a trait object or slice.

```rust
#![allow(unused)]
fn main() {
struct A<'a, T>
where
    i32: Default,           // Allowed, but not useful
    i32: Iterator,          // Error: `i32` is not an iterator
    &'a mut T: Copy,        // (at use) Error: the trait bound is not satisfied
    [T]: Sized,             // (at use) Error: size cannot be known at compilation
{
    f: &'a T,
}
struct UsesA<'a, T>(A<'a, T>);
}
```

```rust
#![allow(unused)]
fn main() {
struct A<'a, T>
where
    i32: Default,           // Allowed, but not useful
    i32: Iterator,          // Error: `i32` is not an iterator
    &'a mut T: Copy,        // (at use) Error: the trait bound is not satisfied
    [T]: Sized,             // (at use) Error: size cannot be known at compilation
{
    f: &'a T,
}
struct UsesA<'a, T>(A<'a, T>);
}
```

Trait and lifetime bounds are also used to nametrait objects.

## ?Sized

?is only used to relax the implicitSizedtrait bound fortype parametersorassociated types.?Sizedmay not be used as a bound for other types.

## Lifetime bounds

Lifetime bounds can be applied to types or to other lifetimes.

The bound'a: 'bis usually read as'aoutlives'b.'a: 'bmeans that'alasts at least as long as'b, so a reference&'a ()is valid whenever&'b ()is valid.

```rust
#![allow(unused)]
fn main() {
fn f<'a, 'b>(x: &'a i32, mut y: &'b i32) where 'a: 'b {
    y = x;                      // &'a i32 is a subtype of &'b i32 because 'a: 'b
    let r: &'b &'a i32 = &&0;   // &'b &'a i32 is well formed because 'a: 'b
}
}
```

```rust
#![allow(unused)]
fn main() {
fn f<'a, 'b>(x: &'a i32, mut y: &'b i32) where 'a: 'b {
    y = x;                      // &'a i32 is a subtype of &'b i32 because 'a: 'b
    let r: &'b &'a i32 = &&0;   // &'b &'a i32 is well formed because 'a: 'b
}
}
```

T: 'ameans that all lifetime parameters ofToutlive'a.
For example, if'ais an unconstrained lifetime parameter, theni32: 'staticand&'static str: 'aare satisfied, butVec<&'a ()>: 'staticis not.

## Higher-ranked trait bounds

SyntaxForLifetimesâforGenericParams

Show Railroad

Trait bounds may behigher rankedover lifetimes. These bounds specify a bound
that is truefor alllifetimes. For example, a bound such asfor<'a> &'a T: PartialEq<i32>would require an implementation like

```rust
#![allow(unused)]
fn main() {
struct T;
impl<'a> PartialEq<i32> for &'a T {
    // ...
   fn eq(&self, other: &i32) -> bool {true}
}
}
```

```rust
#![allow(unused)]
fn main() {
struct T;
impl<'a> PartialEq<i32> for &'a T {
    // ...
   fn eq(&self, other: &i32) -> bool {true}
}
}
```

and could then be used to compare a&'a Twith any lifetime to ani32.

Only a higher-ranked bound can be used here, because the lifetime of the reference is shorter than any possible lifetime parameter on the function:

```rust
#![allow(unused)]
fn main() {
fn call_on_ref_zero<F>(f: F) where for<'a> F: Fn(&'a i32) {
    let zero = 0;
    f(&zero);
}
}
```

```rust
#![allow(unused)]
fn main() {
fn call_on_ref_zero<F>(f: F) where for<'a> F: Fn(&'a i32) {
    let zero = 0;
    f(&zero);
}
}
```

Higher-ranked lifetimes may also be specified just before the trait: the only
difference is thescopeof the lifetime parameter, which extends only to the
end of the following trait instead of the whole bound. This function is
equivalent to the last one.

```rust
#![allow(unused)]
fn main() {
fn call_on_ref_zero<F>(f: F) where F: for<'a> Fn(&'a i32) {
    let zero = 0;
    f(&zero);
}
}
```

```rust
#![allow(unused)]
fn main() {
fn call_on_ref_zero<F>(f: F) where F: for<'a> Fn(&'a i32) {
    let zero = 0;
    f(&zero);
}
}
```

## Implied bounds

Lifetime bounds required for types to be well-formed are sometimes inferred.

```rust
#![allow(unused)]
fn main() {
fn requires_t_outlives_a<'a, T>(x: &'a T) {}
}
```

```rust
#![allow(unused)]
fn main() {
fn requires_t_outlives_a<'a, T>(x: &'a T) {}
}
```

The type parameterTis required to outlive'afor the type&'a Tto be well-formed.
This is inferred because the function signature contains the type&'a Twhich is
only valid ifT: 'aholds.

Implied bounds are added for all parameters and outputs of functions. Inside ofrequires_t_outlives_ayou can assumeT: 'ato hold even if you donât explicitly specify this:

```rust
#![allow(unused)]
fn main() {
fn requires_t_outlives_a_not_implied<'a, T: 'a>() {}

fn requires_t_outlives_a<'a, T>(x: &'a T) {
    // This compiles, because `T: 'a` is implied by
    // the reference type `&'a T`.
    requires_t_outlives_a_not_implied::<'a, T>();
}
}
```

```rust
#![allow(unused)]
fn main() {
fn requires_t_outlives_a_not_implied<'a, T: 'a>() {}

fn requires_t_outlives_a<'a, T>(x: &'a T) {
    // This compiles, because `T: 'a` is implied by
    // the reference type `&'a T`.
    requires_t_outlives_a_not_implied::<'a, T>();
}
}
```

```rust
#![allow(unused)]
fn main() {
fn requires_t_outlives_a_not_implied<'a, T: 'a>() {}
fn not_implied<'a, T>() {
    // This errors, because `T: 'a` is not implied by
    // the function signature.
    requires_t_outlives_a_not_implied::<'a, T>();
}
}
```

```rust
#![allow(unused)]
fn main() {
fn requires_t_outlives_a_not_implied<'a, T: 'a>() {}
fn not_implied<'a, T>() {
    // This errors, because `T: 'a` is not implied by
    // the function signature.
    requires_t_outlives_a_not_implied::<'a, T>();
}
}
```

Only lifetime bounds are implied, trait bounds still have to be explicitly added.
The following example therefore causes an error:

```rust
#![allow(unused)]
fn main() {
use std::fmt::Debug;
struct IsDebug<T: Debug>(T);
// error[E0277]: `T` doesn't implement `Debug`
fn doesnt_specify_t_debug<T>(x: IsDebug<T>) {}
}
```

```rust
#![allow(unused)]
fn main() {
use std::fmt::Debug;
struct IsDebug<T: Debug>(T);
// error[E0277]: `T` doesn't implement `Debug`
fn doesnt_specify_t_debug<T>(x: IsDebug<T>) {}
}
```

Lifetime bounds are also inferred for type definitions and impl blocks for any type:

```rust
#![allow(unused)]
fn main() {
struct Struct<'a, T> {
    // This requires `T: 'a` to be well-formed
    // which is inferred by the compiler.
    field: &'a T,
}

enum Enum<'a, T> {
    // This requires `T: 'a` to be well-formed,
    // which is inferred by the compiler.
    //
    // Note that `T: 'a` is required even when only
    // using `Enum::OtherVariant`.
    SomeVariant(&'a T),
    OtherVariant,
}

trait Trait<'a, T: 'a> {}

// This would error because `T: 'a` is not implied by any type
// in the impl header.
//     impl<'a, T> Trait<'a, T> for () {}

// This compiles as `T: 'a` is implied by the self type `&'a T`.
impl<'a, T> Trait<'a, T> for &'a T {}
}
```

```rust
#![allow(unused)]
fn main() {
struct Struct<'a, T> {
    // This requires `T: 'a` to be well-formed
    // which is inferred by the compiler.
    field: &'a T,
}

enum Enum<'a, T> {
    // This requires `T: 'a` to be well-formed,
    // which is inferred by the compiler.
    //
    // Note that `T: 'a` is required even when only
    // using `Enum::OtherVariant`.
    SomeVariant(&'a T),
    OtherVariant,
}

trait Trait<'a, T: 'a> {}

// This would error because `T: 'a` is not implied by any type
// in the impl header.
//     impl<'a, T> Trait<'a, T> for () {}

// This compiles as `T: 'a` is implied by the self type `&'a T`.
impl<'a, T> Trait<'a, T> for &'a T {}
}
```

## Use bounds

Certain bounds lists may include ause<..>bound to control which generic parameters are captured by theimpl Traitabstract return type.  Seeprecise capturingfor more details.
