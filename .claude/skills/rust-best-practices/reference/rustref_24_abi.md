# Application Binary Interface

Source: https://doc.rust-lang.org/reference/

# Application binary interface (ABI)

This section documents features that affect the ABI of the compiled output of
a crate.

Seeextern functionsfor information on specifying the ABI for exporting
functions. Seeexternal blocksfor information on specifying the ABI for
linking external libraries.

## Theusedattribute

Theusedattributecan only be applied tostaticitems. Thisattributeforces the
compiler to keep the variable in the output object file (.o, .rlib, etc. excluding final binaries)
even if the variable is not used, or referenced, by any other item in the crate.
However, the linker is still free to remove such an item.

Below is an example that shows under what conditions the compiler keeps astaticitem in the
output object file.

```rust
#![allow(unused)]
fn main() {
// foo.rs

// This is kept because of `#[used]`:
#[used]
static FOO: u32 = 0;

// This is removable because it is unused:
#[allow(dead_code)]
static BAR: u32 = 0;

// This is kept because it is publicly reachable:
pub static BAZ: u32 = 0;

// This is kept because it is referenced by a public, reachable function:
static QUUX: u32 = 0;

pub fn quux() -> &'static u32 {
    &QUUX
}

// This is removable because it is referenced by a private, unused (dead) function:
static CORGE: u32 = 0;

#[allow(dead_code)]
fn corge() -> &'static u32 {
    &CORGE
}
}
```

```rust
#![allow(unused)]
fn main() {
// foo.rs

// This is kept because of `#[used]`:
#[used]
static FOO: u32 = 0;

// This is removable because it is unused:
#[allow(dead_code)]
static BAR: u32 = 0;

// This is kept because it is publicly reachable:
pub static BAZ: u32 = 0;

// This is kept because it is referenced by a public, reachable function:
static QUUX: u32 = 0;

pub fn quux() -> &'static u32 {
    &QUUX
}

// This is removable because it is referenced by a private, unused (dead) function:
static CORGE: u32 = 0;

#[allow(dead_code)]
fn corge() -> &'static u32 {
    &CORGE
}
}
```

```console
$ rustc -O --emit=obj --crate-type=rlib foo.rs

$ nm -C foo.o
0000000000000000 R foo::BAZ
0000000000000000 r foo::FOO
0000000000000000 R foo::QUUX
0000000000000000 T foo::quux
```

## Theno_mangleattribute

Theno_mangleattributemay be used on anyitemto disable standard
symbol name mangling. The symbol for the item will be the identifier of the
itemâs name.

Additionally, the item will be publicly exported from the produced library or
object file, similar to theusedattribute.

This attribute is unsafe as an unmangled symbol may collide with another symbol
with the same name (or with a well-known symbol), leading to undefined behavior.

```rust
#![allow(unused)]
fn main() {
#[unsafe(no_mangle)]
extern "C" fn foo() {}
}
```

```rust
#![allow(unused)]
fn main() {
#[unsafe(no_mangle)]
extern "C" fn foo() {}
}
```

> 2024Edition differencesBefore the 2024 edition it is allowed to use theno_mangleattribute without theunsafequalification.

2024Edition differences

Before the 2024 edition it is allowed to use theno_mangleattribute without theunsafequalification.

## Thelink_sectionattribute

Thelink_sectionattributespecifies the section of the object file that afunctionorstaticâs content will be placed into.

Thelink_sectionattribute uses theMetaNameValueStrsyntax to specify the section name.

```rust
#![allow(unused)]
fn main() {
#[unsafe(no_mangle)]
#[unsafe(link_section = ".example_section")]
pub static VAR1: u32 = 1;
}
```

```rust
#![allow(unused)]
fn main() {
#[unsafe(no_mangle)]
#[unsafe(link_section = ".example_section")]
pub static VAR1: u32 = 1;
}
```

This attribute is unsafe as it allows users to place data and code into sections
of memory not expecting them, such as mutable data into read-only areas.

> 2024Edition differencesBefore the 2024 edition it is allowed to use thelink_sectionattribute without theunsafequalification.

2024Edition differences

Before the 2024 edition it is allowed to use thelink_sectionattribute without theunsafequalification.

## Theexport_nameattribute

Theexport_nameattributespecifies the name of the symbol that will be
exported on afunctionorstatic.

Theexport_nameattribute uses theMetaNameValueStrsyntax to specify the symbol name.

```rust
#![allow(unused)]
fn main() {
#[unsafe(export_name = "exported_symbol_name")]
pub fn name_in_rust() { }
}
```

```rust
#![allow(unused)]
fn main() {
#[unsafe(export_name = "exported_symbol_name")]
pub fn name_in_rust() { }
}
```

This attribute is unsafe as a symbol with a custom name may collide with another
symbol with the same name (or with a well-known symbol), leading to undefined
behavior.

> 2024Edition differencesBefore the 2024 edition it is allowed to use theexport_nameattribute without theunsafequalification.

2024Edition differences

Before the 2024 edition it is allowed to use theexport_nameattribute without theunsafequalification.
