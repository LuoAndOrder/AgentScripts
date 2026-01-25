# Macros by Example

Source: https://doc.rust-lang.org/reference/

# Macros by example

SyntaxMacroRulesDefinitionâÂ Â Â Âmacro_rules!IDENTIFIERMacroRulesDef

MacroRulesDefâÂ Â Â Â Â Â(MacroRules);Â Â Â Â |[MacroRules];Â Â Â Â |{MacroRules}

MacroRulesâÂ Â Â ÂMacroRule(;MacroRule)*;?

MacroRuleâÂ Â Â ÂMacroMatcher=>MacroTranscriber

MacroMatcherâÂ Â Â Â Â Â(MacroMatch*)Â Â Â Â |[MacroMatch*]Â Â Â Â |{MacroMatch*}

MacroMatchâÂ Â Â Â Â ÂTokenexcept$anddelimitersÂ Â Â Â |MacroMatcherÂ Â Â Â |$(IDENTIFIER_OR_KEYWORDexceptcrate|RAW_IDENTIFIER):MacroFragSpecÂ Â Â Â |$(MacroMatch+)MacroRepSep?MacroRepOp

MacroFragSpecâÂ Â Â Â Â Âblock|expr|expr_2021|ident|item|lifetime|literalÂ Â Â Â |meta|pat|pat_param|path|stmt|tt|ty|vis

MacroRepSepâTokenexceptdelimitersandMacroRepOp

MacroRepOpâ*|+|?

MacroTranscriberâDelimTokenTree

Show Railroad

macro_rulesallows users to define syntax extension in a declarative way.  We
call such extensions âmacros by exampleâ or simply âmacrosâ.

Each macro by example has a name, and one or morerules. Each rule has two
parts: amatcher, describing the syntax that it matches, and atranscriber,
describing the syntax that will replace a successfully matched invocation. Both
the matcher and the transcriber must be surrounded by delimiters. Macros can
expand to expressions, statements, items (including traits, impls, and foreign
items), types, or patterns.

## Transcribing

When a macro is invoked, the macro expander looks up macro invocations by name,
and tries each macro rule in turn. It transcribes the first successful match; if
this results in an error, then future matches are not tried.

When matching, no lookahead is performed; if the compiler cannot unambiguously determine how to
parse the macro invocation one token at a time, then it is an error. In the
following example, the compiler does not look ahead past the identifier to see
if the following token is a), even though that would allow it to parse the
invocation unambiguously:

```rust
#![allow(unused)]
fn main() {
macro_rules! ambiguity {
    ($($i:ident)* $j:ident) => { };
}

ambiguity!(error); // Error: local ambiguity
}
```

```rust
#![allow(unused)]
fn main() {
macro_rules! ambiguity {
    ($($i:ident)* $j:ident) => { };
}

ambiguity!(error); // Error: local ambiguity
}
```

In both the matcher and the transcriber, the$token is used to invoke special
behaviours from the macro engine (described below inMetavariablesandRepetitions). Tokens that arenât part of such an invocation are matched and
transcribed literally, with one exception. The exception is that the outer
delimiters for the matcher will match any pair of delimiters. Thus, for
instance, the matcher(())will match{()}but not{{}}. The character$cannot be matched or transcribed literally.

### Forwarding a matched fragment

When forwarding a matched fragment to another macro-by-example, matchers in
the second macro will see an opaque AST of the fragment type. The second macro
canât use literal tokens to match the fragments in the matcher, only a
fragment specifier of the same type. Theident,lifetime, andttfragment types are an exception, andcanbe matched by literal tokens. The
following illustrates this restriction:

```rust
#![allow(unused)]
fn main() {
macro_rules! foo {
    ($l:expr) => { bar!($l); }
// ERROR:               ^^ no rules expected this token in macro call
}

macro_rules! bar {
    (3) => {}
}

foo!(3);
}
```

```rust
#![allow(unused)]
fn main() {
macro_rules! foo {
    ($l:expr) => { bar!($l); }
// ERROR:               ^^ no rules expected this token in macro call
}

macro_rules! bar {
    (3) => {}
}

foo!(3);
}
```

