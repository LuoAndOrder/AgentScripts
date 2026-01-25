---
name: rust-best-practices
description: Pragmatic Rust guidelines for writing idiomatic, safe, and performant Rust code. Use when writing, reviewing, refactoring, or designing Rust APIs, error handling, unsafe code, FFI, async patterns, or library architecture.
---

# Rust Best Practices

A comprehensive collection of Rust guidelines from multiple authoritative sources. Load the relevant reference file(s) based on your current task.

## Sources

This skill includes content from 5 ebooks:

1. **Pragmatic Rust Guidelines** (pragmatic_*) - Microsoft's internal Rust guidelines
2. **Rust API Guidelines** (apiguide_*) - Official API design checklist
3. **Rust Style Guide** (styleguide_*) - Official formatting conventions
4. **The Rust Reference** (rustref_*) - Language specification and semantics
5. **Rust Design Patterns** (patterns_*) - Idiomatic patterns and anti-patterns

---

## Quick Reference: When to Load What

### Writing Code (General)
| Task | Primary Reference |
|------|-------------------|
| Naming conventions | [apiguide_02_naming.md](reference/apiguide_02_naming.md) |
| Code formatting | [styleguide_01_introduction.md](reference/styleguide_01_introduction.md) |
| General patterns | [pragmatic_08_universal_guidelines.md](reference/pragmatic_08_universal_guidelines.md) |
| Rust idioms | [patterns_02_idioms_index.md](reference/patterns_02_idioms_index.md) |

### API Design
| Task | Primary Reference |
|------|-------------------|
| API design checklist | [apiguide_01_checklist.md](reference/apiguide_01_checklist.md) |
| Type safety patterns | [apiguide_08_type_safety.md](reference/apiguide_08_type_safety.md) |
| Flexibility patterns | [apiguide_07_flexibility.md](reference/apiguide_07_flexibility.md) |
| Predictability | [apiguide_06_predictability.md](reference/apiguide_06_predictability.md) |
| Library UX design | [pragmatic_12_libraries_ux_guidelines.md](reference/pragmatic_12_libraries_ux_guidelines.md) |
| Future proofing | [apiguide_11_future_proofing.md](reference/apiguide_11_future_proofing.md) |

### Error Handling
| Task | Primary Reference |
|------|-------------------|
| Error types design | [apiguide_03_interoperability.md](reference/apiguide_03_interoperability.md) (C-GOOD-ERR) |
| Application errors | [pragmatic_02_application_guidelines.md](reference/pragmatic_02_application_guidelines.md) |
| Panic handling | [rustref_18_panic.md](reference/rustref_18_panic.md) |

### Type System
| Task | Primary Reference |
|------|-------------------|
| Type coercions | [rustref_29_type_coercions.md](reference/rustref_29_type_coercions.md) |
| Trait bounds | [rustref_28_trait_bounds.md](reference/rustref_28_trait_bounds.md) |
| Type layout | [rustref_30_type_layout.md](reference/rustref_30_type_layout.md) |
| Lifetime elision | [rustref_27_lifetime_elision.md](reference/rustref_27_lifetime_elision.md) |
| Special traits | [rustref_15_special_types_traits.md](reference/rustref_15_special_types_traits.md) |

### Unsafe Code & Safety
| Task | Primary Reference |
|------|-------------------|
| Safety guidelines | [pragmatic_07_safety_guidelines.md](reference/pragmatic_07_safety_guidelines.md) |
| Undefined behavior | [rustref_22_undefined_behavior.md](reference/rustref_22_undefined_behavior.md) |
| Unsafety overview | [rustref_21_unsafety.md](reference/rustref_21_unsafety.md) |
| Destructors | [rustref_26_destructors.md](reference/rustref_26_destructors.md) |

### FFI & Interop
| Task | Primary Reference |
|------|-------------------|
| FFI guidelines | [pragmatic_04_ffi_guidelines.md](reference/pragmatic_04_ffi_guidelines.md) |
| ABI details | [rustref_24_abi.md](reference/rustref_24_abi.md) |
| Linkage | [rustref_19_linkage.md](reference/rustref_19_linkage.md) |
| Inline assembly | [rustref_20_inline_assembly.md](reference/rustref_20_inline_assembly.md) |

### Macros
| Task | Primary Reference |
|------|-------------------|
| Macro design | [apiguide_04_macros.md](reference/apiguide_04_macros.md) |
| macro_rules! | [rustref_05_macros_by_example.md](reference/rustref_05_macros_by_example.md) |
| Proc macros | [rustref_06_procedural_macros.md](reference/rustref_06_procedural_macros.md) |

