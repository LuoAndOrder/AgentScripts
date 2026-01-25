# Type Coercions

Source: https://doc.rust-lang.org/reference/

# Type coercions

Type coercionsare implicit operations that change the type of a value.
They happen automatically at specific locations and are highly restricted in
what types actually coerce.

Any conversions allowed by coercion can also be explicitly performed by thetype cast operator,as.

Coercions are originally defined inRFC 401and expanded upon inRFC 1558.

## Coercion sites

A coercion can only occur at certain coercion sites in a program; these are
typically places where the desired type is explicit or can be derived by
propagation from explicit types (without type inference). Possible coercion
sites are:

- letstatements where an explicit type is given.For example,&mut 42is coerced to have type&i8in the following:#![allow(unused)]fn main() {let _: &i8 = &mut 42;}
letstatements where an explicit type is given.

For example,&mut 42is coerced to have type&i8in the following:

```rust
#![allow(unused)]
fn main() {
let _: &i8 = &mut 42;
}
```

```rust
#![allow(unused)]
fn main() {
let _: &i8 = &mut 42;
}
```

- staticandconstitem declarations (similar toletstatements).
- Arguments for function callsThe value being coerced is the actual parameter, and it is coerced to
the type of the formal parameter.For example,&mut 42is coerced to have type&i8in the following:fn bar(_: &i8) { }

fn main() {
    bar(&mut 42);
}For method calls, the receiver (selfparameter) type is coerced
differently, see the documentation onmethod-call expressionsfor details.
Arguments for function calls

The value being coerced is the actual parameter, and it is coerced to
the type of the formal parameter.

For example,&mut 42is coerced to have type&i8in the following:

```rust
fn bar(_: &i8) { }

fn main() {
    bar(&mut 42);
}
```

```rust
fn bar(_: &i8) { }

fn main() {
    bar(&mut 42);
}
```

For method calls, the receiver (selfparameter) type is coerced
differently, see the documentation onmethod-call expressionsfor details.

- Instantiations of struct, union, or enum variant fieldsFor example,&mut 42is coerced to have type&i8in the following:struct Foo<'a> { x: &'a i8 }

fn main() {
    Foo { x: &mut 42 };
}
Instantiations of struct, union, or enum variant fields

For example,&mut 42is coerced to have type&i8in the following:

```rust
struct Foo<'a> { x: &'a i8 }

fn main() {
    Foo { x: &mut 42 };
}
```

```rust
struct Foo<'a> { x: &'a i8 }

fn main() {
    Foo { x: &mut 42 };
}
```

- Function resultsâeither the final line of a block if it is not
semicolon-terminated or any expression in areturnstatementFor example,xis coerced to have type&dyn Displayin the following:#![allow(unused)]fn main() {use std::fmt::Display;
fn foo(x: &u32) -> &dyn Display {
    x
}}
Function resultsâeither the final line of a block if it is not
semicolon-terminated or any expression in areturnstatement

For example,xis coerced to have type&dyn Displayin the following:

```rust
#![allow(unused)]
fn main() {
use std::fmt::Display;
fn foo(x: &u32) -> &dyn Display {
    x
}
}
```

```rust
#![allow(unused)]
fn main() {
use std::fmt::Display;
fn foo(x: &u32) -> &dyn Display {
    x
}
}
```

If the expression in one of these coercion sites is a coercion-propagating
expression, then the relevant sub-expressions in that expression are also
coercion sites. Propagation recurses from these new coercion sites.
Propagating expressions and their relevant sub-expressions are:

- Array literals, where the array has type[U; n]. Each sub-expression in
the array literal is a coercion site for coercion to typeU.
- Array literals with repeating syntax, where the array has type[U; n]. The
repeated sub-expression is a coercion site for coercion to typeU.
- Tuples, where a tuple is a coercion site to type(U_0, U_1, ..., U_n).
Each sub-expression is a coercion site to the respective type, e.g. the
zeroth sub-expression is a coercion site to typeU_0.
- Parenthesized sub-expressions ((e)): if the expression has typeU, then
the sub-expression is a coercion site toU.
- Blocks: if a block has typeU, then the last expression in the block (if
it is not semicolon-terminated) is a coercion site toU. This includes
blocks which are part of control flow statements, such asif/else, if
the block has a known type.

## Coercion types

Coercion is allowed between the following types:

- TtoUifTis asubtypeofU(reflexive case)
- T_1toT_3whereT_1coerces toT_2andT_2coerces toT_3(transitive case)Note that this is not fully supported yet.
T_1toT_3whereT_1coerces toT_2andT_2coerces toT_3(transitive case)

Note that this is not fully supported yet.

- &mut Tto&T
- *mut Tto*const T
- &Tto*const T
- &mut Tto*mut T
- &Tor&mut Tto&UifTimplementsDeref<Target = U>. For example:use std::ops::Deref;

struct CharContainer {
    value: char,
}

impl Deref for CharContainer {
    type Target = char;

    fn deref<'a>(&'a self) -> &'a char {
        &self.value
    }
}

fn foo(arg: &char) {}

fn main() {
    let x = &mut CharContainer { value: 'y' };
    foo(x); //&mut CharContainer is coerced to &char.
}
&Tor&mut Tto&UifTimplementsDeref<Target = U>. For example:

```rust
use std::ops::Deref;

struct CharContainer {
    value: char,
}

impl Deref for CharContainer {
    type Target = char;

    fn deref<'a>(&'a self) -> &'a char {
        &self.value
    }
}

fn foo(arg: &char) {}

fn main() {
    let x = &mut CharContainer { value: 'y' };
    foo(x); //&mut CharContainer is coerced to &char.
}
```

