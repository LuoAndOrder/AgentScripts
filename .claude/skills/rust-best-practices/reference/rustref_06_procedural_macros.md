# Procedural Macros

Source: https://doc.rust-lang.org/reference/

# Procedural macros

Procedural macrosallow creating syntax extensions as execution of a function.
Procedural macros come in one of three flavors:

- Function-like macros-custom!(...)
- Derive macros-#[derive(CustomDerive)]
- Attribute macros-#[CustomAttribute]
Procedural macros allow you to run code at compile time that operates over Rust
syntax, both consuming and producing Rust syntax. You can sort of think of
procedural macros as functions from an AST to another AST.

Procedural macros must be defined in the root of a crate with thecrate typeofproc-macro.
The macros may not be used from the crate where they are defined, and can only be used when imported in another crate.

> NoteWhen using Cargo, Procedural macro crates are defined with theproc-macrokey in your manifest:[lib]
> proc-macro = true

Note

When using Cargo, Procedural macro crates are defined with theproc-macrokey in your manifest:

```toml
[lib]
proc-macro = true
```

As functions, they must either return syntax, panic, or loop endlessly. Returned
syntax either replaces or adds the syntax depending on the kind of procedural
macro. Panics are caught by the compiler and are turned into a compiler error.
Endless loops are not caught by the compiler which hangs the compiler.

Procedural macros run during compilation, and thus have the same resources that
the compiler has. For example, standard input, error, and output are the same
that the compiler has access to. Similarly, file access is the same. Because
of this, procedural macros have the same security concerns thatCargoâs
build scriptshave.

Procedural macros have two ways of reporting errors. The first is to panic. The
second is to emit acompile_errormacro invocation.

## Theproc_macrocrate

Procedural macro crates almost always will link to the compiler-providedproc_macrocrate. Theproc_macrocrate provides types required for
writing procedural macros and facilities to make it easier.

This crate primarily contains aTokenStreamtype. Procedural macros operate
overtoken streamsinstead of AST nodes, which is a far more stable interface
over time for both the compiler and for procedural macros to target. Atoken streamis roughly equivalent toVec<TokenTree>where aTokenTreecan roughly be thought of as lexical token. For examplefoois anIdenttoken,.is aPuncttoken, and1.2is aLiteraltoken. TheTokenStreamtype, unlikeVec<TokenTree>, is cheap to clone.

All tokens have an associatedSpan. ASpanis an opaque value that cannot
be modified but can be manufactured.Spans represent an extent of source
code within a program and are primarily used for error reporting. While you
cannot modify aSpanitself, you can always change theSpanassociatedwith any token, such as through getting aSpanfrom another token.

## Procedural macro hygiene

Procedural macros areunhygienic. This means they behave as if the output
token stream was simply written inline to the code itâs next to. This means that
itâs affected by external items and also affects external imports.

Macro authors need to be careful to ensure their macros work in as many contexts
as possible given this limitation. This often includes using absolute paths to
items in libraries (for example,::std::option::Optioninstead ofOption) or
by ensuring that generated functions have names that are unlikely to clash with
other functions (like__internal_fooinstead offoo).

## Theproc_macroattribute

Theproc_macroattributedefines afunction-likeprocedural macro.

> ExampleThis macro definition ignores its input and emits a functionanswerinto its scope.#![crate_type = "proc-macro"]extern crate proc_macro;
> use proc_macro::TokenStream;
> 
> #[proc_macro]
> pub fn make_answer(_item: TokenStream) -> TokenStream {
>     "fn answer() -> u32 { 42 }".parse().unwrap()
> }We can use it in a binary crate to print â42â to standard output.extern crate proc_macro_examples;
> use proc_macro_examples::make_answer;
> 
> make_answer!();
> 
> fn main() {
>     println!("{}", answer());
> }

Example

This macro definition ignores its input and emits a functionanswerinto its scope.

```rust
#![crate_type = "proc-macro"]
extern crate proc_macro;
use proc_macro::TokenStream;

#[proc_macro]
pub fn make_answer(_item: TokenStream) -> TokenStream {
    "fn answer() -> u32 { 42 }".parse().unwrap()
}
```

