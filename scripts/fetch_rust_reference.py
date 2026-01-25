#!/usr/bin/env python3
"""
Fetch and extract Rust Reference chapters into separate markdown files.

This extracts the top-level chapters of the Rust Reference. Due to the
large size of the reference (~95 pages), we focus on the main chapters
and skip deeply nested subsections.

Usage:
    python fetch_rust_reference.py <output_dir>

Example:
    python fetch_rust_reference.py ~/.claude/skills/rust-best-practices/reference/
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

BASE_URL = "https://doc.rust-lang.org/reference/"

# Top-level chapters to extract (focusing on most useful ones for best practices)
CHAPTERS = [
    ("introduction.html", "rustref_01_introduction.md", "Introduction"),
    ("notation.html", "rustref_02_notation.md", "Notation"),
    ("lexical-structure.html", "rustref_03_lexical_structure.md", "Lexical Structure"),
    ("macros.html", "rustref_04_macros.md", "Macros"),
    ("macros-by-example.html", "rustref_05_macros_by_example.md", "Macros by Example"),
    ("procedural-macros.html", "rustref_06_procedural_macros.md", "Procedural Macros"),
    ("crates-and-source-files.html", "rustref_07_crates.md", "Crates and Source Files"),
    ("conditional-compilation.html", "rustref_08_conditional_compilation.md", "Conditional Compilation"),
    ("items.html", "rustref_09_items.md", "Items"),
    ("attributes.html", "rustref_10_attributes.md", "Attributes"),
    ("statements-and-expressions.html", "rustref_11_statements_expressions.md", "Statements and Expressions"),
    ("patterns.html", "rustref_12_patterns.md", "Patterns"),
    ("type-system.html", "rustref_13_type_system.md", "Type System"),
    ("types.html", "rustref_14_types.md", "Types"),
    ("special-types-and-traits.html", "rustref_15_special_types_traits.md", "Special Types and Traits"),
    ("names.html", "rustref_16_names.md", "Names"),
    ("memory-model.html", "rustref_17_memory_model.md", "Memory Model"),
    ("panic.html", "rustref_18_panic.md", "Panic"),
    ("linkage.html", "rustref_19_linkage.md", "Linkage"),
    ("inline-assembly.html", "rustref_20_inline_assembly.md", "Inline Assembly"),
    ("unsafety.html", "rustref_21_unsafety.md", "Unsafety"),
    ("behavior-considered-undefined.html", "rustref_22_undefined_behavior.md", "Undefined Behavior"),
    ("const_eval.html", "rustref_23_const_eval.md", "Constant Evaluation"),
    ("abi.html", "rustref_24_abi.md", "Application Binary Interface"),
    ("runtime.html", "rustref_25_runtime.md", "The Rust Runtime"),
    ("destructors.html", "rustref_26_destructors.md", "Destructors"),
    ("lifetime-elision.html", "rustref_27_lifetime_elision.md", "Lifetime Elision"),
    ("trait-bounds.html", "rustref_28_trait_bounds.md", "Trait and Lifetime Bounds"),
    ("type-coercions.html", "rustref_29_type_coercions.md", "Type Coercions"),
    ("type-layout.html", "rustref_30_type_layout.md", "Type Layout"),
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

    print(f"Fetching Rust Reference to: {output_dir}")
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