```rust
use std::ops::Deref;

struct CharContainer {
    value: char,
}

impl Deref for CharContainer {
    type Target = char;

    fn deref<'a>(&'a self) -> &'a char {
        &self.value
    }
}

fn foo(arg: &char) {}

fn main() {
    let x = &mut CharContainer { value: 'y' };
    foo(x); //&mut CharContainer is coerced to &char.
}
```

- &mut Tto&mut UifTimplementsDerefMut<Target = U>.
- TyCtor(T) to TyCtor(U), where TyCtor(T) is one of&T&mut T*const T*mut TBox<T>and whereUcan be obtained fromTbyunsized coercion.
TyCtor(T) to TyCtor(U), where TyCtor(T) is one of

- &T
- &mut T
- *const T
- *mut T
- Box<T>
and whereUcan be obtained fromTbyunsized coercion.

- Function item types tofnpointers
- Non capturing closures tofnpointers
- !to anyT

### Unsized coercions

The following coercions are calledunsized coercions, since they
relate to converting types to unsized types, and are permitted in a few
cases where other coercions are not, as described above. They can still happen
anywhere else a coercion can occur.

Two traits,UnsizeandCoerceUnsized, are used
to assist in this process and expose it for library use. The following
coercions are built-ins and, ifTcan be coerced toUwith one of them, then
an implementation ofUnsize<U>forTwill be provided:

- [T; n]to[T].
- Ttodyn U, whenTimplementsU + Sized, andUisdyn compatible.
- dyn Ttodyn U, whenUis one ofTâssupertraits.This allows dropping auto traits, i.e.dyn T + Autotodyn Uis allowed.This allows adding auto traits if the principal trait has the auto trait as a super trait, i.e. giventrait T: U + Send {},dyn Ttodyn T + Sendor todyn U + Sendcoercions are allowed.
- This allows dropping auto traits, i.e.dyn T + Autotodyn Uis allowed.
- This allows adding auto traits if the principal trait has the auto trait as a super trait, i.e. giventrait T: U + Send {},dyn Ttodyn T + Sendor todyn U + Sendcoercions are allowed.
- Foo<..., T, ...>toFoo<..., U, ...>, when:Foois a struct.TimplementsUnsize<U>.The last field ofFoohas a type involvingT.If that field has typeBar<T>, thenBar<T>implementsUnsize<Bar<U>>.T is not part of the type of any other fields.
- Foois a struct.
- TimplementsUnsize<U>.
- The last field ofFoohas a type involvingT.
- If that field has typeBar<T>, thenBar<T>implementsUnsize<Bar<U>>.
- T is not part of the type of any other fields.
Additionally, a typeFoo<T>can implementCoerceUnsized<Foo<U>>whenTimplementsUnsize<U>orCoerceUnsized<Foo<U>>. This allows it to provide an
unsized coercion toFoo<U>.

> NoteWhile the definition of the unsized coercions and their implementation has been stabilized, the traits themselves are not yet stable and therefore canât be used directly in stable Rust.

Note

While the definition of the unsized coercions and their implementation has been stabilized, the traits themselves are not yet stable and therefore canât be used directly in stable Rust.

## Least upper bound coercions

In some contexts, the compiler must coerce together multiple types to try and
find the most general type. This is called a âLeast Upper Boundâ coercion.
LUB coercion is used and only used in the following situations:

- To find the common type for a series of if branches.
- To find the common type for a series of match arms.
- To find the common type for array elements.
- To find the type for the return type of a closure with multiple return statements.
- To check the type for the return type of a function with multiple return statements.
In each such case, there are a set of typesT0..Tnto be mutually coerced
to some target typeT_t, which is unknown to start.

Computing the LUB
coercion is done iteratively. The target typeT_tbegins as the typeT0.
For each new typeTi, we consider whether

- IfTican be coerced to the current target typeT_t, then no change is made.
- Otherwise, check whetherT_tcan be coerced toTi; if so, theT_tis
changed toTi. (This check is also conditioned on whether all of the source
expressions considered thus far have implicit coercions.)
- If not, try to compute a mutual supertype ofT_tandTi, which will become the new target type.

### Examples:

```rust
#![allow(unused)]
fn main() {
let (a, b, c) = (0, 1, 2);
// For if branches
let bar = if true {
    a
} else if false {
    b
} else {
    c
};

// For match arms
let baw = match 42 {
    0 => a,
    1 => b,
    _ => c,
};

// For array elements
let bax = [a, b, c];

// For closure with multiple return statements
let clo = || {
    if true {
        a
    } else if false {
        b
    } else {
        c
    }
};
let baz = clo();

// For type checking of function with multiple return statements
fn foo() -> i32 {
    let (a, b, c) = (0, 1, 2);
    match 42 {
        0 => a,
        1 => b,
        _ => c,
    }
}
}
```

```rust
#![allow(unused)]
fn main() {
let (a, b, c) = (0, 1, 2);
// For if branches
let bar = if true {
    a
} else if false {
    b
} else {
    c
};

// For match arms
let baw = match 42 {
    0 => a,
    1 => b,
    _ => c,
};

// For array elements
let bax = [a, b, c];

// For closure with multiple return statements
let clo = || {
    if true {
        a
    } else if false {
        b
    } else {
        c
    }
};
let baz = clo();

// For type checking of function with multiple return statements
fn foo() -> i32 {
    let (a, b, c) = (0, 1, 2);
    match 42 {
        0 => a,
        1 => b,
        _ => c,
    }
}
}
```

In these examples, types of theba*are found by LUB coercion. And the
compiler checks whether LUB coercion result ofa,b,cisi32in the
processing of the functionfoo.

### Caveat

This description is obviously informal. Making it more precise is expected to
proceed as part of a general effort to specify the Rust type checker more
precisely.