We can use it in a binary crate to print â42â to standard output.

```rust
extern crate proc_macro_examples;
use proc_macro_examples::make_answer;

make_answer!();

fn main() {
    println!("{}", answer());
}
```

Theproc_macroattribute uses theMetaWordsyntax.

Theproc_macroattribute may only be applied to apubfunction of typefn(TokenStream) -> TokenStreamwhereTokenStreamcomes from theproc_macrocrate. It must have theâRustâ ABI. No other function qualifiers are allowed. It must be located in the root of the crate.

Theproc_macroattribute may only be specified once on a function.

Theproc_macroattribute publicly defines the macro in themacro namespacein the root of the crate with the same name as the function.

A function-like macro invocation of a function-like procedural macro will pass what is inside the delimiters of the macro invocation as the inputTokenStreamargument and replace the entire macro invocation with the outputTokenStreamof the function.

Function-like procedural macros may be invoked in any macro invocation position, which includes:

- Statements
- Expressions
- Patterns
- Type expressions
- Itempositions, including items inexternblocks
- Inherent and traitimplementations
- Trait definitions

## Theproc_macro_deriveattribute

Applying theproc_macro_deriveattributeto a function defines aderive macrothat can be invoked by thederiveattribute. These macros are given the token stream of astruct,enum, oruniondefinition and can emit newitemsafter it. They can also declare and usederive macro helper attributes.

> ExampleThis derive macro ignores its input and appends tokens that define a function.#![crate_type = "proc-macro"]extern crate proc_macro;
> use proc_macro::TokenStream;
> 
> #[proc_macro_derive(AnswerFn)]
> pub fn derive_answer_fn(_item: TokenStream) -> TokenStream {
>     "fn answer() -> u32 { 42 }".parse().unwrap()
> }To use it, we might write:extern crate proc_macro_examples;
> use proc_macro_examples::AnswerFn;
> 
> #[derive(AnswerFn)]
> struct Struct;
> 
> fn main() {
>     assert_eq!(42, answer());
> }

Example

This derive macro ignores its input and appends tokens that define a function.

```rust
#![crate_type = "proc-macro"]
extern crate proc_macro;
use proc_macro::TokenStream;

#[proc_macro_derive(AnswerFn)]
pub fn derive_answer_fn(_item: TokenStream) -> TokenStream {
    "fn answer() -> u32 { 42 }".parse().unwrap()
}
```

To use it, we might write:

```rust
extern crate proc_macro_examples;
use proc_macro_examples::AnswerFn;

#[derive(AnswerFn)]
struct Struct;

fn main() {
    assert_eq!(42, answer());
}
```

The syntax for theproc_macro_deriveattribute is:

SyntaxProcMacroDeriveAttributeâÂ Â Â Âproc_macro_derive(DeriveMacroName(,DeriveMacroAttributes)?,?)

DeriveMacroNameâIDENTIFIER

DeriveMacroAttributesâÂ Â Â Âattributes((IDENTIFIER(,IDENTIFIER)*,?)?)

Show Railroad

The name of the derive macro is given byDeriveMacroName. The optionalattributesargument is described inmacro.proc.derive.attributes.

Theproc_macro_deriveattribute may only be applied to apubfunction with theRust ABIdefined in the root of the crate with a type offn(TokenStream) -> TokenStreamwhereTokenStreamcomes from theproc_macrocrate. The function may beconstand may useexternto explicitly specify the Rust ABI, but it may not use any otherqualifiers(e.g. it may not beasyncorunsafe).

Theproc_macro_deriveattribute may be used only once on a function.

Theproc_macro_deriveattribute publicly defines the derive macro in themacro namespacein the root of the crate.

The inputTokenStreamis the token stream of the item to which thederiveattribute is applied. The outputTokenStreammust be a (possibly empty) set of items. These items are appended following the input item within the samemoduleorblock.

### Derive macro helper attributes

Derive macros can declarederive macro helper attributesto be used within the scope of theitemto which the derive macro is applied. Theseattributesareinert. While their purpose is to be used by the macro that declared them, they can be seen by any macro.

