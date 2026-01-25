# Other Style Advice

Source: https://doc.rust-lang.org/nightly/style-guide/

# Other style advice

## Expressions

Prefer to use Rustâs expression oriented nature where possible;

```rust
#![allow(unused)]
fn main() {
// use
let x = if y { 1 } else { 0 };
// not
let x;
if y {
    x = 1;
} else {
    x = 0;
}
}
```

## Names

- Types shall beUpperCamelCase,
- Enum variants shall beUpperCamelCase,
- Struct fields shall besnake_case,
- Function and method names shall besnake_case,
- Local variables shall besnake_case,
- Macro names shall besnake_case,
- Constants (consts and immutablestatics) shall beSCREAMING_SNAKE_CASE.
- When a name is forbidden because it is a reserved word (such ascrate),
either use a raw identifier (r#crate) or use a trailing underscore
(crate_). Donât misspell the word (krate).

### Modules

Avoid#[path]annotations where possible.
