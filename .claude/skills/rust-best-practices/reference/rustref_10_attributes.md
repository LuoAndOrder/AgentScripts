# Attributes

Source: https://doc.rust-lang.org/reference/

SyntaxInnerAttributeâ#![Attr]

OuterAttributeâ#[Attr]

AttrâÂ Â Â Â Â ÂSimplePathAttrInput?Â Â Â Â |unsafe(SimplePathAttrInput?)

AttrInputâÂ Â Â Â Â ÂDelimTokenTreeÂ Â Â Â |=Expression

Show Railroad

Anattributeis a general, free-form metadatum that is interpreted according
to name, convention, language, and compiler version. Attributes are modeled
on Attributes inECMA-335, with the syntax coming fromECMA-334(C#).

Inner attributes, written with a bang (!) after the hash (#), apply to the form that the attribute is declared within.

> Example#![allow(unused)]fn main() {// General metadata applied to the enclosing module or crate.
> #![crate_type = "lib"]
> 
> // Inner attribute applies to the entire function.
> fn some_unused_variables() {
>   #![allow(unused_variables)]
> 
>   let x = ();
>   let y = ();
>   let z = ();
> }}

Example

```rust
#![allow(unused)]
fn main() {
// General metadata applied to the enclosing module or crate.
#![crate_type = "lib"]

// Inner attribute applies to the entire function.
fn some_unused_variables() {
  #![allow(unused_variables)]

  let x = ();
  let y = ();
  let z = ();
}
}
```

```rust
#![allow(unused)]
fn main() {
// General metadata applied to the enclosing module or crate.
#![crate_type = "lib"]

// Inner attribute applies to the entire function.
fn some_unused_variables() {
  #![allow(unused_variables)]

  let x = ();
  let y = ();
  let z = ();
}
}
```

Outer attributes, written without the bang after the hash, apply to the form that follows the attribute.

> Example#![allow(unused)]fn main() {// A function marked as a unit test
> #[test]
> fn test_foo() {
>     /* ... */
> }
> 
> // A conditionally-compiled module
> #[cfg(target_os = "linux")]
> mod bar {
>     /* ... */
> }
> 
> // A lint attribute used to suppress a warning/error
> #[allow(non_camel_case_types)]
> type int8_t = i8;}

Example

```rust
#![allow(unused)]
fn main() {
// A function marked as a unit test
#[test]
fn test_foo() {
    /* ... */
}

// A conditionally-compiled module
#[cfg(target_os = "linux")]
mod bar {
    /* ... */
}

// A lint attribute used to suppress a warning/error
#[allow(non_camel_case_types)]
type int8_t = i8;
}
```

```rust
#![allow(unused)]
fn main() {
// A function marked as a unit test
#[test]
fn test_foo() {
    /* ... */
}

// A conditionally-compiled module
#[cfg(target_os = "linux")]
mod bar {
    /* ... */
}

// A lint attribute used to suppress a warning/error
#[allow(non_camel_case_types)]
type int8_t = i8;
}
```

The attribute consists of a path to the attribute, followed by an optional
delimited token tree whose interpretation is defined by the attribute.
Attributes other than macro attributes also allow the input to be an equals
sign (=) followed by an expression. See themeta item
syntaxbelow for more details.

An attribute may be unsafe to apply. To avoid undefined behavior when using
these attributes, certain obligations that cannot be checked by the compiler
must be met.  To assert these have been, the attribute is wrapped inunsafe(..), e.g.#[unsafe(no_mangle)].

The following attributes are unsafe:

- export_name
- link_section
- naked
- no_mangle
Attributes can be classified into the following kinds:

- Built-in attributes
- Proc macro attributes
- Derive macro helper attributes
- Tool attributes
Attributes may be applied to many forms in the language:

- Allitem declarationsaccept outer attributes whileexternal blocks,functions,implementations, andmodulesaccept inner attributes.
- Moststatementsaccept outer attributes (seeExpression Attributesfor
limitations on expression statements).
- Block expressionsaccept outer and inner attributes, but only when they are
the outer expression of anexpression statementor the final expression of
another block expression.
- Enumvariants andstructandunionfields accept outer attributes.
- Match expression armsaccept outer attributes.
- Generic lifetime or type parameteraccept outer attributes.
- Expressions accept outer attributes in limited situations, seeExpression
Attributesfor details.
- Function,closureandfunction pointerparameters accept outer attributes. This includes attributes on variadic parameters
denoted with...in function pointers andexternal blocks.
- Inline assemblytemplate strings and operands accept outer attributes. Only certain attributes are accepted semantically; for details, seeasm.attributes.supported-attributes.

## Meta item attribute syntax

A âmeta itemâ is the syntax used for theAttrrule by mostbuilt-in
attributes. It has the following grammar:

SyntaxMetaItemâÂ Â Â Â Â ÂSimplePathÂ Â Â Â |SimplePath=ExpressionÂ Â Â Â |SimplePath(MetaSeq?)

MetaSeqâÂ Â Â ÂMetaItemInner(,MetaItemInner)*,?

MetaItemInnerâÂ Â Â Â Â ÂMetaItemÂ Â Â Â |Expression

Show Railroad

Expressions in meta items must macro-expand to literal expressions, which must not
include integer or float type suffixes. Expressions which are not literal expressions
will be syntactically accepted (and can be passed to proc-macros), but will be rejected after parsing.

Note that if the attribute appears within another macro, it will be expanded
after that outer macro. For example, the following code will expand theSerializeproc-macro first, which must preserve theinclude_str!call in
order for it to be expanded:

```rust
#[derive(Serialize)]
struct Foo {
    #[doc = include_str!("x.md")]
    x: u32
}
```

Additionally, macros in attributes will be expanded only after all other attributes applied to the item:

```rust
#[macro_attr1] // expanded first
#[doc = mac!()] // `mac!` is expanded fourth.
#[macro_attr2] // expanded second
#[derive(MacroDerive1, MacroDerive2)] // expanded third
fn foo() {}
```

Various built-in attributes use different subsets of the meta item syntax to
specify their inputs. The following grammar rules show some commonly used
forms:

SyntaxMetaWordâÂ Â Â ÂIDENTIFIER

MetaNameValueStrâÂ Â Â ÂIDENTIFIER=(STRING_LITERAL|RAW_STRING_LITERAL)

MetaListPathsâÂ Â Â ÂIDENTIFIER((SimplePath(,SimplePath)*,?)?)

MetaListIdentsâÂ Â Â ÂIDENTIFIER((IDENTIFIER(,IDENTIFIER)*,?)?)

MetaListNameValueStrâÂ Â Â ÂIDENTIFIER((MetaNameValueStr(,MetaNameValueStr)*,?)?)

Show Railroad

Some examples of meta items are:

## Active and inert attributes

An attribute is either active or inert. During attribute processing,active
attributesremove themselves from the form they are on whileinert attributesstay on.

Thecfgandcfg_attrattributes are active.Attribute macrosare active. All other attributes are inert.

## Tool attributes

The compiler may allow attributes for external tools where each tool resides
in its own module in thetool prelude. The first segment of the attribute
path is the name of the tool, with one or more additional segments whose
interpretation is up to the tool.

When a tool is not in use, the toolâs attributes are accepted without a
warning. When the tool is in use, the tool is responsible for processing and
interpretation of its attributes.

Tool attributes are not available if theno_implicit_preludeattribute is
used.

```rust
#![allow(unused)]
fn main() {
// Tells the rustfmt tool to not format the following element.
#[rustfmt::skip]
struct S {
}

// Controls the "cyclomatic complexity" threshold for the clippy tool.
#[clippy::cyclomatic_complexity = "100"]
pub fn f() {}
}
```

```rust
#![allow(unused)]
fn main() {
// Tells the rustfmt tool to not format the following element.
#[rustfmt::skip]
struct S {
}

// Controls the "cyclomatic complexity" threshold for the clippy tool.
#[clippy::cyclomatic_complexity = "100"]
pub fn f() {}
}
```

> Noterustccurrently recognizes the tools âclippyâ, ârustfmtâ, âdiagnosticâ, âmiriâ, and ârust_analyzerâ.

Note

rustccurrently recognizes the tools âclippyâ, ârustfmtâ, âdiagnosticâ, âmiriâ, and ârust_analyzerâ.

## Built-in attributes index

The following is an index of all built-in attributes.

- Conditional compilationcfgâ Controls conditional compilation.cfg_attrâ Conditionally includes attributes.
Conditional compilation

- cfgâ Controls conditional compilation.
- cfg_attrâ Conditionally includes attributes.
- Testingtestâ Marks a function as a test.ignoreâ Disables a test function.should_panicâ Indicates a test should generate a panic.
Testing

- testâ Marks a function as a test.
- ignoreâ Disables a test function.
- should_panicâ Indicates a test should generate a panic.
- Derivederiveâ Automatic trait implementations.automatically_derivedâ Marker for implementations created byderive.
Derive

- deriveâ Automatic trait implementations.
- automatically_derivedâ Marker for implementations created byderive.
- Macrosmacro_exportâ Exports amacro_rulesmacro for cross-crate usage.macro_useâ Expands macro visibility, or imports macros from other
crates.proc_macroâ Defines a function-like macro.proc_macro_deriveâ Defines a derive macro.proc_macro_attributeâ Defines an attribute macro.
Macros

