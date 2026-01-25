# Dependability

Source: https://rust-lang.github.io/api-guidelines/

## Functions validate their arguments (C-VALIDATE)

Rust APIs donotgenerally follow therobustness principle: "be conservative
in what you send; be liberal in what you accept".

Instead, Rust code shouldenforcethe validity of input whenever practical.

Enforcement can be achieved through the following mechanisms (listed in order of
preference).

### Static enforcement

Choose an argument type that rules out bad inputs.

For example, prefer

```rust

#![allow(unused)]
fn main() {
fn foo(a: Ascii) { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
fn foo(a: Ascii) { /* ... */ }
}
```

over

```rust

#![allow(unused)]
fn main() {
fn foo(a: u8) { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
fn foo(a: u8) { /* ... */ }
}
```

whereAsciiis awrapperaroundu8that guarantees the highest bit is
zero; see newtype patterns (C-NEWTYPE) for more details on creating typesafe
wrappers.

Static enforcement usually comes at little run-time cost: it pushes the costs to
the boundaries (e.g. when au8is first converted into anAscii). It also
catches bugs early, during compilation, rather than through run-time failures.

On the other hand, some properties are difficult or impossible to express using
types.

### Dynamic enforcement

Validate the input as it is processed (or ahead of time, if necessary). Dynamic
checking is often easier to implement than static checking, but has several
downsides:

- Runtime overhead (unless checking can be done as part of processing the
input).
- Delayed detection of bugs.
- Introduces failure cases, either viapanic!orResult/Optiontypes,
which must then be dealt with by client code.

#### Dynamic enforcement withdebug_assert!

Same as dynamic enforcement, but with the possibility of easily turning off
expensive checks for production builds.

#### Dynamic enforcement with opt-out

Same as dynamic enforcement, but adds sibling functions that opt out of the
checking.

The convention is to mark these opt-out functions with a suffix like_uncheckedor by placing them in arawsubmodule.

The unchecked functions can be used judiciously in cases where (1) performance
dictates avoiding checks and (2) the client is otherwise confident that the
inputs are valid.

## Destructors never fail (C-DTOR-FAIL)

Destructors are executed while panicking, and in that context a failing
destructor causes the program to abort.

Instead of failing in a destructor, provide a separate method for checking for
clean teardown, e.g. aclosemethod, that returns aResultto signal
problems. If thatclosemethod is not called, theDropimplementation
should do the teardown and ignore or log/trace any errors it produces.

## Destructors that may block have alternatives (C-DTOR-BLOCK)

Similarly, destructors should not invoke blocking operations, which can make
debugging much more difficult. Again, consider providing a separate method for
preparing for an infallible, nonblocking teardown.
