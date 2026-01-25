# Linkage

Source: https://doc.rust-lang.org/reference/

> NoteThis section is described more in terms of the compiler than of the language.

Note

This section is described more in terms of the compiler than of the language.

The compiler supports various methods to link crates together both
statically and dynamically. This section will explore the various methods to
link crates together, and more information about native libraries can be
found in theFFI section of the book.

In one session of compilation, the compiler can generate multiple artifacts
through the usage of either command line flags or thecrate_typeattribute.
If one or more command line flags are specified, allcrate_typeattributes will
be ignored in favor of only building the artifacts specified by command line.

- --crate-type=bin,#![crate_type = "bin"]- A runnable executable will be
produced. This requires that there is amainfunction in the crate which
will be run when the program begins executing. This will link in all Rust and
native dependencies, producing a single distributable binary.
This is the default crate type.
- --crate-type=dylib,#![crate_type = "dylib"]- A dynamic Rust library will
be produced. This is different from theliboutput type in that this forces
dynamic library generation. The resulting dynamic library can be used as a
dependency for other libraries and/or executables. This output type will
create*.sofiles on Linux,*.dylibfiles on macOS, and*.dllfiles on
Windows.
--crate-type=staticlib,#![crate_type = "staticlib"]- A static system
library will be produced. This is different from other library outputs in that
the compiler will never attempt to link tostaticliboutputs. The
purpose of this output type is to create a static library containing all of
the local crateâs code along with all upstream dependencies. This output type
will create*.afiles on Linux, macOS and Windows (MinGW), and*.libfiles
on Windows (MSVC). This format is recommended for use in situations such as
linking Rust code into an existing non-Rust application because it will not
have dynamic dependencies on other Rust code.

Note that any dynamic dependencies that the static library may have (such as
dependencies on system libraries, or dependencies on Rust libraries that are
compiled as dynamic libraries) will have to be specified manually when
linking that static library from somewhere. The--print=native-static-libsflag may help with this.

Note that, because the resulting static library contains the code of all the
dependencies, including the standard library, and also exports all public
symbols of them, linking the static library into an executable or shared
library may need special care. In case of a shared library the list of
exported symbols will have to be limited via e.g. a linker or symbol version
script, exported symbols list (macOS), or module definition file (Windows).
Additionally, unused sections can be removed to remove all code of
dependencies that is not actually used (e.g.--gc-sectionsor-dead_stripfor macOS).

- --crate-type=cdylib,#![crate_type = "cdylib"]- A dynamic system
library will be produced.  This is used when compiling
a dynamic library to be loaded from another language.  This output type will
create*.sofiles on Linux,*.dylibfiles on macOS, and*.dllfiles on
Windows.
- --crate-type=rlib,#![crate_type = "rlib"]- A âRust libraryâ file will be
produced. This is used as an intermediate artifact and can be thought of as a
âstatic Rust libraryâ. Theserlibfiles, unlikestaticlibfiles, are
interpreted by the compiler in future linkage. This essentially means
thatrustcwill look for metadata inrlibfiles like it looks for metadata
in dynamic libraries. This form of output is used to produce statically linked
executables as well asstaticliboutputs.
Note that these outputs are stackable in the sense that if multiple are
specified, then the compiler will produce each form of output without
having to recompile. However, this only applies for outputs specified by the
same method. If onlycrate_typeattributes are specified, then they will all
be built, but if one or more--crate-typecommand line flags are specified,
then only those outputs will be built.

With all these different kinds of outputs, if crate A depends on crate B, then
the compiler could find B in various different forms throughout the system. The
only forms looked for by the compiler, however, are therlibformat and the
dynamic library format. With these two options for a dependent library, the
compiler must at some point make a choice between these two formats. With this
in mind, the compiler follows these rules when determining what format of
dependencies will be used:

- If a static library is being produced, all upstream dependencies are
required to be available inrlibformats. This requirement stems from the
reason that a dynamic library cannot be converted into a static format.Note that it is impossible to link in native dynamic dependencies to a static
library, and in this case warnings will be printed about all unlinked native
dynamic dependencies.
If a static library is being produced, all upstream dependencies are
required to be available inrlibformats. This requirement stems from the
reason that a dynamic library cannot be converted into a static format.

