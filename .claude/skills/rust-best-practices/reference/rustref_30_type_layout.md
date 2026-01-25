# Type Layout

Source: https://doc.rust-lang.org/reference/

# Type layout

The layout of a type is its size, alignment, and the relative offsets of its
fields. For enums, how the discriminant is laid out and interpreted is also part
of type layout.

Type layout can be changed with each compilation. Instead of trying to document
exactly what is done, we only document what is guaranteed today.

Note that even types with the same layout can still differ in how they are passed
across function boundaries. For function call ABI compatibility of types,
seehere.

## Size and alignment

All values have an alignment and size.

Thealignmentof a value specifies what addresses are valid to store the value
at. A value of alignmentnmust only be stored at an address that is a
multiple of n. For example, a value with an alignment of 2 must be stored at an
even address, while a value with an alignment of 1 can be stored at any address.
Alignment is measured in bytes, and must be at least 1, and always a power of 2.
The alignment of a value can be checked with thealign_of_valfunction.

Thesizeof a value is the offset in bytes between successive elements in an
array with that item type including alignment padding. The size of a value is
always a multiple of its alignment. Note that some types are zero-sized; 0 is
considered a multiple of any alignment (for example, on some platforms, the type[u16; 0]has size 0 and alignment 2). The size of a value can be checked with
thesize_of_valfunction.

Types where all values have the same size and alignment, and both are known at
compile time, implement theSizedtrait and can be checked with thesize_ofandalign_offunctions. Types that are notSizedare known
asdynamically sized types. Since all values of aSizedtype share the same
size and alignment, we refer to those shared values as the size of the type and
the alignment of the type respectively.

## Primitive data layout

The size of most primitives is given in this table.

usizeandisizehave a size big enough to contain every address on the
target platform. For example, on a 32 bit target, this is 4 bytes, and on a 64
bit target, this is 8 bytes.

The alignment of primitives is platform-specific.
In most cases, their alignment is equal to their size, but it may be less.
In particular,i128andu128are often aligned to 4 or 8 bytes even though
their size is 16, and on many 32-bit platforms,i64,u64, andf64are only
aligned to 4 bytes, not 8.

## Pointers and references layout

Pointers and references have the same layout. Mutability of the pointer or
reference does not change the layout.

Pointers to sized types have the same size and alignment asusize.

Pointers to unsized types are sized. The size and alignment is guaranteed to be
at least equal to the size and alignment of a pointer.

> NoteThough you should not rely on this, all pointers toDSTsare currently twice the size of the size ofusizeand have the same alignment.

Note

Though you should not rely on this, all pointers toDSTsare currently twice the size of the size ofusizeand have the same alignment.

## Array layout

An array of[T; N]has a size ofsize_of::<T>() * Nand the same alignment
ofT. Arrays are laid out so that the zero-basednthelement of the array
is offset from the start of the array byn * size_of::<T>()bytes.

## Slice layout

Slices have the same layout as the section of the array they slice.

> NoteThis is about the raw[T]type, not pointers (&[T],Box<[T]>, etc.) to slices.

Note

This is about the raw[T]type, not pointers (&[T],Box<[T]>, etc.) to slices.

## strLayout

String slices are a UTF-8 representation of characters that have the same layout as slices of type[u8]. A reference&strhas the same layout as a reference&[u8].

## Tuple layout

Tuples are laid out according to theRustrepresentation.

The exception to this is the unit tuple (()), which is guaranteed as a
zero-sized type to have a size of 0 and an alignment of 1.

## Trait object layout

Trait objects have the same layout as the value the trait object is of.

> NoteThis is about the raw trait object types, not pointers (&dyn Trait,Box<dyn Trait>, etc.) to trait objects.

Note

This is about the raw trait object types, not pointers (&dyn Trait,Box<dyn Trait>, etc.) to trait objects.

## Closure layout

Closures have no layout guarantees.

## Representations

All user-defined composite types (structs,enums, andunions) have arepresentationthat specifies what the layout is for the type.

The possible representations for a type are:

- Rust(default)
- C
- Theprimitive representations
- transparent
The representation of a type can be changed by applying thereprattribute
to it. The following example shows a struct with aCrepresentation.

```rust
#![allow(unused)]
fn main() {
#[repr(C)]
struct ThreeInts {
    first: i16,
    second: i8,
    third: i32
}
}
```

