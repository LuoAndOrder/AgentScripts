# Patterns

Source: https://doc.rust-lang.org/reference/

SyntaxPatternâ|?PatternNoTopAlt(|PatternNoTopAlt)*

PatternNoTopAltâÂ Â Â Â Â ÂPatternWithoutRangeÂ Â Â Â |RangePattern

PatternWithoutRangeâÂ Â Â Â Â ÂLiteralPatternÂ Â Â Â |IdentifierPatternÂ Â Â Â |WildcardPatternÂ Â Â Â |RestPatternÂ Â Â Â |ReferencePatternÂ Â Â Â |StructPatternÂ Â Â Â |TupleStructPatternÂ Â Â Â |TuplePatternÂ Â Â Â |GroupedPatternÂ Â Â Â |SlicePatternÂ Â Â Â |PathPatternÂ Â Â Â |MacroInvocation

Show Railroad

Patterns are used to match values against structures and to, optionally, bind variables to values inside these structures.
They are also used in variable declarations and parameters for functions and closures.

The pattern in the following example does four things:

- Tests ifpersonhas thecarfield filled with something.
- Tests if the personâsagefield is between 13 and 19, and binds its value to theperson_agevariable.
- Binds a reference to thenamefield to the variableperson_name.
- Ignores the rest of the fields ofperson.
The remaining fields can have any value and are not bound to any variables.

```rust
#![allow(unused)]
fn main() {
struct Car;
struct Computer;
struct Person {
    name: String,
    car: Option<Car>,
    computer: Option<Computer>,
    age: u8,
}
let person = Person {
    name: String::from("John"),
    car: Some(Car),
    computer: None,
    age: 15,
};
if let
    Person {
        car: Some(_),
        age: person_age @ 13..=19,
        name: ref person_name,
        ..
    } = person
{
    println!("{} has a car and is {} years old.", person_name, person_age);
}
}
```

```rust
#![allow(unused)]
fn main() {
struct Car;
struct Computer;
struct Person {
    name: String,
    car: Option<Car>,
    computer: Option<Computer>,
    age: u8,
}
let person = Person {
    name: String::from("John"),
    car: Some(Car),
    computer: None,
    age: 15,
};
if let
    Person {
        car: Some(_),
        age: person_age @ 13..=19,
        name: ref person_name,
        ..
    } = person
{
    println!("{} has a car and is {} years old.", person_name, person_age);
}
}
```

Patterns are used in:

- letdeclarations
- Functionandclosureparameters
- matchexpressions
- if letexpressions
- while letexpressions
- forexpressions

## Destructuring

Patterns can be used todestructurestructs,enums, andtuples.
Destructuring breaks up a value into its component pieces.
The syntax used is almost the same as when creating such values.

In a pattern whosescrutineeexpression has astruct,enumortupletype, awildcard pattern(_) stands in for asingledata field, whereas anet ceteraorrest pattern(..) stands in forallthe remaining fields of a particular variant.

When destructuring a data structure with named (but not numbered) fields, it is allowed to writefieldnameas a shorthand forfieldname: fieldname.

```rust
#![allow(unused)]
fn main() {
enum Message {
    Quit,
    WriteString(String),
    Move { x: i32, y: i32 },
    ChangeColor(u8, u8, u8),
}
let message = Message::Quit;
match message {
    Message::Quit => println!("Quit"),
    Message::WriteString(write) => println!("{}", &write),
    Message::Move{ x, y: 0 } => println!("move {} horizontally", x),
    Message::Move{ .. } => println!("other move"),
    Message::ChangeColor { 0: red, 1: green, 2: _ } => {
        println!("color change, red: {}, green: {}", red, green);
    }
};
}
```

```rust
#![allow(unused)]
fn main() {
enum Message {
    Quit,
    WriteString(String),
    Move { x: i32, y: i32 },
    ChangeColor(u8, u8, u8),
}
let message = Message::Quit;
match message {
    Message::Quit => println!("Quit"),
    Message::WriteString(write) => println!("{}", &write),
    Message::Move{ x, y: 0 } => println!("move {} horizontally", x),
    Message::Move{ .. } => println!("other move"),
    Message::ChangeColor { 0: red, 1: green, 2: _ } => {
        println!("color change, red: {}, green: {}", red, green);
    }
};
}
```

## Refutability

A pattern is said to berefutablewhen it has the possibility of not being matched by the value it is being matched against.Irrefutablepatterns, on the other hand, always match the value they are being matched against.
Examples:

```rust
#![allow(unused)]
fn main() {
let (x, y) = (1, 2);               // "(x, y)" is an irrefutable pattern

if let (a, 3) = (1, 2) {           // "(a, 3)" is refutable, and will not match
    panic!("Shouldn't reach here");
} else if let (a, 4) = (3, 4) {    // "(a, 4)" is refutable, and will match
    println!("Matched ({}, 4)", a);
}
}
```

```rust
#![allow(unused)]
fn main() {
let (x, y) = (1, 2);               // "(x, y)" is an irrefutable pattern

if let (a, 3) = (1, 2) {           // "(a, 3)" is refutable, and will not match
    panic!("Shouldn't reach here");
} else if let (a, 4) = (3, 4) {    // "(a, 4)" is refutable, and will match
    println!("Matched ({}, 4)", a);
}
}
```

## Literal patterns

SyntaxLiteralPatternâ-?LiteralExpression

Show Railroad

Literal patternsmatch exactly the same value as what is created by the literal. Since negative numbers are notliterals, literals in patterns may be prefixed by an optional minus sign, which acts like the negation operator.

