# Constant Evaluation

Source: https://doc.rust-lang.org/reference/

# Constant evaluation

Constant evaluation is the process of computing the result ofexpressionsduring compilation. Only a subset of all expressions
can be evaluated at compile-time.

## Constant expressions

Certain forms of expressions, called constant expressions, can be evaluated at
compile time.

Inconst contexts, these are the only allowed
expressions, and are always evaluated at compile time.

In other places, such aslet statements, constant expressionsmaybe, but are not guaranteed to be, evaluated at compile time.

Behaviors such as out of boundsarray indexingoroverfloware compiler errors if the value
must be evaluated at compile time (i.e. in const contexts). Otherwise, these
behaviors are warnings, but will likely panic at run-time.

The following expressions are constant expressions, so long as any operands are
also constant expressions and do not cause anyDrop::dropcalls
to be run.

- Literals.
- Const parameters.
- Pathstofunctionsandconstants.
Recursively defining constants is not allowed.
Paths tostaticswith these restrictions:

- Writes tostaticitems are not allowed in any constant evaluation context.
- Reads fromexternstatics are not allowed in any constant evaluation context.
- If the evaluation isnotcarried out in an initializer of astaticitem, then reads from any mutablestaticare not allowed. A mutablestaticis astatic mutitem, or astaticitem with an interior-mutable type.
These requirements are checked only when the constant is evaluated. In other words, having such accesses syntactically occur in const contexts is allowed as long as they never get executed.

- Tuple expressions.
- Array expressions.
- Struct expressions.
- Block expressions, includingunsafeandconstblocks.let statementsand thus irrefutablepatterns, including mutable bindingsassignment expressionscompound assignment expressionsexpression statements
- let statementsand thus irrefutablepatterns, including mutable bindings
- assignment expressions
- compound assignment expressions
- expression statements
- Fieldexpressions.
- Index expressions,array indexingorslicewith ausize.
- Range expressions.
- Closure expressionswhich donât capture variables from the environment.
- Built-innegation,arithmetic,logical,comparisonorlazy booleanoperators used on integer and floating point types,bool, andchar.
All forms ofborrows, including raw borrows, except borrows of expressions whose temporary scopes would be extended (seetemporary lifetime extension) to the end of the program and which are either:

- Mutable borrows.
- Shared borrows of expressions that result in values withinterior mutability.

```rust
#![allow(unused)]
fn main() {
// Due to being in tail position, this borrow extends the scope of the
// temporary to the end of the program. Since the borrow is mutable,
// this is not allowed in a const expression.
const C: &u8 = &mut 0; // ERROR not allowed
}
```

```rust
#![allow(unused)]
fn main() {
// Due to being in tail position, this borrow extends the scope of the
// temporary to the end of the program. Since the borrow is mutable,
// this is not allowed in a const expression.
const C: &u8 = &mut 0; // ERROR not allowed
}
```

```rust
#![allow(unused)]
fn main() {
// Const blocks are similar to initializers of `const` items.
let _: &u8 = const { &mut 0 }; // ERROR not allowed
}
```

```rust
#![allow(unused)]
fn main() {
// Const blocks are similar to initializers of `const` items.
let _: &u8 = const { &mut 0 }; // ERROR not allowed
}
```

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::AtomicU8;
// This is not allowed as 1) the temporary scope is extended to the
// end of the program and 2) the temporary has interior mutability.
const C: &AtomicU8 = &AtomicU8::new(0); // ERROR not allowed
}
```

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::AtomicU8;
// This is not allowed as 1) the temporary scope is extended to the
// end of the program and 2) the temporary has interior mutability.
const C: &AtomicU8 = &AtomicU8::new(0); // ERROR not allowed
}
```

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::AtomicU8;
// As above.
let _: &_ = const { &AtomicU8::new(0) }; // ERROR not allowed
}
```

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::AtomicU8;
// As above.
let _: &_ = const { &AtomicU8::new(0) }; // ERROR not allowed
}
```

```rust
#![allow(unused)]
fn main() {
#![allow(static_mut_refs)]
// Even though this borrow is mutable, it's not of a temporary, so
// this is allowed.
const C: &u8 = unsafe { static mut S: u8 = 0; &mut S }; // OK
}
```

