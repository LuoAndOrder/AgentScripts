# Undefined Behavior

Source: https://doc.rust-lang.org/reference/

# Behavior considered undefined

Rust code is incorrect if it exhibits any of the behaviors in the following
list. This includes code withinunsafeblocks andunsafefunctions.unsafeonly means that avoiding undefined behavior is on the programmer; it
does not change anything about the fact that Rust programs must never cause
undefined behavior.

It is the programmerâs responsibility when writingunsafecode to ensure that
any safe code interacting with theunsafecode cannot trigger these
behaviors.unsafecode that satisfies this property for any safe client is
calledsound; ifunsafecode can be misused by safe code to exhibit
undefined behavior, it isunsound.

> WarningThe following list is not exhaustive; it may grow or shrink. There is no formal model of Rustâs semantics for what is and is not allowed in unsafe code, so there may be more behavior considered unsafe. We also reserve the right to make some of the behavior in that list defined in the future. In other words, this list does not say that anything willdefinitelyalways be undefined in all future Rust version (but we might make such commitments for some list items in the future).Please read theRustonomiconbefore writing unsafe code.

Warning

The following list is not exhaustive; it may grow or shrink. There is no formal model of Rustâs semantics for what is and is not allowed in unsafe code, so there may be more behavior considered unsafe. We also reserve the right to make some of the behavior in that list defined in the future. In other words, this list does not say that anything willdefinitelyalways be undefined in all future Rust version (but we might make such commitments for some list items in the future).

Please read theRustonomiconbefore writing unsafe code.

- Data races.
- Accessing (loading from or storing to) a place that isdanglingorbased on
a misaligned pointer.
- Performing a place projection that violates the requirements ofin-bounds
pointer arithmetic. A place projection is afield
expression, atuple index expression, or anarray/slice index expression.
Breaking the pointer aliasing rules. The exact aliasing rules are not determined yet, but here is an outline of the general principles:&Tmust point to memory that is not mutated while they are live (except for data inside anUnsafeCell<U>),
and&mut Tmust point to memory that is not read or written by any pointer not derived from the reference and that no other reference points to while they are live.Box<T>is treated similar to&'static mut Tfor the purpose of these rules.
The exact liveness duration is not specified, but some bounds exist:

- For references, the liveness duration is upper-bounded by the syntactic
lifetime assigned by the borrow checker; it cannot be live anylongerthan that lifetime.
- Each time a reference or box is dereferenced or reborrowed, it is considered live.
- Each time a reference or box is passed to or returned from a function, it is considered live.
- When a reference (but not aBox!) is passed to a function, it is live at least as long as that function call, again except if the&Tcontains anUnsafeCell<U>.
All this also applies when values of these types are passed in a (nested) field of a compound type, but not behind pointer indirections.

Mutating immutable bytes.
All bytes reachable through aconst-promotedexpression are immutable, as well as bytes reachable through borrows instaticandconstinitializers that have beenlifetime-extendedto'static.
The bytes owned by an immutable binding or immutablestaticare immutable, unless those bytes are part of anUnsafeCell<U>.

Moreover, the bytespointed toby a shared reference, including transitively through other references (both shared and mutable) andBoxes, are immutable; transitivity includes those references stored in fields of compound types.

A mutation is any write of more than 0 bytes which overlaps with any of the relevant bytes (even if that write does not change the memory contents).

- Invoking undefined behavior via compiler intrinsics.
- Executing code compiled with platform features that the current platform
does not support (seetarget_feature),exceptif the platform explicitly documents this to be safe.
- Calling a function with the wrongcall ABI, or unwinding past a stack frame that does not allow unwinding (e.g. by calling a"C-unwind"function imported or transmuted as a"C"function or function pointer).
- Producing aninvalid value. âProducingâ a
value happens any time a value is assigned to or read from a place, passed to
a function/primitive operation or returned from a function/primitive
operation.
- Incorrect use of inline assembly. For more details, refer to therulesto
follow when writing code that uses inline assembly.
- Inconst context: transmuting or otherwise
reinterpreting a pointer (reference, raw pointer, or function pointer) into
some allocation as a non-pointer type (such as integers).
âReinterpretingâ refers to loading the pointer value at integer type without a
cast, e.g. by doing raw pointer casts or using a union.
- Violating assumptions of the Rust runtime. Most assumptions of the Rust runtime are currently not explicitly documented.For assumptions specifically related to unwinding, see thepanic documentation.The runtime assumes that a Rust stack frame is not deallocated without executing destructors for local variables owned by the stack frame. This assumption can be violated by C functions likelongjmp.
- For assumptions specifically related to unwinding, see thepanic documentation.
- The runtime assumes that a Rust stack frame is not deallocated without executing destructors for local variables owned by the stack frame. This assumption can be violated by C functions likelongjmp.

> NoteUndefined behavior affects the entire program. For example, calling a function in C that exhibits undefined behavior of C means your entire program contains undefined behaviour that can also affect the Rust code. And vice versa, undefined behavior in Rust can cause adverse affects on code executed by any FFI calls to other languages.

Note

