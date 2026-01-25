# Interpreter Pattern

Source: https://rust-unofficial.github.io/patterns/

# Interpreter

## Description

If a problem occurs very often and requires long and repetitive steps to solve
it, then the problem instances might be expressed in a simple language and an
interpreter object could solve it by interpreting the sentences written in this
simple language.

Basically, for any kind of problems we define:

- Adomain specific language,
- A grammar for this language,
- An interpreter that solves the problem instances.

## Motivation

Our goal is to translate simple mathematical expressions into postfix
expressions (orReverse Polish notation)
For simplicity, our expressions consist of ten digits0, …,9and two
operations+,-. For example, the expression2 + 4is translated into2 4 +.

## Context Free Grammar for our problem

Our task is translating infix expressions into postfix ones. Let’s define a
context free grammar for a set of infix expressions over0, …,9,+, and-, where:

- Terminal symbols:0,...,9,+,-
- Non-terminal symbols:exp,term
- Start symbol isexp
- And the following are production rules

```ignore
exp -> exp + term
exp -> exp - term
exp -> term
term -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

NOTE:This grammar should be further transformed depending on what we are
going to do with it. For example, we might need to remove left recursion. For
more details please seeCompilers: Principles,Techniques, and Tools(aka Dragon Book).

## Solution

We simply implement a recursive descent parser. For simplicity’s sake, the code
panics when an expression is syntactically wrong (for example2-34or2+5-are wrong according to the grammar definition).

```rust
pub struct Interpreter<'a> {
    it: std::str::Chars<'a>,
}

impl<'a> Interpreter<'a> {
    pub fn new(infix: &'a str) -> Self {
        Self { it: infix.chars() }
    }

    fn next_char(&mut self) -> Option<char> {
        self.it.next()
    }

    pub fn interpret(&mut self, out: &mut String) {
        self.term(out);

        while let Some(op) = self.next_char() {
            if op == '+' || op == '-' {
                self.term(out);
                out.push(op);
            } else {
                panic!("Unexpected symbol '{op}'");
            }
        }
    }

    fn term(&mut self, out: &mut String) {
        match self.next_char() {
            Some(ch) if ch.is_digit(10) => out.push(ch),
            Some(ch) => panic!("Unexpected symbol '{ch}'"),
            None => panic!("Unexpected end of string"),
        }
    }
}

pub fn main() {
    let mut intr = Interpreter::new("2+3");
    let mut postfix = String::new();
    intr.interpret(&mut postfix);
    assert_eq!(postfix, "23+");

    intr = Interpreter::new("1-2+3-4");
    postfix.clear();
    intr.interpret(&mut postfix);
    assert_eq!(postfix, "12-3+4-");
}
```

## Discussion

There may be a wrong perception that the Interpreter design pattern is about
design grammars for formal languages and implementation of parsers for these
grammars. In fact, this pattern is about expressing problem instances in a more
specific way and implementing functions/classes/structs that solve these problem
instances. Rust language hasmacro_rules!that allow us to define special
syntax and rules on how to expand this syntax into source code.

In the following example we create a simplemacro_rules!that computesEuclidean lengthofndimensional vectors. Writingnorm!(x,1,2)might be easier to express and more
efficient than packingx,1,2into aVecand calling a function computing the
length.

```rust
macro_rules! norm {
    ($($element:expr),*) => {
        {
            let mut n = 0.0;
            $(
                n += ($element as f64)*($element as f64);
            )*
            n.sqrt()
        }
    };
}

fn main() {
    let x = -3f64;
    let y = 4f64;

    assert_eq!(3f64, norm!(x));
    assert_eq!(5f64, norm!(x, y));
    assert_eq!(0f64, norm!(0, 0, 0));
    assert_eq!(1f64, norm!(0.5, -0.5, 0.5, -0.5));
}
```

## See also

- Interpreter pattern
- Context free grammar
- macro_rules!
