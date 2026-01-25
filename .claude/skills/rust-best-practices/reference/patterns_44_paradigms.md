# Programming Paradigms

Source: https://rust-unofficial.github.io/patterns/

# Programming paradigms

One of the biggest hurdles to understanding functional programs when coming from
an imperative background is the shift in thinking. Imperative programs describehowto do something, whereas declarative programs describewhatto do.
Let’s sum the numbers from 1 to 10 to show this.

## Imperative

```rust
#![allow(unused)]
fn main() {
let mut sum = 0;
for i in 1..11 {
    sum += i;
}
println!("{sum}");
}
```

With imperative programs, we have to play compiler to see what is happening.
Here, we start with asumof0. Next, we iterate through the range from 1
to 10. Each time through the loop, we add the corresponding value in the range.
Then we print it out.

This is how most of us start out programming. We learn that a program is a set
of steps.

## Declarative

```rust
#![allow(unused)]
fn main() {
println!("{}", (1..11).fold(0, |a, b| a + b));
}
```

Whoa! This is really different! What’s going on here? Remember that with
declarative programs we are describingwhatto do, rather thanhowto do
it.foldis a function thatcomposesfunctions. The
name is a convention from Haskell.

Here, we are composing functions of addition (this closure:|a, b| a + b) with
a range from 1 to 10. The0is the starting point, soais0at first.bis the first element of the range,1.0 + 1 = 1is the result. So now wefoldagain, witha = 1,b = 2and so1 + 2 = 3is the next result. This
process continues until we get to the last element in the range,10.
