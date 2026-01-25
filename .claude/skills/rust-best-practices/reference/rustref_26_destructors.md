# Destructors

Source: https://doc.rust-lang.org/reference/

When aninitializedvariableortemporarygoes out ofscope, itsdestructoris run or it isdropped.Assignmentalso runs the destructor of its left-hand operand, if itâs initialized. If a
variable has been partially initialized, only its initialized fields are
dropped.

The destructor of a typeTconsists of:

- IfT: Drop, calling<T as core::ops::Drop>::drop
- Recursively running the destructor of all of its fields.The fields of astructare dropped in declaration order.The fields of the activeenum variantare dropped in declaration order.The fields of atupleare dropped in order.The elements of anarrayor ownedsliceare dropped from the
first element to the last.The variables that aclosurecaptures by move are dropped in an
unspecified order.Trait objectsrun the destructor of the underlying type.Other types donât result in any further drops.
- The fields of astructare dropped in declaration order.
- The fields of the activeenum variantare dropped in declaration order.
- The fields of atupleare dropped in order.
- The elements of anarrayor ownedsliceare dropped from the
first element to the last.
- The variables that aclosurecaptures by move are dropped in an
unspecified order.
- Trait objectsrun the destructor of the underlying type.
- Other types donât result in any further drops.
If a destructor must be run manually, such as when implementing your own smart
pointer,core::ptr::drop_in_placecan be used.

Some examples:

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);

impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("{}", self.0);
    }
}

let mut overwritten = PrintOnDrop("drops when overwritten");
overwritten = PrintOnDrop("drops when scope ends");

let tuple = (PrintOnDrop("Tuple first"), PrintOnDrop("Tuple second"));

let moved;
// No destructor run on assignment.
moved = PrintOnDrop("Drops when moved");
// Drops now, but is then uninitialized.
moved;

// Uninitialized does not drop.
let uninitialized: PrintOnDrop;

// After a partial move, only the remaining fields are dropped.
let mut partial_move = (PrintOnDrop("first"), PrintOnDrop("forgotten"));
// Perform a partial move, leaving only `partial_move.0` initialized.
core::mem::forget(partial_move.1);
// When partial_move's scope ends, only the first field is dropped.
}
```

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);

impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("{}", self.0);
    }
}

let mut overwritten = PrintOnDrop("drops when overwritten");
overwritten = PrintOnDrop("drops when scope ends");

let tuple = (PrintOnDrop("Tuple first"), PrintOnDrop("Tuple second"));

let moved;
// No destructor run on assignment.
moved = PrintOnDrop("Drops when moved");
// Drops now, but is then uninitialized.
moved;

// Uninitialized does not drop.
let uninitialized: PrintOnDrop;

// After a partial move, only the remaining fields are dropped.
let mut partial_move = (PrintOnDrop("first"), PrintOnDrop("forgotten"));
// Perform a partial move, leaving only `partial_move.0` initialized.
core::mem::forget(partial_move.1);
// When partial_move's scope ends, only the first field is dropped.
}
```

## Drop scopes

Each variable or temporary is associated to adrop scope. When control flow
leaves a drop scope all variables associated to that scope are dropped in
reverse order of declaration (for variables) or creation (for temporaries).

Drop scopes can be determined by replacingfor,if, andwhileexpressions with equivalent expressions usingmatch,loopandbreak.

Overloaded operators are not distinguished from built-in operators andbinding
modesare not considered.

Given a function, or closure, there are drop scopes for:

- The entire function
- Eachstatement
- Eachexpression
- Each block, including the function bodyIn the case of ablock expression, the scope for the block and the
expression are the same scope.
- In the case of ablock expression, the scope for the block and the
expression are the same scope.
- Each arm of amatchexpression
Drop scopes are nested within one another as follows. When multiple scopes are
left at once, such as when returning from a function, variables are dropped
from the inside outwards.