> WarningC string and raw C string literals are accepted in literal patterns, but&CStrdoesnât implement structural equality (#[derive(Eq, PartialEq)]) and therefore any suchmatchon a&CStrwill be rejected with a type error.

Warning

C string and raw C string literals are accepted in literal patterns, but&CStrdoesnât implement structural equality (#[derive(Eq, PartialEq)]) and therefore any suchmatchon a&CStrwill be rejected with a type error.

Literal patterns are always refutable.

Examples:

```rust
#![allow(unused)]
fn main() {
for i in -2..5 {
    match i {
        -1 => println!("It's minus one"),
        1 => println!("It's a one"),
        2|4 => println!("It's either a two or a four"),
        _ => println!("Matched none of the arms"),
    }
}
}
```

```rust
#![allow(unused)]
fn main() {
for i in -2..5 {
    match i {
        -1 => println!("It's minus one"),
        1 => println!("It's a one"),
        2|4 => println!("It's either a two or a four"),
        _ => println!("Matched none of the arms"),
    }
}
}
```

## Identifier patterns

SyntaxIdentifierPatternâref?mut?IDENTIFIER(@PatternNoTopAlt)?

Show Railroad

Identifier patterns bind the value they match to a variable in thevalue namespace.

The identifier must be unique within the pattern.

The variable will shadow any variables of the same name in scope.
Thescopeof the new binding depends on the context of where the pattern is used (such as aletbinding or amatcharm).

Patterns that consist of only an identifier, possibly with amut, match any value and bind it to that identifier.
This is the most commonly used pattern in variable declarations and parameters for functions and closures.

```rust
#![allow(unused)]
fn main() {
let mut variable = 10;
fn sum(x: i32, y: i32) -> i32 {
   x + y
}
}
```

```rust
#![allow(unused)]
fn main() {
let mut variable = 10;
fn sum(x: i32, y: i32) -> i32 {
   x + y
}
}
```

To bind the matched value of a pattern to a variable, use the syntaxvariable @ subpattern.
For example, the following binds the value 2 toe(not the entire range: the range here is a range subpattern).

```rust
#![allow(unused)]
fn main() {
let x = 2;

match x {
    e @ 1 ..= 5 => println!("got a range element {}", e),
    _ => println!("anything"),
}
}
```

```rust
#![allow(unused)]
fn main() {
let x = 2;

match x {
    e @ 1 ..= 5 => println!("got a range element {}", e),
    _ => println!("anything"),
}
}
```

By default, identifier patterns bind a variable to a copy of or move from the matched value depending on whether the matched value implementsCopy.

This can be changed to bind to a reference by using therefkeyword, or to a mutable reference usingref mut. For example:

```rust
#![allow(unused)]
fn main() {
let a = Some(10);
match a {
    None => (),
    Some(value) => (),
}

match a {
    None => (),
    Some(ref value) => (),
}
}
```

```rust
#![allow(unused)]
fn main() {
let a = Some(10);
match a {
    None => (),
    Some(value) => (),
}

match a {
    None => (),
    Some(ref value) => (),
}
}
```

In the first match expression, the value is copied (or moved).
In the second match, a reference to the same memory location is bound to the variable value.
This syntax is needed because in destructuring subpatterns the&operator canât be applied to the valueâs fields.
For example, the following is not valid:

```rust
#![allow(unused)]
fn main() {
struct Person {
   name: String,
   age: u8,
}
let value = Person { name: String::from("John"), age: 23 };
if let Person { name: &person_name, age: 18..=150 } = value { }
}
```

```rust
#![allow(unused)]
fn main() {
struct Person {
   name: String,
   age: u8,
}
let value = Person { name: String::from("John"), age: 23 };
if let Person { name: &person_name, age: 18..=150 } = value { }
}
```

To make it valid, write the following:

```rust
#![allow(unused)]
fn main() {
struct Person {
   name: String,
   age: u8,
}
let value = Person { name: String::from("John"), age: 23 };
if let Person { name: ref person_name, age: 18..=150 } = value { }
}
```

```rust
#![allow(unused)]
fn main() {
struct Person {
   name: String,
   age: u8,
}
let value = Person { name: String::from("John"), age: 23 };
if let Person { name: ref person_name, age: 18..=150 } = value { }
}
```

Thus,refis not something that is being matched against.
Its objective is exclusively to make the matched binding a reference, instead of potentially copying or moving what was matched.

Path patternstake precedence over identifier patterns.

> NoteWhen a pattern is a single-segment identifier, the grammar is ambiguous whether it means anIdentifierPatternor aPathPattern. This ambiguity can only be resolved aftername resolution.#![allow(unused)]fn main() {const EXPECTED_VALUE: u8 = 42;
> //    ^^^^^^^^^^^^^^ That this constant is in scope affects how the
> //                   patterns below are treated.
> 
> fn check_value(x: u8) -> Result<u8, u8> {
>     match x {
>         EXPECTED_VALUE => Ok(x),
>     //  ^^^^^^^^^^^^^^ Parsed as a `PathPattern` that resolves to
>     //                 the constant `42`.
>         other_value => Err(x),
>     //  ^^^^^^^^^^^ Parsed as an `IdentifierPattern`.
>     }
> }
> 
> // If `EXPECTED_VALUE` were treated as an `IdentifierPattern` above,
> // that pattern would always match, making the function always return
> // `Ok(_) regardless of the input.
> assert_eq!(check_value(42), Ok(42));
> assert_eq!(check_value(43), Err(43));}

Note

When a pattern is a single-segment identifier, the grammar is ambiguous whether it means anIdentifierPatternor aPathPattern. This ambiguity can only be resolved aftername resolution.

```rust
#![allow(unused)]
fn main() {
const EXPECTED_VALUE: u8 = 42;
//    ^^^^^^^^^^^^^^ That this constant is in scope affects how the
//                   patterns below are treated.

fn check_value(x: u8) -> Result<u8, u8> {
    match x {
        EXPECTED_VALUE => Ok(x),
    //  ^^^^^^^^^^^^^^ Parsed as a `PathPattern` that resolves to
    //                 the constant `42`.
        other_value => Err(x),
    //  ^^^^^^^^^^^ Parsed as an `IdentifierPattern`.
    }
}

// If `EXPECTED_VALUE` were treated as an `IdentifierPattern` above,
// that pattern would always match, making the function always return
// `Ok(_) regardless of the input.
assert_eq!(check_value(42), Ok(42));
assert_eq!(check_value(43), Err(43));
}
```

```rust
#![allow(unused)]
fn main() {
const EXPECTED_VALUE: u8 = 42;
//    ^^^^^^^^^^^^^^ That this constant is in scope affects how the
//                   patterns below are treated.

fn check_value(x: u8) -> Result<u8, u8> {
    match x {
        EXPECTED_VALUE => Ok(x),
    //  ^^^^^^^^^^^^^^ Parsed as a `PathPattern` that resolves to
    //                 the constant `42`.
        other_value => Err(x),
    //  ^^^^^^^^^^^ Parsed as an `IdentifierPattern`.
    }
}

// If `EXPECTED_VALUE` were treated as an `IdentifierPattern` above,
// that pattern would always match, making the function always return
// `Ok(_) regardless of the input.
assert_eq!(check_value(42), Ok(42));
assert_eq!(check_value(43), Err(43));
}
```

It is an error ifreforref mutis specified and the identifier shadows a constant.

Identifier patterns are irrefutable if the@subpattern is irrefutable or the subpattern is not specified.

### Binding modes

To service better ergonomics, patterns operate in differentbinding modesin order to make it easier to bind references to values.
When a reference value is matched by a non-reference pattern, it will be automatically treated as areforref mutbinding.
Example:

```rust
#![allow(unused)]
fn main() {
let x: &Option<i32> = &Some(3);
if let Some(y) = x {
    // y was converted to `ref y` and its type is &i32
}
}
```

```rust
#![allow(unused)]
fn main() {
let x: &Option<i32> = &Some(3);
if let Some(y) = x {
    // y was converted to `ref y` and its type is &i32
}
}
```

Non-reference patternsinclude all patterns except bindings,wildcard patterns(_),constpatternsof reference types, andreference patterns.

If a binding pattern does not explicitly haveref,ref mut, ormut, then it uses thedefault binding modeto determine how the variable is bound.

The default binding mode starts in âmoveâ mode which uses move semantics.

When matching a pattern, the compiler starts from the outside of the pattern and works inwards.

Each time a reference is matched using a non-reference pattern, it will automatically dereference the value and update the default binding mode.

References will set the default binding mode toref.

Mutable references will set the mode toref mutunless the mode is alreadyrefin which case it remainsref.

If the automatically dereferenced value is still a reference, it is dereferenced and this process repeats.

The binding pattern may only explicitly specify areforref mutbinding mode, or specify mutability withmut, when the default binding mode is âmoveâ. For example, these are not accepted:

```rust
#![allow(unused)]
fn main() {
let [mut x] = &[()]; //~ ERROR
let [ref x] = &[()]; //~ ERROR
let [ref mut x] = &mut [()]; //~ ERROR
}
```

```rust
#![allow(unused)]
fn main() {
let [mut x] = &[()]; //~ ERROR
let [ref x] = &[()]; //~ ERROR
let [ref mut x] = &mut [()]; //~ ERROR
}
```

> 2024Edition differencesBefore the 2024 edition, bindings could explicitly specify areforref mutbinding mode even when the default binding mode was not âmoveâ, and they could specify mutability on such bindings withmut. In these editions, specifyingmuton a binding set the binding mode to âmoveâ regardless of the current default binding mode.

2024Edition differences

Before the 2024 edition, bindings could explicitly specify areforref mutbinding mode even when the default binding mode was not âmoveâ, and they could specify mutability on such bindings withmut. In these editions, specifyingmuton a binding set the binding mode to âmoveâ regardless of the current default binding mode.

Similarly, a reference pattern may only appear when the default binding mode is âmoveâ. For example, this is not accepted:

```rust
#![allow(unused)]
fn main() {
let [&x] = &[&()]; //~ ERROR
}
```

```rust
#![allow(unused)]
fn main() {
let [&x] = &[&()]; //~ ERROR
}
```

> 2024Edition differencesBefore the 2024 edition, reference patterns could appear even when the default binding mode was not âmoveâ, and had both the effect of matching against the scrutinee and of causing the default binding mode to be reset to âmoveâ.

2024Edition differences

Before the 2024 edition, reference patterns could appear even when the default binding mode was not âmoveâ, and had both the effect of matching against the scrutinee and of causing the default binding mode to be reset to âmoveâ.

Move bindings and reference bindings can be mixed together in the same pattern.
Doing so will result in partial move of the object bound to and the object cannot be used afterwards.
This applies only if the type cannot be copied.

In the example below,nameis moved out ofperson.
Trying to usepersonas a whole orperson.namewould result in an error because ofpartial move.

Example:

```rust
#![allow(unused)]
fn main() {
struct Person {
   name: String,
   age: u8,
}
let person = Person{ name: String::from("John"), age: 23 };
// `name` is moved from person and `age` referenced
let Person { name, ref age } = person;
}
```

```rust
#![allow(unused)]
fn main() {
struct Person {
   name: String,
   age: u8,
}
let person = Person{ name: String::from("John"), age: 23 };
// `name` is moved from person and `age` referenced
let Person { name, ref age } = person;
}
```

## Wildcard pattern

SyntaxWildcardPatternâ_

Show Railroad

Thewildcard pattern(an underscore symbol) matches any value.
It is used to ignore values when they donât matter.

Inside other patterns it matches a single data field (as opposed to the..which matches the remaining fields).

Unlike identifier patterns, it does not copy, move or borrow the value it matches.

Examples:

```rust
#![allow(unused)]
fn main() {
let x = 20;
let (a, _) = (10, x);   // the x is always matched by _
assert_eq!(a, 10);

// ignore a function/closure param
let real_part = |a: f64, _: f64| { a };

// ignore a field from a struct
struct RGBA {
   r: f32,
   g: f32,
   b: f32,
   a: f32,
}
let color = RGBA{r: 0.4, g: 0.1, b: 0.9, a: 0.5};
let RGBA{r: red, g: green, b: blue, a: _} = color;
assert_eq!(color.r, red);
assert_eq!(color.g, green);
assert_eq!(color.b, blue);

// accept any Some, with any value
let x = Some(10);
if let Some(_) = x {}
}
```

```rust
#![allow(unused)]
fn main() {
let x = 20;
let (a, _) = (10, x);   // the x is always matched by _
assert_eq!(a, 10);

// ignore a function/closure param
let real_part = |a: f64, _: f64| { a };

// ignore a field from a struct
struct RGBA {
   r: f32,
   g: f32,
   b: f32,
   a: f32,
}
let color = RGBA{r: 0.4, g: 0.1, b: 0.9, a: 0.5};
let RGBA{r: red, g: green, b: blue, a: _} = color;
assert_eq!(color.r, red);
assert_eq!(color.g, green);
assert_eq!(color.b, blue);

// accept any Some, with any value
let x = Some(10);
if let Some(_) = x {}
}
```

The wildcard pattern is always irrefutable.

## Rest pattern

SyntaxRestPatternâ..

Show Railroad

Therest pattern(the..token) acts as a variable-length pattern which matches zero or more elements that havenât been matched already before and after.

It may only be used intuple,tuple struct, andslicepatterns, and may only appear once as one of the elements in those patterns.
It is also allowed in anidentifier patternforslice patternsonly.

The rest pattern is always irrefutable.

Examples:

```rust
#![allow(unused)]
fn main() {
let words = vec!["a", "b", "c"];
let slice = &words[..];
match slice {
    [] => println!("slice is empty"),
    [one] => println!("single element {}", one),
    [head, tail @ ..] => println!("head={} tail={:?}", head, tail),
}

match slice {
    // Ignore everything but the last element, which must be "!".
    [.., "!"] => println!("!!!"),

    // `start` is a slice of everything except the last element, which must be "z".
    [start @ .., "z"] => println!("starts with: {:?}", start),

    // `end` is a slice of everything but the first element, which must be "a".
    ["a", end @ ..] => println!("ends with: {:?}", end),

    // 'whole' is the entire slice and `last` is the final element
    whole @ [.., last] => println!("the last element of {:?} is {}", whole, last),

    rest => println!("{:?}", rest),
}

if let [.., penultimate, _] = slice {
    println!("next to last is {}", penultimate);
}

let tuple = (1, 2, 3, 4, 5);
// The rest pattern may also be used in tuple and tuple
// struct patterns.
match tuple {
    (1, .., y, z) => println!("y={} z={}", y, z),
    (.., 5) => println!("tail must be 5"),
    (..) => println!("matches everything else"),
}
}
```

```rust
#![allow(unused)]
fn main() {
let words = vec!["a", "b", "c"];
let slice = &words[..];
match slice {
    [] => println!("slice is empty"),
    [one] => println!("single element {}", one),
    [head, tail @ ..] => println!("head={} tail={:?}", head, tail),
}

match slice {
    // Ignore everything but the last element, which must be "!".
    [.., "!"] => println!("!!!"),

    // `start` is a slice of everything except the last element, which must be "z".
    [start @ .., "z"] => println!("starts with: {:?}", start),

    // `end` is a slice of everything but the first element, which must be "a".
    ["a", end @ ..] => println!("ends with: {:?}", end),

    // 'whole' is the entire slice and `last` is the final element
    whole @ [.., last] => println!("the last element of {:?} is {}", whole, last),

    rest => println!("{:?}", rest),
}

if let [.., penultimate, _] = slice {
    println!("next to last is {}", penultimate);
}

let tuple = (1, 2, 3, 4, 5);
// The rest pattern may also be used in tuple and tuple
// struct patterns.
match tuple {
    (1, .., y, z) => println!("y={} z={}", y, z),
    (.., 5) => println!("tail must be 5"),
    (..) => println!("matches everything else"),
}
}
```

## Range patterns

SyntaxRangePatternâÂ Â Â Â Â ÂRangeExclusivePatternÂ Â Â Â |RangeInclusivePatternÂ Â Â Â |RangeFromPatternÂ Â Â Â |RangeToExclusivePatternÂ Â Â Â |RangeToInclusivePatternÂ Â Â Â |ObsoleteRangePatternâ1

RangeExclusivePatternâÂ Â Â Â Â ÂRangePatternBound..RangePatternBound

RangeInclusivePatternâÂ Â Â Â Â ÂRangePatternBound..=RangePatternBound

RangeFromPatternâÂ Â Â Â Â ÂRangePatternBound..

RangeToExclusivePatternâÂ Â Â Â Â Â..RangePatternBound

RangeToInclusivePatternâÂ Â Â Â Â Â..=RangePatternBound

ObsoleteRangePatternâÂ Â Â ÂRangePatternBound...RangePatternBound

RangePatternBoundâÂ Â Â Â Â ÂLiteralPatternÂ Â Â Â |PathExpression

Show Railroad

Range patternsmatch scalar values within the range defined by their bounds.
They comprise asigil(..or..=) and a bound on one or both sides.

A bound on the left of the sigil is called alower bound.
A bound on the right is called anupper bound.

Theexclusive range patternmatches all values from the lower bound up to, but not including the upper bound.
It is written as its lower bound, followed by.., followed by the upper bound.

For example, a pattern'm'..'p'will match only'm','n'and'o', specificallynotincluding'p'.

Theinclusive range patternmatches all values from the lower bound up to and including the upper bound.
It is written as its lower bound, followed by..=, followed by the upper bound.

For example, a pattern'm'..='p'will match only the values'm','n','o', and'p'.

Thefrom range patternmatches all values greater than or equal to the lower bound.
It is written as its lower bound followed by...

For example,1..will match any integer greater than or equal to 1, such as 1, 9, or 9001, or 9007199254740991 (if it is of an appropriate size), but not 0, and not negative numbers for signed integers.

Theto exclusive range patternmatches all values less than the upper bound.
It is written as..followed by the upper bound.

For example,..10will match any integer less than 10, such as 9, 1, 0, and for signed integer types, all negative values.

Theto inclusive range patternmatches all values less than or equal to the upper bound.
It is written as..=followed by the upper bound.

For example,..=10will match any integer less than or equal to 10, such as 10, 1, 0, and for signed integer types, all negative values.

The lower bound cannot be greater than the upper bound.
That is, ina..=b, a â¤ b must be the case.
For example, it is an error to have a range pattern10..=0.

A bound is written as one of:

- A character, byte, integer, or float literal.
- A-followed by an integer or float literal.
- Apath.

> NoteWe syntactically accept more than this for aRangePatternBound. We later reject the other things semantically.

Note

We syntactically accept more than this for aRangePatternBound. We later reject the other things semantically.

If a bound is written as a path, after macro resolution, the path must resolve to a constant item of the typechar, an integer type, or a float type.

The range pattern matches the type of its upper and lower bounds, which must be the same type.

If a bound is apath, the bound matches the type and has the value of theconstantthe path resolves to.

If a bound is a literal, the bound matches the type and has the value of the correspondingliteral expression.

If a bound is a literal preceded by a-, the bound matches the same type as the correspondingliteral expressionand has the value ofnegatingthe value of the corresponding literal expression.

For float range patterns, the constant may not be aNaN.

Examples:

```rust
#![allow(unused)]
fn main() {
let c = 'f';
let valid_variable = match c {
    'a'..='z' => true,
    'A'..='Z' => true,
    'Î±'..='Ï' => true,
    _ => false,
};

let ph = 10;
println!("{}", match ph {
    0..7 => "acid",
    7 => "neutral",
    8..=14 => "base",
    _ => unreachable!(),
});

let uint: u32 = 5;
match uint {
    0 => "zero!",
    1.. => "positive number!",
};

// using paths to constants:
const TROPOSPHERE_MIN : u8 = 6;
const TROPOSPHERE_MAX : u8 = 20;

const STRATOSPHERE_MIN : u8 = TROPOSPHERE_MAX + 1;
const STRATOSPHERE_MAX : u8 = 50;

const MESOSPHERE_MIN : u8 = STRATOSPHERE_MAX + 1;
const MESOSPHERE_MAX : u8 = 85;

let altitude = 70;

println!("{}", match altitude {
    TROPOSPHERE_MIN..=TROPOSPHERE_MAX => "troposphere",
    STRATOSPHERE_MIN..=STRATOSPHERE_MAX => "stratosphere",
    MESOSPHERE_MIN..=MESOSPHERE_MAX => "mesosphere",
    _ => "outer space, maybe",
});

pub mod binary {
    pub const MEGA : u64 = 1024*1024;
    pub const GIGA : u64 = 1024*1024*1024;
}
let n_items = 20_832_425;
let bytes_per_item = 12;
if let size @ binary::MEGA..=binary::GIGA = n_items * bytes_per_item {
    println!("It fits and occupies {} bytes", size);
}

trait MaxValue {
    const MAX: u64;
}
impl MaxValue for u8 {
    const MAX: u64 = (1 << 8) - 1;
}
impl MaxValue for u16 {
    const MAX: u64 = (1 << 16) - 1;
}
impl MaxValue for u32 {
    const MAX: u64 = (1 << 32) - 1;
}
// using qualified paths:
println!("{}", match 0xfacade {
    0 ..= <u8 as MaxValue>::MAX => "fits in a u8",
    0 ..= <u16 as MaxValue>::MAX => "fits in a u16",
    0 ..= <u32 as MaxValue>::MAX => "fits in a u32",
    _ => "too big",
});
}
```

```rust
#![allow(unused)]
fn main() {
let c = 'f';
let valid_variable = match c {
    'a'..='z' => true,
    'A'..='Z' => true,
    'Î±'..='Ï' => true,
    _ => false,
};

let ph = 10;
println!("{}", match ph {
    0..7 => "acid",
    7 => "neutral",
    8..=14 => "base",
    _ => unreachable!(),
});

let uint: u32 = 5;
match uint {
    0 => "zero!",
    1.. => "positive number!",
};

// using paths to constants:
const TROPOSPHERE_MIN : u8 = 6;
const TROPOSPHERE_MAX : u8 = 20;

const STRATOSPHERE_MIN : u8 = TROPOSPHERE_MAX + 1;
const STRATOSPHERE_MAX : u8 = 50;

const MESOSPHERE_MIN : u8 = STRATOSPHERE_MAX + 1;
const MESOSPHERE_MAX : u8 = 85;

let altitude = 70;

println!("{}", match altitude {
    TROPOSPHERE_MIN..=TROPOSPHERE_MAX => "troposphere",
    STRATOSPHERE_MIN..=STRATOSPHERE_MAX => "stratosphere",
    MESOSPHERE_MIN..=MESOSPHERE_MAX => "mesosphere",
    _ => "outer space, maybe",
});

pub mod binary {
    pub const MEGA : u64 = 1024*1024;
    pub const GIGA : u64 = 1024*1024*1024;
}
let n_items = 20_832_425;
let bytes_per_item = 12;
if let size @ binary::MEGA..=binary::GIGA = n_items * bytes_per_item {
    println!("It fits and occupies {} bytes", size);
}

trait MaxValue {
    const MAX: u64;
}
impl MaxValue for u8 {
    const MAX: u64 = (1 << 8) - 1;
}
impl MaxValue for u16 {
    const MAX: u64 = (1 << 16) - 1;
}
impl MaxValue for u32 {
    const MAX: u64 = (1 << 32) - 1;
}
// using qualified paths:
println!("{}", match 0xfacade {
    0 ..= <u8 as MaxValue>::MAX => "fits in a u8",
    0 ..= <u16 as MaxValue>::MAX => "fits in a u16",
    0 ..= <u32 as MaxValue>::MAX => "fits in a u32",
    _ => "too big",
});
}
```

Range patterns for fix-width integer andchartypes are irrefutable when they span the entire set of possible values of a type.
For example,0u8..=255u8is irrefutable.

The range of values for an integer type is the closed range from its minimum to maximum value.

The range of values for achartype are precisely those ranges containing all Unicode Scalar Values:'\u{0000}'..='\u{D7FF}'and'\u{E000}'..='\u{10FFFF}'.

RangeFromPatterncannot be used as a top-level pattern for subpatterns inslice patterns.
For example, the pattern[1.., _]is not a valid pattern.

> 2021Edition differencesBefore the 2021 edition, range patterns with both a lower and upper bound may also be written using...in place of..=, with the same meaning.

2021Edition differences

Before the 2021 edition, range patterns with both a lower and upper bound may also be written using...in place of..=, with the same meaning.

## Reference patterns

SyntaxReferencePatternâ (&|&&)mut?PatternWithoutRange

Show Railroad

Reference patterns dereference the pointers that are being matched and, thus, borrow them.

For example, these two matches onx: &i32are equivalent:

```rust
#![allow(unused)]
fn main() {
let int_reference = &3;

let a = match *int_reference { 0 => "zero", _ => "some" };
let b = match int_reference { &0 => "zero", _ => "some" };

assert_eq!(a, b);
}
```

```rust
#![allow(unused)]
fn main() {
let int_reference = &3;

let a = match *int_reference { 0 => "zero", _ => "some" };
let b = match int_reference { &0 => "zero", _ => "some" };

assert_eq!(a, b);
}
```

The grammar production for reference patterns has to match the token&&to match a reference to a reference because it is a token by itself, not two&tokens.

Adding themutkeyword dereferences a mutable reference. The mutability must match the mutability of the reference.

Reference patterns are always irrefutable.

## Struct patterns

SyntaxStructPatternâÂ Â Â ÂPathInExpression{Â Â Â Â Â Â Â ÂStructPatternElements?Â Â Â Â}

StructPatternElementsâÂ Â Â Â Â ÂStructPatternFields(,|,StructPatternEtCetera)?Â Â Â Â |StructPatternEtCetera

StructPatternFieldsâÂ Â Â ÂStructPatternField(,StructPatternField)*

StructPatternFieldâÂ Â Â ÂOuterAttribute*Â Â Â Â (Â Â Â Â Â Â Â ÂTUPLE_INDEX:PatternÂ Â Â Â Â Â |IDENTIFIER:PatternÂ Â Â Â Â Â |ref?mut?IDENTIFIERÂ Â Â Â )

StructPatternEtCeteraâ..

Show Railroad

Struct patterns match struct, enum, and union values that match all criteria defined by its subpatterns.
They are also used todestructurea struct, enum, or union value.

On a struct pattern, the fields are referenced by name, index (in the case of tuple structs) or ignored by use of..:

```rust
#![allow(unused)]
fn main() {
struct Point {
    x: u32,
    y: u32,
}
let s = Point {x: 1, y: 1};

match s {
    Point {x: 10, y: 20} => (),
    Point {y: 10, x: 20} => (),    // order doesn't matter
    Point {x: 10, ..} => (),
    Point {..} => (),
}

struct PointTuple (
    u32,
    u32,
);
let t = PointTuple(1, 2);

match t {
    PointTuple {0: 10, 1: 20} => (),
    PointTuple {1: 10, 0: 20} => (),   // order doesn't matter
    PointTuple {0: 10, ..} => (),
    PointTuple {..} => (),
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
}
let m = Message::Quit;

match m {
    Message::Quit => (),
    Message::Move {x: 10, y: 20} => (),
    Message::Move {..} => (),
}
}
```

```rust
#![allow(unused)]
fn main() {
struct Point {
    x: u32,
    y: u32,
}
let s = Point {x: 1, y: 1};

match s {
    Point {x: 10, y: 20} => (),
    Point {y: 10, x: 20} => (),    // order doesn't matter
    Point {x: 10, ..} => (),
    Point {..} => (),
}

struct PointTuple (
    u32,
    u32,
);
let t = PointTuple(1, 2);

match t {
    PointTuple {0: 10, 1: 20} => (),
    PointTuple {1: 10, 0: 20} => (),   // order doesn't matter
    PointTuple {0: 10, ..} => (),
    PointTuple {..} => (),
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
}
let m = Message::Quit;

match m {
    Message::Quit => (),
    Message::Move {x: 10, y: 20} => (),
    Message::Move {..} => (),
}
}
```

If..is not used, a struct pattern used to match a struct is required to specify all fields:

```rust
#![allow(unused)]
fn main() {
struct Struct {
   a: i32,
   b: char,
   c: bool,
}
let mut struct_value = Struct{a: 10, b: 'X', c: false};

match struct_value {
    Struct{a: 10, b: 'X', c: false} => (),
    Struct{a: 10, b: 'X', ref c} => (),
    Struct{a: 10, b: 'X', ref mut c} => (),
    Struct{a: 10, b: 'X', c: _} => (),
    Struct{a: _, b: _, c: _} => (),
}
}
```

```rust
#![allow(unused)]
fn main() {
struct Struct {
   a: i32,
   b: char,
   c: bool,
}
let mut struct_value = Struct{a: 10, b: 'X', c: false};

match struct_value {
    Struct{a: 10, b: 'X', c: false} => (),
    Struct{a: 10, b: 'X', ref c} => (),
    Struct{a: 10, b: 'X', ref mut c} => (),
    Struct{a: 10, b: 'X', c: _} => (),
    Struct{a: _, b: _, c: _} => (),
}
}
```

A struct pattern used to match a union must specify exactly one field (seePattern matching on unions).

TheIDENTIFIERsyntax matches any value and binds it to a variable with the same name as the given field. It is a shorthand forfieldname: fieldname. Therefandmutqualifiers can be included with the behavior as described inpatterns.ident.ref.

```rust
#![allow(unused)]
fn main() {
struct Struct {
   a: i32,
   b: char,
   c: bool,
}
let struct_value = Struct{a: 10, b: 'X', c: false};

let Struct { a, b, c } = struct_value;
}
```

```rust
#![allow(unused)]
fn main() {
struct Struct {
   a: i32,
   b: char,
   c: bool,
}
let struct_value = Struct{a: 10, b: 'X', c: false};

let Struct { a, b, c } = struct_value;
}
```

A struct pattern is refutable if thePathInExpressionresolves to a constructor of an enum with more than one variant, or one of its subpatterns is refutable.

A struct pattern matches against the struct, union, or enum variant whose constructor is resolved fromPathInExpressionin thetype namespace. Seepatterns.tuple-struct.namespacefor more details.

## Tuple struct patterns

SyntaxTupleStructPatternâPathInExpression(TupleStructItems?)

TupleStructItemsâPattern(,Pattern)*,?

Show Railroad

Tuple struct patterns match tuple struct and enum values that match all criteria defined by its subpatterns.
They are also used todestructurea tuple struct or enum value.

A tuple struct pattern is refutable if thePathInExpressionresolves to a constructor of an enum with more than one variant, or one of its subpatterns is refutable.

A tuple struct pattern matches against the tuple struct ortuple-like enum variantwhose constructor is resolved fromPathInExpressionin thevalue namespace.

> NoteConversely, a struct pattern for a tuple struct ortuple-like enum variant, e.g.S { 0: _ }, matches against the tuple struct or variant whose constructor is resolved in thetype namespace.enum E1 { V(u16) }
> enum E2 { V(u32) }
> 
> // Import `E1::V` from the type namespace only.
> mod _0 {
>     const V: () = (); // For namespace masking.
>     pub(super) use super::E1::*;
> }
> use _0::*;
> 
> // Import `E2::V` from the value namespace only.
> mod _1 {
>     struct V {} // For namespace masking.
>     pub(super) use super::E2::*;
> }
> use _1::*;
> 
> fn f() {
>     // This struct pattern matches against the tuple-like
>     // enum variant whose constructor was found in the type
>     // namespace.
>     let V { 0: ..=u16::MAX } = (loop {}) else { loop {} };
>     // This tuple struct pattern matches against the tuple-like
>     // enum variant whose constructor was found in the value
>     // namespace.
>     let V(..=u32::MAX) = (loop {}) else { loop {} };
> }// Required due to the odd behavior of `super` within functions.fn main() {}The Lang team has made certain decisions, such as inPR #138458, that raise questions about the desirability of using the value namespace in this way for patterns, as described inPR #140593. It might be prudent to not intentionally rely on this nuance in your code.

Note

Conversely, a struct pattern for a tuple struct ortuple-like enum variant, e.g.S { 0: _ }, matches against the tuple struct or variant whose constructor is resolved in thetype namespace.

```rust
enum E1 { V(u16) }
enum E2 { V(u32) }

