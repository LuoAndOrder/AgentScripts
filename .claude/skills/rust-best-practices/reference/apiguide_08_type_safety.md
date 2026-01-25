# Type Safety

Source: https://rust-lang.github.io/api-guidelines/

# Type safety

## Newtypes provide static distinctions (C-NEWTYPE)

Newtypes can statically distinguish between different interpretations of an
underlying type.

For example, af64value might be used to represent a quantity in miles or in
kilometers. Using newtypes, we can keep track of the intended interpretation:

```rust

#![allow(unused)]
fn main() {
struct Miles(pub f64);
struct Kilometers(pub f64);

impl Miles {
    fn to_kilometers(self) -> Kilometers { /* ... */ }
}
impl Kilometers {
    fn to_miles(self) -> Miles { /* ... */ }
}
}
```

```rust

#![allow(unused)]
fn main() {
struct Miles(pub f64);
struct Kilometers(pub f64);

impl Miles {
    fn to_kilometers(self) -> Kilometers { /* ... */ }
}
impl Kilometers {
    fn to_miles(self) -> Miles { /* ... */ }
}
}
```

Once we have separated these two types, we can statically ensure that we do not
confuse them. For example, the function

```rust

#![allow(unused)]
fn main() {
fn are_we_there_yet(distance_travelled: Miles) -> bool { /* ... */ }
}
```

```rust

#![allow(unused)]
fn main() {
fn are_we_there_yet(distance_travelled: Miles) -> bool { /* ... */ }
}
```

cannot accidentally be called with aKilometersvalue. The compiler will
remind us to perform the conversion, thus averting certaincatastrophic bugs.

## Arguments convey meaning through types, notboolorOption(C-CUSTOM-TYPE)

Prefer

```rust

#![allow(unused)]
fn main() {
let w = Widget::new(Small, Round)
}
```

```rust

#![allow(unused)]
fn main() {
let w = Widget::new(Small, Round)
}
```

over

```rust

#![allow(unused)]
fn main() {
let w = Widget::new(true, false)
}
```

```rust

#![allow(unused)]
fn main() {
let w = Widget::new(true, false)
}
```

Core types likebool,u8andOptionhave many possible interpretations.

Use a deliberate type (whether enum, struct, or tuple) to convey interpretation
and invariants. In the above example, it is not immediately clear whattrueandfalseare conveying without looking up the argument names, butSmallandRoundare more suggestive.

Using custom types makes it easier to expand the options later on, for example
by adding anExtraLargevariant.

See the newtype pattern (C-NEWTYPE) for a no-cost way to wrap existing types
with a distinguished name.

## Types for a set of flags arebitflags, not enums (C-BITFLAG)

Rust supportsenumtypes with explicitly specified discriminants:

```rust

#![allow(unused)]
fn main() {
enum Color {
    Red = 0xff0000,
    Green = 0x00ff00,
    Blue = 0x0000ff,
}
}
```

```rust

#![allow(unused)]
fn main() {
enum Color {
    Red = 0xff0000,
    Green = 0x00ff00,
    Blue = 0x0000ff,
}
}
```

Custom discriminants are useful when anenumtype needs to be serialized to an
integer value compatibly with some other system/language. They support
"typesafe" APIs: by taking aColor, rather than an integer, a function is
guaranteed to get well-formed inputs, even if it later views those inputs as
integers.

Anenumallows an API to request exactly one choice from among many. Sometimes
an API's input is instead the presence or absence of a set of flags. In C code,
this is often done by having each flag correspond to a particular bit, allowing
a single integer to represent, say, 32 or 64 flags. Rust'sbitflagscrate
provides a typesafe representation of this pattern.

```rust
use bitflags::bitflags;

bitflags! {
    struct Flags: u32 {
        const FLAG_A = 0b00000001;
        const FLAG_B = 0b00000010;
        const FLAG_C = 0b00000100;
    }
}

fn f(settings: Flags) {
    if settings.contains(Flags::FLAG_A) {
        println!("doing thing A");
    }
    if settings.contains(Flags::FLAG_B) {
        println!("doing thing B");
    }
    if settings.contains(Flags::FLAG_C) {
        println!("doing thing C");
    }
}

fn main() {
    f(Flags::FLAG_A | Flags::FLAG_C);
}
```