### Documentation
| Task | Primary Reference |
|------|-------------------|
| Doc comments | [apiguide_05_documentation.md](reference/apiguide_05_documentation.md) |
| Documentation patterns | [pragmatic_03_documentation.md](reference/pragmatic_03_documentation.md) |

### Performance
| Task | Primary Reference |
|------|-------------------|
| Performance guidelines | [pragmatic_06_performance_guidelines.md](reference/pragmatic_06_performance_guidelines.md) |
| Const evaluation | [rustref_23_const_eval.md](reference/rustref_23_const_eval.md) |

### Library Development
| Task | Primary Reference |
|------|-------------------|
| Building crates | [pragmatic_09_libraries_building_guidelines.md](reference/pragmatic_09_libraries_building_guidelines.md) |
| Interoperability | [pragmatic_10_libraries_interoperability_guidelines.md](reference/pragmatic_10_libraries_interoperability_guidelines.md) |
| Testing & resilience | [pragmatic_11_libraries_resilience_guidelines.md](reference/pragmatic_11_libraries_resilience_guidelines.md) |
| Release requirements | [apiguide_12_necessities.md](reference/apiguide_12_necessities.md) |

### Code Formatting
| Task | Primary Reference |
|------|-------------------|
| Module items | [styleguide_02_items.md](reference/styleguide_02_items.md) |
| Statements | [styleguide_03_statements.md](reference/styleguide_03_statements.md) |
| Expressions | [styleguide_04_expressions.md](reference/styleguide_04_expressions.md) |
| Types | [styleguide_05_types.md](reference/styleguide_05_types.md) |
| Cargo.toml | [styleguide_07_cargo.md](reference/styleguide_07_cargo.md) |

### Pattern Matching
| Task | Primary Reference |
|------|-------------------|
| Pattern syntax | [rustref_12_patterns.md](reference/rustref_12_patterns.md) |

### Conditional Compilation
| Task | Primary Reference |
|------|-------------------|
| cfg attributes | [rustref_08_conditional_compilation.md](reference/rustref_08_conditional_compilation.md) |

### Attributes
| Task | Primary Reference |
|------|-------------------|
| Attribute reference | [rustref_10_attributes.md](reference/rustref_10_attributes.md) |

### Design Patterns
| Task | Primary Reference |
|------|-------------------|
| Builder pattern | [patterns_29_builder.md](reference/patterns_29_builder.md) |
| Newtype pattern | [patterns_24_newtype.md](reference/patterns_24_newtype.md) |
| RAII guards | [patterns_25_raii.md](reference/patterns_25_raii.md) |
| Command pattern | [patterns_22_command.md](reference/patterns_22_command.md) |
| Strategy pattern | [patterns_26_strategy.md](reference/patterns_26_strategy.md) |
| Visitor pattern | [patterns_27_visitor.md](reference/patterns_27_visitor.md) |
| Fold pattern | [patterns_30_fold.md](reference/patterns_30_fold.md) |
| Compose structs | [patterns_32_compose_structs.md](reference/patterns_32_compose_structs.md) |

### Anti-patterns (What NOT to do)
| Task | Primary Reference |
|------|-------------------|
| Borrow checker workarounds | [patterns_40_borrow_clone.md](reference/patterns_40_borrow_clone.md) |
| deny(warnings) issues | [patterns_41_deny_warnings.md](reference/patterns_41_deny_warnings.md) |
| Deref polymorphism | [patterns_42_deref_polymorphism.md](reference/patterns_42_deref_polymorphism.md) |

### Functional Programming
| Task | Primary Reference |
|------|-------------------|
| FP paradigms in Rust | [patterns_44_paradigms.md](reference/patterns_44_paradigms.md) |
| Generics as type classes | [patterns_45_generics_type_classes.md](reference/patterns_45_generics_type_classes.md) |
| Functional optics | [patterns_46_optics.md](reference/patterns_46_optics.md) |

### FFI Patterns & Idioms
| Task | Primary Reference |
|------|-------------------|
| FFI error handling | [patterns_18_ffi_errors.md](reference/patterns_18_ffi_errors.md) |
| FFI string handling | [patterns_19_ffi_accepting_strings.md](reference/patterns_19_ffi_accepting_strings.md) |
| Object-based FFI APIs | [patterns_37_ffi_export.md](reference/patterns_37_ffi_export.md) |
| FFI type wrappers | [patterns_38_ffi_wrappers.md](reference/patterns_38_ffi_wrappers.md) |

---

## Key Guidelines Summary

