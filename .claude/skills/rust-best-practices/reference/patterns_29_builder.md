# Builder Pattern

Source: https://rust-unofficial.github.io/patterns/

# Builder

## Description

Construct an object with calls to a builder helper.

## Example

```rust
#![allow(unused)]
fn main() {
#[derive(Debug, PartialEq)]
pub struct Foo {
    // Lots of complicated fields.
    bar: String,
}

impl Foo {
    // This method will help users to discover the builder
    pub fn builder() -> FooBuilder {
        FooBuilder::default()
    }
}

#[derive(Default)]
pub struct FooBuilder {
    // Probably lots of optional fields.
    bar: String,
}

impl FooBuilder {
    pub fn new(/* ... */) -> FooBuilder {
        // Set the minimally required fields of Foo.
        FooBuilder {
            bar: String::from("X"),
        }
    }

    pub fn name(mut self, bar: String) -> FooBuilder {
        // Set the name on the builder itself, and return the builder by value.
        self.bar = bar;
        self
    }

    // If we can get away with not consuming the Builder here, that is an
    // advantage. It means we can use the FooBuilder as a template for constructing
    // many Foos.
    pub fn build(self) -> Foo {
        // Create a Foo from the FooBuilder, applying all settings in FooBuilder
        // to Foo.
        Foo { bar: self.bar }
    }
}

#[test]
fn builder_test() {
    let foo = Foo {
        bar: String::from("Y"),
    };
    let foo_from_builder: Foo = FooBuilder::new().name(String::from("Y")).build();
    assert_eq!(foo, foo_from_builder);
}
}
```

## Motivation

Useful when you would otherwise require many constructors or where construction
has side effects.

## Advantages

Separates methods for building from other methods.

Prevents proliferation of constructors.

Can be used for one-liner initialisation as well as more complex construction.

When you add new fields to the target struct, you can update the builder to
leave client code backwards compatible.

## Disadvantages

More complex than creating a struct object directly, or a simple constructor
function.

## Discussion

This pattern is seen more frequently in Rust (and for simpler objects) than in
many other languages because Rust lacks overloading and default values for
function parameters. Since you can only have a single method with a given name,
having multiple constructors is less nice in Rust than in C++, Java, or others.

This pattern is often used where the builder object is useful in its own right,
rather than being just a builder. For example, seestd::process::Commandis a builder forChild(a process).
In these cases, theTandTBuildernaming pattern is not used.

The example takes and returns the builder by value. It is often more ergonomic
(and more efficient) to take and return the builder as a mutable reference. The
borrow checker makes this work naturally. This approach has the advantage that
one can write code like

```rust
let mut fb = FooBuilder::new();
fb.a();
fb.b();
let f = fb.build();
```

as well as theFooBuilder::new().a().b().build()style.

## See also

- Description in the style guide
- derive_builder, a crate for
automatically implementing this pattern while avoiding the boilerplate.
- Constructor patternfor when construction is simpler.
- Builder pattern (wikipedia)
- Construction of complex values
