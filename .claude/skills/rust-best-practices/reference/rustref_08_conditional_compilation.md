# Conditional Compilation

Source: https://doc.rust-lang.org/reference/

# Conditional compilation

SyntaxConfigurationPredicateâÂ Â Â Â Â ÂConfigurationOptionÂ Â Â Â |ConfigurationAllÂ Â Â Â |ConfigurationAnyÂ Â Â Â |ConfigurationNotÂ Â Â Â |trueÂ Â Â Â |false

ConfigurationOptionâÂ Â Â ÂIDENTIFIER(=(STRING_LITERAL|RAW_STRING_LITERAL) )?

ConfigurationAllâÂ Â Â Âall(ConfigurationPredicateList?)

ConfigurationAnyâÂ Â Â Âany(ConfigurationPredicateList?)

ConfigurationNotâÂ Â Â Ânot(ConfigurationPredicate)

ConfigurationPredicateListâÂ Â Â ÂConfigurationPredicate(,ConfigurationPredicate)*,?

Show Railroad

Conditionally compiled source codeis source code that is compiled only under certain conditions.

Source code can be made conditionally compiled using thecfgandcfg_attrattributesand the built-incfgmacro.

Whether to compile can depend on the target architecture of the compiled crate, arbitrary values passed to the compiler, and other things further described below.

Each form of conditional compilation takes aconfiguration predicatethat
evaluates to true or false. The predicate is one of the following:

- A configuration option. The predicate is true if the option is set, and false if it is unset.
- all()with a comma-separated list of configuration predicates. It is true if all of the given predicates are true, or if the list is empty.
- any()with a comma-separated list of configuration predicates. It is true if at least one of the given predicates is true. If there are no predicates, it is false.
- not()with a configuration predicate. It is true if its predicate is false and false if its predicate is true.
- trueorfalseliterals, which are always true or false respectively.
Configuration optionsare either names or key-value pairs, and are either set or unset.

Names are written as a single identifier, such asunix.

Key-value pairs are written as an identifier,=, and then a string, such astarget_arch = "x86_64".

> NoteWhitespace around the=is ignored, sofoo="bar"andfoo = "bar"are equivalent.

Note

Whitespace around the=is ignored, sofoo="bar"andfoo = "bar"are equivalent.

Keys do not need to be unique. For example, bothfeature = "std"andfeature = "serde"can be set at the same time.

## Set configuration options

Which configuration options are set is determined statically during the
compilation of the crate.

Some options arecompiler-setbased on data about the compilation.

Other options arearbitrarily-setbased on input passed to the compiler outside of the code.

It is not possible to set a
configuration option from within the source code of the crate being compiled.

> NoteForrustc, arbitrary-set configuration options are set using the--cfgflag. Configuration values for a specified target can be displayed withrustc --print cfg --target $TARGET.

Note

Forrustc, arbitrary-set configuration options are set using the--cfgflag. Configuration values for a specified target can be displayed withrustc --print cfg --target $TARGET.

> NoteConfiguration options with the keyfeatureare a convention used byCargofor specifying compile-time options and optional dependencies.

Note

Configuration options with the keyfeatureare a convention used byCargofor specifying compile-time options and optional dependencies.

### target_arch

Key-value option set once with the targetâs CPU architecture. The value is
similar to the first element of the platformâs target triple, but not
identical.

Example values:

- "x86"
- "x86_64"
- "mips"
- "powerpc"
- "powerpc64"
- "arm"
- "aarch64"

### target_feature

Key-value option set for each platform feature available for the current
compilation target.

Example values:

- "avx"
- "avx2"
- "crt-static"
- "rdrand"
- "sse"
- "sse2"
- "sse4.1"
See thetarget_featureattributefor more details on the available
features.

An additional feature ofcrt-staticis available to thetarget_featureoption to indicate that astatic C runtimeis available.

### target_os

Key-value option set once with the targetâs operating system. This value is
similar to the second and third element of the platformâs target triple.

Example values:

- "windows"
- "macos"
- "ios"
- "linux"
- "android"
- "freebsd"
- "dragonfly"
- "openbsd"
- "netbsd"
- "none"(typical for embedded targets)

### target_family

Key-value option providing a more generic description of a target, such as the family of the
operating systems or architectures that the target generally falls into. Any number oftarget_familykey-value pairs can be set.

Example values:

- "unix"
- "windows"
- "wasm"
- Both"unix"and"wasm"

### unixandwindows

unixis set iftarget_family = "unix"is set.