Note that it is impossible to link in native dynamic dependencies to a static
library, and in this case warnings will be printed about all unlinked native
dynamic dependencies.

- If anrlibfile is being produced, then there are no restrictions on what
format the upstream dependencies are available in. It is simply required that
all upstream dependencies be available for reading metadata from.The reason for this is thatrlibfiles do not contain any of their upstream
dependencies. It wouldnât be very efficient for allrlibfiles to contain a
copy oflibstd.rlib!
If anrlibfile is being produced, then there are no restrictions on what
format the upstream dependencies are available in. It is simply required that
all upstream dependencies be available for reading metadata from.

The reason for this is thatrlibfiles do not contain any of their upstream
dependencies. It wouldnât be very efficient for allrlibfiles to contain a
copy oflibstd.rlib!

- If an executable is being produced and the-C prefer-dynamicflag is not
specified, then dependencies are first attempted to be found in therlibformat. If some dependencies are not available in an rlib format, then
dynamic linking is attempted (see below).
If a dynamic library or an executable that is being dynamically linked is
being produced, then the compiler will attempt to reconcile the available
dependencies in either the rlib or dylib format to create a final product.

A major goal of the compiler is to ensure that a library never appears more
than once in any artifact. For example, if dynamic libraries B and C were
each statically linked to library A, then a crate could not link to B and C
together because there would be two copies of A. The compiler allows mixing
the rlib and dylib formats, but this restriction must be satisfied.

The compiler currently implements no method of hinting what format a library
should be linked with. When dynamically linking, the compiler will attempt to
maximize dynamic dependencies while still allowing some dependencies to be
linked in via an rlib.

For most situations, having all libraries available as a dylib is recommended
if dynamically linking. For other situations, the compiler will emit a
warning if it is unable to determine which formats to link each library with.

In general,--crate-type=binor--crate-type=libshould be sufficient for
all compilation needs, and the other options are just available if more
fine-grained control is desired over the output format of a crate.

## Static and dynamic C runtimes

The standard library in general strives to support both statically linked and
dynamically linked C runtimes for targets as appropriate. For example thex86_64-pc-windows-msvcandx86_64-unknown-linux-musltargets typically come
with both runtimes and the user selects which one theyâd like. All targets in
the compiler have a default mode of linking to the C runtime. Typically targets
are linked dynamically by default, but there are exceptions which are static by
default such as:

- arm-unknown-linux-musleabi
- arm-unknown-linux-musleabihf
- armv7-unknown-linux-musleabihf
- i686-unknown-linux-musl
- x86_64-unknown-linux-musl
The linkage of the C runtime is configured to respect thecrt-statictarget
feature. These target features are typically configured from the command line
via flags to the compiler itself. For example to enable a static runtime you
would execute:

```sh
rustc -C target-feature=+crt-static foo.rs
```

whereas to link dynamically to the C runtime you would execute:

```sh
rustc -C target-feature=-crt-static foo.rs
```

Targets which do not support switching between linkage of the C runtime will
ignore this flag. Itâs recommended to inspect the resulting binary to ensure
that itâs linked as you would expect after the compiler succeeds.

Crates may also learn about how the C runtime is being linked. Code on MSVC, for
example, needs to be compiled differently (e.g. with/MTor/MD) depending
on the runtime being linked. This is exported currently through thecfgattributetarget_featureoption:

```rust
#![allow(unused)]
fn main() {
#[cfg(target_feature = "crt-static")]
fn foo() {
    println!("the C runtime should be statically linked");
}

#[cfg(not(target_feature = "crt-static"))]
fn foo() {
    println!("the C runtime should be dynamically linked");
}
}
```

```rust
#![allow(unused)]
fn main() {
#[cfg(target_feature = "crt-static")]
fn foo() {
    println!("the C runtime should be statically linked");
}

#[cfg(not(target_feature = "crt-static"))]
fn foo() {
    println!("the C runtime should be dynamically linked");
}
}
```

