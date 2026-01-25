# Collections Are Smart Pointers

Source: https://rust-unofficial.github.io/patterns/

# Collections are smart pointers

## Description

Use theDereftrait to
treat collections like smart pointers, offering owning and borrowed views of
data.

## Example

```rust
use std::ops::Deref;

struct Vec<T> {
    data: RawVec<T>,
    //..
}

impl<T> Deref for Vec<T> {
    type Target = [T];

    fn deref(&self) -> &[T] {
        //..
    }
}
```

AVec<T>is an owning collection ofTs, while a slice (&[T]) is a borrowed
collection ofTs. ImplementingDerefforVecallows implicit dereferencing
from&Vec<T>to&[T]and includes the relationship in auto-dereferencing
searches. Most methods you might expect to be implemented forVecs are instead
implemented for slices.

AlsoStringand&strhave a similar relation.

## Motivation

Ownership and borrowing are key aspects of the Rust language. Data structures
must account for these semantics properly to give a good user experience. When
implementing a data structure that owns its data, offering a borrowed view of
that data allows for more flexible APIs.

## Advantages

Most methods can be implemented only for the borrowed view, they are then
implicitly available for the owning view.

Gives clients a choice between borrowing or taking ownership of data.

## Disadvantages

Methods and traits only available via dereferencing are not taken into account
when bounds checking, so generic programming with data structures using this
pattern can get complex (see theBorrowandAsReftraits, etc.).

## Discussion

Smart pointers and collections are analogous: a smart pointer points to a single
object, whereas a collection points to many objects. From the point of view of
the type system, there is little difference between the two. A collection owns
its data if the only way to access each datum is via the collection and the
collection is responsible for deleting the data (even in cases of shared
ownership, some kind of borrowed view may be appropriate). If a collection owns
its data, it is usually useful to provide a view of the data as borrowed so that
it can be referenced multiple times.

Most smart pointers (e.g.,Foo<T>) implementDeref<Target=T>. However,
collections will usually dereference to a custom type.[T]andstrhave some
language support, but in the general case, this is not necessary.Foo<T>can
implementDeref<Target=Bar<T>>whereBaris a dynamically sized type and&Bar<T>is a borrowed view of the data inFoo<T>.

Commonly, ordered collections will implementIndexforRanges to provide
slicing syntax. The target will be the borrowed view.

## See also

- Deref polymorphism anti-pattern.
- Documentation forDereftrait.