- The entire function scope is the outer most scope.
- The function body block is contained within the scope of the entire function.
- The parent of the expression in an expression statement is the scope of the
statement.
- The parent of the initializer of aletstatementis theletstatementâs
scope.
- The parent of a statement scope is the scope of the block that contains the
statement.
- The parent of the expression for amatchguard is the scope of the arm that
the guard is for.
- The parent of the expression after the=>in amatchexpression is the
scope of the arm that itâs in.
- The parent of the arm scope is the scope of thematchexpression that it
belongs to.
- The parent of all other scopes is the scope of the immediately enclosing
expression.

### Scopes of function parameters

All function parameters are in the scope of the entire function body, so are
dropped last when evaluating the function. Each actual function parameter is
dropped after any bindings introduced in that parameterâs pattern.

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
// Drops `y`, then the second parameter, then `x`, then the first parameter
fn patterns_in_parameters(
    (x, _): (PrintOnDrop, PrintOnDrop),
    (_, y): (PrintOnDrop, PrintOnDrop),
) {}

// drop order is 3 2 0 1
patterns_in_parameters(
    (PrintOnDrop("0"), PrintOnDrop("1")),
    (PrintOnDrop("2"), PrintOnDrop("3")),
);
}
```

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
// Drops `y`, then the second parameter, then `x`, then the first parameter
fn patterns_in_parameters(
    (x, _): (PrintOnDrop, PrintOnDrop),
    (_, y): (PrintOnDrop, PrintOnDrop),
) {}

// drop order is 3 2 0 1
patterns_in_parameters(
    (PrintOnDrop("0"), PrintOnDrop("1")),
    (PrintOnDrop("2"), PrintOnDrop("3")),
);
}
```

### Scopes of local variables

Local variables declared in aletstatement are associated to the scope of
the block that contains theletstatement. Local variables declared in amatchexpression are associated to the arm scope of thematcharm that they
are declared in.

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
let declared_first = PrintOnDrop("Dropped last in outer scope");
{
    let declared_in_block = PrintOnDrop("Dropped in inner scope");
}
let declared_last = PrintOnDrop("Dropped first in outer scope");
}
```

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
let declared_first = PrintOnDrop("Dropped last in outer scope");
{
    let declared_in_block = PrintOnDrop("Dropped in inner scope");
}
let declared_last = PrintOnDrop("Dropped first in outer scope");
}
```

Variables in patterns are dropped in reverse order of declaration within the pattern.

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
let (declared_first, declared_last) = (
    PrintOnDrop("Dropped last"),
    PrintOnDrop("Dropped first"),
);
}
```

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
let (declared_first, declared_last) = (
    PrintOnDrop("Dropped last"),
    PrintOnDrop("Dropped first"),
);
}
```

For the purpose of drop order,or-patternsdeclare bindings in the order given by the first subpattern.

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
// Drops `x` before `y`.
fn or_pattern_drop_order<T>(
    (Ok([x, y]) | Err([y, x])): Result<[T; 2], [T; 2]>
//   ^^^^^^^^^^   ^^^^^^^^^^^ This is the second subpattern.
//   |
//   This is the first subpattern.
//
//   In the first subpattern, `x` is declared before `y`. Since it is
//   the first subpattern, that is the order used even if the second
//   subpattern, where the bindings are declared in the opposite
//   order, is matched.
) {}

// Here we match the first subpattern, and the drops happen according
// to the declaration order in the first subpattern.
or_pattern_drop_order(Ok([
    PrintOnDrop("Declared first, dropped last"),
    PrintOnDrop("Declared last, dropped first"),
]));

// Here we match the second subpattern, and the drops still happen
// according to the declaration order in the first subpattern.
or_pattern_drop_order(Err([
    PrintOnDrop("Declared last, dropped first"),
    PrintOnDrop("Declared first, dropped last"),
]));
}
```

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
// Drops `x` before `y`.
fn or_pattern_drop_order<T>(
    (Ok([x, y]) | Err([y, x])): Result<[T; 2], [T; 2]>
//   ^^^^^^^^^^   ^^^^^^^^^^^ This is the second subpattern.
//   |
//   This is the first subpattern.
//
//   In the first subpattern, `x` is declared before `y`. Since it is
//   the first subpattern, that is the order used even if the second
//   subpattern, where the bindings are declared in the opposite
//   order, is matched.
) {}

// Here we match the first subpattern, and the drops happen according
// to the declaration order in the first subpattern.
or_pattern_drop_order(Ok([
    PrintOnDrop("Declared first, dropped last"),
    PrintOnDrop("Declared last, dropped first"),
]));

// Here we match the second subpattern, and the drops still happen
// according to the declaration order in the first subpattern.
or_pattern_drop_order(Err([
    PrintOnDrop("Declared last, dropped first"),
    PrintOnDrop("Declared first, dropped last"),
]));
}
```

