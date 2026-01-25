#!/usr/bin/env python3
"""
Fetch and extract Rust API Guidelines chapters into separate markdown files.

Usage:
    python fetch_api_guidelines.py <output_dir>

Example:
    python fetch_api_guidelines.py ~/.claude/skills/rust-best-practices/reference/
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

BASE_URL = "https://rust-lang.github.io/api-guidelines/"

# Chapters to extract (in order)
CHAPTERS = [
    ("about.html", "apiguide_00_about.md", "About"),
    ("checklist.html", "apiguide_01_checklist.md", "Checklist"),
    ("naming.html", "apiguide_02_naming.md", "Naming"),
    ("interoperability.html", "apiguide_03_interoperability.md", "Interoperability"),
    ("macros.html", "apiguide_04_macros.md", "Macros"),
    ("documentation.html", "apiguide_05_documentation.md", "Documentation"),
    ("predictability.html", "apiguide_06_predictability.md", "Predictability"),
    ("flexibility.html", "apiguide_07_flexibility.md", "Flexibility"),
    ("type-safety.html", "apiguide_08_type_safety.md", "Type Safety"),
    ("dependability.html", "apiguide_09_dependability.md", "Dependability"),
    ("debuggability.html", "apiguide_10_debuggability.md", "Debuggability"),
    ("future-proofing.html", "apiguide_11_future_proofing.md", "Future Proofing"),
    ("necessities.html", "apiguide_12_necessities.md", "Necessities"),
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

    print(f"Fetching Rust API Guidelines to: {output_dir}")
    print(f"Found {len(CHAPTERS)} chapters to extract\n")

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
        except Exception as e:
            print(f"FAILED: {e}")

    print(f"\nDone! Files written to: {output_dir}")


if __name__ == "__main__":
    main()
