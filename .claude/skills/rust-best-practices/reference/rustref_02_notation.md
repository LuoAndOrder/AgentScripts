# Notation

Source: https://doc.rust-lang.org/reference/

## Grammar

The following notations are used by theLexerandSyntaxgrammar snippets:

Sequences have a higher precedence than|alternation.

### String table productions

Some rules in the grammar â notablyunary operators,binary
operators, andkeywordsâ are given in a simplified form: as a listing
of printable strings. These cases form a subset of the rules regarding thetokenrule, and are assumed to be the result of a lexical-analysis
phase feeding the parser, driven by aDFA, operating over the disjunction of all such string table
entries.

When such a string inmonospacefont occurs inside the grammar,
it is an implicit reference to a single member of such a string table
production. Seetokensfor more information.

### Grammar visualizations

Below each grammar block is a button to toggle the display of asyntax diagram. A square element is a non-terminal rule, and a rounded rectangle is a terminal.