### Temporary scopes

Thetemporary scopeof an expression is the scope that is used for the
temporary variable that holds the result of that expression when used in aplace context, unless it ispromoted.

Apart from lifetime extension, the temporary scope of an expression is the
smallest scope that contains the expression and is one of the following:

- The entire function.
- A statement.
- The body of anif,whileorloopexpression.
- Theelseblock of anifexpression.
- The non-pattern matching condition expression of aniforwhileexpression,
or amatchguard.
- The body expression for a match arm.
- Each operand of alazy boolean expression.
- The pattern-matching condition(s) and consequent body ofif(destructors.scope.temporary.edition2024).
- The pattern-matching condition and loop body ofwhile.
- The entirety of the tail expression of a block (destructors.scope.temporary.edition2024).

> NoteThescrutineeof amatchexpression is not a temporary scope, so temporaries in the scrutinee can be dropped after thematchexpression. For example, the temporary for1inmatch 1 { ref mut z => z };lives until the end of the statement.

Note

Thescrutineeof amatchexpression is not a temporary scope, so temporaries in the scrutinee can be dropped after thematchexpression. For example, the temporary for1inmatch 1 { ref mut z => z };lives until the end of the statement.

> NoteThe desugaring of adestructuring assignmentrestricts the temporary scope of its assigned value operand (the RHS). For details, seeexpr.assign.destructure.tmp-scopes.

Note

The desugaring of adestructuring assignmentrestricts the temporary scope of its assigned value operand (the RHS). For details, seeexpr.assign.destructure.tmp-scopes.

> 2024Edition differencesThe 2024 edition added two new temporary scope narrowing rules:if lettemporaries are dropped before theelseblock, and temporaries of tail expressions of blocks are dropped immediately after the tail expression is evaluated.

2024Edition differences

The 2024 edition added two new temporary scope narrowing rules:if lettemporaries are dropped before theelseblock, and temporaries of tail expressions of blocks are dropped immediately after the tail expression is evaluated.

Some examples:

```rust
#![allow(unused)]
fn main() {
#![allow(irrefutable_let_patterns)]
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
let local_var = PrintOnDrop("local var");

// Dropped once the condition has been evaluated
if PrintOnDrop("If condition").0 == "If condition" {
    // Dropped at the end of the block
    PrintOnDrop("If body").0
} else {
    unreachable!()
};

if let "if let scrutinee" = PrintOnDrop("if let scrutinee").0 {
    PrintOnDrop("if let consequent").0
    // `if let consequent` dropped here
}
// `if let scrutinee` is dropped here
else {
    PrintOnDrop("if let else").0
    // `if let else` dropped here
};

while let x = PrintOnDrop("while let scrutinee").0 {
    PrintOnDrop("while let loop body").0;
    break;
    // `while let loop body` dropped here.
    // `while let scrutinee` dropped here.
}

// Dropped before the first ||
(PrintOnDrop("first operand").0 == ""
// Dropped before the )
|| PrintOnDrop("second operand").0 == "")
// Dropped before the ;
|| PrintOnDrop("third operand").0 == "";

// Scrutinee is dropped at the end of the function, before local variables
// (because this is the tail expression of the function body block).
match PrintOnDrop("Matched value in final expression") {
    // Dropped once the condition has been evaluated
    _ if PrintOnDrop("guard condition").0 == "" => (),
    _ => (),
}
}
```

