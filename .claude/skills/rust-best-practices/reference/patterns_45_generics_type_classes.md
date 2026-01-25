# Generics as Type Classes

Source: https://rust-unofficial.github.io/patterns/

## Description

Rust’s type system is designed more like functional languages (like Haskell)
rather than imperative languages (like Java and C++). As a result, Rust can turn
many kinds of programming problems into “static typing” problems. This is one of
the biggest wins of choosing a functional language, and is critical to many of
Rust’s compile time guarantees.

A key part of this idea is the way generic types work. In C++ and Java, for
example, generic types are a meta-programming construct for the compiler.vector<int>andvector<char>in C++ are just two different copies of the
same boilerplate code for avectortype (known as atemplate) with two
different types filled in.

In Rust, a generic type parameter creates what is known in functional languages
as a “type class constraint”, and each different parameter filled in by an end
useractually changes the type. In other words,Vec<isize>andVec<char>are two different types, which are recognized as distinct by all parts of the
type system.

This is calledmonomorphization, where different types are created frompolymorphiccode. This special behavior requiresimplblocks to specify
generic parameters. Different values for the generic type cause different types,
and different types can have differentimplblocks.

In object-oriented languages, classes can inherit behavior from their parents.
However, this allows the attachment of not only additional behavior to
particular members of a type class, but extra behavior as well.

The nearest equivalent is the runtime polymorphism in Javascript and Python,
where new members can be added to objects willy-nilly by any constructor.
However, unlike those languages, all of Rust’s additional methods can be type
checked when they are used, because their generics are statically defined. That
makes them more usable while remaining safe.

## Example

Suppose you are designing a storage server for a series of lab machines. Because
of the software involved, there are two different protocols you need to support:
BOOTP (for PXE network boot), and NFS (for remote mount storage).

Your goal is to have one program, written in Rust, which can handle both of
them. It will have protocol handlers and listen for both kinds of requests. The
main application logic will then allow a lab administrator to configure storage
and security controls for the actual files.

The requests from machines in the lab for files contain the same basic
information, no matter what protocol they came from: an authentication method,
and a file name to retrieve. A straightforward implementation would look
something like this:

```rust
enum AuthInfo {
    Nfs(crate::nfs::AuthInfo),
    Bootp(crate::bootp::AuthInfo),
}

struct FileDownloadRequest {
    file_name: PathBuf,
    authentication: AuthInfo,
}
```

This design might work well enough. But now suppose you needed to support adding
metadata that wasprotocol specific. For example, with NFS, you wanted to
determine what their mount point was in order to enforce additional security
rules.

The way the current struct is designed leaves the protocol decision until
runtime. That means any method that applies to one protocol and not the other
requires the programmer to do a runtime check.

Here is how getting an NFS mount point would look:

```rust
struct FileDownloadRequest {
    file_name: PathBuf,
    authentication: AuthInfo,
    mount_point: Option<PathBuf>,
}

impl FileDownloadRequest {
    // ... other methods ...

    /// Gets an NFS mount point if this is an NFS request. Otherwise,
    /// return None.
    pub fn mount_point(&self) -> Option<&Path> {
        self.mount_point.as_ref()
    }
}
```

Every caller ofmount_point()must check forNoneand write code to handle
it. This is true even if they know only NFS requests are ever used in a given
code path!

It would be far more optimal to cause a compile-time error if the different
request types were confused. After all, the entire path of the user’s code,
including what functions from the library they use, will know whether a request
is an NFS request or a BOOTP request.

In Rust, this is actually possible! The solution is toadd a generic typein
order to split the API.

Here is what that looks like:

```rust
use std::path::{Path, PathBuf};

mod nfs {
    #[derive(Clone)]
    pub(crate) struct AuthInfo(String); // NFS session management omitted
}

mod bootp {
    pub(crate) struct AuthInfo(); // no authentication in bootp
}

// Keep the module private to prevent outside users from inventing their own protocols.
mod proto_trait {
    use super::{bootp, nfs};
    use std::path::{Path, PathBuf};

    pub(crate) trait ProtoKind {
        type AuthInfo;
        fn auth_info(&self) -> Self::AuthInfo;
    }

    pub struct Nfs {
        auth: nfs::AuthInfo,
        mount_point: PathBuf,
    }

    impl Nfs {
        pub(crate) fn mount_point(&self) -> &Path {
            &self.mount_point
        }
    }

    impl ProtoKind for Nfs {
        type AuthInfo = nfs::AuthInfo;
        fn auth_info(&self) -> Self::AuthInfo {
            self.auth.clone()
        }
    }

    pub struct Bootp(); // no additional metadata

    impl ProtoKind for Bootp {
        type AuthInfo = bootp::AuthInfo;
        fn auth_info(&self) -> Self::AuthInfo {
            bootp::AuthInfo()
        }
    }
}

use proto_trait::ProtoKind; // keep internal to prevent impls
pub use proto_trait::{Bootp, Nfs}; // re-export so callers can see them

struct FileDownloadRequest<P: ProtoKind> {
    file_name: PathBuf,
    protocol: P,
}

// all common API parts go into a generic impl block
impl<P: ProtoKind> FileDownloadRequest<P> {
    fn file_path(&self) -> &Path {
        &self.file_name
    }

    fn auth_info(&self) -> P::AuthInfo {
        self.protocol.auth_info()
    }
}

// all protocol-specific impls go into their own block
impl FileDownloadRequest<Nfs> {
    fn mount_point(&self) -> &Path {
        self.protocol.mount_point()
    }
}

fn main() {
    // your code here
}
```