The following illustrates how tokens can be directly matched after matching attfragment:

```rust
#![allow(unused)]
fn main() {
// compiles OK
macro_rules! foo {
    ($l:tt) => { bar!($l); }
}

macro_rules! bar {
    (3) => {}
}

foo!(3);
}
```

```rust
#![allow(unused)]
fn main() {
// compiles OK
macro_rules! foo {
    ($l:tt) => { bar!($l); }
}

macro_rules! bar {
    (3) => {}
}

foo!(3);
}
```

## Metavariables

In the matcher,$name:fragment-specifiermatches a Rust syntax
fragment of the kind specified and binds it to the metavariable$name.

Valid fragment specifiers are:

- block: aBlockExpression
- expr: anExpression
- expr_2021: anExpressionexceptUnderscoreExpressionandConstBlockExpression(seemacro.decl.meta.edition2024)
- ident: anIDENTIFIER_OR_KEYWORDexcept_,RAW_IDENTIFIER, or$crate
- item: anItem
- lifetime: aLIFETIME_TOKEN
- literal: matches-?LiteralExpression
- meta: anAttr, the contents of an attribute
- pat: aPattern(seemacro.decl.meta.edition2021)
- pat_param: aPatternNoTopAlt
- path: aTypePathstyle path
- stmt: aStatementwithout the trailing semicolon (except for item statements that require semicolons)
- tt: aTokenTreeÂ (a singletokenor tokens in matching delimiters(),[], or{})
- ty: aType
- vis: a possibly emptyVisibilityqualifier
In the transcriber, metavariables are referred to simply by$name, since
the fragment kind is specified in the matcher. Metavariables are replaced with
the syntax element that matched them.
Metavariables can be transcribed more than once or not at all.

The keyword metavariable$cratecan be used to refer to the current crate.

> 2021Edition differencesStarting with the 2021 edition,patfragment-specifiers match top-level or-patterns (that is, they acceptPattern).Before the 2021 edition, they match exactly the same fragments aspat_param(that is, they acceptPatternNoTopAlt).The relevant edition is the one in effect for themacro_rules!definition.

2021Edition differences

Starting with the 2021 edition,patfragment-specifiers match top-level or-patterns (that is, they acceptPattern).

Before the 2021 edition, they match exactly the same fragments aspat_param(that is, they acceptPatternNoTopAlt).

The relevant edition is the one in effect for themacro_rules!definition.

> 2024Edition differencesBefore the 2024 edition,exprfragment specifiers do not matchUnderscoreExpressionorConstBlockExpressionat the top level. They are allowed within subexpressions.Theexpr_2021fragment specifier exists to maintain backwards compatibility with editions before 2024.

2024Edition differences

Before the 2024 edition,exprfragment specifiers do not matchUnderscoreExpressionorConstBlockExpressionat the top level. They are allowed within subexpressions.

Theexpr_2021fragment specifier exists to maintain backwards compatibility with editions before 2024.

## Repetitions

In both the matcher and transcriber, repetitions are indicated by placing the
tokens to be repeated inside$(â¦), followed by a repetition operator,
optionally with a separator token between.

The separator token can be any token
other than a delimiter or one of the repetition operators, but;and,are
the most common. For instance,$( $i:ident ),*represents any number of
identifiers separated by commas. Nested repetitions are permitted.

The repetition operators are:

- *â indicates any number of repetitions.
- +â indicates any number but at least one.
- ?â indicates an optional fragment with zero or one occurrence.
Since?represents at most one occurrence, it cannot be used with a
separator.

The repeated fragment both matches and transcribes to the specified number of
the fragment, separated by the separator token. Metavariables are matched to
every repetition of their corresponding fragment. For instance, the$( $i:ident ),*example above matches$ito all of the identifiers in the list.

During transcription, additional restrictions apply to repetitions so that the
compiler knows how to expand them properly:

