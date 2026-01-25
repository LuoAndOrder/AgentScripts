# Introduction

Source: https://rust-unofficial.github.io/patterns/

## Participation

If you are interested in contributing to this book, check out thecontribution guidelines.

## News

- 2025-12-14: New pattern added:Use custom traits to avoid complex type bounds
- 2024-03-17: You can now download thebook in PDF format.

## Design patterns

In software development, we often come across problems that share similarities
regardless of the environment they appear in. Although the implementation
details are crucial to solve the task at hand, we may abstract from these
particularities to find the common practices that are generically applicable.

Design patterns are a collection of reusable and tested solutions to recurring
problems in engineering. They make our software more modular, maintainable, and
extensible. Moreover, these patterns provide a common language for developers,
making them an excellent tool for effective communication when problem-solving
in teams.

Keep in mind: Each pattern comes with its own set of trade-offs. It’s crucial to
focus on why you choose a particular pattern rather than just on how to
implement it.1

## Design patterns in Rust

Rust is not object-oriented, and the combination of all its characteristics,
such as functional elements, a strong type system, and the borrow checker, makes
it unique. Because of this, Rust design patterns vary with respect to other
traditional object-oriented programming languages. That’s why we decided to
write this book. We hope you enjoy reading it! The book is divided in three main
chapters:

- Idioms: guidelines to follow when coding. They are the
social norms of the community. You should break them only if you have a good
reason for it.
- Design patterns: methods to solve common problems when
coding.
- Anti-patterns: methods to solve common problems
when coding. However, while design patterns give us benefits, anti-patterns
create more problems.
- https://www.infoq.com/podcasts/software-architecture-hard-parts/(Archive)↩
https://www.infoq.com/podcasts/software-architecture-hard-parts/(Archive)↩