### Error Handling
- Libraries: Use canonical error structs with `Backtrace` (M-ERRORS-CANONICAL-STRUCTS)
- Applications: May use `anyhow`/`eyre` (M-APP-ERROR)
- Panics mean "stop the program" - not for error propagation (M-PANIC-IS-STOP)

### Safety
- `unsafe` only for: novel abstractions, performance (after benchmarking), or FFI (M-UNSAFE)
- All code must be sound - no exceptions (M-UNSOUND)
- `unsafe` marker only for UB risk, not "dangerous" operations (M-UNSAFE-IMPLIES-UB)

### API Design (Rust API Guidelines)
- C-COMMON-TRAITS: Types eagerly implement common traits (Copy, Clone, Eq, Debug, etc.)
- C-CONV-TRAITS: Use From, AsRef, AsMut for conversions
- C-NEWTYPE: Newtypes provide static distinctions
- C-BUILDER: Builders enable construction of complex values
- C-VALIDATE: Functions validate their arguments
- C-SEALED: Sealed traits protect against downstream implementations

### Formatting (Rust Style Guide)
- Indent with 4 spaces, no tabs
- Max line width: 100 characters
- Use trailing commas when followed by newlines
- Prefer line comments (`//`) over block comments

### Performance
- Identify hot paths early, create benchmarks (M-HOTPATH)
- Long-running async tasks need yield points (M-YIELD-POINTS)
- Use mimalloc for applications (M-MIMALLOC-APPS)

### Libraries
- Features must be additive (M-FEATURES-ADDITIVE)
- Libraries must work out of the box on Tier 1 platforms (M-OOBE)
- Don't leak external types in public APIs (M-DONT-LEAK-TYPES)
- Public futures must be `Send` (M-TYPES-SEND)

---

## All Reference Files

### Pragmatic Rust Guidelines (Microsoft)
- [pragmatic_01_ai_guidelines.md](reference/pragmatic_01_ai_guidelines.md) - AI/agent code patterns
- [pragmatic_02_application_guidelines.md](reference/pragmatic_02_application_guidelines.md) - Application-level code
- [pragmatic_03_documentation.md](reference/pragmatic_03_documentation.md) - Documentation standards
- [pragmatic_04_ffi_guidelines.md](reference/pragmatic_04_ffi_guidelines.md) - FFI and C interop
- [pragmatic_06_performance_guidelines.md](reference/pragmatic_06_performance_guidelines.md) - Performance optimization
- [pragmatic_07_safety_guidelines.md](reference/pragmatic_07_safety_guidelines.md) - Unsafe code and soundness
- [pragmatic_08_universal_guidelines.md](reference/pragmatic_08_universal_guidelines.md) - General patterns
- [pragmatic_09_libraries_building_guidelines.md](reference/pragmatic_09_libraries_building_guidelines.md) - Crate structure
- [pragmatic_10_libraries_interoperability_guidelines.md](reference/pragmatic_10_libraries_interoperability_guidelines.md) - Type leaking, Send/Sync
- [pragmatic_11_libraries_resilience_guidelines.md](reference/pragmatic_11_libraries_resilience_guidelines.md) - Testing, mocking
- [pragmatic_12_libraries_ux_guidelines.md](reference/pragmatic_12_libraries_ux_guidelines.md) - API design, builders

### Rust API Guidelines (Official)
- [apiguide_00_about.md](reference/apiguide_00_about.md) - About the guidelines
- [apiguide_01_checklist.md](reference/apiguide_01_checklist.md) - Quick reference checklist
- [apiguide_02_naming.md](reference/apiguide_02_naming.md) - Naming conventions
- [apiguide_03_interoperability.md](reference/apiguide_03_interoperability.md) - Traits and conversions
- [apiguide_04_macros.md](reference/apiguide_04_macros.md) - Macro design
- [apiguide_05_documentation.md](reference/apiguide_05_documentation.md) - Documentation
- [apiguide_06_predictability.md](reference/apiguide_06_predictability.md) - Predictable APIs
- [apiguide_07_flexibility.md](reference/apiguide_07_flexibility.md) - Flexible APIs
- [apiguide_08_type_safety.md](reference/apiguide_08_type_safety.md) - Type safety patterns
- [apiguide_09_dependability.md](reference/apiguide_09_dependability.md) - Reliable APIs
- [apiguide_10_debuggability.md](reference/apiguide_10_debuggability.md) - Debug support
- [apiguide_11_future_proofing.md](reference/apiguide_11_future_proofing.md) - Future compatibility
- [apiguide_12_necessities.md](reference/apiguide_12_necessities.md) - Release requirements

