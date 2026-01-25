# Concatenating Strings with format!

Source: https://rust-unofficial.github.io/patterns/

# Concatenating strings withformat!

## Description

It is possible to build up strings using thepushandpush_strmethods on a
mutableString, or using its+operator. However, it is often more
convenient to useformat!, especially where there is a mix of literal and
non-literal strings.

## Example

```rust
#![allow(unused)]
fn main() {
fn say_hello(name: &str) -> String {
    // We could construct the result string manually.
    // let mut result = "Hello ".to_owned();
    // result.push_str(name);
    // result.push('!');
    // result

    // But using format! is better.
    format!("Hello {name}!")
}
}
```

## Advantages

Usingformat!is usually the most succinct and readable way to combine
strings.

## Disadvantages

It is usually not the most efficient way to combine strings - a series ofpushoperations on a mutable string is usually the most efficient (especially if the
string has been pre-allocated to the expected size).