```rust
#![allow(unused)]
fn main() {
#![allow(irrefutable_let_patterns)]
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
let local_var = PrintOnDrop("local var");

// Dropped once the condition has been evaluated
if PrintOnDrop("If condition").0 == "If condition" {
    // Dropped at the end of the block
    PrintOnDrop("If body").0
} else {
    unreachable!()
};

if let "if let scrutinee" = PrintOnDrop("if let scrutinee").0 {
    PrintOnDrop("if let consequent").0
    // `if let consequent` dropped here
}
// `if let scrutinee` is dropped here
else {
    PrintOnDrop("if let else").0
    // `if let else` dropped here
};

while let x = PrintOnDrop("while let scrutinee").0 {
    PrintOnDrop("while let loop body").0;
    break;
    // `while let loop body` dropped here.
    // `while let scrutinee` dropped here.
}

// Dropped before the first ||
(PrintOnDrop("first operand").0 == ""
// Dropped before the )
|| PrintOnDrop("second operand").0 == "")
// Dropped before the ;
|| PrintOnDrop("third operand").0 == "";

// Scrutinee is dropped at the end of the function, before local variables
// (because this is the tail expression of the function body block).
match PrintOnDrop("Matched value in final expression") {
    // Dropped once the condition has been evaluated
    _ if PrintOnDrop("guard condition").0 == "" => (),
    _ => (),
}
}
```

### Operands