```rust
#![allow(unused)]
fn main() {
#[repr(C)]
struct ThreeInts {
    first: i16,
    second: i8,
    third: i32
}
}
```

The alignment may be raised or lowered with thealignandpackedmodifiers
respectively. They alter the representation specified in the attribute.
If no representation is specified, the default one is altered.

```rust
#![allow(unused)]
fn main() {
// Default representation, alignment lowered to 2.
#[repr(packed(2))]
struct PackedStruct {
    first: i16,
    second: i8,
    third: i32
}

// C representation, alignment raised to 8
#[repr(C, align(8))]
struct AlignedStruct {
    first: i16,
    second: i8,
    third: i32
}
}
```

```rust
#![allow(unused)]
fn main() {
// Default representation, alignment lowered to 2.
#[repr(packed(2))]
struct PackedStruct {
    first: i16,
    second: i8,
    third: i32
}

// C representation, alignment raised to 8
#[repr(C, align(8))]
struct AlignedStruct {
    first: i16,
    second: i8,
    third: i32
}
}
```

> NoteAs a consequence of the representation being an attribute on the item, the representation does not depend on generic parameters. Any two types with the same name have the same representation. For example,Foo<Bar>andFoo<Baz>both have the same representation.

Note

As a consequence of the representation being an attribute on the item, the representation does not depend on generic parameters. Any two types with the same name have the same representation. For example,Foo<Bar>andFoo<Baz>both have the same representation.

The representation of a type can change the padding between fields, but does
not change the layout of the fields themselves. For example, a struct with aCrepresentation that contains a structInnerwith theRustrepresentation will not change the layout ofInner.

### TheRustrepresentation

TheRustrepresentation is the default representation for nominal types
without areprattribute. Using this representation explicitly through areprattribute is guaranteed to be the same as omitting the attribute
entirely.

The only data layout guarantees made by this representation are those required
for soundness. They are:

- The fields are properly aligned.
- The fields do not overlap.
- The alignment of the type is at least the maximum alignment of its fields.
Formally, the first guarantee means that the offset of any field is divisible by
that fieldâs alignment.

The second guarantee means that the fields can be
ordered such that the offset plus the size of any field is less than or equal to
the offset of the next field in the ordering. The ordering does not have to be
the same as the order in which the fields are specified in the declaration of
the type.

Be aware that the second guarantee does not imply that the fields have distinct
addresses: zero-sized types may have the same address as other fields in the
same struct.

There are no other guarantees of data layout made by this representation.

### TheCrepresentation

TheCrepresentation is designed for dual purposes. One purpose is for
creating types that are interoperable with the C Language. The second purpose is
to create types that you can soundly perform operations on that rely on data
layout such as reinterpreting values as a different type.

Because of this dual purpose, it is possible to create types that are not useful
for interfacing with the C programming language.

This representation can be applied to structs, unions, and enums. The exception
iszero-variant enumsfor which theCrepresentation is an error.

#### #[repr(C)]Structs

The alignment of the struct is the alignment of the most-aligned field in it.

The size and offset of fields is determined by the following algorithm.

Start with a current offset of 0 bytes.

For each field in declaration order in the struct, first determine the size and
alignment of the field. If the current offset is not a multiple of the fieldâs
alignment, then add padding bytes to the current offset until it is a multiple
of the fieldâs alignment. The offset for the field is what the current offset
is now. Then increase the current offset by the size of the field.

Finally, the size of the struct is the current offset rounded up to the nearest
multiple of the structâs alignment.

Here is this algorithm described in pseudocode.

```rust
/// Returns the amount of padding needed after `offset` to ensure that the
/// following address will be aligned to `alignment`.
fn padding_needed_for(offset: usize, alignment: usize) -> usize {
    let misalignment = offset % alignment;
    if misalignment > 0 {
        // round up to next multiple of `alignment`
        alignment - misalignment
    } else {
        // already a multiple of `alignment`
        0
    }
}

struct.alignment = struct.fields().map(|field| field.alignment).max();

let current_offset = 0;

for field in struct.fields_in_declaration_order() {
    // Increase the current offset so that it's a multiple of the alignment
    // of this field. For the first field, this will always be zero.
    // The skipped bytes are called padding bytes.
    current_offset += padding_needed_for(current_offset, field.alignment);

    struct[field].offset = current_offset;

    current_offset += field.size;
}

struct.size = current_offset + padding_needed_for(current_offset, struct.alignment);
```