- A metavariable must appear in exactly the same number, kind, and nesting
order of repetitions in the transcriber as it did in the matcher. So for the
matcher$( $i:ident ),*, the transcribers=> { $i },=> { $( $( $i)* )* }, and=> { $( $i )+ }are all illegal, but=> { $( $i );* }is correct and replaces a comma-separated list of
identifiers with a semicolon-separated list.

## Scoping, exporting, and importing

For historical reasons, the scoping of macros by example does not work entirely
like items. Macros have two forms of scope: textual scope, and path-based scope.
Textual scope is based on the order that things appear in source files, or even
across multiple files, and is the default scoping. It is explained further below.
Path-based scope works exactly the same way that item scoping does. The scoping,
exporting, and importing of macros is controlled largely by attributes.

When a macro is invoked by an unqualified identifier (not part of a multi-part
path), it is first looked up in textual scoping. If this does not yield any
results, then it is looked up in path-based scoping. If the macroâs name is
qualified with a path, then it is only looked up in path-based scoping.

```rust
use lazy_static::lazy_static; // Path-based import.

macro_rules! lazy_static { // Textual definition.
    (lazy) => {};
}

lazy_static!{lazy} // Textual lookup finds our macro first.
self::lazy_static!{} // Path-based lookup ignores our macro, finds imported one.
```

### Textual scope

Textual scope is based largely on the order that things appear in source files,
and works similarly to the scope of local variables declared withletexcept
it also applies at the module level. Whenmacro_rules!is used to define a
macro, the macro enters the scope after the definition (note that it can still
be used recursively, since names are looked up from the invocation site), up
until its surrounding scope, typically a module, is closed. This can enter child
modules and even span across multiple files:

```rust
//// src/lib.rs
mod has_macro {
    // m!{} // Error: m is not in scope.

    macro_rules! m {
        () => {};
    }
    m!{} // OK: appears after declaration of m.

    mod uses_macro;
}

// m!{} // Error: m is not in scope.

//// src/has_macro/uses_macro.rs

m!{} // OK: appears after declaration of m in src/lib.rs
```

It is not an error to define a macro multiple times; the most recent declaration
will shadow the previous one unless it has gone out of scope.

```rust
#![allow(unused)]
fn main() {
macro_rules! m {
    (1) => {};
}

m!(1);

mod inner {
    m!(1);

    macro_rules! m {
        (2) => {};
    }
    // m!(1); // Error: no rule matches '1'
    m!(2);

    macro_rules! m {
        (3) => {};
    }
    m!(3);
}

m!(1);
}
```

```rust
#![allow(unused)]
fn main() {
macro_rules! m {
    (1) => {};
}

m!(1);

mod inner {
    m!(1);

    macro_rules! m {
        (2) => {};
    }
    // m!(1); // Error: no rule matches '1'
    m!(2);

    macro_rules! m {
        (3) => {};
    }
    m!(3);
}

m!(1);
}
```

Macros can be declared and used locally inside functions as well, and work
similarly:

```rust
#![allow(unused)]
fn main() {
fn foo() {
    // m!(); // Error: m is not in scope.
    macro_rules! m {
        () => {};
    }
    m!();
}

// m!(); // Error: m is not in scope.
}
```

```rust
#![allow(unused)]
fn main() {
fn foo() {
    // m!(); // Error: m is not in scope.
    macro_rules! m {
        () => {};
    }
    m!();
}

// m!(); // Error: m is not in scope.
}
```

### Themacro_useattribute

Themacro_useattributehas two purposes: it may be used on modules to extend the scope of macros defined within them, and it may be used onextern crateto import macros from another crate into themacro_useprelude.

> Example#![allow(unused)]fn main() {#[macro_use]
> mod inner {
>     macro_rules! m {
>         () => {};
>     }
> }
> m!();}#[macro_use]
> extern crate log;

Example

```rust
#![allow(unused)]
fn main() {
#[macro_use]
mod inner {
    macro_rules! m {
        () => {};
    }
}
m!();
}
```