Temporaries are also created to hold the result of operands to an expression
while the other operands are evaluated. The temporaries are associated to the
scope of the expression with that operand. Since the temporaries are moved from
once the expression is evaluated, dropping them has no effect unless one of the
operands to an expression breaks out of the expression, returns, orpanics.

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
loop {
    // Tuple expression doesn't finish evaluating so operands drop in reverse order
    (
        PrintOnDrop("Outer tuple first"),
        PrintOnDrop("Outer tuple second"),
        (
            PrintOnDrop("Inner tuple first"),
            PrintOnDrop("Inner tuple second"),
            break,
        ),
        PrintOnDrop("Never created"),
    );
}
}
```

```rust
#![allow(unused)]
fn main() {
struct PrintOnDrop(&'static str);
impl Drop for PrintOnDrop {
    fn drop(&mut self) {
        println!("drop({})", self.0);
    }
}
loop {
    // Tuple expression doesn't finish evaluating so operands drop in reverse order
    (
        PrintOnDrop("Outer tuple first"),
        PrintOnDrop("Outer tuple second"),
        (
            PrintOnDrop("Inner tuple first"),
            PrintOnDrop("Inner tuple second"),
            break,
        ),
        PrintOnDrop("Never created"),
    );
}
}
```

### Constant promotion

Promotion of a value expression to a'staticslot occurs when the expression
could be written in a constant and borrowed, and that borrow could be dereferenced
where
the expression was originally written, without changing the runtime behavior.
That is, the promoted expression can be evaluated at compile-time and the
resulting value does not containinterior mutabilityordestructors(these
properties are determined based on the value where possible, e.g.&Nonealways has the type&'static Option<_>, as it contains nothing disallowed).

### Temporary lifetime extension

> NoteThe exact rules for temporary lifetime extension are subject to change. This is describing the current behavior only.

Note

The exact rules for temporary lifetime extension are subject to change. This is describing the current behavior only.

The temporary scopes for expressions inletstatements are sometimesextendedto the scope of the block containing theletstatement. This is
done when the usual temporary scope would be too small, based on certain
syntactic rules. For example:

```rust
#![allow(unused)]
fn main() {
let x = &mut 0;
// Usually a temporary would be dropped by now, but the temporary for `0` lives
// to the end of the block.
println!("{}", x);
}
```

```rust
#![allow(unused)]
fn main() {
let x = &mut 0;
// Usually a temporary would be dropped by now, but the temporary for `0` lives
// to the end of the block.
println!("{}", x);
}
```

Lifetime extension also applies tostaticandconstitems, where it
makes temporaries live until the end of the program. For example:

```rust
#![allow(unused)]
fn main() {
const C: &Vec<i32> = &Vec::new();
// Usually this would be a dangling reference as the `Vec` would only
// exist inside the initializer expression of `C`, but instead the
// borrow gets lifetime-extended so it effectively has `'static` lifetime.
println!("{:?}", C);
}
```

```rust
#![allow(unused)]
fn main() {
const C: &Vec<i32> = &Vec::new();
// Usually this would be a dangling reference as the `Vec` would only
// exist inside the initializer expression of `C`, but instead the
// borrow gets lifetime-extended so it effectively has `'static` lifetime.
println!("{:?}", C);
}
```

If aborrow,dereference,field, ortuple indexing expressionhas an extended temporary scope, then so does its operand. If anindexing expressionhas an extended temporary scope, then the indexed expression also has an extended temporary scope.

#### Extending based on patterns

Anextending patternis either:

- Anidentifier patternthat binds by reference or mutable reference.#![allow(unused)]fn main() {fn temp() {}let ref x = temp(); // Binds by reference.x;let ref mut x = temp(); // Binds by mutable reference.x;}
Anidentifier patternthat binds by reference or mutable reference.

```rust
#![allow(unused)]
fn main() {
fn temp() {}
let ref x = temp(); // Binds by reference.
x;
let ref mut x = temp(); // Binds by mutable reference.
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
let ref x = temp(); // Binds by reference.
x;
let ref mut x = temp(); // Binds by mutable reference.
x;
}
```

Astruct,tuple,tuple struct,slice, oror-patternwhere at least one of the direct subpatterns is an extending pattern.

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::{AtomicU64, Ordering::Relaxed};
static X: AtomicU64 = AtomicU64::new(0);
struct W<T>(T);
impl<T> Drop for W<T> { fn drop(&mut self) { X.fetch_add(1, Relaxed); } }
let W { 0: ref x } = W(()); // Struct pattern.
x;
let W(ref x) = W(()); // Tuple struct pattern.
x;
let (W(ref x),) = (W(()),); // Tuple pattern.
x;
let [W(ref x), ..] = [W(())]; // Slice pattern.
x;
let (Ok(W(ref x)) | Err(&ref x)) = Ok(W(())); // Or pattern.
x;
//
// All of the temporaries above are still live here.
assert_eq!(0, X.load(Relaxed));
}
```

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::{AtomicU64, Ordering::Relaxed};
static X: AtomicU64 = AtomicU64::new(0);
struct W<T>(T);
impl<T> Drop for W<T> { fn drop(&mut self) { X.fetch_add(1, Relaxed); } }
let W { 0: ref x } = W(()); // Struct pattern.
x;
let W(ref x) = W(()); // Tuple struct pattern.
x;
let (W(ref x),) = (W(()),); // Tuple pattern.
x;
let [W(ref x), ..] = [W(())]; // Slice pattern.
x;
let (Ok(W(ref x)) | Err(&ref x)) = Ok(W(())); // Or pattern.
x;
//
// All of the temporaries above are still live here.
assert_eq!(0, X.load(Relaxed));
}
```

Soref x,V(ref x)and[ref x, y]are all extending patterns, butx,&ref xand&(ref x,)are not.

If the pattern in aletstatement is an extending pattern then the temporary
scope of the initializer expression is extended.

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// This is an extending pattern, so the temporary scope is extended.
let ref x = *&temp(); // OK
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// This is an extending pattern, so the temporary scope is extended.
let ref x = *&temp(); // OK
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// This is neither an extending pattern nor an extending expression,
// so the temporary is dropped at the semicolon.
let &ref x = *&&temp(); // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// This is neither an extending pattern nor an extending expression,
// so the temporary is dropped at the semicolon.
let &ref x = *&&temp(); // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// This is not an extending pattern but it is an extending expression,
// so the temporary lives beyond the `let` statement.
let &ref x = &*&temp(); // OK
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// This is not an extending pattern but it is an extending expression,
// so the temporary lives beyond the `let` statement.
let &ref x = &*&temp(); // OK
x;
}
```

- tests/ui/lifetimes/temporary-lifetime-extension-tuple-ctor.rs

#### Extending based on expressions

For a let statement with an initializer, anextending expressionis an
expression which is one of the following:

