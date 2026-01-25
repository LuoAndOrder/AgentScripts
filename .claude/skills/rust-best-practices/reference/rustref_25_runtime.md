# The Rust Runtime

Source: https://doc.rust-lang.org/reference/

# The Rust runtime

This section documents features that define some aspects of the Rust runtime.

## Theglobal_allocatorattribute

Theglobal_allocatorattributeselects amemory allocator.

> Example#![allow(unused)]fn main() {use core::alloc::{GlobalAlloc, Layout};
> use std::alloc::System;
> 
> struct MyAllocator;
> 
> unsafe impl GlobalAlloc for MyAllocator {
>     unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
>         unsafe { System.alloc(layout) }
>     }
>     unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
>         unsafe { System.dealloc(ptr, layout) }
>     }
> }
> 
> #[global_allocator]
> static GLOBAL: MyAllocator = MyAllocator;}

Example

```rust
#![allow(unused)]
fn main() {
use core::alloc::{GlobalAlloc, Layout};
use std::alloc::System;

struct MyAllocator;

unsafe impl GlobalAlloc for MyAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        unsafe { System.alloc(layout) }
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        unsafe { System.dealloc(ptr, layout) }
    }
}

#[global_allocator]
static GLOBAL: MyAllocator = MyAllocator;
}
```

```rust
#![allow(unused)]
fn main() {
use core::alloc::{GlobalAlloc, Layout};
use std::alloc::System;

struct MyAllocator;

unsafe impl GlobalAlloc for MyAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        unsafe { System.alloc(layout) }
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        unsafe { System.dealloc(ptr, layout) }
    }
}

#[global_allocator]
static GLOBAL: MyAllocator = MyAllocator;
}
```

Theglobal_allocatorattribute uses theMetaWordsyntax.

Theglobal_allocatorattribute may only be applied to astatic itemwhose type implements theGlobalAlloctrait.

Theglobal_allocatorattribute may only be used once on an item.

Theglobal_allocatorattribute may only be used once in the crate graph.

Theglobal_allocatorattribute is exported from thestandard library prelude.

## Thewindows_subsystemattribute

Thewindows_subsystemattributesets thesubsystemwhen linking on a Windows target.

> Example#![allow(unused)]#![windows_subsystem = "windows"]fn main() {}

Example

```rust
#![allow(unused)]
#![windows_subsystem = "windows"]
fn main() {
}
```

```rust
#![allow(unused)]
#![windows_subsystem = "windows"]
fn main() {
}
```

Thewindows_subsystemattribute uses theMetaNameValueStrsyntax. Accepted values are"console"and"windows".

Thewindows_subsystemattribute may only be applied to the crate root.

Only the first use ofwindows_subsystemhas effect.

> Noterustclints against any use following the first. This may become an error in the future.

Note

rustclints against any use following the first. This may become an error in the future.

Thewindows_subsystemattribute is ignored on non-Windows targets and non-bincrate types.

The"console"subsystem is the default. If a console process is run from an existing console then it will be attached to that console; otherwise a new console window will be created.

The"windows"subsystem will run detached from any existing console.

> NoteThe"windows"subsystem is commonly used by GUI applications that do not want to display a console window on startup.

Note

The"windows"subsystem is commonly used by GUI applications that do not want to display a console window on startup.