windowsis set iftarget_family = "windows"is set.

### target_env

Key-value option set with further disambiguating information about the target
platform with information about the ABI orlibcused. For historical reasons,
this value is only defined as not the empty-string when actually needed for
disambiguation. Thus, for example, on many GNU platforms, this value will be
empty. This value is similar to the fourth element of the platformâs target
triple. One difference is that embedded ABIs such asgnueabihfwill simply
definetarget_envas"gnu".

Example values:

- ""
- "gnu"
- "msvc"
- "musl"
- "sgx"
- "sim"
- "macabi"

### target_abi

Key-value option set to further disambiguate the target with information about
the target ABI.

For historical reasons, this value is only defined as not the empty-string when actually
needed for disambiguation. Thus, for example, on many GNU platforms, this value will be
empty.

Example values:

- ""
- "llvm"
- "eabihf"
- "abi64"

### target_endian

Key-value option set once with either a value of âlittleâ or âbigâ depending
on the endianness of the targetâs CPU.

### target_pointer_width

Key-value option set once with the targetâs pointer width in bits.

Example values:

- "16"
- "32"
- "64"

### target_vendor

Key-value option set once with the vendor of the target.

Example values:

- "apple"
- "fortanix"
- "pc"
- "unknown"

### target_has_atomic

Key-value option set for each bit width that the target supports
atomic loads, stores, and compare-and-swap operations.

When this cfg is present, all of the stablecore::sync::atomicAPIs are available for
the relevant atomic width.

Possible values:

- "8"
- "16"
- "32"
- "64"
- "128"
- "ptr"

### test

Enabled when compiling the test harness. Done withrustcby using the--testflag. SeeTestingfor more on testing support.

### debug_assertions

Enabled by default when compiling without optimizations.
This can be used to enable extra debugging code in development but not in
production.  For example, it controls the behavior of the standard libraryâsdebug_assert!macro.

### proc_macro

Set when the crate being compiled is being compiled with theproc_macrocrate type.

### panic

Key-value option set depending on thepanic strategy. Note that more values may be added in the future.

Example values:

- "abort"
- "unwind"

## Forms of conditional compilation

### Thecfgattribute

Thecfgattributeconditionally includes the form to which it is attached based on a configuration predicate.

> Example#![allow(unused)]fn main() {// The function is only included in the build when compiling for macOS
> #[cfg(target_os = "macos")]
> fn macos_only() {
>   // ...
> }
> 
> // This function is only included when either foo or bar is defined
> #[cfg(any(foo, bar))]
> fn needs_foo_or_bar() {
>   // ...
> }
> 
> // This function is only included when compiling for a unixish OS with a 32-bit
> // architecture
> #[cfg(all(unix, target_pointer_width = "32"))]
> fn on_32bit_unix() {
>   // ...
> }
> 
> // This function is only included when foo is not defined
> #[cfg(not(foo))]
> fn needs_not_foo() {
>   // ...
> }
> 
> // This function is only included when the panic strategy is set to unwind
> #[cfg(panic = "unwind")]
> fn when_unwinding() {
>   // ...
> }}

Example

```rust
#![allow(unused)]
fn main() {
// The function is only included in the build when compiling for macOS
#[cfg(target_os = "macos")]
fn macos_only() {
  // ...
}

// This function is only included when either foo or bar is defined
#[cfg(any(foo, bar))]
fn needs_foo_or_bar() {
  // ...
}

// This function is only included when compiling for a unixish OS with a 32-bit
// architecture
#[cfg(all(unix, target_pointer_width = "32"))]
fn on_32bit_unix() {
  // ...
}

// This function is only included when foo is not defined
#[cfg(not(foo))]
fn needs_not_foo() {
  // ...
}

// This function is only included when the panic strategy is set to unwind
#[cfg(panic = "unwind")]
fn when_unwinding() {
  // ...
}
}
```

```rust
#![allow(unused)]
fn main() {
// The function is only included in the build when compiling for macOS
#[cfg(target_os = "macos")]
fn macos_only() {
  // ...
}

// This function is only included when either foo or bar is defined
#[cfg(any(foo, bar))]
fn needs_foo_or_bar() {
  // ...
}

// This function is only included when compiling for a unixish OS with a 32-bit
// architecture
#[cfg(all(unix, target_pointer_width = "32"))]
fn on_32bit_unix() {
  // ...
}

// This function is only included when foo is not defined
#[cfg(not(foo))]
fn needs_not_foo() {
  // ...
}

// This function is only included when the panic strategy is set to unwind
#[cfg(panic = "unwind")]
fn when_unwinding() {
  // ...
}
}
```

