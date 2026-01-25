# Items

Source: https://doc.rust-lang.org/reference/

SyntaxItemâÂ Â Â ÂOuterAttribute*(VisItem|MacroItem)

VisItemâÂ Â Â ÂVisibility?Â Â Â Â (Â Â Â Â Â Â Â ÂModuleÂ Â Â Â Â Â |ExternCrateÂ Â Â Â Â Â |UseDeclarationÂ Â Â Â Â Â |FunctionÂ Â Â Â Â Â |TypeAliasÂ Â Â Â Â Â |StructÂ Â Â Â Â Â |EnumerationÂ Â Â Â Â Â |UnionÂ Â Â Â Â Â |ConstantItemÂ Â Â Â Â Â |StaticItemÂ Â Â Â Â Â |TraitÂ Â Â Â Â Â |ImplementationÂ Â Â Â Â Â |ExternBlockÂ Â Â Â )

MacroItemâÂ Â Â Â Â ÂMacroInvocationSemiÂ Â Â Â |MacroRulesDefinition

Show Railroad

Anitemis a component of a crate. Items are organized within a crate by a
nested set ofmodules. Every crate has a single âoutermostâ anonymous module;
all further items within the crate havepathswithin the module tree of the
crate.

Items are entirely determined at compile-time, generally remain fixed during
execution, and may reside in read-only memory.

There are several kinds of items:

- modules
- extern cratedeclarations
- usedeclarations
- function definitions
- type definitions
- struct definitions
- enumeration definitions
- union definitions
- constant items
- static items
- trait definitions
- implementations
- externblocks
Items may be declared in theroot of the crate, amodule, or ablock expression.

A subset of items, calledassociated items, may be declared intraitsandimplementations.

A subset of items, called external items, may be declared inexternblocks.

Items may be defined in any order, with the exception ofmacro_ruleswhich has its own scoping behavior.

Name resolutionof item names allows items to be defined before or after where the item is referred to in the module or block.

Seeitem scopesfor information on the scoping rules of items.
