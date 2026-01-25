# Special Types and Traits

Source: https://doc.rust-lang.org/reference/

# Special types and traits

Certain types and traits that exist inthe standard libraryare known to the
Rust compiler. This chapter documents the special features of these types and
traits.

## Box<T>

Box<T>has a few special features that Rust doesnât currently allow for user
defined types.

- Thedereference operatorforBox<T>produces a place which can be moved
from. This means that the*operator and the destructor ofBox<T>are
built-in to the language.
- Methodscan takeBox<Self>as a receiver.
- A trait may be implemented forBox<T>in the same crate asT, which theorphan rulesprevent for other generic types.

## Rc<T>

Methodscan takeRc<Self>as a receiver.

## Arc<T>

Methodscan takeArc<Self>as a receiver.

## Pin<P>

Methodscan takePin<P>as a receiver.

## UnsafeCell<T>

std::cell::UnsafeCell<T>is used forinterior mutability. It ensures that
the compiler doesnât perform optimisations that are incorrect for such types.

It also ensures thatstaticitemswhich have a type with interior
mutability arenât placed in memory marked as read only.

## PhantomData<T>

std::marker::PhantomData<T>is a zero-sized, minimum alignment, type that
is considered to own aTfor the purposes ofvariance,drop check, andauto traits.

## Operator traits

The traits instd::opsandstd::cmpare used to overloadoperators,indexing expressions, andcall expressions.

## DerefandDerefMut

As well as overloading the unary*operator,DerefandDerefMutare
also used inmethod resolutionandderef coercions.

## Drop

TheDroptrait provides adestructor, to be run whenever a value of this
type is to be destroyed.

## Copy

TheCopytrait changes the semantics of a type implementing it.

Values whose type implementsCopyare copied rather than moved upon assignment.

Copycan only be implemented for types which do not implementDrop, and whose fields are allCopy.
For enums, this means all fields of all variants have to beCopy.
For unions, this means all variants have to beCopy.

Copyis implemented by the compiler for

- TuplesofCopytypes
- Function pointers
- Function items
- Closuresthat capture no values or that only capture values ofCopytypes

## Clone

TheClonetrait is a supertrait ofCopy, so it also needs compiler
generated implementations.

It is implemented by the compiler for the following types:

- Types with a built-inCopyimplementation (see above)
- TuplesofClonetypes
- Closuresthat only capture values ofClonetypes or capture no values from the environment

## Send

TheSendtrait indicates that a value of this type is safe to send from one
thread to another.

## Sync

TheSynctrait indicates that a value of this type is safe to share between
multiple threads.

This trait must be implemented for all types used in immutablestaticitems.

## Termination

TheTerminationtrait indicates the acceptable return types for themain functionandtest functions.

## Auto traits

TheSend,Sync,Unpin,UnwindSafe, andRefUnwindSafetraits areauto
traits. Auto traits have special properties.

If no explicit implementation or negative implementation is written out for an
auto trait for a given type, then the compiler implements it automatically
according to the following rules:

- &T,&mut T,*const T,*mut T,[T; n], and[T]implement the trait
ifTdoes.
- Function item types and function pointers automatically implement the trait.
- Structs, enums, unions, and tuples implement the trait if all of their fields
do.
- Closures implement the trait if the types of all of their captures do. A
closure that captures aTby shared reference and aUby value implements
any auto traits that both&TandUdo.
For generic types (counting the built-in types above as generic overT), if a
generic implementation is available, then the compiler does not automatically
implement it for types that could use the implementation except that they do not
meet the requisite trait bounds. For instance, the standard library implementsSendfor all&TwhereTisSync; this means that the compiler will not
implementSendfor&TifTisSendbut notSync.

Auto traits can also have negative implementations, shown asimpl !AutoTrait for Tin the standard library documentation, that override the automatic
implementations. For example*mut Thas a negative implementation ofSend,
and so*mut Tis notSend, even ifTis. There is currently no stable way
to specify additional negative implementations; they exist only in the standard
library.

Auto traits may be added as an additional bound to anytrait object, even
though normally only one trait is allowed. For instance,Box<dyn Debug + Send + UnwindSafe>is a valid type.

## Sized

TheSizedtrait indicates that the size of this type is known at compile-time; that is, itâs not adynamically sized type.

Type parameters(exceptSelfin traits) areSizedby default, as areassociated types.

Sizedis always implemented automatically by the compiler, not byimplementation items.

These implicitSizedbounds may be relaxed by using the special?Sizedbound.
