# Iterating over an Option

Source: https://rust-unofficial.github.io/patterns/

# Iterating over anOption

## Description

Optioncan be viewed as a container that contains either zero or one element.
In particular, it implements theIntoIteratortrait, and as such can be used
with generic code that needs such a type.

## Examples

SinceOptionimplementsIntoIterator, it can be used as an argument to.extend():

```rust
#![allow(unused)]
fn main() {
let turing = Some("Turing");
let mut logicians = vec!["Curry", "Kleene", "Markov"];

logicians.extend(turing);

// equivalent to
if let Some(turing_inner) = turing {
    logicians.push(turing_inner);
}
}
```

If you need to tack anOptionto the end of an existing iterator, you can pass
it to.chain():

```rust
#![allow(unused)]
fn main() {
let turing = Some("Turing");
let logicians = vec!["Curry", "Kleene", "Markov"];

for logician in logicians.iter().chain(turing.iter()) {
    println!("{logician} is a logician");
}
}
```

Note that if theOptionis alwaysSome, then it is more idiomatic to usestd::iter::onceon the
element instead.

Also, sinceOptionimplementsIntoIterator, it’s possible to iterate over it
using aforloop. This is equivalent to matching it withif let Some(..),
and in most cases you should prefer the latter.

## See also

- std::iter::onceis an
iterator which yields exactly one element. It’s a more readable alternative toSome(foo).into_iter().
std::iter::onceis an
iterator which yields exactly one element. It’s a more readable alternative toSome(foo).into_iter().

- Iterator::filter_mapis a version ofIterator::map,
specialized to mapping functions which returnOption.
Iterator::filter_mapis a version ofIterator::map,
specialized to mapping functions which returnOption.

- Theref_slicecrate provides functions
for converting anOptionto a zero- or one-element slice.
Theref_slicecrate provides functions
for converting anOptionto a zero- or one-element slice.

- Documentation forOption<T>
Documentation forOption<T>