> WarningThis pseudocode uses a naive algorithm that ignores overflow issues for the sake of clarity. To perform memory layout computations in actual code, useLayout.

Warning

This pseudocode uses a naive algorithm that ignores overflow issues for the sake of clarity. To perform memory layout computations in actual code, useLayout.

> NoteThis algorithm can produce zero-sized structs. In C, an empty struct declaration likestruct Foo { }is illegal. However, both gcc and clang support options to enable such structs, and assign them size zero. C++, in contrast, gives empty structs a size of 1, unless they are inherited from or they are fields that have the[[no_unique_address]]attribute, in which case they do not increase the overall size of the struct.

Note

This algorithm can produce zero-sized structs. In C, an empty struct declaration likestruct Foo { }is illegal. However, both gcc and clang support options to enable such structs, and assign them size zero. C++, in contrast, gives empty structs a size of 1, unless they are inherited from or they are fields that have the[[no_unique_address]]attribute, in which case they do not increase the overall size of the struct.

#### #[repr(C)]Unions

A union declared with#[repr(C)]will have the same size and alignment as an
equivalent C union declaration in the C language for the target platform.

The union will have a size of the maximum size of all of its fields rounded to
its alignment, and an alignment of the maximum alignment of all of its fields.
These maximums may come from different fields.

```rust
#![allow(unused)]
fn main() {
#[repr(C)]
union Union {
    f1: u16,
    f2: [u8; 4],
}

assert_eq!(std::mem::size_of::<Union>(), 4);  // From f2
assert_eq!(std::mem::align_of::<Union>(), 2); // From f1

#[repr(C)]
union SizeRoundedUp {
   a: u32,
   b: [u16; 3],
}

assert_eq!(std::mem::size_of::<SizeRoundedUp>(), 8);  // Size of 6 from b,
                                                      // rounded up to 8 from
                                                      // alignment of a.
assert_eq!(std::mem::align_of::<SizeRoundedUp>(), 4); // From a
}
```

```rust
#![allow(unused)]
fn main() {
#[repr(C)]
union Union {
    f1: u16,
    f2: [u8; 4],
}

assert_eq!(std::mem::size_of::<Union>(), 4);  // From f2
assert_eq!(std::mem::align_of::<Union>(), 2); // From f1

#[repr(C)]
union SizeRoundedUp {
   a: u32,
   b: [u16; 3],
}

assert_eq!(std::mem::size_of::<SizeRoundedUp>(), 8);  // Size of 6 from b,
                                                      // rounded up to 8 from
                                                      // alignment of a.
assert_eq!(std::mem::align_of::<SizeRoundedUp>(), 4); // From a
}
```

#### #[repr(C)]Field-less Enums

Forfield-less enums, theCrepresentation has the size and alignment of
the defaultenumsize and alignment for the target platformâs C ABI.

> NoteThe enum representation in C is implementation defined, so this is really a âbest guessâ. In particular, this may be incorrect when the C code of interest is compiled with certain flags.

Note

The enum representation in C is implementation defined, so this is really a âbest guessâ. In particular, this may be incorrect when the C code of interest is compiled with certain flags.

> WarningThere are crucial differences between anenumin the C language and Rustâsfield-less enumswith this representation. Anenumin C is mostly atypedefplus some named constants; in other words, an object of anenumtype can hold any integer value. For example, this is often used for bitflags inC. In contrast, Rustâsfield-less enumscan only legally hold the discriminant values, everything else isundefined behavior. Therefore, using a field-less enum in FFI to model a Cenumis often wrong.

Warning

There are crucial differences between anenumin the C language and Rustâsfield-less enumswith this representation. Anenumin C is mostly atypedefplus some named constants; in other words, an object of anenumtype can hold any integer value. For example, this is often used for bitflags inC. In contrast, Rustâsfield-less enumscan only legally hold the discriminant values, everything else isundefined behavior. Therefore, using a field-less enum in FFI to model a Cenumis often wrong.

#### #[repr(C)]Enums With Fields

The representation of arepr(C)enum with fields is arepr(C)struct with
two fields, also called a âtagged unionâ in C:

- arepr(C)version of the enum with all fields removed (âthe tagâ)
- arepr(C)union ofrepr(C)structs for the fields of each variant that had
them (âthe payloadâ)

> NoteDue to the representation ofrepr(C)structs and unions, if a variant has a single field there is no difference between putting that field directly in the union or wrapping it in a struct; any system which wishes to manipulate such anenumâs representation may therefore use whichever form is more convenient or consistent for them.