With this approach, if the user were to make a mistake and use the wrong type;

```rust
fn main() {
    let mut socket = crate::bootp::listen()?;
    while let Some(request) = socket.next_request()? {
        match request.mount_point().as_ref() {
            "/secure" => socket.send("Access denied"),
            _ => {} // continue on...
        }
        // Rest of the code here
    }
}
```

They would get a syntax error. The typeFileDownloadRequest<Bootp>does not
implementmount_point(), only the typeFileDownloadRequest<Nfs>does. And
that is created by the NFS module, not the BOOTP module of course!

## Advantages

First, it allows fields that are common to multiple states to be de-duplicated.
By making the non-shared fields generic, they are implemented once.

Second, it makes theimplblocks easier to read, because they are broken down
by state. Methods common to all states are typed once in one block, and methods
unique to one state are in a separate block.

Both of these mean there are fewer lines of code, and they are better organized.

## Disadvantages

This currently increases the size of the binary, due to the way monomorphization
is implemented in the compiler. Hopefully the implementation will be able to
improve in the future.

## Alternatives

- If a type seems to need a “split API” due to construction or partial
initialization, consider theBuilder Patterninstead.
If a type seems to need a “split API” due to construction or partial
initialization, consider theBuilder Patterninstead.

- If the API between types does not change – only the behavior does – then theStrategy Patternis better used
instead.
If the API between types does not change – only the behavior does – then theStrategy Patternis better used
instead.

## See also

This pattern is used throughout the standard library:

- Vec<u8>can be cast from a String, unlike every other type ofVec<T>.1
- Iterators can be cast into a binary heap, but only if they contain a type that
implements theOrdtrait.2
- Theto_stringmethod was specialized forCowonly of typestr.3
It is also used by several popular crates to allow API flexibility:

- Theembedded-halecosystem used for embedded devices makes extensive use of
this pattern. For example, it allows statically verifying the configuration of
device registers used to control embedded pins. When a pin is put into a mode,
it returns aPin<MODE>struct, whose generic determines the functions usable
in that mode, which are not on thePinitself.4
Theembedded-halecosystem used for embedded devices makes extensive use of
this pattern. For example, it allows statically verifying the configuration of
device registers used to control embedded pins. When a pin is put into a mode,
it returns aPin<MODE>struct, whose generic determines the functions usable
in that mode, which are not on thePinitself.4

- ThehyperHTTP client library uses this to expose rich APIs for different
pluggable requests. Clients with different connectors have different methods
on them as well as different trait implementations, while a core set of
methods apply to any connector.5
ThehyperHTTP client library uses this to expose rich APIs for different
pluggable requests. Clients with different connectors have different methods
on them as well as different trait implementations, while a core set of
methods apply to any connector.5

- The “type state” pattern – where an object gains and loses API based on an
internal state or invariant – is implemented in Rust using the same basic
concept, and a slightly different technique.6
The “type state” pattern – where an object gains and loses API based on an
internal state or invariant – is implemented in Rust using the same basic
concept, and a slightly different technique.6

- See:impl From<CString> for Vec<u8>↩
See:impl From<CString> for Vec<u8>↩

- See:impl<T: Ord> FromIterator<T> for BinaryHeap<T>↩
See:impl<T: Ord> FromIterator<T> for BinaryHeap<T>↩

- See:impl<‘_> ToString for Cow<’_, str>↩
See:impl<‘_> ToString for Cow<’_, str>↩

- Example:https://docs.rs/stm32f30x-hal/0.1.0/stm32f30x_hal/gpio/gpioa/struct.PA0.html↩
Example:https://docs.rs/stm32f30x-hal/0.1.0/stm32f30x_hal/gpio/gpioa/struct.PA0.html↩

- See:https://docs.rs/hyper/0.14.5/hyper/client/struct.Client.html↩
See:https://docs.rs/hyper/0.14.5/hyper/client/struct.Client.html↩

- See:The Case for the Type State PatternandRusty Typestate Series (an extensive thesis)↩
See:The Case for the Type State PatternandRusty Typestate Series (an extensive thesis)↩