- macro_exportâ Exports amacro_rulesmacro for cross-crate usage.
- macro_useâ Expands macro visibility, or imports macros from other
crates.
- proc_macroâ Defines a function-like macro.
- proc_macro_deriveâ Defines a derive macro.
- proc_macro_attributeâ Defines an attribute macro.
- Diagnosticsallow,expect,warn,deny,forbidâ Alters the default lint level.deprecatedâ Generates deprecation notices.must_useâ Generates a lint for unused values.diagnostic::on_unimplementedâ Hints the compiler to emit a certain error
message if a trait is not implemented.diagnostic::do_not_recommendâ Hints the compiler to not show a certain trait impl in error messages.
Diagnostics

- allow,expect,warn,deny,forbidâ Alters the default lint level.
- deprecatedâ Generates deprecation notices.
- must_useâ Generates a lint for unused values.
- diagnostic::on_unimplementedâ Hints the compiler to emit a certain error
message if a trait is not implemented.
- diagnostic::do_not_recommendâ Hints the compiler to not show a certain trait impl in error messages.
ABI, linking, symbols, and FFI

- linkâ Specifies a native library to link with anexternblock.
- link_nameâ Specifies the name of the symbol for functions or statics
in anexternblock.
- link_ordinalâ Specifies the ordinal of the symbol for functions or
statics in anexternblock.
- no_linkâ Prevents linking an extern crate.
- reprâ Controls type layout.
- crate_typeâ Specifies the type of crate (library, executable, etc.).
- no_mainâ Disables emitting themainsymbol.
- export_nameâ Specifies the exported symbol name for a function or
static.
- link_sectionâ Specifies the section of an object file to use for a
function or static.
- no_mangleâ Disables symbol name encoding.
- usedâ Forces the compiler to keep a static item in the output
object file.
- crate_nameâ Specifies the crate name.
- Code generationinlineâ Hint to inline code.coldâ Hint that a function is unlikely to be called.nakedâ Prevent the compiler from emitting a function prologue and epilogue.no_builtinsâ Disables use of certain built-in functions.target_featureâ Configure platform-specific code generation.track_callerâ Pass the parent call location tostd::panic::Location::caller().instruction_setâ Specify the instruction set used to generate a functions code
Code generation

- inlineâ Hint to inline code.
- coldâ Hint that a function is unlikely to be called.
- nakedâ Prevent the compiler from emitting a function prologue and epilogue.
- no_builtinsâ Disables use of certain built-in functions.
- target_featureâ Configure platform-specific code generation.
- track_callerâ Pass the parent call location tostd::panic::Location::caller().
- instruction_setâ Specify the instruction set used to generate a functions code
- Documentationdocâ Specifies documentation. SeeThe Rustdoc Bookfor more
information.Doc commentsare transformed intodocattributes.
Documentation

- docâ Specifies documentation. SeeThe Rustdoc Bookfor more
information.Doc commentsare transformed intodocattributes.
- Preludesno_stdâ Removes std from the prelude.no_implicit_preludeâ Disables prelude lookups within a module.
Preludes

- no_stdâ Removes std from the prelude.
- no_implicit_preludeâ Disables prelude lookups within a module.
- Modulespathâ Specifies the filename for a module.
Modules

- pathâ Specifies the filename for a module.
- Limitsrecursion_limitâ Sets the maximum recursion limit for certain
compile-time operations.type_length_limitâ Sets the maximum size of a polymorphic type.
Limits

- recursion_limitâ Sets the maximum recursion limit for certain
compile-time operations.
- type_length_limitâ Sets the maximum size of a polymorphic type.
- Runtimepanic_handlerâ Sets the function to handle panics.global_allocatorâ Sets the global memory allocator.windows_subsystemâ Specifies the windows subsystem to link with.
Runtime

- panic_handlerâ Sets the function to handle panics.
- global_allocatorâ Sets the global memory allocator.
- windows_subsystemâ Specifies the windows subsystem to link with.
- Featuresfeatureâ Used to enable unstable or experimental compiler features. SeeThe Unstable Bookfor features implemented inrustc.
Features

- featureâ Used to enable unstable or experimental compiler features. SeeThe Unstable Bookfor features implemented inrustc.
- Type Systemnon_exhaustiveâ Indicate that a type will have more fields/variants
added in future.
Type System

- non_exhaustiveâ Indicate that a type will have more fields/variants
added in future.
- Debuggerdebugger_visualizerâ Embeds a file that specifies debugger output for a type.collapse_debuginfoâ Controls how macro invocations are encoded in debuginfo.
Debugger

- debugger_visualizerâ Embeds a file that specifies debugger output for a type.
- collapse_debuginfoâ Controls how macro invocations are encoded in debuginfo.
