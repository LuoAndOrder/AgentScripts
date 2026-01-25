# The Default Trait

Source: https://rust-unofficial.github.io/patterns/

# TheDefaultTrait

## Description

Many types in Rust have aconstructor. However, this isspecificto the
type; Rust cannot abstract over “everything that has anew()method”. To allow
this, theDefaulttrait was conceived, which can be used with containers and
other generic types (e.g. seeOption::unwrap_or_default()). Notably, some
containers already implement it where applicable.

Not only do one-element containers likeCow,BoxorArcimplementDefaultfor containedDefaulttypes, one can automatically#[derive(Default)]for structs whose fields all implement it, so the more
types implementDefault, the more useful it becomes.

On the other hand, constructors can take multiple arguments, while thedefault()method does not. There can even be multiple constructors with
different names, but there can only be oneDefaultimplementation per type.

## Example

```rust
use std::{path::PathBuf, time::Duration};

// note that we can simply auto-derive Default here.
#[derive(Default, Debug, PartialEq)]
struct MyConfiguration {
    // Option defaults to None
    output: Option<PathBuf>,
    // Vecs default to empty vector
    search_path: Vec<PathBuf>,
    // Duration defaults to zero time
    timeout: Duration,
    // bool defaults to false
    check: bool,
}

impl MyConfiguration {
    // add setters here
}

fn main() {
    // construct a new instance with default values
    let mut conf = MyConfiguration::default();
    // do something with conf here
    conf.check = true;
    println!("conf = {conf:#?}");

    // partial initialization with default values, creates the same instance
    let conf1 = MyConfiguration {
        check: true,
        ..Default::default()
    };
    assert_eq!(conf, conf1);
}
```

## See also

- Theconstructoridiom is another way to generate instances that may or may
not be “default”
- TheDefaultdocumentation (scroll down for the list of implementors)
- Option::unwrap_or_default()
- derive(new)
