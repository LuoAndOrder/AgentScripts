# Statements

Source: https://doc.rust-lang.org/nightly/style-guide/

## Let statements

Put a space after the:and on both sides of the=(if they are present).
Donât put a space before the semicolon.

```rust
#![allow(unused)]
fn main() {
// A comment.
let pattern: Type = expr;

let pattern;
let pattern: Type;
let pattern = expr;
}
```

If possible, format the declaration on a single line. If not possible, then try
splitting after the=, if the declaration fits on two lines. Block-indent the
expression.

```rust
#![allow(unused)]
fn main() {
let pattern: Type =
    expr;
}
```

If the first line still does not fit on a single line, split after the:, and
use block indentation. If the type requires multiple lines, even after
line-breaking after the:, then place the first line on the same line as the:, subject to thecombining rules.

```rust
#![allow(unused)]
fn main() {
let pattern:
    Type =
    expr;
}
```

e.g,

```rust
#![allow(unused)]
fn main() {
let Foo {
    f: abcd,
    g: qwer,
}: Foo<Bar> =
    Foo { f, g };

let (abcd,
    defg):
    Baz =
{ ... }
}
```

If the expression covers multiple lines, if the first line of the expression
fits in the remaining space, it stays on the same line as the=, and the rest
of the expression is not further indented. If the first line does not fit, then
put the expression on subsequent lines, block indented. If the expression is a
block and the type or pattern cover multiple lines, put the opening brace on a
new line and not indented (this provides separation for the interior of the
block from the type); otherwise, the opening brace follows the=.

Examples:

```rust
#![allow(unused)]
fn main() {
let foo = Foo {
    f: abcd,
    g: qwer,
};

let foo =
    ALongName {
        f: abcd,
        g: qwer,
    };

let foo: Type = {
    an_expression();
    ...
};

let foo:
    ALongType =
{
    an_expression();
    ...
};

let Foo {
    f: abcd,
    g: qwer,
}: Foo<Bar> = Foo {
    f: blimblimblim,
    g: blamblamblam,
};

let Foo {
    f: abcd,
    g: qwer,
}: Foo<Bar> = foo(
    blimblimblim,
    blamblamblam,
);
}
```

### else blocks (let-else statements)

A let statement can contain anelsecomponent, making it a let-else statement.
In this case, always apply the same formatting rules to the components preceding
theelseblock (i.e. thelet pattern: Type = initializer_exprportion)
as describedfor other let statements.

Format the entire let-else statement on a single line if all the following are
true:

- the entire statement isshort
- theelseblock contains only a single-line expression and no statements
- theelseblock contains no comments
- the let statement components preceding theelseblock can be formatted on a single line

```rust
#![allow(unused)]
fn main() {
let Some(1) = opt else { return };
}
```

Otherwise, the let-else statement requires some line breaks.

If breaking a let-else statement across multiple lines, never break between theelseand the{, and always break before the}.

If the let statement components preceding theelsecan be formatted on a
single line, but the let-else does not qualify to be placed entirely on a
single line, put theelse {on the same line as the initializer expression,
with a space between them, then break the line after the{. Indent the
closing}to match thelet, and indent the contained block one step
further.

```rust
#![allow(unused)]
fn main() {
let Some(1) = opt else {
    return;
};

let Some(1) = opt else {
    // nope
    return
};
}
```

If the let statement components preceding theelsecan be formatted on a
single line, but theelse {does not fit on the same line, break the line
before theelse.

```rust
#![allow(unused)]
fn main() {
    let Some(x) = some_really_really_really_really_really_really_really_really_really_long_name
    else {
        return;
    };
}
```

If the initializer expression is multi-line, put theelsekeyword and opening
brace of the block (i.e.else {) on the same line as the end of the
initializer expression, with a space between them, if and only if all the
following are true:

- The initializer expression ends with one or more closing
parentheses, square brackets, and/or braces
- There is nothing else on that line
- That line has the same indentation level as the initialletkeyword.
For example:

```rust
#![allow(unused)]
fn main() {
let Some(x) = y.foo(
    "abc",
    fairly_long_identifier,
    "def",
    "123456",
    "string",
    "cheese",
) else {
    bar()
}
}
```

Otherwise, put theelsekeyword and opening brace on the next line after the
end of the initializer expression, with theelsekeyword at the same
indentation level as theletkeyword.

For example:

```rust
fn main() {
    let Some(x) = abcdef()
        .foo(
            "abc",
            some_really_really_really_long_ident,
            "ident",
            "123456",
        )
        .bar()
        .baz()
        .qux("fffffffffffffffff")
    else {
        return
    };

    let Some(aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa) =
        bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
    else {
        return;
    };

    let LongStructName(AnotherStruct {
        multi,
        line,
        pattern,
    }) = slice.as_ref()
    else {
        return;
    };

    let LongStructName(AnotherStruct {
        multi,
        line,
        pattern,
    }) = multi_line_function_call(
        arg1,
        arg2,
        arg3,
        arg4,
    ) else {
        return;
    };
}
```

## Macros in statement position

For a macro use in statement position, use parentheses or square brackets as
delimiters, and terminate it with a semicolon. Do not put spaces around the
name,!, the delimiters, or the;.

```rust
#![allow(unused)]
fn main() {
// A comment.
a_macro!(...);
}
```

## Expressions in statement position

Do not put space between the expression and the semicolon.

```rust
<expr>;
```

Terminate all expressions in statement position with a semicolon, unless they
end with a block or are used as the value for a block.

E.g.,

```rust
#![allow(unused)]
fn main() {
{
    an_expression();
    expr_as_value()
}

return foo();

loop {
    break;
}
}
```

Use a semicolon where an expression has void type, even if it could be
propagated. E.g.,

```rust
#![allow(unused)]
fn main() {
fn foo() { ... }

fn bar() {
    foo();
}
}
```