### Rust Style Guide (Official)
- [styleguide_01_introduction.md](reference/styleguide_01_introduction.md) - Style overview
- [styleguide_02_items.md](reference/styleguide_02_items.md) - Module items
- [styleguide_03_statements.md](reference/styleguide_03_statements.md) - Statements
- [styleguide_04_expressions.md](reference/styleguide_04_expressions.md) - Expressions
- [styleguide_05_types.md](reference/styleguide_05_types.md) - Types and bounds
- [styleguide_06_advice.md](reference/styleguide_06_advice.md) - Other advice
- [styleguide_07_cargo.md](reference/styleguide_07_cargo.md) - Cargo.toml conventions
- [styleguide_08_principles.md](reference/styleguide_08_principles.md) - Guiding principles
- [styleguide_09_editions.md](reference/styleguide_09_editions.md) - Style editions
- [styleguide_10_nightly.md](reference/styleguide_10_nightly.md) - Nightly syntax

### The Rust Reference (Official)
- [rustref_01_introduction.md](reference/rustref_01_introduction.md) - Introduction
- [rustref_02_notation.md](reference/rustref_02_notation.md) - Notation
- [rustref_03_lexical_structure.md](reference/rustref_03_lexical_structure.md) - Lexical structure
- [rustref_04_macros.md](reference/rustref_04_macros.md) - Macros overview
- [rustref_05_macros_by_example.md](reference/rustref_05_macros_by_example.md) - macro_rules!
- [rustref_06_procedural_macros.md](reference/rustref_06_procedural_macros.md) - Proc macros
- [rustref_07_crates.md](reference/rustref_07_crates.md) - Crates and source files
- [rustref_08_conditional_compilation.md](reference/rustref_08_conditional_compilation.md) - cfg attributes
- [rustref_09_items.md](reference/rustref_09_items.md) - Items overview
- [rustref_10_attributes.md](reference/rustref_10_attributes.md) - Attributes
- [rustref_11_statements_expressions.md](reference/rustref_11_statements_expressions.md) - Statements/expressions
- [rustref_12_patterns.md](reference/rustref_12_patterns.md) - Pattern matching
- [rustref_13_type_system.md](reference/rustref_13_type_system.md) - Type system overview
- [rustref_14_types.md](reference/rustref_14_types.md) - Types
- [rustref_15_special_types_traits.md](reference/rustref_15_special_types_traits.md) - Special types
- [rustref_16_names.md](reference/rustref_16_names.md) - Names and namespaces
- [rustref_17_memory_model.md](reference/rustref_17_memory_model.md) - Memory model
- [rustref_18_panic.md](reference/rustref_18_panic.md) - Panic handling
- [rustref_19_linkage.md](reference/rustref_19_linkage.md) - Linkage
- [rustref_20_inline_assembly.md](reference/rustref_20_inline_assembly.md) - Inline assembly
- [rustref_21_unsafety.md](reference/rustref_21_unsafety.md) - Unsafety
- [rustref_22_undefined_behavior.md](reference/rustref_22_undefined_behavior.md) - Undefined behavior
- [rustref_23_const_eval.md](reference/rustref_23_const_eval.md) - Const evaluation
- [rustref_24_abi.md](reference/rustref_24_abi.md) - ABI
- [rustref_25_runtime.md](reference/rustref_25_runtime.md) - Rust runtime
- [rustref_26_destructors.md](reference/rustref_26_destructors.md) - Destructors
- [rustref_27_lifetime_elision.md](reference/rustref_27_lifetime_elision.md) - Lifetime elision
- [rustref_28_trait_bounds.md](reference/rustref_28_trait_bounds.md) - Trait bounds
- [rustref_29_type_coercions.md](reference/rustref_29_type_coercions.md) - Type coercions
- [rustref_30_type_layout.md](reference/rustref_30_type_layout.md) - Type layout

