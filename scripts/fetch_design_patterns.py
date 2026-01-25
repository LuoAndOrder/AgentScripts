#!/usr/bin/env python3
"""
Fetch and extract Rust Design Patterns chapters into separate markdown files.

Usage:
    python fetch_design_patterns.py <output_dir>

Example:
    python fetch_design_patterns.py ~/.claude/skills/rust-best-practices/reference/
"""

import re
import sys
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: This script requires 'requests' and 'beautifulsoup4' packages.")
    print("Install with: pip install requests beautifulsoup4")
    sys.exit(1)

BASE_URL = "https://rust-unofficial.github.io/patterns/"

# Chapters to extract (grouped by category)
CHAPTERS = [
    # Introduction
    ("intro.html", "patterns_01_intro.md", "Introduction"),

    # Idioms
    ("idioms/index.html", "patterns_02_idioms_index.md", "Idioms"),
    ("idioms/coercion-arguments.html", "patterns_03_coercion_arguments.md", "Use Borrowed Types for Arguments"),
    ("idioms/concat-format.html", "patterns_04_concat_format.md", "Concatenating Strings with format!"),
    ("idioms/ctor.html", "patterns_05_constructor.md", "Constructor"),
    ("idioms/default.html", "patterns_06_default_trait.md", "The Default Trait"),
    ("idioms/deref.html", "patterns_07_deref.md", "Collections Are Smart Pointers"),
    ("idioms/dtor-finally.html", "patterns_08_dtor_finally.md", "Finalisation in Destructors"),
    ("idioms/mem-replace.html", "patterns_09_mem_replace.md", "mem::take and mem::replace"),
    ("idioms/on-stack-dyn-dispatch.html", "patterns_10_on_stack_dispatch.md", "On-Stack Dynamic Dispatch"),
    ("idioms/option-iter.html", "patterns_11_option_iter.md", "Iterating over an Option"),
    ("idioms/pass-var-to-closure.html", "patterns_12_closure_vars.md", "Pass Variables to Closure"),
    ("idioms/priv-extend.html", "patterns_13_priv_extend.md", "Privacy For Extensibility"),
    ("idioms/rustdoc-init.html", "patterns_14_rustdoc_init.md", "Easy Doc Initialization"),
    ("idioms/temporary-mutability.html", "patterns_15_temp_mutability.md", "Temporary Mutability"),
    ("idioms/return-consumed-arg-on-error.html", "patterns_16_return_consumed.md", "Return Consumed Arg on Error"),

    # FFI Idioms
    ("idioms/ffi/intro.html", "patterns_17_ffi_idioms_intro.md", "FFI Idioms"),
    ("idioms/ffi/errors.html", "patterns_18_ffi_errors.md", "FFI Idiomatic Errors"),
    ("idioms/ffi/accepting-strings.html", "patterns_19_ffi_accepting_strings.md", "FFI Accepting Strings"),
    ("idioms/ffi/passing-strings.html", "patterns_20_ffi_passing_strings.md", "FFI Passing Strings"),

    # Behavioural Patterns
    ("patterns/behavioural/intro.html", "patterns_21_behavioural_intro.md", "Behavioural Patterns"),
    ("patterns/behavioural/command.html", "patterns_22_command.md", "Command Pattern"),
    ("patterns/behavioural/interpreter.html", "patterns_23_interpreter.md", "Interpreter Pattern"),
    ("patterns/behavioural/newtype.html", "patterns_24_newtype.md", "Newtype Pattern"),
    ("patterns/behavioural/RAII.html", "patterns_25_raii.md", "RAII Guards"),
    ("patterns/behavioural/strategy.html", "patterns_26_strategy.md", "Strategy Pattern"),
    ("patterns/behavioural/visitor.html", "patterns_27_visitor.md", "Visitor Pattern"),

    # Creational Patterns
    ("patterns/creational/intro.html", "patterns_28_creational_intro.md", "Creational Patterns"),
    ("patterns/creational/builder.html", "patterns_29_builder.md", "Builder Pattern"),
    ("patterns/creational/fold.html", "patterns_30_fold.md", "Fold Pattern"),

    # Structural Patterns
    ("patterns/structural/intro.html", "patterns_31_structural_intro.md", "Structural Patterns"),
    ("patterns/structural/compose-structs.html", "patterns_32_compose_structs.md", "Compose Structs"),
    ("patterns/structural/small-crates.html", "patterns_33_small_crates.md", "Prefer Small Crates"),
    ("patterns/structural/unsafe-mods.html", "patterns_34_unsafe_mods.md", "Contain Unsafety in Small Modules"),
    ("patterns/structural/trait-for-bounds.html", "patterns_35_trait_bounds.md", "Custom Traits for Type Bounds"),

    # FFI Patterns
    ("patterns/ffi/intro.html", "patterns_36_ffi_patterns_intro.md", "FFI Patterns"),
    ("patterns/ffi/export.html", "patterns_37_ffi_export.md", "Object-Based APIs"),
    ("patterns/ffi/wrappers.html", "patterns_38_ffi_wrappers.md", "Type Consolidation into Wrappers"),

    # Anti-patterns
    ("anti_patterns/index.html", "patterns_39_anti_index.md", "Anti-patterns"),
    ("anti_patterns/borrow_clone.html", "patterns_40_borrow_clone.md", "Clone to Satisfy Borrow Checker"),
    ("anti_patterns/deny-warnings.html", "patterns_41_deny_warnings.md", "deny(warnings) Anti-pattern"),
    ("anti_patterns/deref.html", "patterns_42_deref_polymorphism.md", "Deref Polymorphism Anti-pattern"),

    # Functional Programming
    ("functional/index.html", "patterns_43_functional_index.md", "Functional Programming"),
    ("functional/paradigms.html", "patterns_44_paradigms.md", "Programming Paradigms"),
    ("functional/generics-type-classes.html", "patterns_45_generics_type_classes.md", "Generics as Type Classes"),
    ("functional/optics.html", "patterns_46_optics.md", "Functional Optics"),

    # Additional Resources
    ("additional_resources/index.html", "patterns_47_resources_index.md", "Additional Resources"),
    ("additional_resources/design-principles.html", "patterns_48_design_principles.md", "Design Principles"),
]