Also note that Cargo build scripts can learn about this feature throughenvironment variables. In a build script you can detect the linkage
via:

```rust
use std::env;

fn main() {
    let linkage = env::var("CARGO_CFG_TARGET_FEATURE").unwrap_or(String::new());

    if linkage.contains("crt-static") {
        println!("the C runtime will be statically linked");
    } else {
        println!("the C runtime will be dynamically linked");
    }
}
```

```rust
use std::env;

fn main() {
    let linkage = env::var("CARGO_CFG_TARGET_FEATURE").unwrap_or(String::new());

    if linkage.contains("crt-static") {
        println!("the C runtime will be statically linked");
    } else {
        println!("the C runtime will be dynamically linked");
    }
}
```

To use this feature locally, you typically will use theRUSTFLAGSenvironment
variable to specify flags to the compiler through Cargo. For example to compile
a statically linked binary on MSVC you would execute:

```sh
RUSTFLAGS='-C target-feature=+crt-static' cargo build --target x86_64-pc-windows-msvc
```

## Mixed Rust and foreign codebases

If you are mixing Rust with foreign code (e.g. C, C++) and wish to make a single
binary containing both types of code, you have two approaches for the final
binary link:

- Userustc. Pass any non-Rust libraries using-L <directory>and-l<library>rustc arguments, and/or#[link]directives in your Rust code. If you need to
link against.ofiles you can use-Clink-arg=file.o.
- Use your foreign linker. In this case, you first need to generate a Ruststaticlibtarget and pass that into your foreign linker invocation. If you need to link
multiple Rust subsystems, you will need to generate asinglestaticlibperhaps using lots ofextern cratestatements to include multiple Rustrlibs.
Multiple Ruststaticlibfiles are likely to conflict.
Passingrlibs directly into your foreign linker is currently unsupported.

> NoteRust code compiled or linked with a different instance of the Rust runtime counts as âforeign codeâ for the purpose of this section.

Note

Rust code compiled or linked with a different instance of the Rust runtime counts as âforeign codeâ for the purpose of this section.

### Prohibited linkage and unwinding

Panic unwinding can only be used if the binary is built consistently according to the following rules.

A Rust artifact is calledpotentially unwindingif any of the following conditions is met:

- The artifact uses theunwindpanic handler.
- The artifact contains a crate built with theunwindpanic strategythat makes a call to a function using a-unwindABI.
- The artifact makes a"Rust"ABI call to code running in another Rust artifact that has a separate copy of the Rust runtime, and that other artifact is potentially unwinding.

> NoteThis definition captures whether a"Rust"ABI call inside a Rust artifact can ever unwind.

Note

This definition captures whether a"Rust"ABI call inside a Rust artifact can ever unwind.

If a Rust artifact is potentially unwinding, then all its crates must be built with theunwindpanic strategy. Otherwise, unwinding can cause undefined behavior.

> NoteIf you are usingrustcto link, these rules are enforced automatically. If you arenotusingrustcto link, you must take care to ensure that unwinding is handled consistently across the entire binary. Linking withoutrustcincludes usingdlopenor similar facilities where linking is done by the system runtime withoutrustcbeing involved. This can only happen when mixing code with different-C panicflags, so most users do not have to be concerned about this.

Note

If you are usingrustcto link, these rules are enforced automatically. If you arenotusingrustcto link, you must take care to ensure that unwinding is handled consistently across the entire binary. Linking withoutrustcincludes usingdlopenor similar facilities where linking is done by the system runtime withoutrustcbeing involved. This can only happen when mixing code with different-C panicflags, so most users do not have to be concerned about this.

> NoteTo guarantee that a library will be sound (and linkable withrustc) regardless of the panic runtime used at link-time, theffi_unwind_callslintmay be used. The lint flags any calls to-unwindforeign functions or function pointers.

Note

To guarantee that a library will be sound (and linkable withrustc) regardless of the panic runtime used at link-time, theffi_unwind_callslintmay be used. The lint flags any calls to-unwindforeign functions or function pointers.