Note

Due to the representation ofrepr(C)structs and unions, if a variant has a single field there is no difference between putting that field directly in the union or wrapping it in a struct; any system which wishes to manipulate such anenumâs representation may therefore use whichever form is more convenient or consistent for them.

```rust
#![allow(unused)]
fn main() {
// This Enum has the same representation as ...
#[repr(C)]
enum MyEnum {
    A(u32),
    B(f32, u64),
    C { x: u32, y: u8 },
    D,
 }

// ... this struct.
#[repr(C)]
struct MyEnumRepr {
    tag: MyEnumDiscriminant,
    payload: MyEnumFields,
}

// This is the discriminant enum.
#[repr(C)]
enum MyEnumDiscriminant { A, B, C, D }

// This is the variant union.
#[repr(C)]
union MyEnumFields {
    A: MyAFields,
    B: MyBFields,
    C: MyCFields,
    D: MyDFields,
}

#[repr(C)]
#[derive(Copy, Clone)]
struct MyAFields(u32);

#[repr(C)]
#[derive(Copy, Clone)]
struct MyBFields(f32, u64);

#[repr(C)]
#[derive(Copy, Clone)]
struct MyCFields { x: u32, y: u8 }

// This struct could be omitted (it is a zero-sized type), and it must be in
// C/C++ headers.
#[repr(C)]
#[derive(Copy, Clone)]
struct MyDFields;
}
```

```rust
#![allow(unused)]
fn main() {
// This Enum has the same representation as ...
#[repr(C)]
enum MyEnum {
    A(u32),
    B(f32, u64),
    C { x: u32, y: u8 },
    D,
 }

// ... this struct.
#[repr(C)]
struct MyEnumRepr {
    tag: MyEnumDiscriminant,
    payload: MyEnumFields,
}

// This is the discriminant enum.
#[repr(C)]
enum MyEnumDiscriminant { A, B, C, D }

// This is the variant union.
#[repr(C)]
union MyEnumFields {
    A: MyAFields,
    B: MyBFields,
    C: MyCFields,
    D: MyDFields,
}

#[repr(C)]
#[derive(Copy, Clone)]
struct MyAFields(u32);

#[repr(C)]
#[derive(Copy, Clone)]
struct MyBFields(f32, u64);

#[repr(C)]
#[derive(Copy, Clone)]
struct MyCFields { x: u32, y: u8 }

// This struct could be omitted (it is a zero-sized type), and it must be in
// C/C++ headers.
#[repr(C)]
#[derive(Copy, Clone)]
struct MyDFields;
}
```

### Primitive representations

Theprimitive representationsare the representations with the same names as
the primitive integer types. That is:u8,u16,u32,u64,u128,usize,i8,i16,i32,i64,i128, andisize.

Primitive representations can only be applied to enumerations and have
different behavior whether the enum has fields or no fields. It is an error
forzero-variant enumsto have a primitive representation. Combining
two primitive representations together is an error.

#### Primitive representation of field-less enums

Forfield-less enums, primitive representations set the size and alignment to
be the same as the primitive type of the same name. For example, a field-less
enum with au8representation can only have discriminants between 0 and 255
inclusive.

#### Primitive representation of enums with fields

The representation of a primitive representation enum is arepr(C)union ofrepr(C)structs for each variant with a field. The first field of each struct
in the union is the primitive representation version of the enum with all fields
removed (âthe tagâ) and the remaining fields are the fields of that variant.

> NoteThis representation is unchanged if the tag is given its own member in the union, should that make manipulation more clear for you (although to follow the C++ standard the tag member should be wrapped in astruct).

Note

This representation is unchanged if the tag is given its own member in the union, should that make manipulation more clear for you (although to follow the C++ standard the tag member should be wrapped in astruct).

```rust
#![allow(unused)]
fn main() {
// This enum has the same representation as ...
#[repr(u8)]
enum MyEnum {
    A(u32),
    B(f32, u64),
    C { x: u32, y: u8 },
    D,
 }

// ... this union.
#[repr(C)]
union MyEnumRepr {
    A: MyVariantA,
    B: MyVariantB,
    C: MyVariantC,
    D: MyVariantD,
}

// This is the discriminant enum.
#[repr(u8)]
#[derive(Copy, Clone)]
enum MyEnumDiscriminant { A, B, C, D }

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantA(MyEnumDiscriminant, u32);

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantB(MyEnumDiscriminant, f32, u64);

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantC { tag: MyEnumDiscriminant, x: u32, y: u8 }

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantD(MyEnumDiscriminant);
}
```