// Import `E1::V` from the type namespace only.
mod _0 {
    const V: () = (); // For namespace masking.
    pub(super) use super::E1::*;
}
use _0::*;

// Import `E2::V` from the value namespace only.
mod _1 {
    struct V {} // For namespace masking.
    pub(super) use super::E2::*;
}
use _1::*;

fn f() {
    // This struct pattern matches against the tuple-like
    // enum variant whose constructor was found in the type
    // namespace.
    let V { 0: ..=u16::MAX } = (loop {}) else { loop {} };
    // This tuple struct pattern matches against the tuple-like
    // enum variant whose constructor was found in the value
    // namespace.
    let V(..=u32::MAX) = (loop {}) else { loop {} };
}
// Required due to the odd behavior of `super` within functions.
fn main() {}
```

```rust
enum E1 { V(u16) }
enum E2 { V(u32) }

// Import `E1::V` from the type namespace only.
mod _0 {
    const V: () = (); // For namespace masking.
    pub(super) use super::E1::*;
}
use _0::*;

// Import `E2::V` from the value namespace only.
mod _1 {
    struct V {} // For namespace masking.
    pub(super) use super::E2::*;
}
use _1::*;

fn f() {
    // This struct pattern matches against the tuple-like
    // enum variant whose constructor was found in the type
    // namespace.
    let V { 0: ..=u16::MAX } = (loop {}) else { loop {} };
    // This tuple struct pattern matches against the tuple-like
    // enum variant whose constructor was found in the value
    // namespace.
    let V(..=u32::MAX) = (loop {}) else { loop {} };
}
// Required due to the odd behavior of `super` within functions.
fn main() {}
```

The Lang team has made certain decisions, such as inPR #138458, that raise questions about the desirability of using the value namespace in this way for patterns, as described inPR #140593. It might be prudent to not intentionally rely on this nuance in your code.

## Tuple patterns

SyntaxTuplePatternâ(TuplePatternItems?)

TuplePatternItemsâÂ Â Â Â Â ÂPattern,Â Â Â Â |RestPatternÂ Â Â Â |Pattern(,Pattern)+,?

Show Railroad

Tuple patterns match tuple values that match all criteria defined by its subpatterns.
They are also used todestructurea tuple.

The form(..)with a singleRestPatternis a special form that does not require a comma, and matches a tuple of any size.

The tuple pattern is refutable when one of its subpatterns is refutable.

An example of using tuple patterns:

```rust
#![allow(unused)]
fn main() {
let pair = (10, "ten");
let (a, b) = pair;

assert_eq!(a, 10);
assert_eq!(b, "ten");
}
```

```rust
#![allow(unused)]
fn main() {
let pair = (10, "ten");
let (a, b) = pair;

assert_eq!(a, 10);
assert_eq!(b, "ten");
}
```

## Grouped patterns

SyntaxGroupedPatternâ(Pattern)

Show Railroad

Enclosing a pattern in parentheses can be used to explicitly control the precedence of compound patterns.
For example, a reference pattern next to a range pattern such as&0..=5is ambiguous and is not allowed, but can be expressed with parentheses.

```rust
#![allow(unused)]
fn main() {
let int_reference = &3;
match int_reference {
    &(0..=5) => (),
    _ => (),
}
}
```

```rust
#![allow(unused)]
fn main() {
let int_reference = &3;
match int_reference {
    &(0..=5) => (),
    _ => (),
}
}
```

## Slice patterns

SyntaxSlicePatternâ[SlicePatternItems?]

SlicePatternItemsâPattern(,Pattern)*,?

Show Railroad

Slice patterns can match both arrays of fixed size and slices of dynamic size.

```rust
#![allow(unused)]
fn main() {
// Fixed size
let arr = [1, 2, 3];
match arr {
    [1, _, _] => "starts with one",
    [a, b, c] => "starts with something else",
};
}
```

```rust
#![allow(unused)]
fn main() {
// Fixed size
let arr = [1, 2, 3];
match arr {
    [1, _, _] => "starts with one",
    [a, b, c] => "starts with something else",
};
}
```

```rust
#![allow(unused)]
fn main() {
// Dynamic size
let v = vec![1, 2, 3];
match v[..] {
    [a, b] => { /* this arm will not apply because the length doesn't match */ }
    [a, b, c] => { /* this arm will apply */ }
    _ => { /* this wildcard is required, since the length is not known statically */ }
};
}
```

```rust
#![allow(unused)]
fn main() {
// Dynamic size
let v = vec![1, 2, 3];
match v[..] {
    [a, b] => { /* this arm will not apply because the length doesn't match */ }
    [a, b, c] => { /* this arm will apply */ }
    _ => { /* this wildcard is required, since the length is not known statically */ }
};
}
```

Slice patterns are irrefutable when matching an array as long as each element is irrefutable.

When matching a slice, it is irrefutable only in the form with a single..rest patternoridentifier patternwith the..rest pattern as a subpattern.

Within a slice, a range pattern without both lower and upper bound must be enclosed in parentheses, as in(a..), to clarify it is intended to match against a single slice element.
A range pattern with both lower and upper bound, likea..=b, is not required to be enclosed in parentheses.

## Path patterns

SyntaxPathPatternâPathExpression

Show Railroad

Path patternsare patterns that refer either to constant values or
to structs or enum variants that have no fields.

Unqualified path patterns can refer to:

- enum variants
- structs
- constants
- associated constants
Qualified path patterns can only refer to associated constants.

Path patterns are irrefutable when they refer to structs or an enum variant when the enum has only one variant or a constant whose type is irrefutable.
They are refutable when they refer to refutable constants or enum variants for enums with multiple variants.

### Constant patterns

When a constantCof typeTis used as a pattern, we first check thatT: PartialEq.

Furthermore we require that the value ofChas (recursive) structural equality, which is defined recursively as follows:

- Integers as well asstr,boolandcharvalues always have structural equality.
- Tuples, arrays, and slices have structural equality if all their fields/elements have structural equality.
(In particular,()and[]always have structural equality.)
- References have structural equality if the value they point to has structural equality.
- A value ofstructorenumtype has structural equality if itsPartialEqinstance is derived via#[derive(PartialEq)],
and all fields (for enums: of the active variant) have structural equality.
- A raw pointer has structural equality if it was defined as a constant integer (and then cast/transmuted).
- A float value has structural equality if it is not aNaN.
- Nothing else has structural equality.
In particular, the value ofCmust be known at pattern-building time (which is pre-monomorphization).
This means that associated consts that involve generic parameters cannot be used as patterns.

The value ofCmust not contain any references to mutable statics (static mutitems or interior mutablestaticitems) orexternstatics.

After ensuring all conditions are met, the constant value is translated into a pattern, and now behaves exactly as-if that pattern had been written directly.
In particular, it fully participates in exhaustiveness checking.
(For raw pointers, constants are the only way to write such patterns. Only_is ever considered exhaustive for these types.)

## Or-patterns

Or-patternsare patterns that match on one of two or more sub-patterns (for exampleA | B | C).
They can nest arbitrarily.
Syntactically, or-patterns are allowed in any of the places where other patterns are allowed (represented by thePatternproduction), with the exceptions oflet-bindings and function and closure arguments (represented by thePatternNoTopAltproduction).

### Static semantics

- Given a patternp | qat some depth for some arbitrary patternspandq, the pattern is considered ill-formed if:the type inferred forpdoes not unify with the type inferred forq, orthe same set of bindings are not introduced inpandq, orthe type of any two bindings with the same name inpandqdo not unify with respect to types or binding modes.Unification of types is in all instances aforementioned exact and implicittype coercionsdo not apply.
Given a patternp | qat some depth for some arbitrary patternspandq, the pattern is considered ill-formed if:

- the type inferred forpdoes not unify with the type inferred forq, or
- the same set of bindings are not introduced inpandq, or
- the type of any two bindings with the same name inpandqdo not unify with respect to types or binding modes.
Unification of types is in all instances aforementioned exact and implicittype coercionsdo not apply.

- When type checking an expressionmatch e_s { a_1 => e_1, ... a_n => e_n },
for each match arma_iwhich contains a pattern of formp_i | q_i,
the patternp_i | q_iis considered ill formed if,
at the depthdwhere it exists the fragment ofe_sat depthd,
the type of the expression fragment does not unify withp_i | q_i.
With respect to exhaustiveness checking, a patternp | qis considered to coverpas well asq.
For some constructorc(x, ..)the distributive law applies such thatc(p | q, ..rest)covers the same set of value asc(p, ..rest) | c(q, ..rest)does.
This can be applied recursively until there are no more nested patterns of formp | qother than those that exist at the top level.

Note that byâconstructorâwe do not refer to tuple struct patterns, but rather we refer to a pattern for any product type.
This includes enum variants, tuple structs, structs with named fields, arrays, tuples, and slices.

### Dynamic semantics

- The dynamic semantics of pattern matching a scrutinee expressione_sagainst a patternc(p | q, ..rest)at depthdwherecis some constructor,pandqare arbitrary patterns,
andrestis optionally any remaining potential factors inc,
is defined as being the same as that ofc(p, ..rest) | c(q, ..rest).

### Precedence with other undelimited patterns

As shown elsewhere in this chapter, there are several types of patterns that are syntactically undelimited, including identifier patterns, reference patterns, and or-patterns.
Or-patterns always have the lowest-precedence.
This allows us to reserve syntactic space for a possible future type ascription feature and also to reduce ambiguity.
For example,x @ A(..) | B(..)will result in an error thatxis not bound in all patterns.&A(x) | B(x)will result in a type mismatch betweenxin the different subpatterns.

- TheObsoleteRangePatternsyntax has been removed in the 2021 edition.â©
TheObsoleteRangePatternsyntax has been removed in the 2021 edition.â©