- The initializer expression.
- The operand of an extendingborrowexpression.
- Thesuper operandsof an extendingsuper macro callexpression.
- The operand(s) of an extendingarray,cast,braced struct, ortupleexpression.
- The arguments to an extendingtuple structortuple enum variantconstructor expression.
- The final expression of an extendingblock expressionexcept for anasync block expression.
- The final expression of an extendingifexpressionâs consequent,else if, orelseblock.
- An arm expression of an extendingmatchexpression.

> NoteThe desugaring of adestructuring assignmentmakes its assigned value operand (the RHS) an extending expression within a newly-introduced block. For details, seeexpr.assign.destructure.tmp-ext.

Note

The desugaring of adestructuring assignmentmakes its assigned value operand (the RHS) an extending expression within a newly-introduced block. For details, seeexpr.assign.destructure.tmp-ext.

So the borrow expressions in&mut 0,(&1, &mut 2), andSome(&mut 3)are all extending expressions. The borrows in&0 + &1andf(&mut 0)are not.

The operand of an extendingborrowexpression has itstemporary scopeextended.

Thesuper temporariesof an extendingsuper macro callexpression have theirscopesextended.

> Noterustcdoes not treatarray repeat operandsof extendingarrayexpressions as extending expressions. Whether it should is an open question.For details, seeRust issue #146092.

Note

rustcdoes not treatarray repeat operandsof extendingarrayexpressions as extending expressions. Whether it should is an open question.

For details, seeRust issue #146092.

#### Examples

Here are some examples where expressions have extended temporary scopes:

```rust
#![allow(unused)]
fn main() {
use core::pin::pin;
use core::sync::atomic::{AtomicU64, Ordering::Relaxed};
static X: AtomicU64 = AtomicU64::new(0);
#[derive(Debug)] struct S;
impl Drop for S { fn drop(&mut self) { X.fetch_add(1, Relaxed); } }
const fn temp() -> S { S }
let x = &temp(); // Operand of borrow.
x;
let x = &raw const *&temp(); // Operand of raw borrow.
assert_eq!(X.load(Relaxed), 0);
let x = &temp() as &dyn Send; // Operand of cast.
x;
let x = (&*&temp(),); // Operand of tuple constructor.
x;
struct W<T>(T);
let x = W(&temp()); // Argument to tuple struct constructor.
x;
let x = Some(&temp()); // Argument to tuple enum variant constructor.
x;
let x = { [Some(&temp())] }; // Final expr of block.
x;
let x = const { &temp() }; // Final expr of `const` block.
x;
let x = unsafe { &temp() }; // Final expr of `unsafe` block.
x;
let x = if true { &temp() } else { &temp() };
//              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
//           Final exprs of `if`/`else` blocks.
x;
let x = match () { _ => &temp() }; // `match` arm expression.
x;
let x = pin!(temp()); // Super operand of super macro call expression.
x;
let x = pin!({ &mut temp() }); // As above.
x;
let x = format_args!("{:?}", temp()); // As above.
x;
//
// All of the temporaries above are still live here.
assert_eq!(0, X.load(Relaxed));
}
```

```rust
#![allow(unused)]
fn main() {
use core::pin::pin;
use core::sync::atomic::{AtomicU64, Ordering::Relaxed};
static X: AtomicU64 = AtomicU64::new(0);
#[derive(Debug)] struct S;
impl Drop for S { fn drop(&mut self) { X.fetch_add(1, Relaxed); } }
const fn temp() -> S { S }
let x = &temp(); // Operand of borrow.
x;
let x = &raw const *&temp(); // Operand of raw borrow.
assert_eq!(X.load(Relaxed), 0);
let x = &temp() as &dyn Send; // Operand of cast.
x;
let x = (&*&temp(),); // Operand of tuple constructor.
x;
struct W<T>(T);
let x = W(&temp()); // Argument to tuple struct constructor.
x;
let x = Some(&temp()); // Argument to tuple enum variant constructor.
x;
let x = { [Some(&temp())] }; // Final expr of block.
x;
let x = const { &temp() }; // Final expr of `const` block.
x;
let x = unsafe { &temp() }; // Final expr of `unsafe` block.
x;
let x = if true { &temp() } else { &temp() };
//              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
//           Final exprs of `if`/`else` blocks.
x;
let x = match () { _ => &temp() }; // `match` arm expression.
x;
let x = pin!(temp()); // Super operand of super macro call expression.
x;
let x = pin!({ &mut temp() }); // As above.
x;
let x = format_args!("{:?}", temp()); // As above.
x;
//
// All of the temporaries above are still live here.
assert_eq!(0, X.load(Relaxed));
}
```