Undefined behavior affects the entire program. For example, calling a function in C that exhibits undefined behavior of C means your entire program contains undefined behaviour that can also affect the Rust code. And vice versa, undefined behavior in Rust can cause adverse affects on code executed by any FFI calls to other languages.

## Pointed-to bytes

The span of bytes a pointer or reference âpoints toâ is determined by the pointer value and the size of the pointee type (usingsize_of_val).

## Places based on misaligned pointers

A place is said to be âbased on a misaligned pointerâ if the last*projection
during place computation was performed on a pointer that was not aligned for its
type. (If there is no*projection in the place expression, then this is
accessing the field of a local orstaticand rustc will guarantee proper alignment. If
there are multiple*projection, then each of them incurs a load of the
pointer-to-be-dereferenced itself from memory, and each of these loads is
subject to the alignment constraint. Note that some*projections can be
omitted in surface Rust syntax due to automatic dereferencing; we are
considering the fully expanded place expression here.)

For instance, ifptrhas type*const SwhereShas an alignment of 8, thenptrmust be 8-aligned or else(*ptr).fis âbased on an misaligned pointerâ.
This is true even if the type of the fieldfisu8(i.e., a type with
alignment 1). In other words, the alignment requirement derives from the type of
the pointer that was dereferenced,notthe type of the field that is being
accessed.

Note that a place based on a misaligned pointer only leads to Undefined Behavior
when it is loaded from or stored to.

&raw const/&raw muton such a place is allowed.

&/&muton a place requires the alignment of the field type (or
else the program would be âproducing an invalid valueâ), which generally is a
less restrictive requirement than being based on an aligned pointer.

Taking a reference will lead to a compiler error in cases where the field type might be
more aligned than the type that contains it, i.e.,repr(packed). This means
that being based on an aligned pointer is always sufficient to ensure that the
new reference is aligned, but it is not always necessary.

## Dangling pointers

A reference/pointer is âdanglingâ if not all of the bytes itpoints toare part of the same live allocation (so in particular they all have to be
part ofsomeallocation).

If the size is 0, then the pointer is trivially never âdanglingâ
(even if it is a null pointer).

Note that dynamically sized types (such as slices and strings) point to their
entire range, so it is important that the length metadata is never too large.

In particular, the dynamic size of a Rust value (as determined bysize_of_val)
must never exceedisize::MAX, since it is impossible for a single allocation
to be larger thanisize::MAX.

## Invalid values

The Rust compiler assumes that all values produced during program execution are
âvalidâ, and producing an invalid value is hence immediate UB.

Whether a value is valid depends on the type:

- Aboolvalue must befalse(0) ortrue(1).
- Afnpointer value must be non-null.
- Acharvalue must not be a surrogate (i.e., must not be in the range0xD800..=0xDFFF) and must be equal to or less thanchar::MAX.
- A!value must never exist.
- An integer (i*/u*), floating point value (f*), or raw pointer must be
initialized, i.e., must not be obtained from uninitialized memory.
- Astrvalue is treated like[u8], i.e. it must be initialized.
- Anenummust have a valid discriminant, and all fields of the variant indicated by that discriminant must be valid at their respective type.
- Astruct, tuple, and array requires all fields/elements to be valid at their respective type.
- For aunion, the exact validity requirements are not decided yet.
Obviously, all values that can be created entirely in safe code are valid.
If the union has a zero-sized field, then every possible value is valid.
Further details arestill being debated.
- A reference orBox<T>must be aligned and non-null, it cannot bedangling, and it must point to a valid value
(in case of dynamically sized types, using the actual dynamic type of the
pointee as determined by the metadata).
Note that the last point (about pointing to a valid value) remains a subject of some debate.
- The metadata of a wide reference,Box<T>, or raw pointer must match
the type of the unsized tail:dyn Traitmetadata must be a pointer to a compiler-generated vtable forTrait.
(For raw pointers, this requirement remains a subject of some debate.)Slice ([T]) metadata must be a validusize.
Furthermore, for wide references andBox<T>, slice metadata is invalid
if it makes the total size of the pointed-to value bigger thanisize::MAX.
- dyn Traitmetadata must be a pointer to a compiler-generated vtable forTrait.
(For raw pointers, this requirement remains a subject of some debate.)
- Slice ([T]) metadata must be a validusize.
Furthermore, for wide references andBox<T>, slice metadata is invalid
if it makes the total size of the pointed-to value bigger thanisize::MAX.
- If a type has a custom range of a valid values, then a valid value must be in that range.
In the standard library, this affectsNonNull<T>andNonZero<T>.Noterustcachieves this with the unstablerustc_layout_scalar_valid_range_*attributes.
If a type has a custom range of a valid values, then a valid value must be in that range.
In the standard library, this affectsNonNull<T>andNonZero<T>.

> Noterustcachieves this with the unstablerustc_layout_scalar_valid_range_*attributes.

Note

rustcachieves this with the unstablerustc_layout_scalar_valid_range_*attributes.

Note:Uninitialized memory is also implicitly invalid for any type that has
a restricted set of valid values. In other words, the only cases in which
reading uninitialized memory is permitted are insideunions and in âpaddingâ
(the gaps between the fields of a type).