### Rust Design Patterns (Community)
**Idioms:**
- [patterns_01_intro.md](reference/patterns_01_intro.md) - Introduction
- [patterns_02_idioms_index.md](reference/patterns_02_idioms_index.md) - Idioms overview
- [patterns_03_coercion_arguments.md](reference/patterns_03_coercion_arguments.md) - Use borrowed types for arguments
- [patterns_04_concat_format.md](reference/patterns_04_concat_format.md) - Concatenating strings with format!
- [patterns_05_constructor.md](reference/patterns_05_constructor.md) - Constructor idiom
- [patterns_06_default_trait.md](reference/patterns_06_default_trait.md) - The Default trait
- [patterns_07_deref.md](reference/patterns_07_deref.md) - Collections are smart pointers
- [patterns_08_dtor_finally.md](reference/patterns_08_dtor_finally.md) - Finalisation in destructors
- [patterns_09_mem_replace.md](reference/patterns_09_mem_replace.md) - mem::take and mem::replace
- [patterns_10_on_stack_dispatch.md](reference/patterns_10_on_stack_dispatch.md) - On-stack dynamic dispatch
- [patterns_11_option_iter.md](reference/patterns_11_option_iter.md) - Iterating over an Option
- [patterns_12_closure_vars.md](reference/patterns_12_closure_vars.md) - Pass variables to closure
- [patterns_13_priv_extend.md](reference/patterns_13_priv_extend.md) - Privacy for extensibility
- [patterns_14_rustdoc_init.md](reference/patterns_14_rustdoc_init.md) - Easy doc initialization
- [patterns_15_temp_mutability.md](reference/patterns_15_temp_mutability.md) - Temporary mutability
- [patterns_16_return_consumed.md](reference/patterns_16_return_consumed.md) - Return consumed arg on error

**FFI Idioms:**
- [patterns_17_ffi_idioms_intro.md](reference/patterns_17_ffi_idioms_intro.md) - FFI idioms intro
- [patterns_18_ffi_errors.md](reference/patterns_18_ffi_errors.md) - Idiomatic FFI errors
- [patterns_19_ffi_accepting_strings.md](reference/patterns_19_ffi_accepting_strings.md) - Accepting strings in FFI
- [patterns_20_ffi_passing_strings.md](reference/patterns_20_ffi_passing_strings.md) - Passing strings in FFI

**Behavioural Patterns:**
- [patterns_21_behavioural_intro.md](reference/patterns_21_behavioural_intro.md) - Behavioural patterns intro
- [patterns_22_command.md](reference/patterns_22_command.md) - Command pattern
- [patterns_23_interpreter.md](reference/patterns_23_interpreter.md) - Interpreter pattern
- [patterns_24_newtype.md](reference/patterns_24_newtype.md) - Newtype pattern
- [patterns_25_raii.md](reference/patterns_25_raii.md) - RAII guards
- [patterns_26_strategy.md](reference/patterns_26_strategy.md) - Strategy pattern
- [patterns_27_visitor.md](reference/patterns_27_visitor.md) - Visitor pattern

**Creational Patterns:**
- [patterns_28_creational_intro.md](reference/patterns_28_creational_intro.md) - Creational patterns intro
- [patterns_29_builder.md](reference/patterns_29_builder.md) - Builder pattern
- [patterns_30_fold.md](reference/patterns_30_fold.md) - Fold pattern

**Structural Patterns:**
- [patterns_31_structural_intro.md](reference/patterns_31_structural_intro.md) - Structural patterns intro
- [patterns_32_compose_structs.md](reference/patterns_32_compose_structs.md) - Compose structs
- [patterns_33_small_crates.md](reference/patterns_33_small_crates.md) - Prefer small crates
- [patterns_34_unsafe_mods.md](reference/patterns_34_unsafe_mods.md) - Contain unsafety in small modules
- [patterns_35_trait_bounds.md](reference/patterns_35_trait_bounds.md) - Custom traits for type bounds

**FFI Patterns:**
- [patterns_36_ffi_patterns_intro.md](reference/patterns_36_ffi_patterns_intro.md) - FFI patterns intro
- [patterns_37_ffi_export.md](reference/patterns_37_ffi_export.md) - Object-based APIs
- [patterns_38_ffi_wrappers.md](reference/patterns_38_ffi_wrappers.md) - Type consolidation wrappers

**Anti-patterns:**
- [patterns_39_anti_index.md](reference/patterns_39_anti_index.md) - Anti-patterns intro
- [patterns_40_borrow_clone.md](reference/patterns_40_borrow_clone.md) - Clone to satisfy borrow checker
- [patterns_41_deny_warnings.md](reference/patterns_41_deny_warnings.md) - deny(warnings) anti-pattern
- [patterns_42_deref_polymorphism.md](reference/patterns_42_deref_polymorphism.md) - Deref polymorphism

**Functional Programming:**
- [patterns_43_functional_index.md](reference/patterns_43_functional_index.md) - Functional programming intro
- [patterns_44_paradigms.md](reference/patterns_44_paradigms.md) - Programming paradigms
- [patterns_45_generics_type_classes.md](reference/patterns_45_generics_type_classes.md) - Generics as type classes
- [patterns_46_optics.md](reference/patterns_46_optics.md) - Functional optics

**Additional Resources:**
- [patterns_47_resources_index.md](reference/patterns_47_resources_index.md) - Additional resources
- [patterns_48_design_principles.md](reference/patterns_48_design_principles.md) - Design principles