```rust
#![allow(unused)]
fn main() {
// This enum has the same representation as ...
#[repr(u8)]
enum MyEnum {
    A(u32),
    B(f32, u64),
    C { x: u32, y: u8 },
    D,
 }

// ... this union.
#[repr(C)]
union MyEnumRepr {
    A: MyVariantA,
    B: MyVariantB,
    C: MyVariantC,
    D: MyVariantD,
}

// This is the discriminant enum.
#[repr(u8)]
#[derive(Copy, Clone)]
enum MyEnumDiscriminant { A, B, C, D }

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantA(MyEnumDiscriminant, u32);

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantB(MyEnumDiscriminant, f32, u64);

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantC { tag: MyEnumDiscriminant, x: u32, y: u8 }

#[repr(C)]
#[derive(Clone, Copy)]
struct MyVariantD(MyEnumDiscriminant);
}
```

#### Combining primitive representations of enums with fields and#[repr(C)]

For enums with fields, it is also possible to combinerepr(C)and a
primitive representation (e.g.,repr(C, u8)). This modifies therepr(C)by
changing the representation of the discriminant enum to the chosen primitive
instead. So, if you chose theu8representation, then the discriminant enum
would have a size and alignment of 1 byte.

The discriminant enum from the exampleearlierthen becomes:

```rust
#![allow(unused)]
fn main() {
#[repr(C, u8)] // `u8` was added
enum MyEnum {
    A(u32),
    B(f32, u64),
    C { x: u32, y: u8 },
    D,
 }

// ...

#[repr(u8)] // So `u8` is used here instead of `C`
enum MyEnumDiscriminant { A, B, C, D }

// ...
}
```

```rust
#![allow(unused)]
fn main() {
#[repr(C, u8)] // `u8` was added
enum MyEnum {
    A(u32),
    B(f32, u64),
    C { x: u32, y: u8 },
    D,
 }

// ...

#[repr(u8)] // So `u8` is used here instead of `C`
enum MyEnumDiscriminant { A, B, C, D }

// ...
}
```

For example, with arepr(C, u8)enum it is not possible to have 257 unique
discriminants (âtagsâ) whereas the same enum with only arepr(C)attribute
will compile without any problems.

Using a primitive representation in addition torepr(C)can change the size of
an enum from therepr(C)form:

```rust
#![allow(unused)]
fn main() {
#[repr(C)]
enum EnumC {
    Variant0(u8),
    Variant1,
}

#[repr(C, u8)]
enum Enum8 {
    Variant0(u8),
    Variant1,
}

#[repr(C, u16)]
enum Enum16 {
    Variant0(u8),
    Variant1,
}

// The size of the C representation is platform dependent
assert_eq!(std::mem::size_of::<EnumC>(), 8);
// One byte for the discriminant and one byte for the value in Enum8::Variant0
assert_eq!(std::mem::size_of::<Enum8>(), 2);
// Two bytes for the discriminant and one byte for the value in Enum16::Variant0
// plus one byte of padding.
assert_eq!(std::mem::size_of::<Enum16>(), 4);
}
```

```rust
#![allow(unused)]
fn main() {
#[repr(C)]
enum EnumC {
    Variant0(u8),
    Variant1,
}

#[repr(C, u8)]
enum Enum8 {
    Variant0(u8),
    Variant1,
}

#[repr(C, u16)]
enum Enum16 {
    Variant0(u8),
    Variant1,
}

// The size of the C representation is platform dependent
assert_eq!(std::mem::size_of::<EnumC>(), 8);
// One byte for the discriminant and one byte for the value in Enum8::Variant0
assert_eq!(std::mem::size_of::<Enum8>(), 2);
// Two bytes for the discriminant and one byte for the value in Enum16::Variant0
// plus one byte of padding.
assert_eq!(std::mem::size_of::<Enum16>(), 4);
}
```

### The alignment modifiers

Thealignandpackedmodifiers can be used to respectively raise or lower
the alignment ofstructs andunions.packedmay also alter the padding
between fields (although it will not alter the padding inside of any field).
On their own,alignandpackeddo not provide guarantees about the order
of fields in the layout of a struct or the layout of an enum variant, although
they may be combined with representations (such asC) which do provide such
guarantees.

