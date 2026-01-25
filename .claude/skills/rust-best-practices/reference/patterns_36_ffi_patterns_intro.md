# FFI Patterns

Source: https://rust-unofficial.github.io/patterns/

Writing FFI code is an entire course in itself. However, there are several
idioms here that can act as pointers, and avoid traps for inexperienced users of
unsafe Rust.

This section contains design patterns that may be useful when doing FFI.

- Object-Based APIdesign that has good memory safety
characteristics, and a clean boundary of what is safe and what is unsafe
Object-Based APIdesign that has good memory safety
characteristics, and a clean boundary of what is safe and what is unsafe

- Type Consolidation into Wrappers- group multiple Rust types
together into an opaque “object”
Type Consolidation into Wrappers- group multiple Rust types
together into an opaque “object”
