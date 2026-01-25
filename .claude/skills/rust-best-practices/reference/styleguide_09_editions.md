# Rust Style Editions

Source: https://doc.rust-lang.org/nightly/style-guide/

# Rust style editions

The default Rust style evolves over time, as Rust does. However, to avoid
breaking established code style, and CI jobs checking code style, changes to
the default Rust style only appear instyle editions.

Code written in a givenRust editionuses the corresponding Rust style edition by default. To make it easier to
migrate code style separately from the semantic changes between Rust editions,
formatting tools such asrustfmtallow updating the style edition separately
from the Rust edition.

The current version of the style guide describes the latest Rust style edition.
Each distinct past style will have a corresponding archived version of the
style guide.

Note that archived versions of the style guide do not document formatting for
newer Rust constructs that did not exist at the time that version of the style
guide was archived. However, each style edition will still format all
constructs valid in that Rust edition, with the style of newer constructs
coming from the first subsequent style edition providing formatting rules for
that construct (without any of the systematic/global changes from that style
edition).

Not all Rust editions have corresponding changes to the Rust style. For
instance, Rust 2015, Rust 2018, and Rust 2021 all use the same style edition.

## Rust next style edition

- Never break within a nullary function callfunc()or a unit literal().

## Rust 2024 style edition

This style guide describes the Rust 2024 style edition. The Rust 2024 style
edition is currently nightly-only and may change before the release of Rust
2024.

For a full history of changes in the Rust 2024 style edition, see the git
history of the style guide. Notable changes in the Rust 2024 style edition
include:

- Miscellaneousrustfmtbugfixes.
- Use version-sort (sortx8,x16,x32,x64,x128in that order).
- Change âASCIIbeticalâ sort to Unicode-aware ânon-lowercase before lowercaseâ.

## Rust 2015/2018/2021 style edition

The archived version of the style guide athttps://github.com/rust-lang/rust/tree/37343f4a4d4ed7ad0891cb79e8eb25acf43fb821/src/doc/style-guide/srcdescribes the style edition corresponding to Rust 2015, Rust 2018, and Rust
2021.
