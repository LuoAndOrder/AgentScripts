# On-Stack Dynamic Dispatch

Source: https://rust-unofficial.github.io/patterns/

## Description

We can dynamically dispatch over multiple values, however, to do so, we need to
declare multiple variables to bind differently-typed objects. To extend the
lifetime as necessary, we can use deferred conditional initialization, as seen
below:

## Example

```rust
use std::io;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
let arg = "-";

// We need to describe the type to get dynamic dispatch.
let readable: &mut dyn io::Read = if arg == "-" {
    &mut io::stdin()
} else {
    &mut fs::File::open(arg)?
};

// Read from `readable` here.

Ok(())
}
```

## Motivation

Rust monomorphises code by default. This means a copy of the code will be
generated for each type it is used with and optimized independently. While this
allows for very fast code on the hot path, it also bloats the code in places
where performance is not of the essence, thus costing compile time and cache
usage.

Luckily, Rust allows us to use dynamic dispatch, but we have to explicitly ask
for it.

## Advantages

We do not need to allocate anything on the heap. Neither do we need to
initialize something we won’t use later, nor do we need to monomorphize the
whole code that follows to work with bothFileorStdin.

## Disadvantages

Before Rust 1.79.0, the code needed twoletbindings with deferred
initialization, which made up more moving parts than theBox-based version:

```rust
// We still need to ascribe the type for dynamic dispatch.
let readable: Box<dyn io::Read> = if arg == "-" {
    Box::new(io::stdin())
} else {
    Box::new(fs::File::open(arg)?)
};
// Read from `readable` here.
```

Luckily, this disadvantage is now gone. Yay!

## Discussion

Since Rust 1.79.0, the compiler will automatically extend the lifetimes of
temporary values within&or&mutas long as possible within the scope of
the function.

This means we can simply use a&mutvalue here without worrying about placing
the contents into someletbinding (which would have been needed for deferred
initialization, which was the solution used before that change).

We still have a place for each value (even if that place is temporary), the
compiler knows the size of each value and each borrowed value outlives all
references borrowed from it.

## See also

- Finalisation in destructorsandRAII guardscan benefit from tight control
over lifetimes.
- For conditionally filledOption<&T>s of (mutable) references, one can
initialize anOption<T>directly and use its.as_ref()method to get an
optional reference.
