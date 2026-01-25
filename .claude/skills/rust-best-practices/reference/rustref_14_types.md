# Types

Source: https://doc.rust-lang.org/reference/

Every variable, item, and value in a Rust program has a type. Thetypeof avaluedefines the interpretation of the memory holding it and the operations
that may be performed on the value.

Built-in types are tightly integrated into the language, in nontrivial ways
that are not possible to emulate in user-defined types.

User-defined types have limited capabilities.

The list of types is:

- Primitive types:BooleanâboolNumericâ integer and floatTextualâcharandstrNeverâ!â a type with no values
- Booleanâbool
- Numericâ integer and float
- Textualâcharandstr
- Neverâ!â a type with no values
- Sequence types:TupleArraySlice
- Tuple
- Array
- Slice
- User-defined types:StructEnumUnion
- Struct
- Enum
- Union
- Function types:FunctionsClosures
- Functions
- Closures
- Pointer types:ReferencesRaw pointersFunction pointers
- References
- Raw pointers
- Function pointers
- Trait types:Trait objectsImpl trait
- Trait objects
- Impl trait

## Type expressions

SyntaxTypeâÂ Â Â Â Â ÂTypeNoBoundsÂ Â Â Â |ImplTraitTypeÂ Â Â Â |TraitObjectType

TypeNoBoundsâÂ Â Â Â Â ÂParenthesizedTypeÂ Â Â Â |ImplTraitTypeOneBoundÂ Â Â Â |TraitObjectTypeOneBoundÂ Â Â Â |TypePathÂ Â Â Â |TupleTypeÂ Â Â Â |NeverTypeÂ Â Â Â |RawPointerTypeÂ Â Â Â |ReferenceTypeÂ Â Â Â |ArrayTypeÂ Â Â Â |SliceTypeÂ Â Â Â |InferredTypeÂ Â Â Â |QualifiedPathInTypeÂ Â Â Â |BareFunctionTypeÂ Â Â Â |MacroInvocation

Show Railroad

Atype expressionas defined in theTypegrammar rule above is the syntax
for referring to a type. It may refer to:

- Sequence types (tuple,array,slice).
- Type pathswhich can reference:Primitive types (boolean,numeric,textual).Paths to anitem(struct,enum,union,type alias,trait).SelfpathwhereSelfis the implementing type.Generictype parameters.
- Primitive types (boolean,numeric,textual).
- Paths to anitem(struct,enum,union,type alias,trait).
- SelfpathwhereSelfis the implementing type.
- Generictype parameters.
- Pointer types (reference,raw pointer,function pointer).
- Theinferred typewhich asks the compiler to determine the type.
- Parentheseswhich are used for disambiguation.
- Trait types:Trait objectsandimpl trait.
- Thenevertype.
- Macroswhich expand to a type expression.

### Parenthesized types

SyntaxParenthesizedTypeâ(Type)

Show Railroad

In some situations the combination of types may be ambiguous. Use parentheses
around a type to avoid ambiguity. For example, the+operator fortype
boundarieswithin areference typeis unclear where the
boundary applies, so the use of parentheses is required. Grammar rules that
require this disambiguation use theTypeNoBoundsrule instead ofType.

```rust
#![allow(unused)]
fn main() {
use std::any::Any;
type T<'a> = &'a (dyn Any + Send);
}
```

```rust
#![allow(unused)]
fn main() {
use std::any::Any;
type T<'a> = &'a (dyn Any + Send);
}
```

## Recursive types

Nominal types âstructs,enumerations, andunionsâ may be
recursive. That is, eachenumvariant orstructorunionfield may
refer, directly or indirectly, to the enclosingenumorstructtype
itself.

Such recursion has restrictions:

- Recursive types must include a nominal type in the recursion (not meretype
aliases, or other structural types such asarraysortuples). Sotype Rec = &'static [Rec]is not allowed.
- The size of a recursive type must be finite; in other words the recursive
fields of the type must bepointer types.
An example of arecursivetype and its use:

```rust
#![allow(unused)]
fn main() {
enum List<T> {
    Nil,
    Cons(T, Box<List<T>>)
}

let a: List<i32> = List::Cons(7, Box::new(List::Cons(13, Box::new(List::Nil))));
}
```

```rust
#![allow(unused)]
fn main() {
enum List<T> {
    Nil,
    Cons(T, Box<List<T>>)
}

let a: List<i32> = List::Cons(7, Box::new(List::Cons(13, Box::new(List::Nil))));
}
```
