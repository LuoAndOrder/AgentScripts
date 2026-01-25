# Memory Model

Source: https://doc.rust-lang.org/reference/

# Memory model

> WarningThe memory model of Rust is incomplete and not fully decided.

Warning

The memory model of Rust is incomplete and not fully decided.

## Bytes

The most basic unit of memory in Rust is a byte.

> NoteWhile bytes are typically lowered to hardware bytes, Rust uses an âabstractâ notion of bytes that can make distinctions which are absent in hardware, such as being uninitialized, or storing part of a pointer. Those distinctions can affect whether your program has undefined behavior, so they still have tangible impact on how compiled Rust programs behave.

Note

While bytes are typically lowered to hardware bytes, Rust uses an âabstractâ notion of bytes that can make distinctions which are absent in hardware, such as being uninitialized, or storing part of a pointer. Those distinctions can affect whether your program has undefined behavior, so they still have tangible impact on how compiled Rust programs behave.

Each byte may have one of the following values:

- An initialized byte containing au8value and optionalprovenance,
- An uninitialized byte.

> NoteThe above list is not yet guaranteed to be exhaustive.

Note

The above list is not yet guaranteed to be exhaustive.
