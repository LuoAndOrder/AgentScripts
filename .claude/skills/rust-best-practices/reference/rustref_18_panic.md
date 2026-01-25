# Panic

Source: https://doc.rust-lang.org/reference/

Rust provides a mechanism to prevent a function from returning normally, and instead âpanic,â which is a response to an error condition that is typically not expected to be recoverable within the context in which the error is encountered.

Some language constructs, such as out-of-boundsarray indexing, panic automatically.

There are also language features that provide a level of control over panic behavior:

- Apanic handlerdefines the behavior of a panic.
- FFI ABIsmay alter how panics behave.

> NoteThe standard library provides the capability to explicitly panic via thepanic!macro.

Note

The standard library provides the capability to explicitly panic via thepanic!macro.

## Thepanic_handlerattribute

Thepanic_handlerattributecan be applied to a function to define the behavior of panics.

Thepanic_handlerattribute can only be applied to a function with signaturefn(&PanicInfo) -> !.

> NoteThePanicInfostruct contains information about the location of the panic.

Note

ThePanicInfostruct contains information about the location of the panic.

There must be a singlepanic_handlerfunction in the dependency graph.

Below is shown apanic_handlerfunction that logs the panic message and then halts the thread.

```rust
#![no_std]

use core::fmt::{self, Write};
use core::panic::PanicInfo;

struct Sink {
    // ..
   _0: (),
}

impl Sink {
    fn new() -> Sink { Sink { _0: () }}
}

impl fmt::Write for Sink {
    fn write_str(&mut self, _: &str) -> fmt::Result { Ok(()) }
}

#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    let mut sink = Sink::new();

    // logs "panicked at '$reason', src/main.rs:27:4" to some `sink`
    let _ = writeln!(sink, "{}", info);

    loop {}
}
```

### Standard behavior

stdprovides two different panic handlers:

- unwindâ unwinds the stack and is potentially recoverable.
- abortââ aborts the process and is non-recoverable.
Not all targets may provide theunwindhandler.

> NoteThe panic handler used when linking withstdcan be set with the-C panicCLI flag. The default for most targets isunwind.The standard libraryâs panic behavior can be modified at runtime with thestd::panic::set_hookfunction.

Note

The panic handler used when linking withstdcan be set with the-C panicCLI flag. The default for most targets isunwind.

The standard libraryâs panic behavior can be modified at runtime with thestd::panic::set_hookfunction.

Linking ano_stdbinary, dylib, cdylib, or staticlib will require specifying your own panic handler.

## Panic strategy

Thepanic strategydefines the kind of panic behavior that a crate is built to support.

> NoteThe panic strategy can be chosen inrustcwith the-C panicCLI flag.When generating a binary, dylib, cdylib, or staticlib and linking withstd, the-C panicCLI flag also influences whichpanic handleris used.

Note

The panic strategy can be chosen inrustcwith the-C panicCLI flag.

When generating a binary, dylib, cdylib, or staticlib and linking withstd, the-C panicCLI flag also influences whichpanic handleris used.

> NoteWhen compiling code with theabortpanic strategy, the optimizer may assume that unwinding across Rust frames is impossible, which can result in both code-size and runtime speed improvements.

Note

When compiling code with theabortpanic strategy, the optimizer may assume that unwinding across Rust frames is impossible, which can result in both code-size and runtime speed improvements.

> NoteSeelink.unwindingfor restrictions on linking crates with different panic strategies. An implication is that crates built with theunwindstrategy can use theabortpanic handler, but theabortstrategy cannot use theunwindpanic handler.

Note

Seelink.unwindingfor restrictions on linking crates with different panic strategies. An implication is that crates built with theunwindstrategy can use theabortpanic handler, but theabortstrategy cannot use theunwindpanic handler.

## Unwinding

Panicking may either be recoverable or non-recoverable, though it can be configured (by choosing a non-unwinding panic handler) to always be non-recoverable. (The converse is not true: theunwindhandler does not guarantee that all panics are recoverable, only that panicking via thepanic!macro and similar standard library mechanisms is recoverable.)

When a panic occurs, theunwindhandler âunwindsâ Rust frames, just as C++âsthrowunwinds C++ frames, until the panic reaches the point of recovery (for instance at a thread boundary). This means that as the panic traverses Rust frames, live objects in those frames thatimplementDropwill have theirdropmethods called. Thus, when normal execution resumes, no-longer-accessible objects will have been âcleaned upâ just as if they had gone out of scope normally.

> NoteAs long as this guarantee of resource-cleanup is preserved, âunwindingâ may be implemented without actually using the mechanism used by C++ for the target platform.

Note

As long as this guarantee of resource-cleanup is preserved, âunwindingâ may be implemented without actually using the mechanism used by C++ for the target platform.

> NoteThe standard library provides two mechanisms for recovering from a panic,std::panic::catch_unwind(which enables recovery within the panicking thread) andstd::thread::spawn(which automatically sets up panic recovery for the spawned thread so that other threads may continue running).

Note

The standard library provides two mechanisms for recovering from a panic,std::panic::catch_unwind(which enables recovery within the panicking thread) andstd::thread::spawn(which automatically sets up panic recovery for the spawned thread so that other threads may continue running).

### Unwinding across FFI boundaries

It is possible to unwind across FFI boundaries using anappropriate ABI declaration. While useful in certain cases, this creates unique opportunities for undefined behavior, especially when multiple language runtimes are involved.

Unwinding with the wrong ABI is undefined behavior:

- Causing an unwind into Rust code from a foreign function that was called via a function declaration or pointer declared with a non-unwinding ABI, such as"C","system", etc. (For example, this case occurs when such a function written in C++ throws an exception that is uncaught and propagates to Rust.)
- Calling a Rustexternfunction that unwinds (withextern "C-unwind"or another ABI that permits unwinding) from code that does not support unwinding, such as code compiled with GCC or Clang using-fno-exceptions
Catching a foreign unwinding operation (such as a C++ exception) usingstd::panic::catch_unwind,std::thread::JoinHandle::join, or by letting it propagate beyond the Rustmain()function or thread root will have one of two behaviors, and it is unspecified which will occur:

- The process aborts.
- The function returns aResult::Errcontaining an opaque type.

> NoteRust code compiled or linked with a different instance of the Rust standard library counts as a âforeign exceptionâ for the purpose of this guarantee. Thus, a library that usespanic!and is linked against one version of the Rust standard library, invoked from an application that uses a different version of the standard library, may cause the entire application to abort even if the library is only used within a child thread.

Note

Rust code compiled or linked with a different instance of the Rust standard library counts as a âforeign exceptionâ for the purpose of this guarantee. Thus, a library that usespanic!and is linked against one version of the Rust standard library, invoked from an application that uses a different version of the standard library, may cause the entire application to abort even if the library is only used within a child thread.

There are currently no guarantees about the behavior that occurs when a foreign runtime attempts to dispose of, or rethrow, a Rustpanicpayload. In other words, an unwind originated from a Rust runtime must either lead to termination of the process or be caught by the same runtime.
