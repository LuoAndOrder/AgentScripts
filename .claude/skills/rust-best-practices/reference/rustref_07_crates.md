# Crates and Source Files

Source: https://doc.rust-lang.org/reference/

# Crates and source files

SyntaxCrateâÂ Â Â ÂInnerAttribute*Â Â Â ÂItem*

Show Railroad

> NoteAlthough Rust, like any other language, can be implemented by an interpreter as well as a compiler, the only existing implementation is a compiler, and the language has always been designed to be compiled. For these reasons, this section assumes a compiler.

Note

Although Rust, like any other language, can be implemented by an interpreter as well as a compiler, the only existing implementation is a compiler, and the language has always been designed to be compiled. For these reasons, this section assumes a compiler.

Rustâs semantics obey aphase distinctionbetween compile-time and
run-time.1Semantic rules that have astatic
interpretationgovern the success or failure of compilation, while
semantic rules that have adynamic interpretationgovern the behavior of the
program at run-time.

The compilation model centers on artifacts calledcrates. Each compilation
processes a single crate in source form, and if successful, produces a single
crate in binary form: either an executable or some sort of
library.2

Acrateis a unit of compilation and linking, as well as versioning,
distribution, and runtime loading. A crate contains atreeof nestedmodulescopes. The top level of this tree is a module that is
anonymous (from the point of view of paths within the module) and any item
within a crate has a canonicalmodule pathdenoting its location
within the crateâs module tree.

The Rust compiler is always invoked with a single source file as input, and
always produces a single output crate. The processing of that source file may
result in other source files being loaded as modules. Source files have the
extension.rs.

A Rust source file describes a module, the name and location of which â
in the module tree of the current crate â are defined from outside the
source file: either by an explicitModuleitem in a referencing
source file, or by the name of the crate itself.

Every source file is a
module, but not every module needs its own source file:module
definitionscan be nested within one file.

Each source file contains a sequence of zero or moreItemdefinitions, and
may optionally begin with any number ofattributesthat apply to the containing module, most of which influence the behavior of
the compiler.

The anonymous crate module can have additional attributes that
apply to the crate as a whole.

> NoteThe fileâs contents may be preceded by ashebang.

Note

The fileâs contents may be preceded by ashebang.

```rust
#![allow(unused)]
fn main() {
// Specify the crate name.
#![crate_name = "projx"]

// Specify the type of output artifact.
#![crate_type = "lib"]

// Turn on a warning.
// This can be done in any module, not just the anonymous crate module.
#![warn(non_camel_case_types)]
}
```

```rust
#![allow(unused)]
fn main() {
// Specify the crate name.
#![crate_name = "projx"]

// Specify the type of output artifact.
#![crate_type = "lib"]

// Turn on a warning.
// This can be done in any module, not just the anonymous crate module.
#![warn(non_camel_case_types)]
}
```

## Main functions

A crate that contains amainfunctioncan be compiled to an executable.

If amainfunction is present, it must take no arguments, must not declare anytrait or lifetime bounds, must not have anywhere clauses, and its return
type must implement theTerminationtrait.

```rust
fn main() {}
```

```rust
fn main() {}
```

```rust
fn main() -> ! {
    std::process::exit(0);
}
```

```rust
fn main() -> ! {
    std::process::exit(0);
}
```

```rust
fn main() -> impl std::process::Termination {
    std::process::ExitCode::SUCCESS
}
```

```rust
fn main() -> impl std::process::Termination {
    std::process::ExitCode::SUCCESS
}
```

Themainfunction may be an import, e.g. from an external crate or from the current one.

```rust
#![allow(unused)]
fn main() {
mod foo {
    pub fn bar() {
        println!("Hello, world!");
    }
}
use foo::bar as main;
}
```

```rust
#![allow(unused)]
fn main() {
mod foo {
    pub fn bar() {
        println!("Hello, world!");
    }
}
use foo::bar as main;
}
```

> NoteTypes with implementations ofTerminationin the standard library include:()!InfallibleExitCodeResult<T, E> where T: Termination, E: Debug

Note

Types with implementations ofTerminationin the standard library include:

- ()
- !
- Infallible
- ExitCode
- Result<T, E> where T: Termination, E: Debug

### Uncaught foreign unwinding

When a âforeignâ unwind (e.g. an exception thrown from C++ code, or apanic!in Rust code using a different panic handler) propagates beyond themainfunction, the process will be safely terminated. This may take the form of an abort, in which case it is not guaranteed that anyDropcalls will be executed, and the error output may be less informative than if the runtime had been terminated by a ânativeâ Rustpanic.

For more information, see thepanic documentation.

### Theno_mainattribute

Theno_mainattributemay be applied at the crate level to disable emitting themainsymbol for an executable binary. This is useful when some other object being linked to definesmain.

## Thecrate_nameattribute

Thecrate_nameattributemay be applied at the crate level to specify the
name of the crate with theMetaNameValueStrsyntax.

```rust
#![allow(unused)]
#![crate_name = "mycrate"]
fn main() {
}
```

```rust
#![allow(unused)]
#![crate_name = "mycrate"]
fn main() {
}
```

The crate name must not be empty, and must only containUnicode alphanumericor_(U+005F) characters.

- This distinction would also exist in an interpreter.
Static checks like syntactic analysis, type checking, and lints should
happen before the program is executed regardless of when it is executed.â©
This distinction would also exist in an interpreter.
Static checks like syntactic analysis, type checking, and lints should
happen before the program is executed regardless of when it is executed.â©

- A crate is somewhat analogous to anassemblyin the
ECMA-335 CLI model, alibraryin the SML/NJ Compilation Manager, aunitin the Owens and Flatt module system, or aconfigurationin Mesa.â©
A crate is somewhat analogous to anassemblyin the
ECMA-335 CLI model, alibraryin the SML/NJ Compilation Manager, aunitin the Owens and Flatt module system, or aconfigurationin Mesa.â©