def fetch_page(url: str) -> str:
    """Fetch a page and return its HTML content."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def extract_content(html: str, title: str) -> str:
    """Extract main content from HTML and convert to markdown-like format."""
    soup = BeautifulSoup(html, "html.parser")

    # Find the main content area
    main = soup.find("main") or soup.find("div", {"id": "content"})
    if not main:
        return ""

    # Remove navigation elements
    for nav in main.find_all(["nav", "script", "style"]):
        nav.decompose()

    # Convert to text, preserving structure
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"Source: {BASE_URL}")
    lines.append("")

    for element in main.descendants:
        if element.name == "h1":
            text = element.get_text(strip=True)
            if text and text != title:
                lines.append(f"\n# {text}\n")
        elif element.name == "h2":
            text = element.get_text(strip=True)
            if text:
                lines.append(f"\n## {text}\n")
        elif element.name == "h3":
            text = element.get_text(strip=True)
            if text:
                lines.append(f"\n### {text}\n")
        elif element.name == "h4":
            text = element.get_text(strip=True)
            if text:
                lines.append(f"\n#### {text}\n")
        elif element.name == "p":
            text = element.get_text(strip=True)
            if text:
                lines.append(f"{text}\n")
        elif element.name == "pre":
            code = element.get_text()
            lang = "rust"
            if element.find("code"):
                classes = element.find("code").get("class", [])
                for cls in classes:
                    if cls.startswith("language-"):
                        lang = cls.replace("language-", "")
            lines.append(f"\n```{lang}")
            lines.append(code.rstrip())
            lines.append("```\n")
        elif element.name == "li":
            # Only process direct text, not nested elements
            if element.parent.name in ["ul", "ol"]:
                text = element.get_text(strip=True)
                if text and len(text) < 500:  # Skip overly long items
                    lines.append(f"- {text}")
        elif element.name == "blockquote":
            text = element.get_text(strip=True)
            if text:
                quoted = "\n".join(f"> {line}" for line in text.split("\n"))
                lines.append(f"\n{quoted}\n")

    content = "\n".join(lines)

    # Clean up multiple blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    return content.strip() + "\n"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    output_dir = Path(sys.argv[1]).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching Rust Design Patterns to: {output_dir}")
    print(f"Found {len(CHAPTERS)} chapters to extract\n")

    success_count = 0
    for html_file, output_file, title in CHAPTERS:
        url = BASE_URL + html_file
        print(f"  Fetching {title}... ", end="", flush=True)

        try:
            html = fetch_page(url)
            content = extract_content(html, title)

            output_path = output_dir / output_file
            output_path.write_text(content, encoding="utf-8")

            line_count = len(content.split("\n"))
            print(f"OK ({line_count} lines)")
            success_count += 1
        except Exception as e:
            print(f"FAILED: {e}")

    print(f"\nDone! {success_count}/{len(CHAPTERS)} files written to: {output_dir}")


if __name__ == "__main__":
    main()
