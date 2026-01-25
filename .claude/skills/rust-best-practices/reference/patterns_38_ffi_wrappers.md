# Type Consolidation into Wrappers

Source: https://rust-unofficial.github.io/patterns/

## Description

This pattern is designed to allow gracefully handling multiple related types,
while minimizing the surface area for memory unsafety.

One of the cornerstones of Rust’s aliasing rules is lifetimes. This ensures that
many patterns of access between types can be memory safe, data race safety
included.

However, when Rust types are exported to other languages, they are usually
transformed into pointers. In Rust, a pointer means “the user manages the
lifetime of the pointee.” It is their responsibility to avoid memory unsafety.

Some level of trust in the user code is thus required, notably around
use-after-free which Rust can do nothing about. However, some API designs place
higher burdens than others on the code written in the other language.

The lowest risk API is the “consolidated wrapper”, where all possible
interactions with an object are folded into a “wrapper type”, while keeping the
Rust API clean.

## Code Example

To understand this, let us look at a classic example of an API to export:
iteration through a collection.

That API looks like this:

- The iterator is initialized withfirst_key.
- Each call tonext_keywill advance the iterator.
- Calls tonext_keyif the iterator is at the end will do nothing.
- As noted above, the iterator is “wrapped into” the collection (unlike the
native Rust API).
If the iterator implementsnth()efficiently, then it is possible to make it
ephemeral to each function call:

```rust
struct MySetWrapper {
    myset: MySet,
    iter_next: usize,
}

impl MySetWrapper {
    pub fn first_key(&mut self) -> Option<&Key> {
        self.iter_next = 0;
        self.next_key()
    }
    pub fn next_key(&mut self) -> Option<&Key> {
        if let Some(next) = self.myset.keys().nth(self.iter_next) {
            self.iter_next += 1;
            Some(next)
        } else {
            None
        }
    }
}
```

As a result, the wrapper is simple and contains nounsafecode.

## Advantages

This makes APIs safer to use, avoiding issues with lifetimes between types. SeeObject-Based APIsfor more on the advantages and pitfalls this
avoids.

## Disadvantages

Often, wrapping types is quite difficult, and sometimes a Rust API compromise
would make things easier.

As an example, consider an iterator which does not efficiently implementnth(). It would definitely be worth putting in special logic to make the
object handle iteration internally, or to support a different access pattern
efficiently that only the Foreign Function API will use.

### Trying to Wrap Iterators (and Failing)

To wrap any type of iterator into the API correctly, the wrapper would need to
do what a C version of the code would do: erase the lifetime of the iterator,
and manage it manually.

Suffice it to say, this isincrediblydifficult.

Here is an illustration of justonepitfall.

A first version ofMySetWrapperwould look like this:

```rust
struct MySetWrapper {
    myset: MySet,
    iter_next: usize,
    // created from a transmuted Box<KeysIter + 'self>
    iterator: Option<NonNull<KeysIter<'static>>>,
}
```

Withtransmutebeing used to extend a lifetime, and a pointer to hide it, it’s
ugly already. But it gets even worse:any other operation can cause Rustundefined behaviour.

Consider that theMySetin the wrapper could be manipulated by other functions
during iteration, such as storing a new value to the key it was iterating over.
The API doesn’t discourage this, and in fact some similar C libraries expect it.

A simple implementation ofmyset_storewould be:

```rust
pub mod unsafe_module {

    // other module content

    pub fn myset_store(myset: *mut MySetWrapper, key: datum, value: datum) -> libc::c_int {
        // DO NOT USE THIS CODE. IT IS UNSAFE TO DEMONSTRATE A PROBLEM.

        let myset: &mut MySet = unsafe {
            // SAFETY: whoops, UB occurs in here!
            &mut (*myset).myset
        };

        /* ...check and cast key and value data... */

        match myset.store(casted_key, casted_value) {
            Ok(_) => 0,
            Err(e) => e.into(),
        }
    }
}
```

If the iterator exists when this function is called, we have violated one of
Rust’s aliasing rules. According to Rust, the mutable reference in this block
must haveexclusiveaccess to the object. If the iterator simply exists, it’s
not exclusive, so we haveundefined behaviour!1

To avoid this, we must have a way of ensuring that mutable reference really is
exclusive. That basically means clearing out the iterator’s shared reference
while it exists, and then reconstructing it. In most cases, that will still be
less efficient than the C version.

Some may ask: how can C do this more efficiently? The answer is, it cheats.
Rust’s aliasing rules are the problem, and C simply ignores them for its
pointers. In exchange, it is common to see code that is declared in the manual
as “not thread safe” under some or all circumstances. In fact, theGNU C libraryhas an entire lexicon dedicated to concurrent behavior!

Rust would rather make everything memory safe all the time, for both safety and
optimizations that C code cannot attain. Being denied access to certain
shortcuts is the price Rust programmers need to pay.

- For the C programmers out there scratching their heads, the iterator need
not be readduringthis code to cause the UB. The exclusivity rule also
enables compiler optimizations which may cause inconsistent observations by
the iterator’s shared reference (e.g. stack spills or reordering
instructions for efficiency). These observations may happenany time afterthe mutable reference is created.↩
For the C programmers out there scratching their heads, the iterator need
not be readduringthis code to cause the UB. The exclusivity rule also
enables compiler optimizations which may cause inconsistent observations by
the iterator’s shared reference (e.g. stack spills or reordering
instructions for efficiency). These observations may happenany time afterthe mutable reference is created.↩
