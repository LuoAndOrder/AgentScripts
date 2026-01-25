# Guiding Principles

Source: https://doc.rust-lang.org/nightly/style-guide/

# Guiding principles and rationale

When deciding on style guidelines, the style team follows these guiding
principles (in rough priority order):

- readabilityscan-abilityavoiding misleading formattingaccessibility - readable and editable by users using the widest
variety of hardware, including non-visual accessibility interfacesreadability of code in contexts without syntax highlighting or IDE
assistance, such as rustc error messages, diffs, grep, and other
plain-text contexts
readability

- scan-ability
- avoiding misleading formatting
- accessibility - readable and editable by users using the widest
variety of hardware, including non-visual accessibility interfaces
- readability of code in contexts without syntax highlighting or IDE
assistance, such as rustc error messages, diffs, grep, and other
plain-text contexts
- aestheticssense of âbeautyâconsistent with other languages/tools
aesthetics

- sense of âbeautyâ
- consistent with other languages/tools
- specificscompatibility with version control practices - preserving diffs,
merge-friendliness, etc.preventing rightward driftminimising vertical space
specifics

- compatibility with version control practices - preserving diffs,
merge-friendliness, etc.
- preventing rightward drift
- minimising vertical space
- applicationease of manual applicationease of implementation (inrustfmt, and in other tools/editors/code generators)internal consistencysimplicity of formatting rules
application

- ease of manual application
- ease of implementation (inrustfmt, and in other tools/editors/code generators)
- internal consistency
- simplicity of formatting rules