```rust
#![allow(unused)]
fn main() {
#[macro_use]
mod inner {
    macro_rules! m {
        () => {};
    }
}
m!();
}
```

```rust
#[macro_use]
extern crate log;
```

When used on modules, themacro_useattribute uses theMetaWordsyntax.

When used onextern crate, it uses theMetaWordandMetaListIdentssyntaxes. For more on how these syntaxes may be used, seemacro.decl.scope.macro_use.prelude.

Themacro_useattribute may be applied to modules orextern crate.

> Noterustcignores use in other positions but lints against it. This may become an error in the future.

Note

rustcignores use in other positions but lints against it. This may become an error in the future.

Themacro_useattribute may not be used onextern crate self.

Themacro_useattribute may be used any number of times on a form.

Multiple instances ofmacro_usein theMetaListIdentssyntax may be specified. The union of all specified macros will be imported.

> NoteOn modules,rustclints against anyMetaWordmacro_useattributes following the first.Onextern crate,rustclints against anymacro_useattributes that have no effect due to not importing any macros not already imported by anothermacro_useattribute. If two or moreMetaListIdentsmacro_useattributes import the same macro, the first is linted against. If anyMetaWordmacro_useattributes are present, allMetaListIdentsmacro_useattributes are linted against. If two or moreMetaWordmacro_useattributes are present, the ones following the first are linted against.

Note

On modules,rustclints against anyMetaWordmacro_useattributes following the first.

Onextern crate,rustclints against anymacro_useattributes that have no effect due to not importing any macros not already imported by anothermacro_useattribute. If two or moreMetaListIdentsmacro_useattributes import the same macro, the first is linted against. If anyMetaWordmacro_useattributes are present, allMetaListIdentsmacro_useattributes are linted against. If two or moreMetaWordmacro_useattributes are present, the ones following the first are linted against.

Whenmacro_useis used on a module, the moduleâs macro scope extends beyond the moduleâs lexical scope.

> Example#![allow(unused)]fn main() {#[macro_use]
> mod inner {
>     macro_rules! m {
>         () => {};
>     }
> }
> m!(); // OK}

Example

```rust
#![allow(unused)]
fn main() {
#[macro_use]
mod inner {
    macro_rules! m {
        () => {};
    }
}
m!(); // OK
}
```

```rust
#![allow(unused)]
fn main() {
#[macro_use]
mod inner {
    macro_rules! m {
        () => {};
    }
}
m!(); // OK
}
```

Specifyingmacro_useon anextern cratedeclaration in the crate root imports exported macros from that crate.

Macros imported this way are imported into themacro_useprelude, not textually, which means that they can be shadowed by any other name. Macros imported bymacro_usecan be used before the import statement.

> Noterustccurrently prefers the last macro imported in case of conflict. Donât rely on this. This behavior is unusual, as imports in Rust are generally order-independent. This behavior ofmacro_usemay change in the future.For details, seeRust issue #148025.

Note

rustccurrently prefers the last macro imported in case of conflict. Donât rely on this. This behavior is unusual, as imports in Rust are generally order-independent. This behavior ofmacro_usemay change in the future.

For details, seeRust issue #148025.

When using theMetaWordsyntax, all exported macros are imported. When using theMetaListIdentssyntax, only the specified macros are imported.

> Example#[macro_use(lazy_static)] // Or `#[macro_use]` to import all macros.
> extern crate lazy_static;
> 
> lazy_static!{}
> // self::lazy_static!{} // ERROR: lazy_static is not defined in `self`.

Example

```rust
#[macro_use(lazy_static)] // Or `#[macro_use]` to import all macros.
extern crate lazy_static;