A helper attribute for a derive macro is declared by adding its identifier to theattributeslist in theproc_macro_deriveattribute.

> ExampleThis declares a helper attribute and then ignores it.#![crate_type="proc-macro"]extern crate proc_macro;use proc_macro::TokenStream;#[proc_macro_derive(WithHelperAttr, attributes(helper))]
> pub fn derive_with_helper_attr(_item: TokenStream) -> TokenStream {
>     TokenStream::new()
> }To use it, we might write:#[derive(WithHelperAttr)]
> struct Struct {
>     #[helper] field: (),
> }

Example

This declares a helper attribute and then ignores it.

```rust
#![crate_type="proc-macro"]
extern crate proc_macro;
use proc_macro::TokenStream;

#[proc_macro_derive(WithHelperAttr, attributes(helper))]
pub fn derive_with_helper_attr(_item: TokenStream) -> TokenStream {
    TokenStream::new()
}
```

To use it, we might write:

```rust
#[derive(WithHelperAttr)]
struct Struct {
    #[helper] field: (),
}
```

## Theproc_macro_attributeattribute

Theproc_macro_attributeattributedefines anattribute macrowhich can be used as anouter attribute.

> ExampleThis attribute macro takes the input stream and emits it as-is, effectively being a no-op attribute.#![crate_type = "proc-macro"]extern crate proc_macro;use proc_macro::TokenStream;#[proc_macro_attribute]
> pub fn return_as_is(_attr: TokenStream, item: TokenStream) -> TokenStream {
>     item
> }

Example

This attribute macro takes the input stream and emits it as-is, effectively being a no-op attribute.

```rust
#![crate_type = "proc-macro"]
extern crate proc_macro;
use proc_macro::TokenStream;

#[proc_macro_attribute]
pub fn return_as_is(_attr: TokenStream, item: TokenStream) -> TokenStream {
    item
}
```

> ExampleThis shows, in the output of the compiler, the stringifiedTokenStreamsthat attribute macros see.// my-macro/src/lib.rsextern crate proc_macro;use proc_macro::TokenStream;#[proc_macro_attribute]
> pub fn show_streams(attr: TokenStream, item: TokenStream) -> TokenStream {
>     println!("attr: \"{attr}\"");
>     println!("item: \"{item}\"");
>     item
> }// src/lib.rs
> extern crate my_macro;
> 
> use my_macro::show_streams;
> 
> // Example: Basic function.
> #[show_streams]
> fn invoke1() {}
> // out: attr: ""
> // out: item: "fn invoke1() {}"
> 
> // Example: Attribute with input.
> #[show_streams(bar)]
> fn invoke2() {}
> // out: attr: "bar"
> // out: item: "fn invoke2() {}"
> 
> // Example: Multiple tokens in the input.
> #[show_streams(multiple => tokens)]
> fn invoke3() {}
> // out: attr: "multiple => tokens"
> // out: item: "fn invoke3() {}"
> 
> // Example: Delimiters in the input.
> #[show_streams { delimiters }]
> fn invoke4() {}
> // out: attr: "delimiters"
> // out: item: "fn invoke4() {}"

Example

This shows, in the output of the compiler, the stringifiedTokenStreamsthat attribute macros see.

```rust
// my-macro/src/lib.rs
extern crate proc_macro;
use proc_macro::TokenStream;
#[proc_macro_attribute]
pub fn show_streams(attr: TokenStream, item: TokenStream) -> TokenStream {
    println!("attr: \"{attr}\"");
    println!("item: \"{item}\"");
    item
}
```

```rust
// src/lib.rs
extern crate my_macro;

use my_macro::show_streams;

// Example: Basic function.
#[show_streams]
fn invoke1() {}
// out: attr: ""
// out: item: "fn invoke1() {}"

// Example: Attribute with input.
#[show_streams(bar)]
fn invoke2() {}
// out: attr: "bar"
// out: item: "fn invoke2() {}"

// Example: Multiple tokens in the input.
#[show_streams(multiple => tokens)]
fn invoke3() {}
// out: attr: "multiple => tokens"
// out: item: "fn invoke3() {}"

// Example: Delimiters in the input.
#[show_streams { delimiters }]
fn invoke4() {}
// out: attr: "delimiters"
// out: item: "fn invoke4() {}"
```

