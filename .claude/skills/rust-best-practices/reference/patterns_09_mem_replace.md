# mem::take and mem::replace

Source: https://rust-unofficial.github.io/patterns/

# mem::{take(_), replace(_)}to keep owned values in changed enums

## Description

Say we have a&mut MyEnumwhich has (at least) two variants,A { name: String, x: u8 }andB { name: String }. Now we want to changeMyEnum::Ato aBifxis zero, while keepingMyEnum::Bintact.

We can do this without cloning thename.

## Example

```rust
#![allow(unused)]
fn main() {
use std::mem;

enum MyEnum {
    A { name: String, x: u8 },
    B { name: String },
}

fn a_to_b(e: &mut MyEnum) {
    if let MyEnum::A { name, x: 0 } = e {
        // This takes out our `name` and puts in an empty String instead
        // (note that empty strings don't allocate).
        // Then, construct the new enum variant (which will
        // be assigned to `*e`).
        *e = MyEnum::B {
            name: mem::take(name),
        }
    }
}
}
```

This also works with more variants:

```rust
#![allow(unused)]
fn main() {
use std::mem;

enum MultiVariateEnum {
    A { name: String },
    B { name: String },
    C,
    D,
}

fn swizzle(e: &mut MultiVariateEnum) {
    use MultiVariateEnum::*;
    *e = match e {
        // Ownership rules do not allow taking `name` by value, but we cannot
        // take the value out of a mutable reference, unless we replace it:
        A { name } => B {
            name: mem::take(name),
        },
        B { name } => A {
            name: mem::take(name),
        },
        C => D,
        D => C,
    }
}
}
```

## Motivation

When working with enums, we may want to change an enum value in place, perhaps
to another variant. This is usually done in two phases to keep the borrow
checker happy. In the first phase, we observe the existing value and look at its
parts to decide what to do next. In the second phase we may conditionally change
the value (as in the example above).

The borrow checker won’t allow us to take outnameof the enum (becausesomethingmust be there.) We could of course.clone()name and put the clone
into ourMyEnum::B, but that would be an instance of theClone to satisfy the borrow checkeranti-pattern. Anyway, we can avoid the extra allocation by changingewith
only a mutable borrow.

mem::takelets us swap out the value, replacing it with its default value, and
returning the previous value. ForString, the default value is an emptyString, which does not need to allocate. As a result, we get the originalnameas an owned value. We can then wrap this in another enum.

NOTE:mem::replaceis very similar, but allows us to specify what to
replace the value with. An equivalent to ourmem::takeline would bemem::replace(name, String::new()).

Note, however, that if we are using anOptionand want to replace its value
with aNone,Option’stake()method provides a shorter and more idiomatic
alternative.

## Advantages

Look ma, no allocation! Also you may feel like Indiana Jones while doing it.

## Disadvantages

This gets a bit wordy. Getting it wrong repeatedly will make you hate the borrow
checker. The compiler may fail to optimize away the double store, resulting in
reduced performance as opposed to what you’d do in unsafe languages.

Furthermore, the type you are taking needs to implement theDefaulttrait. However, if the type you’re working with
doesn’t implement this, you can instead usemem::replace.

## Discussion

This pattern is only of interest in Rust. In GC’d languages, you’d take the
reference to the value by default (and the GC would keep track of refs), and in
other low-level languages like C you’d simply alias the pointer and fix things
later.

However, in Rust, we have to do a little more work to do this. An owned value
may only have one owner, so to take it out, we need to put something back in –
like Indiana Jones, replacing the artifact with a bag of sand.

## See also

This gets rid of theClone to satisfy the borrow checkeranti-pattern in a specific case.