lazy_static!{}
// self::lazy_static!{} // ERROR: lazy_static is not defined in `self`.
```

Macros to be imported withmacro_usemust be exported withmacro_export.

### Themacro_exportattribute

Themacro_exportattributeexports the macro from the crate and makes it available in the root of the crate for path-based resolution.

> Example#![allow(unused)]fn main() {self::m!();
> //  ^^^^ OK: Path-based lookup finds `m` in the current module.
> m!(); // As above.
> 
> mod inner {
>     super::m!();
>     crate::m!();
> }
> 
> mod mac {
>     #[macro_export]
>     macro_rules! m {
>         () => {};
>     }
> }}

Example

```rust
#![allow(unused)]
fn main() {
self::m!();
//  ^^^^ OK: Path-based lookup finds `m` in the current module.
m!(); // As above.

mod inner {
    super::m!();
    crate::m!();
}

mod mac {
    #[macro_export]
    macro_rules! m {
        () => {};
    }
}
}
```

```rust
#![allow(unused)]
fn main() {
self::m!();
//  ^^^^ OK: Path-based lookup finds `m` in the current module.
m!(); // As above.

mod inner {
    super::m!();
    crate::m!();
}

mod mac {
    #[macro_export]
    macro_rules! m {
        () => {};
    }
}
}
```

Themacro_exportattribute uses theMetaWordandMetaListIdentssyntaxes. With theMetaListIdentssyntax, it accepts a singlelocal_inner_macrosvalue.

Themacro_exportattribute may be applied tomacro_rulesdefinitions.

> Noterustcignores use in other positions but lints against it. This may become an error in the future.

Note

rustcignores use in other positions but lints against it. This may become an error in the future.

Only the first use ofmacro_exporton a macro has effect.

> Noterustclints against any use following the first.

Note

rustclints against any use following the first.

By default, macros only havetextual scopeand cannot be resolved by path. When themacro_exportattribute is used, the macro is made available in the crate root and can be referred to by its path.

> ExampleWithoutmacro_export, macros only have textual scope, so path-based resolution of the macro fails.macro_rules! m {
>     () => {};
> }
> self::m!(); // ERROR
> crate::m!(); // ERRORfn main() {}Withmacro_export, path-based resolution works.#[macro_export]
> macro_rules! m {
>     () => {};
> }
> self::m!(); // OK
> crate::m!(); // OKfn main() {}

Example

Withoutmacro_export, macros only have textual scope, so path-based resolution of the macro fails.

```rust
macro_rules! m {
    () => {};
}
self::m!(); // ERROR
crate::m!(); // ERROR
fn main() {}
```

```rust
macro_rules! m {
    () => {};
}
self::m!(); // ERROR
crate::m!(); // ERROR
fn main() {}
```

Withmacro_export, path-based resolution works.

```rust
#[macro_export]
macro_rules! m {
    () => {};
}
self::m!(); // OK
crate::m!(); // OK
fn main() {}
```

```rust
#[macro_export]
macro_rules! m {
    () => {};
}
self::m!(); // OK
crate::m!(); // OK
fn main() {}
```

Themacro_exportattribute causes a macro to be exported from the crate root so that it can be referred to in other crates by path.

> ExampleGiven the following in alogcrate:#![allow(unused)]fn main() {#[macro_export]
> macro_rules! warn {
>     ($message:expr) => { eprintln!("WARN: {}", $message) };
> }}From another crate, you can refer to the macro by path:fn main() {
>     log::warn!("example warning");
> }

Example

Given the following in alogcrate:

```rust
#![allow(unused)]
fn main() {
#[macro_export]
macro_rules! warn {
    ($message:expr) => { eprintln!("WARN: {}", $message) };
}
}
```

```rust
#![allow(unused)]
fn main() {
#[macro_export]
macro_rules! warn {
    ($message:expr) => { eprintln!("WARN: {}", $message) };
}
}
```

From another crate, you can refer to the macro by path:

```rust
fn main() {
    log::warn!("example warning");
}
```

macro_exportallows the use ofmacro_useon anextern crateto import the macro into themacro_useprelude.

> ExampleGiven the following in alogcrate:#![allow(unused)]fn main() {#[macro_export]
> macro_rules! warn {
>     ($message:expr) => { eprintln!("WARN: {}", $message) };
> }}Usingmacro_usein a dependent crate allows you to use the macro from the prelude:#[macro_use]
> extern crate log;
> 
> pub mod util {
>     pub fn do_thing() {
>         // Resolved via macro prelude.
>         warn!("example warning");
>     }
> }

Example

Given the following in alogcrate:

```rust
#![allow(unused)]
fn main() {
#[macro_export]
macro_rules! warn {
    ($message:expr) => { eprintln!("WARN: {}", $message) };
}
}
```

```rust
#![allow(unused)]
fn main() {
#[macro_export]
macro_rules! warn {
    ($message:expr) => { eprintln!("WARN: {}", $message) };
}
}
```

Usingmacro_usein a dependent crate allows you to use the macro from the prelude:

```rust
#[macro_use]
extern crate log;