Here are some examples where expressions donât have extended temporary scopes:

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Arguments to function calls are not extending expressions. The
// temporary is dropped at the semicolon.
let x = core::convert::identity(&temp()); // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Arguments to function calls are not extending expressions. The
// temporary is dropped at the semicolon.
let x = core::convert::identity(&temp()); // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
trait Use { fn use_temp(&self) -> &Self { self } }
impl Use for () {}
// Receivers of method calls are not extending expressions.
let x = (&temp()).use_temp(); // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
trait Use { fn use_temp(&self) -> &Self { self } }
impl Use for () {}
// Receivers of method calls are not extending expressions.
let x = (&temp()).use_temp(); // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Scrutinees of match expressions are not extending expressions.
let x = match &temp() { x => x }; // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Scrutinees of match expressions are not extending expressions.
let x = match &temp() { x => x }; // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Final expressions of `async` blocks are not extending expressions.
let x = async { &temp() }; // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Final expressions of `async` blocks are not extending expressions.
let x = async { &temp() }; // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Final expressions of closures are not extending expressions.
let x = || &temp(); // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Final expressions of closures are not extending expressions.
let x = || &temp(); // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Operands of loop breaks are not extending expressions.
let x = loop { break &temp() }; // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Operands of loop breaks are not extending expressions.
let x = loop { break &temp() }; // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Operands of breaks to labels are not extending expressions.
let x = 'a: { break 'a &temp() }; // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// Operands of breaks to labels are not extending expressions.
let x = 'a: { break 'a &temp() }; // ERROR
x;
}
```

```rust
#![allow(unused)]
fn main() {
use core::pin::pin;
fn temp() {}
// The argument to `pin!` is only an extending expression if the call
// is an extending expression. Since it's not, the inner block is not
// an extending expression, so the temporaries in its trailing
// expression are dropped immediately.
pin!({ &temp() }); // ERROR
}
```

```rust
#![allow(unused)]
fn main() {
use core::pin::pin;
fn temp() {}
// The argument to `pin!` is only an extending expression if the call
// is an extending expression. Since it's not, the inner block is not
// an extending expression, so the temporaries in its trailing
// expression are dropped immediately.
pin!({ &temp() }); // ERROR
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// As above.
format_args!("{:?}", { &temp() }); // ERROR
}
```

```rust
#![allow(unused)]
fn main() {
fn temp() {}
// As above.
format_args!("{:?}", { &temp() }); // ERROR
}
```

## Not running destructors

### Manually suppressing destructors

core::mem::forgetcan be used to prevent the destructor of a variable from being run,
andcore::mem::ManuallyDropprovides a wrapper to prevent a
variable or field from being dropped automatically.

> NotePreventing a destructor from being run viacore::mem::forgetor other means is safe even if it has a type that isnât'static. Besides the places where destructors are guaranteed to run as defined by this document, types maynotsafely rely on a destructor being run for soundness.

Note

Preventing a destructor from being run viacore::mem::forgetor other means is safe even if it has a type that isnât'static. Besides the places where destructors are guaranteed to run as defined by this document, types maynotsafely rely on a destructor being run for soundness.

### Process termination without unwinding

There are some ways to terminate the process withoutunwinding, in which case destructors will not be run.

The standard library providesstd::process::exitandstd::process::abortto do this explicitly. Additionally, if thepanic handleris set toabort, panicking will always terminate the process without destructors being run.

There is one additional case to be aware of: when a panic reaches anon-unwinding ABI boundary, either no destructors will run, or all destructors up until the ABI boundary will run.
