# Names

Source: https://doc.rust-lang.org/reference/

Anentityis a language construct that can be referred to in some way within
the source program, usually via apath. Entities includetypes,items,generic parameters,variable bindings,loop labels,lifetimes,fields,attributes, andlints.

Adeclarationis a syntactical construct that can introduce anameto
refer to an entity. Entity names are valid within ascopeâ a region of
source text where that name may be referenced.

Some entities areexplicitly declaredin the
source code, and some areimplicitly declaredas part of the language or compiler extensions.

Pathsare used to refer to an entity, possibly in another module or type.

Lifetimes and loop labels use adedicated syntaxusing a
leading quote.

Names are segregated into differentnamespaces, allowing entities in
different namespaces to share the same name without conflict.

Name resolutionis the compile-time process of tying paths, identifiers,
and labels to entity declarations.

Access to certain names may be restricted based on theirvisibility.

## Explicitly declared entities

Entities that explicitly introduce a name in the source code are:

- Items:Module declarationsExternal crate declarationsUse declarationsFunction declarationsandfunction parametersType aliasesstruct,union,enum, enum variant declarations, and their named
fieldsConstant item declarationsStatic item declarationsTrait item declarationsand theirassociated itemsExternal block itemsmacro_rulesdeclarationsandmatcher metavariablesImplementationassociated items
- Module declarations
- External crate declarations
- Use declarations
- Function declarationsandfunction parameters
- Type aliases
- struct,union,enum, enum variant declarations, and their named
fields
- Constant item declarations
- Static item declarations
- Trait item declarationsand theirassociated items
- External block items
- macro_rulesdeclarationsandmatcher metavariables
- Implementationassociated items
- Expressions:Closureparameterswhile letpattern bindingsforpattern bindingsif letpattern bindingsmatchpattern bindingsLoop labels
- Closureparameters
- while letpattern bindings
- forpattern bindings
- if letpattern bindings
- matchpattern bindings
- Loop labels
- Generic parameters
- Higher ranked trait bounds
- letstatementpattern bindings
- Themacro_useattributecan introduce macro names from another crate
- Themacro_exportattributecan introduce an alias for the macro into the crate root
Additionally,macro invocationsandattributescan introduce names by
expanding to one of the above items.

## Implicitly declared entities

The following entities are implicitly defined by the language, or are
introduced by compiler options and extensions:

- Language prelude:Boolean typeâboolTextual typesâcharandstrInteger typesâi8,i16,i32,i64,i128,u8,u16,u32,u64,u128Machine-dependent integer typesâusizeandisizefloating-point typesâf32andf64
- Boolean typeâbool
- Textual typesâcharandstr
- Integer typesâi8,i16,i32,i64,i128,u8,u16,u32,u64,u128
- Machine-dependent integer typesâusizeandisize
- floating-point typesâf32andf64
- Built-in attributes
- Standard library preludeitems, attributes, and macros
- Standard librarycrates in the root module
- External crateslinked by the compiler
- Tool attributes
- Lintsandtool lint attributes
- Derive helper attributesare valid within an item without being explicitly imported
- The'staticlifetime
Additionally, the crate root module does not have a name, but can be referred
to with certainpath qualifiersor aliases.