```rust
use bitflags::bitflags;

bitflags! {
    struct Flags: u32 {
        const FLAG_A = 0b00000001;
        const FLAG_B = 0b00000010;
        const FLAG_C = 0b00000100;
    }
}

fn f(settings: Flags) {
    if settings.contains(Flags::FLAG_A) {
        println!("doing thing A");
    }
    if settings.contains(Flags::FLAG_B) {
        println!("doing thing B");
    }
    if settings.contains(Flags::FLAG_C) {
        println!("doing thing C");
    }
}

fn main() {
    f(Flags::FLAG_A | Flags::FLAG_C);
}
```

## Builders enable construction of complex values (C-BUILDER)

Some data structures are complicated to construct, due to their construction
needing:

- a large number of inputs
- compound data (e.g. slices)
- optional configuration data
- choice between several flavors
which can easily lead to a large number of distinct constructors with many
arguments each.

IfTis such a data structure, consider introducing aTbuilder:

- Introduce a separate data typeTBuilderfor incrementally configuring aTvalue. When possible, choose a better name: e.g.Commandis the builder
for achild process,Urlcan be created from aParseOptions.
- The builder constructor should take as parameters only the datarequiredto
make aT.
- The builder should offer a suite of convenient methods for configuration,
including setting up compound inputs (like slices) incrementally. These
methods should returnselfto allow chaining.
- The builder should provide one or more "terminal" methods for actually
building aT.
The builder pattern is especially appropriate when building aTinvolves side
effects, such as spawning a task or launching a process.

In Rust, there are two variants of the builder pattern, differing in the
treatment of ownership, as described below.

### Non-consuming builders (preferred)

In some cases, constructing the finalTdoes not require the builder itself to
be consumed. The following variant onstd::process::Commandis one example:

```rust

#![allow(unused)]
fn main() {
// NOTE: the actual Command API does not use owned Strings;
// this is a simplified version.

pub struct Command {
    program: String,
    args: Vec<String>,
    cwd: Option<String>,
    // etc
}

impl Command {
    pub fn new(program: String) -> Command {
        Command {
            program: program,
            args: Vec::new(),
            cwd: None,
        }
    }

    /// Add an argument to pass to the program.
    pub fn arg(&mut self, arg: String) -> &mut Command {
        self.args.push(arg);
        self
    }

    /// Add multiple arguments to pass to the program.
    pub fn args(&mut self, args: &[String]) -> &mut Command {
        self.args.extend_from_slice(args);
        self
    }

    /// Set the working directory for the child process.
    pub fn current_dir(&mut self, dir: String) -> &mut Command {
        self.cwd = Some(dir);
        self
    }

    /// Executes the command as a child process, which is returned.
    pub fn spawn(&self) -> io::Result<Child> {
        /* ... */
    }
}
}
```

```rust

#![allow(unused)]
fn main() {
// NOTE: the actual Command API does not use owned Strings;
// this is a simplified version.

pub struct Command {
    program: String,
    args: Vec<String>,
    cwd: Option<String>,
    // etc
}

impl Command {
    pub fn new(program: String) -> Command {
        Command {
            program: program,
            args: Vec::new(),
            cwd: None,
        }
    }

    /// Add an argument to pass to the program.
    pub fn arg(&mut self, arg: String) -> &mut Command {
        self.args.push(arg);
        self
    }

    /// Add multiple arguments to pass to the program.
    pub fn args(&mut self, args: &[String]) -> &mut Command {
        self.args.extend_from_slice(args);
        self
    }

    /// Set the working directory for the child process.
    pub fn current_dir(&mut self, dir: String) -> &mut Command {
        self.cwd = Some(dir);
        self
    }

    /// Executes the command as a child process, which is returned.
    pub fn spawn(&self) -> io::Result<Child> {
        /* ... */
    }
}
}
```