The alignment is specified as an integer parameter in the form of#[repr(align(x))]or#[repr(packed(x))]. The alignment value must be a
power of two from 1 up to 229. Forpacked, if no value is given,
as in#[repr(packed)], then the value is 1.

Foralign, if the specified alignment is less than the alignment of the type
without thealignmodifier, then the alignment is unaffected.

Forpacked, if the specified alignment is greater than the typeâs alignment
without thepackedmodifier, then the alignment and layout is unaffected.

The alignments of each field, for the purpose of positioning fields, is the
smaller of the specified alignment and the alignment of the fieldâs type.

Inter-field padding is guaranteed to be the minimum required in order to
satisfy each fieldâs (possibly altered) alignment (although note that, on its
own,packeddoes not provide any guarantee about field ordering). An
important consequence of these rules is that a type with#[repr(packed(1))](or#[repr(packed)]) will have no inter-field padding.

Thealignandpackedmodifiers cannot be applied on the same type and apackedtype cannot transitively contain anotheraligned type.alignandpackedmay only be applied to theRustandCrepresentations.

Thealignmodifier can also be applied on anenum.
When it is, the effect on theenumâs alignment is the same as if theenumwas wrapped in a newtypestructwith the samealignmodifier.

> NoteReferences to unaligned fields are not allowed because it isundefined behavior. When fields are unaligned due to an alignment modifier, consider the following options for using references and dereferences:#![allow(unused)]fn main() {#[repr(packed)]
> struct Packed {
>     f1: u8,
>     f2: u16,
> }
> let mut e = Packed { f1: 1, f2: 2 };
> // Instead of creating a reference to a field, copy the value to a local variable.
> let x = e.f2;
> // Or in situations like `println!` which creates a reference, use braces
> // to change it to a copy of the value.
> println!("{}", {e.f2});
> // Or if you need a pointer, use the unaligned methods for reading and writing
> // instead of dereferencing the pointer directly.
> let ptr: *const u16 = &raw const e.f2;
> let value = unsafe { ptr.read_unaligned() };
> let mut_ptr: *mut u16 = &raw mut e.f2;
> unsafe { mut_ptr.write_unaligned(3) }}

Note

References to unaligned fields are not allowed because it isundefined behavior. When fields are unaligned due to an alignment modifier, consider the following options for using references and dereferences:

```rust
#![allow(unused)]
fn main() {
#[repr(packed)]
struct Packed {
    f1: u8,
    f2: u16,
}
let mut e = Packed { f1: 1, f2: 2 };
// Instead of creating a reference to a field, copy the value to a local variable.
let x = e.f2;
// Or in situations like `println!` which creates a reference, use braces
// to change it to a copy of the value.
println!("{}", {e.f2});
// Or if you need a pointer, use the unaligned methods for reading and writing
// instead of dereferencing the pointer directly.
let ptr: *const u16 = &raw const e.f2;
let value = unsafe { ptr.read_unaligned() };
let mut_ptr: *mut u16 = &raw mut e.f2;
unsafe { mut_ptr.write_unaligned(3) }
}
```

```rust
#![allow(unused)]
fn main() {
#[repr(packed)]
struct Packed {
    f1: u8,
    f2: u16,
}
let mut e = Packed { f1: 1, f2: 2 };
// Instead of creating a reference to a field, copy the value to a local variable.
let x = e.f2;
// Or in situations like `println!` which creates a reference, use braces
// to change it to a copy of the value.
println!("{}", {e.f2});
// Or if you need a pointer, use the unaligned methods for reading and writing
// instead of dereferencing the pointer directly.
let ptr: *const u16 = &raw const e.f2;
let value = unsafe { ptr.read_unaligned() };
let mut_ptr: *mut u16 = &raw mut e.f2;
unsafe { mut_ptr.write_unaligned(3) }
}
```

### Thetransparentrepresentation

Thetransparentrepresentation can only be used on astructor anenumwith a single variant that has:

- any number of fields with size 0 and alignment 1 (e.g.PhantomData<T>), and
- at most one other field.
Structs and enums with this representation have the same layout and ABI
as the only non-size 0 non-alignment 1 field, if present, or unit otherwise.

This is different than theCrepresentation because
a struct with theCrepresentation will always have the ABI of aCstructwhile, for example, a struct with thetransparentrepresentation with a
primitive field will have the ABI of the primitive field.

Because this representation delegates type layout to another type, it cannot be
used with any other representation.
