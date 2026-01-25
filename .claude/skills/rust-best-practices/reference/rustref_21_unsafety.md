# Unsafety

Source: https://doc.rust-lang.org/reference/

Unsafe operations are those that can potentially violate the memory-safety
guarantees of Rustâs static semantics.

The following language level features cannot be used in the safe subset of
Rust:

- Dereferencing araw pointer.
- Reading or writing amutableor unsafeexternalstatic variable.
- Accessing a field of aunion, other than to assign to it.
- Calling an unsafe function.
- Calling a safe function marked with atarget_featurefrom a function that does not have atarget_featureattribute enabling the same features (seeattributes.codegen.target_feature.safety-restrictions).
- Implementing anunsafe trait.
- Declaring anexternblock1.
- Applying anunsafe attributeto an item.
- Prior to the 2024 edition, extern blocks were allowed to be declared withoutunsafe.â©
Prior to the 2024 edition, extern blocks were allowed to be declared withoutunsafe.â©