```rust
#![allow(unused)]
fn main() {
#![allow(static_mut_refs)]
// Even though this borrow is mutable, it's not of a temporary, so
// this is allowed.
const C: &u8 = unsafe { static mut S: u8 = 0; &mut S }; // OK
}
```

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::AtomicU8;
// Even though this borrow is of a value with interior mutability,
// it's not of a temporary, so this is allowed.
const C: &AtomicU8 = {
    static S: AtomicU8 = AtomicU8::new(0); &S // OK
};
}
```

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::AtomicU8;
// Even though this borrow is of a value with interior mutability,
// it's not of a temporary, so this is allowed.
const C: &AtomicU8 = {
    static S: AtomicU8 = AtomicU8::new(0); &S // OK
};
}
```

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::AtomicU8;
// This shared borrow of an interior mutable temporary is allowed
// because its scope is not extended.
const C: () = { _ = &AtomicU8::new(0); }; // OK
}
```

```rust
#![allow(unused)]
fn main() {
use core::sync::atomic::AtomicU8;
// This shared borrow of an interior mutable temporary is allowed
// because its scope is not extended.
const C: () = { _ = &AtomicU8::new(0); }; // OK
}
```

```rust
#![allow(unused)]
fn main() {
// Even though the borrow is mutable and the temporary lives to the
// end of the program due to promotion, this is allowed because the
// borrow is not in tail position and so the scope of the temporary
// is not extended via temporary lifetime extension.
const C: () = { let _: &'static mut [u8] = &mut []; }; // OK
//                                              ~~
//                                     Promoted temporary.
}
```

```rust
#![allow(unused)]
fn main() {
// Even though the borrow is mutable and the temporary lives to the
// end of the program due to promotion, this is allowed because the
// borrow is not in tail position and so the scope of the temporary
// is not extended via temporary lifetime extension.
const C: () = { let _: &'static mut [u8] = &mut []; }; // OK
//                                              ~~
//                                     Promoted temporary.
}
```

> NoteIn other words â to focus on whatâs allowed rather than whatâs not allowed â shared borrows of interior mutable data and mutable borrows are only allowed in aconst contextwhen the borrowedplace expressionistransient,indirect, orstatic.A place expression istransientif it is a variable local to the current const context or an expression whose temporary scope is contained inside the current const context.#![allow(unused)]fn main() {// The borrow is of a variable local to the initializer, therefore
> // this place expression is transient.
> const C: () = { let mut x = 0; _ = &mut x; };}#![allow(unused)]fn main() {// The borrow is of a temporary whose scope has not been extended,
> // therefore this place expression is transient.
> const C: () = { _ = &mut 0u8; };}#![allow(unused)]fn main() {// When a temporary is promoted but not lifetime extended, its
> // place expression is still treated as transient.
> const C: () = { let _: &'static mut [u8] = &mut []; };}A place expression isindirectif it is adereference expression.#![allow(unused)]fn main() {const C: () = { _ = &mut *(&mut 0); };}A place expression isstaticif it is astaticitem.#![allow(unused)]fn main() {#![allow(static_mut_refs)]const C: &u8 = unsafe { static mut S: u8 = 0; &mut S };}

Note

In other words â to focus on whatâs allowed rather than whatâs not allowed â shared borrows of interior mutable data and mutable borrows are only allowed in aconst contextwhen the borrowedplace expressionistransient,indirect, orstatic.

A place expression istransientif it is a variable local to the current const context or an expression whose temporary scope is contained inside the current const context.

```rust
#![allow(unused)]
fn main() {
// The borrow is of a variable local to the initializer, therefore
// this place expression is transient.
const C: () = { let mut x = 0; _ = &mut x; };
}
```

```rust
#![allow(unused)]
fn main() {
// The borrow is of a variable local to the initializer, therefore
// this place expression is transient.
const C: () = { let mut x = 0; _ = &mut x; };
}
```

```rust
#![allow(unused)]
fn main() {
// The borrow is of a temporary whose scope has not been extended,
// therefore this place expression is transient.
const C: () = { _ = &mut 0u8; };
}
```

```rust
#![allow(unused)]
fn main() {
// The borrow is of a temporary whose scope has not been extended,
// therefore this place expression is transient.
const C: () = { _ = &mut 0u8; };
}
```

```rust
#![allow(unused)]
fn main() {
// When a temporary is promoted but not lifetime extended, its
// place expression is still treated as transient.
const C: () = { let _: &'static mut [u8] = &mut []; };
}
```

```rust
#![allow(unused)]
fn main() {
// When a temporary is promoted but not lifetime extended, its
// place expression is still treated as transient.
const C: () = { let _: &'static mut [u8] = &mut []; };
}
```

A place expression isindirectif it is adereference expression.

```rust
#![allow(unused)]
fn main() {
const C: () = { _ = &mut *(&mut 0); };
}
```

```rust
#![allow(unused)]
fn main() {
const C: () = { _ = &mut *(&mut 0); };
}
```

A place expression isstaticif it is astaticitem.

```rust
#![allow(unused)]
fn main() {
#![allow(static_mut_refs)]
const C: &u8 = unsafe { static mut S: u8 = 0; &mut S };
}
```

```rust
#![allow(unused)]
fn main() {
#![allow(static_mut_refs)]
const C: &u8 = unsafe { static mut S: u8 = 0; &mut S };
}
```

> NoteOne surprising consequence of these rules is that we allow this,#![allow(unused)]fn main() {const C: &[u8] = { let x: &mut [u8] = &mut []; x }; // OK
> //                                    ~~~~~~~
> // Empty arrays are promoted even behind mutable borrows.}but we disallow this similar code:#![allow(unused)]fn main() {const C: &[u8] = &mut []; // ERROR
> //               ~~~~~~~
> //           Tail expression.}The difference between these is that, in the first, the empty array ispromotedbut its scope does not undergotemporary lifetime extension, so we consider theplace expressionto be transient (even though after promotion the place indeed lives to the end of the program). In the second, the scope of the empty array temporary does undergo lifetime extension, and so it is rejected due to being a mutable borrow of a lifetime-extended temporary (and therefore borrowing a non-transient place expression).The effect is surprising because temporary lifetime extension, in this case, causes less code to compile than would without it.Seeissue #143129for more details.

Note

One surprising consequence of these rules is that we allow this,

```rust
#![allow(unused)]
fn main() {
const C: &[u8] = { let x: &mut [u8] = &mut []; x }; // OK
//                                    ~~~~~~~
// Empty arrays are promoted even behind mutable borrows.
}
```

```rust
#![allow(unused)]
fn main() {
const C: &[u8] = { let x: &mut [u8] = &mut []; x }; // OK
//                                    ~~~~~~~
// Empty arrays are promoted even behind mutable borrows.
}
```

but we disallow this similar code:

```rust
#![allow(unused)]
fn main() {
const C: &[u8] = &mut []; // ERROR
//               ~~~~~~~
//           Tail expression.
}
```

```rust
#![allow(unused)]
fn main() {
const C: &[u8] = &mut []; // ERROR
//               ~~~~~~~
//           Tail expression.
}
```

The difference between these is that, in the first, the empty array ispromotedbut its scope does not undergotemporary lifetime extension, so we consider theplace expressionto be transient (even though after promotion the place indeed lives to the end of the program). In the second, the scope of the empty array temporary does undergo lifetime extension, and so it is rejected due to being a mutable borrow of a lifetime-extended temporary (and therefore borrowing a non-transient place expression).

The effect is surprising because temporary lifetime extension, in this case, causes less code to compile than would without it.

Seeissue #143129for more details.

- Dereference expressions.#![allow(unused)]fn main() {use core::cell::UnsafeCell;const _: u8 = unsafe {
    let x: *mut u8 = &raw mut *&mut 0;
    //                        ^^^^^^^
    //             Dereference of mutable reference.
    *x = 1; // Dereference of mutable pointer.
    *(x as *const u8) // Dereference of constant pointer.
};
const _: u8 = unsafe {
    let x = &UnsafeCell::new(0);
    *x.get() = 1; // Mutation of interior mutable value.
    *x.get()
};}
Dereference expressions.

```rust
#![allow(unused)]
fn main() {
use core::cell::UnsafeCell;
const _: u8 = unsafe {
    let x: *mut u8 = &raw mut *&mut 0;
    //                        ^^^^^^^
    //             Dereference of mutable reference.
    *x = 1; // Dereference of mutable pointer.
    *(x as *const u8) // Dereference of constant pointer.
};
const _: u8 = unsafe {
    let x = &UnsafeCell::new(0);
    *x.get() = 1; // Mutation of interior mutable value.
    *x.get()
};
}
```

```rust
#![allow(unused)]
fn main() {
use core::cell::UnsafeCell;
const _: u8 = unsafe {
    let x: *mut u8 = &raw mut *&mut 0;
    //                        ^^^^^^^
    //             Dereference of mutable reference.
    *x = 1; // Dereference of mutable pointer.
    *(x as *const u8) // Dereference of constant pointer.
};
const _: u8 = unsafe {
    let x = &UnsafeCell::new(0);
    *x.get() = 1; // Mutation of interior mutable value.
    *x.get()
};
}
```

- Groupedexpressions.
- Castexpressions, exceptpointer to address casts andfunction pointer to address casts.
- pointer to address casts and
- function pointer to address casts.
- Calls ofconst functionsand const methods.
- loopandwhileexpressions.
- ifandmatchexpressions.

## Const context

Aconst contextis one of the following:

- Array type length expressions
- Array repeat length expressions
- The initializer ofconstantsstaticsenum discriminants
- constants
- statics
- enum discriminants
- Aconst generic argument
- Aconst block
Const contexts that are used as parts of types (array type and repeat length
expressions as well as const generic arguments) can only make restricted use of
surrounding generic parameters: such an expression must either be a single bare
const generic parameter, or an arbitrary expression not making use of any
generics.

## Const functions

Aconst functionis a function that can be called from a const context. It is defined with theconstqualifier, and also includestuple structandtuple enum variantconstructors.

> Example#![allow(unused)]fn main() {const fn square(x: i32) -> i32 { x * x }
> 
> const VALUE: i32 = square(12);}

Example

```rust
#![allow(unused)]
fn main() {
const fn square(x: i32) -> i32 { x * x }

const VALUE: i32 = square(12);
}
```

```rust
#![allow(unused)]
fn main() {
const fn square(x: i32) -> i32 { x * x }

const VALUE: i32 = square(12);
}
```

When called from a const context, a const function is interpreted by the compiler at compile time. The interpretation happens in the environment of the compilation target and not the host. Sousizeis32bits if you are compiling against a32bit system, irrelevant of whether you are building on a64bit or a32bit system.

When a const function is called from outside a const context, it behaves the same as if it did not have theconstqualifier.

The body of a const function may only useconstant expressions.

Const functions are not allowed to beasync.

The types of a const functionâs parameters and return type are restricted to those that are compatible with a const context.
