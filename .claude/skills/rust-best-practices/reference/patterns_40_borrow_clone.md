# Clone to Satisfy Borrow Checker

Source: https://rust-unofficial.github.io/patterns/

# Clone to satisfy the borrow checker

## Description

The borrow checker prevents Rust users from developing otherwise unsafe code by
ensuring that either: only one mutable reference exists, or potentially many but
all immutable references exist. If the code written does not hold true to these
conditions, this anti-pattern arises when the developer resolves the compiler
error by cloning the variable.

## Example

```rust
#![allow(unused)]
fn main() {
// define any variable
let mut x = 5;

// Borrow `x` -- but clone it first
let y = &mut (x.clone());

// without the x.clone() two lines prior, this line would fail on compile as
// x has been borrowed
// thanks to x.clone(), x was never borrowed, and this line will run.
println!("{x}");

// perform some action on the borrow to prevent rust from optimizing this
//out of existence
*y += 1;
}
```

## Motivation

It is tempting, particularly for beginners, to use this pattern to resolve
confusing issues with the borrow checker. However, there are serious
consequences. Using.clone()causes a copy of the data to be made. Any changes
between the two are not synchronized – as if two completely separate variables
exist.

There are special cases –Rc<T>is designed to handle clones intelligently.
It internally manages exactly one copy of the data. Invoking.clone()onRcproduces a newRcinstance, which points to the same data as the sourceRc,
while increasing a reference count. The same applies toArc, the thread-safe
counterpart ofRc.

In general, clones should be deliberate, with full understanding of the
consequences. If a clone is used to make a borrow checker error disappear,
that’s a good indication this anti-pattern may be in use.

Even though.clone()is an indication of a bad pattern, sometimesit is fine
to write inefficient code, in cases such as when:

- the developer is still new to ownership
- the code doesn’t have great speed or memory constraints (like hackathon
projects or prototypes)
- satisfying the borrow checker is really complicated, and you prefer to
optimize readability over performance
If an unnecessary clone is suspected, TheRust Book’s chapter on Ownershipshould be understood fully before assessing whether the clone is required or
not.

Also be sure to always runcargo clippyin your project, which will detect
some cases in which.clone()is not necessary.

## See also

- mem::{take(_), replace(_)}to keep owned values in changed enums
- Rc<T>documentation, which handles .clone() intelligently
- Arc<T>documentation, a thread-safe reference-counting pointer
- Tricks with ownership in Rust
