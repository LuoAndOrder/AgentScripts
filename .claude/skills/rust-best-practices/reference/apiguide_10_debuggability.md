# Debuggability

Source: https://rust-lang.github.io/api-guidelines/

## All public types implementDebug(C-DEBUG)

If there are exceptions, they are rare.

## Debugrepresentation is never empty (C-DEBUG-NONEMPTY)

Even for conceptually empty values, theDebugrepresentation should never be
empty.

```rust

#![allow(unused)]
fn main() {
let empty_str = "";
assert_eq!(format!("{:?}", empty_str), "\"\"");

let empty_vec = Vec::<bool>::new();
assert_eq!(format!("{:?}", empty_vec), "[]");
}
```

```rust

#![allow(unused)]
fn main() {
let empty_str = "";
assert_eq!(format!("{:?}", empty_str), "\"\"");

let empty_vec = Vec::<bool>::new();
assert_eq!(format!("{:?}", empty_vec), "[]");
}
```