pub mod util {
    pub fn do_thing() {
        // Resolved via macro prelude.
        warn!("example warning");
    }
}
```

Addinglocal_inner_macrosto themacro_exportattribute causes all single-segment macro invocations in the macro definition to have an implicit$crate::prefix.

> NoteThis is intended primarily as a tool to migrate code written before$cratewas added to the language to work with Rust 2018âs path-based imports of macros. Its use is discouraged in new code.

Note

This is intended primarily as a tool to migrate code written before$cratewas added to the language to work with Rust 2018âs path-based imports of macros. Its use is discouraged in new code.

> Example#![allow(unused)]fn main() {#[macro_export(local_inner_macros)]
> macro_rules! helped {
>     () => { helper!() } // Automatically converted to $crate::helper!().
> }
> 
> #[macro_export]
> macro_rules! helper {
>     () => { () }
> }}

Example

```rust
#![allow(unused)]
fn main() {
#[macro_export(local_inner_macros)]
macro_rules! helped {
    () => { helper!() } // Automatically converted to $crate::helper!().
}

#[macro_export]
macro_rules! helper {
    () => { () }
}
}
```

```rust
#![allow(unused)]
fn main() {
#[macro_export(local_inner_macros)]
macro_rules! helped {
    () => { helper!() } // Automatically converted to $crate::helper!().
}

#[macro_export]
macro_rules! helper {
    () => { () }
}
}
```

## Hygiene

Macros by example havemixed-site hygiene. This means thatloop labels,block labels, and local variables are looked up at the macro definition site while other symbols are looked up at the macro invocation site. For example:

```rust
#![allow(unused)]
fn main() {
let x = 1;
fn func() {
    unreachable!("this is never called")
}

macro_rules! check {
    () => {
        assert_eq!(x, 1); // Uses `x` from the definition site.
        func();           // Uses `func` from the invocation site.
    };
}

{
    let x = 2;
    fn func() { /* does not panic */ }
    check!();
}
}
```

```rust
#![allow(unused)]
fn main() {
let x = 1;
fn func() {
    unreachable!("this is never called")
}

macro_rules! check {
    () => {
        assert_eq!(x, 1); // Uses `x` from the definition site.
        func();           // Uses `func` from the invocation site.
    };
}

{
    let x = 2;
    fn func() { /* does not panic */ }
    check!();
}
}
```

Labels and local variables defined in macro expansion are not shared between invocations, so this code doesnât compile:

```rust
#![allow(unused)]
fn main() {
macro_rules! m {
    (define) => {
        let x = 1;
    };
    (refer) => {
        dbg!(x);
    };
}

m!(define);
m!(refer);
}
```

```rust
#![allow(unused)]
fn main() {
macro_rules! m {
    (define) => {
        let x = 1;
    };
    (refer) => {
        dbg!(x);
    };
}

m!(define);
m!(refer);
}
```

A special case is the$cratemetavariable. It refers to the crate defining the macro, and can be used at the start of the path to look up items or macros which are not in scope at the invocation site.

```rust
//// Definitions in the `helper_macro` crate.
#[macro_export]
macro_rules! helped {
    // () => { helper!() } // This might lead to an error due to 'helper' not being in scope.
    () => { $crate::helper!() }
}

#[macro_export]
macro_rules! helper {
    () => { () }
}