Theproc_macro_attributeattribute uses theMetaWordsyntax.

Theproc_macro_attributeattribute may only be applied to apubfunction of typefn(TokenStream, TokenStream) -> TokenStreamwhereTokenStreamcomes from theproc_macrocrate. It must have theâRustâ ABI. No other function qualifiers are allowed. It must be located in the root of the crate.

Theproc_macro_attributeattribute may only be specified once on a function.

Theproc_macro_attributeattribute defines the attribute in themacro namespacein the root of the crate with the same name as the function.

Attribute macros can only be used on:

- Items
- Items inexternblocks
- Inherent and traitimplementations
- Trait definitions
The firstTokenStreamparameter is the delimited token tree following the attributeâs name but not including the outer delimiters. If the applied attribute contains only the attribute name or the attribute name followed by empty delimiters, theTokenStreamis empty.

The secondTokenStreamis the rest of theitem, including otherattributeson theitem.

The item to which the attribute is applied is replaced by the zero or more items in the returnedTokenStream.

## Declarative macro tokens and procedural macro tokens

Declarativemacro_rulesmacros and procedural macros use similar, but
different definitions for tokens (or ratherTokenTrees.)

Token trees inmacro_rules(corresponding tottmatchers) are defined as

- Delimited groups ((...),{...}, etc)
- All operators supported by the language, both single-character and
multi-character ones (+,+=).Note that this set doesnât include the single quote'.
- Note that this set doesnât include the single quote'.
- Literals ("string",1, etc)Note that negation (e.g.-1) is never a part of such literal tokens,
but a separate operator token.
- Note that negation (e.g.-1) is never a part of such literal tokens,
but a separate operator token.
- Identifiers, including keywords (ident,r#ident,fn)
- Lifetimes ('ident)
- Metavariable substitutions inmacro_rules(e.g.$my_exprinmacro_rules! mac { ($my_expr: expr) => { $my_expr } }after themacâs
expansion, which will be considered a single token tree regardless of the
passed expression)
Token trees in procedural macros are defined as

- Delimited groups ((...),{...}, etc)
- All punctuation characters used in operators supported by the language (+,
but not+=), and also the single quote'character (typically used in
lifetimes, see below for lifetime splitting and joining behavior)
- Literals ("string",1, etc)Negation (e.g.-1) is supported as a part of integer
and floating point literals.
- Negation (e.g.-1) is supported as a part of integer
and floating point literals.
- Identifiers, including keywords (ident,r#ident,fn)
Mismatches between these two definitions are accounted for when token streams
are passed to and from procedural macros.Note that the conversions below may happen lazily, so they might not happen if
the tokens are not actually inspected.

When passed to a proc-macro

- All multi-character operators are broken into single characters.
- Lifetimes are broken into a'character and an identifier.
- The keyword metavariable$crateis passed as a single identifier.
- All other metavariable substitutions are represented as their underlying
token streams.Such token streams may be wrapped into delimited groups (Group) with
implicit delimiters (Delimiter::None) when itâs necessary for
preserving parsing priorities.ttandidentsubstitutions are never wrapped into such groups and
always represented as their underlying token trees.
- Such token streams may be wrapped into delimited groups (Group) with
implicit delimiters (Delimiter::None) when itâs necessary for
preserving parsing priorities.
- ttandidentsubstitutions are never wrapped into such groups and
always represented as their underlying token trees.
When emitted from a proc macro

- Punctuation characters are glued into multi-character operators
when applicable.
- Single quotes'joined with identifiers are glued into lifetimes.
- Negative literals are converted into two tokens (the-and the literal)
possibly wrapped into a delimited group (Group) with implicit delimiters
(Delimiter::None) when itâs necessary for preserving parsing priorities.
Note that neither declarative nor procedural macros support doc comment tokens
(e.g./// Doc), so they are always converted to token streams representing
their equivalent#[doc = r"str"]attributes when passed to macros.