The syntax for thecfgattribute is:

SyntaxCfgAttributeâcfg(ConfigurationPredicate)

Show Railroad

Thecfgattribute may be used anywhere attributes are allowed.

Thecfgattribute may be used any number of times on a form. The form to which the attributes are attached will not be included if any of thecfgpredicates are false except as described incfg.attr.crate-level-attrs.

If the predicates are true, the form is rewritten to not have thecfgattributes on it. If any predicate is false, the form is removed from the source code.

When a crate-levelcfghas a false predicate, the crate itself still exists. Any crate attributes preceding thecfgare kept, and any crate attributes following thecfgare removed as well as removing all of the following crate contents.

> ExampleThe behavior of not removing the preceding attributes allows you to do things such as include#![no_std]to avoid linkingstdeven if a#![cfg(...)]has otherwise removed the contents of the crate. For example:// This `no_std` attribute is kept even though the crate-level `cfg`
> // attribute is false.
> #![no_std]
> #![cfg(false)]
> 
> // This function is not included.
> pub fn example() {}

Example

The behavior of not removing the preceding attributes allows you to do things such as include#![no_std]to avoid linkingstdeven if a#![cfg(...)]has otherwise removed the contents of the crate. For example:

```rust
// This `no_std` attribute is kept even though the crate-level `cfg`
// attribute is false.
#![no_std]
#![cfg(false)]

// This function is not included.
pub fn example() {}
```

### Thecfg_attrattribute

Thecfg_attrattributeconditionally includes attributes based on a configuration predicate.

> ExampleThe following module will either be found atlinux.rsorwindows.rsbased on the target.#[cfg_attr(target_os = "linux", path = "linux.rs")]
> #[cfg_attr(windows, path = "windows.rs")]
> mod os;

Example

The following module will either be found atlinux.rsorwindows.rsbased on the target.

```rust
#[cfg_attr(target_os = "linux", path = "linux.rs")]
#[cfg_attr(windows, path = "windows.rs")]
mod os;
```

The syntax for thecfg_attrattribute is:

SyntaxCfgAttrAttributeâcfg_attr(ConfigurationPredicate,CfgAttrs?)

CfgAttrsâAttr(,Attr)*,?

Show Railroad

Thecfg_attrattribute may be used anywhere attributes are allowed.

Thecfg_attrattribute may be used any number of times on a form.

Thecrate_typeandcrate_nameattributes cannot be used withcfg_attr.

When the configuration predicate is true,cfg_attrexpands out to the attributes listed after the predicate.

Zero, one, or more attributes may be listed. Multiple attributes will each be expanded into separate attributes.

> Example#[cfg_attr(feature = "magic", sparkles, crackles)]
> fn bewitched() {}
> 
> // When the `magic` feature flag is enabled, the above will expand to:
> #[sparkles]
> #[crackles]
> fn bewitched() {}

Example

```rust
#[cfg_attr(feature = "magic", sparkles, crackles)]
fn bewitched() {}

// When the `magic` feature flag is enabled, the above will expand to:
#[sparkles]
#[crackles]
fn bewitched() {}
```

> NoteThecfg_attrcan expand to anothercfg_attr. For example,#[cfg_attr(target_os = "linux", cfg_attr(feature = "multithreaded", some_other_attribute))]is valid. This example would be equivalent to#[cfg_attr(all(target_os = "linux", feature ="multithreaded"), some_other_attribute)].

Note

Thecfg_attrcan expand to anothercfg_attr. For example,#[cfg_attr(target_os = "linux", cfg_attr(feature = "multithreaded", some_other_attribute))]is valid. This example would be equivalent to#[cfg_attr(all(target_os = "linux", feature ="multithreaded"), some_other_attribute)].

### Thecfgmacro

The built-incfgmacro takes in a single configuration predicate and evaluates
to thetrueliteral when the predicate is true and thefalseliteral when
it is false.

For example:

```rust
#![allow(unused)]
fn main() {
let machine_kind = if cfg!(unix) {
  "unix"
} else if cfg!(windows) {
  "windows"
} else {
  "unknown"
};

println!("I'm running on a {} machine!", machine_kind);
}
```

```rust
#![allow(unused)]
fn main() {
let machine_kind = if cfg!(unix) {
  "unix"
} else if cfg!(windows) {
  "windows"
} else {
  "unknown"
};

println!("I'm running on a {} machine!", machine_kind);
}
```