//// Usage in another crate.
// Note that `helper_macro::helper` is not imported!
use helper_macro::helped;

fn unit() {
    helped!();
}
```

Note that, because$craterefers to the current crate, it must be used with a
fully qualified module path when referring to non-macro items:

```rust
#![allow(unused)]
fn main() {
pub mod inner {
    #[macro_export]
    macro_rules! call_foo {
        () => { $crate::inner::foo() };
    }

    pub fn foo() {}
}
}
```

```rust
#![allow(unused)]
fn main() {
pub mod inner {
    #[macro_export]
    macro_rules! call_foo {
        () => { $crate::inner::foo() };
    }

    pub fn foo() {}
}
}
```

Additionally, even though$crateallows a macro to refer to items within its
own crate when expanding, its use has no effect on visibility. An item or macro
referred to must still be visible from the invocation site. In the following
example, any attempt to invokecall_foo!()from outside its crate will fail
becausefoo()is not public.

```rust
#![allow(unused)]
fn main() {
#[macro_export]
macro_rules! call_foo {
    () => { $crate::foo() };
}

fn foo() {}
}
```

```rust
#![allow(unused)]
fn main() {
#[macro_export]
macro_rules! call_foo {
    () => { $crate::foo() };
}

fn foo() {}
}
```

> NotePrior to Rust 1.30,$crateandlocal_inner_macroswere unsupported. They were added alongsidepath-based imports of macros, to ensure that helper macros did not need to be manually imported by users of a macro-exporting crate. Crates written for earlier versions of Rust that use helper macros need to be modified to use$crateorlocal_inner_macrosto work well with path-based imports.

Note

Prior to Rust 1.30,$crateandlocal_inner_macroswere unsupported. They were added alongsidepath-based imports of macros, to ensure that helper macros did not need to be manually imported by users of a macro-exporting crate. Crates written for earlier versions of Rust that use helper macros need to be modified to use$crateorlocal_inner_macrosto work well with path-based imports.

## Follow-set ambiguity restrictions

The parser used by the macro system is reasonably powerful, but it is limited in
order to prevent ambiguity in current or future versions of the language.

In particular, in addition to the rule about ambiguous expansions, a nonterminal
matched by a metavariable must be followed by a token which has been decided can
be safely used after that kind of match.

As an example, a macro matcher like$i:expr [ , ]could in theory be accepted
in Rust today, since[,]cannot be part of a legal expression and therefore
the parse would always be unambiguous. However, because[can start trailing
expressions,[is not a character which can safely be ruled out as coming
after an expression. If[,]were accepted in a later version of Rust, this
matcher would become ambiguous or would misparse, breaking working code.
Matchers like$i:expr,or$i:expr;would be legal, however, because,and;are legal expression separators. The specific rules are:

- exprandstmtmay only be followed by one of:=>,,, or;.
- pat_parammay only be followed by one of:=>,,,=,|,if, orin.
- patmay only be followed by one of:=>,,,=,if, orin.
- pathandtymay only be followed by one of:=>,,,=,|,;,:,>,>>,[,{,as,where, or a macro variable ofblockfragment specifier.
- vismay only be followed by one of:,, an identifier other than a
non-rawpriv, any token that can begin a type, or a metavariable with aident,ty, orpathfragment specifier.
- All other fragment specifiers have no restrictions.

> 2021Edition differencesBefore the 2021 edition,patmay also be followed by|.

2021Edition differences

Before the 2021 edition,patmay also be followed by|.

When repetitions are involved, then the rules apply to every possible number of
expansions, taking separators into account. This means:

- If the repetition includes a separator, that separator must be able to
follow the contents of the repetition.
- If the repetition can repeat multiple times (*or+), then the contents
must be able to follow themselves.
- The contents of the repetition must be able to follow whatever comes
before, and whatever comes after must be able to follow the contents of the
repetition.
- If the repetition can match zero times (*or?), then whatever comes
after must be able to follow whatever comes before.
For more detail, see theformal specification.
