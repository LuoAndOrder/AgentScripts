# Macros

Source: https://doc.rust-lang.org/reference/

The functionality and syntax of Rust can be extended with custom definitions
called macros. They are given names, and invoked through a consistent
syntax:some_extension!(...).

There are two ways to define new macros:

- Macros by Exampledefine new syntax in a higher-level, declarative way.
- Procedural Macrosdefine function-like macros, custom derives, and custom
attributes using functions that operate on input tokens.

## Macro invocation

SyntaxMacroInvocationâÂ Â Â ÂSimplePath!DelimTokenTree

DelimTokenTreeâÂ Â Â Â Â Â(TokenTree*)Â Â Â Â |[TokenTree*]Â Â Â Â |{TokenTree*}

TokenTreeâÂ Â Â ÂTokenexceptdelimiters|DelimTokenTree

MacroInvocationSemiâÂ Â Â Â Â ÂSimplePath!(TokenTree*);Â Â Â Â |SimplePath![TokenTree*];Â Â Â Â |SimplePath!{TokenTree*}

Show Railroad

A macro invocation expands a macro at compile time and replaces the
invocation with the result of the macro. Macros may be invoked in the
following situations:

- Expressionsandstatements
- Patterns
- Types
- Itemsincludingassociated items
- macro_rulestranscribers
- External blocks
When used as an item or a statement, theMacroInvocationSemiform is used
where a semicolon is required at the end when not using curly braces.Visibility qualifiersare never allowed before a macro invocation ormacro_rulesdefinition.

```rust
#![allow(unused)]
fn main() {
// Used as an expression.
let x = vec![1,2,3];

// Used as a statement.
println!("Hello!");

// Used in a pattern.
macro_rules! pat {
    ($i:ident) => (Some($i))
}

if let pat!(x) = Some(1) {
    assert_eq!(x, 1);
}

// Used in a type.
macro_rules! Tuple {
    { $A:ty, $B:ty } => { ($A, $B) };
}

type N2 = Tuple!(i32, i32);

// Used as an item.
use std::cell::RefCell;
thread_local!(static FOO: RefCell<u32> = RefCell::new(1));

// Used as an associated item.
macro_rules! const_maker {
    ($t:ty, $v:tt) => { const CONST: $t = $v; };
}
trait T {
    const_maker!{i32, 7}
}

// Macro calls within macros.
macro_rules! example {
    () => { println!("Macro call in a macro!") };
}
// Outer macro `example` is expanded, then inner macro `println` is expanded.
example!();
}
```

```rust
#![allow(unused)]
fn main() {
// Used as an expression.
let x = vec![1,2,3];

// Used as a statement.
println!("Hello!");

// Used in a pattern.
macro_rules! pat {
    ($i:ident) => (Some($i))
}

if let pat!(x) = Some(1) {
    assert_eq!(x, 1);
}

// Used in a type.
macro_rules! Tuple {
    { $A:ty, $B:ty } => { ($A, $B) };
}

type N2 = Tuple!(i32, i32);

// Used as an item.
use std::cell::RefCell;
thread_local!(static FOO: RefCell<u32> = RefCell::new(1));

// Used as an associated item.
macro_rules! const_maker {
    ($t:ty, $v:tt) => { const CONST: $t = $v; };
}
trait T {
    const_maker!{i32, 7}
}

// Macro calls within macros.
macro_rules! example {
    () => { println!("Macro call in a macro!") };
}
// Outer macro `example` is expanded, then inner macro `println` is expanded.
example!();
}
```
