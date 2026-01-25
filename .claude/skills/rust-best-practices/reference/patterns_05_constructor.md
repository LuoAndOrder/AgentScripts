# Constructor

Source: https://rust-unofficial.github.io/patterns/

# Constructors

## Description

Rust does not have constructors as a language construct. Instead, the convention
is to use anassociated functionnewto create an
object:

```rust
#![allow(unused)]
fn main() {
/// Time in seconds.
///
/// # Example
///
/// ```
/// let s = Second::new(42);
/// assert_eq!(42, s.value());
/// ```
pub struct Second {
    value: u64,
}

impl Second {
    // Constructs a new instance of [`Second`].
    // Note this is an associated function - no self.
    pub fn new(value: u64) -> Self {
        Self { value }
    }

    /// Returns the value in seconds.
    pub fn value(&self) -> u64 {
        self.value
    }
}
}
```

## Default Constructors

Rust supports default constructors with theDefaulttrait:

```rust
#![allow(unused)]
fn main() {
/// Time in seconds.
///
/// # Example
///
/// ```
/// let s = Second::default();
/// assert_eq!(0, s.value());
/// ```
pub struct Second {
    value: u64,
}

impl Second {
    /// Returns the value in seconds.
    pub fn value(&self) -> u64 {
        self.value
    }
}

impl Default for Second {
    fn default() -> Self {
        Self { value: 0 }
    }
}
}
```

Defaultcan also be derived if all types of all fields implementDefault,
like they do withSecond:

```rust
#![allow(unused)]
fn main() {
/// Time in seconds.
///
/// # Example
///
/// ```
/// let s = Second::default();
/// assert_eq!(0, s.value());
/// ```
#[derive(Default)]
pub struct Second {
    value: u64,
}

impl Second {
    /// Returns the value in seconds.
    pub fn value(&self) -> u64 {
        self.value
    }
}
}
```

Note:It is common and expected for types to implement bothDefaultand an
emptynewconstructor.newis the constructor convention in Rust, and users
expect it to exist, so if it is reasonable for the basic constructor to take no
arguments, then it should, even if it is functionally identical to default.

Hint:The advantage of implementing or derivingDefaultis that your type
can now be used where aDefaultimplementation is required, most prominently,
any of the*or_defaultfunctions in the standard library.

## See also

- Thedefault idiomfor a more in-depth description of theDefaulttrait.
Thedefault idiomfor a more in-depth description of theDefaulttrait.

- Thebuilder patternfor constructing
objects where there are multiple configurations.
Thebuilder patternfor constructing
objects where there are multiple configurations.

- API Guidelines/C-COMMON-TRAITSfor
implementing both,Defaultandnew.
API Guidelines/C-COMMON-TRAITSfor
implementing both,Defaultandnew.