Note that thespawnmethod, which actually uses the builder configuration to
spawn a process, takes the builder by shared reference. This is possible because
spawning the process does not require ownership of the configuration data.

Because the terminalspawnmethod only needs a reference, the configuration
methods take and return a mutable borrow ofself.

#### The benefit

By using borrows throughout,Commandcan be used conveniently for both
one-liner and more complex constructions:

```rust

#![allow(unused)]
fn main() {
// One-liners
Command::new("/bin/cat").arg("file.txt").spawn();

// Complex configuration
let mut cmd = Command::new("/bin/ls");
if size_sorted {
    cmd.arg("-S");
}
cmd.arg(".");
cmd.spawn();
}
```

```rust

#![allow(unused)]
fn main() {
// One-liners
Command::new("/bin/cat").arg("file.txt").spawn();

// Complex configuration
let mut cmd = Command::new("/bin/ls");
if size_sorted {
    cmd.arg("-S");
}
cmd.arg(".");
cmd.spawn();
}
```

### Consuming builders

Sometimes builders must transfer ownership when constructing the final typeT,
meaning that the terminal methods must takeselfrather than&self.

```rust

#![allow(unused)]
fn main() {
impl TaskBuilder {
    /// Name the task-to-be.
    pub fn named(mut self, name: String) -> TaskBuilder {
        self.name = Some(name);
        self
    }

    /// Redirect task-local stdout.
    pub fn stdout(mut self, stdout: Box<io::Write + Send>) -> TaskBuilder {
        self.stdout = Some(stdout);
        self
    }

    /// Creates and executes a new child task.
    pub fn spawn<F>(self, f: F) where F: FnOnce() + Send {
        /* ... */
    }
}
}
```

```rust

#![allow(unused)]
fn main() {
impl TaskBuilder {
    /// Name the task-to-be.
    pub fn named(mut self, name: String) -> TaskBuilder {
        self.name = Some(name);
        self
    }

    /// Redirect task-local stdout.
    pub fn stdout(mut self, stdout: Box<io::Write + Send>) -> TaskBuilder {
        self.stdout = Some(stdout);
        self
    }

    /// Creates and executes a new child task.
    pub fn spawn<F>(self, f: F) where F: FnOnce() + Send {
        /* ... */
    }
}
}
```

Here, thestdoutconfiguration involves passing ownership of anio::Write,
which must be transferred to the task upon construction (inspawn).

When the terminal methods of the builder require ownership, there is a basic
tradeoff:

- If the other builder methods take/return a mutable borrow, the complex
configuration case will work well, but one-liner configuration becomes
impossible.
If the other builder methods take/return a mutable borrow, the complex
configuration case will work well, but one-liner configuration becomes
impossible.

- If the other builder methods take/return an ownedself, one-liners continue
to work well but complex configuration is less convenient.
If the other builder methods take/return an ownedself, one-liners continue
to work well but complex configuration is less convenient.

Under the rubric of making easy things easy and hard things possible, all
builder methods for a consuming builder should take and return an ownedself. Then client code works as follows:

```rust

#![allow(unused)]
fn main() {
// One-liners
TaskBuilder::new("my_task").spawn(|| { /* ... */ });

// Complex configuration
let mut task = TaskBuilder::new();
task = task.named("my_task_2"); // must re-assign to retain ownership
if reroute {
    task = task.stdout(mywriter);
}
task.spawn(|| { /* ... */ });
}
```

```rust

#![allow(unused)]
fn main() {
// One-liners
TaskBuilder::new("my_task").spawn(|| { /* ... */ });

// Complex configuration
let mut task = TaskBuilder::new();
task = task.named("my_task_2"); // must re-assign to retain ownership
if reroute {
    task = task.stdout(mywriter);
}
task.spawn(|| { /* ... */ });
}
```

One-liners work as before, because ownership is threaded through each of the
builder methods until being consumed byspawn. Complex configuration, however,
is more verbose: it requires re-assigning the builder at each step.
