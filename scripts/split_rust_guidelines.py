#!/usr/bin/env python3
"""
Split the Pragmatic Rust Guidelines all.txt into separate chapter files.

Usage:
    python split_rust_guidelines.py <input_file> <output_dir>

Example:
    python split_rust_guidelines.py ~/Downloads/all.txt ~/.claude/skills/rust-best-practices/reference/
"""

import re
import sys
from pathlib import Path

# Define the sections in order with their output filenames
# Format: (header_pattern, output_filename)
SECTIONS = [
    ("# AI Guidelines", "01_ai_guidelines.md"),
    ("# Application Guidelines", "02_application_guidelines.md"),
    ("# Documentation", "03_documentation.md"),
    ("# FFI Guidelines", "04_ffi_guidelines.md"),
    ("# Library Guidelines", "05_library_guidelines.md"),
    ("# Performance Guidelines", "06_performance_guidelines.md"),
    ("# Safety Guidelines", "07_safety_guidelines.md"),
    ("# Universal Guidelines", "08_universal_guidelines.md"),
    ("# Libraries / Building Guidelines", "09_libraries_building_guidelines.md"),
    ("# Libraries / Interoperability Guidelines", "10_libraries_interoperability_guidelines.md"),
    ("# Libraries / Resilience Guidelines", "11_libraries_resilience_guidelines.md"),
    ("# Libraries / UX Guidelines", "12_libraries_ux_guidelines.md"),
]


def find_section_boundaries(content: str) -> list[tuple[str, int, int]]:
    """
    Find the start and end positions of each section.
    Returns list of (filename, start_pos, end_pos).
    """
    boundaries = []

    for i, (header, filename) in enumerate(SECTIONS):
        # Find the header position
        pattern = re.compile(r'^' + re.escape(header) + r'\s*$', re.MULTILINE)
        match = pattern.search(content)

        if match:
            start_pos = match.start()
            boundaries.append((filename, header, start_pos))

    # Sort by position
    boundaries.sort(key=lambda x: x[2])

    # Calculate end positions (start of next section or end of file)
    result = []
    for i, (filename, header, start_pos) in enumerate(boundaries):
        if i + 1 < len(boundaries):
            end_pos = boundaries[i + 1][2]
        else:
            end_pos = len(content)
        result.append((filename, start_pos, end_pos))

    return result


def clean_content(content: str) -> str:
    """
    Clean up the content:
    - Remove image references (they won't work in the skill)
    - Convert custom HTML-ish tags to markdown
    - Strip trailing whitespace
    """
    # Remove image references like ![TEXT](filename.png)
    content = re.sub(r'!\[TEXT\]\([^)]+\.png\)', '', content)

    # Convert <why>...</why> to **Why:** ...
    content = re.sub(r'<why>([^<]+)</why>', r'**Why:** \1', content)

    # Convert <version>...</version> to nothing (or could keep as metadata)
    content = re.sub(r'<version>[^<]+</version>', '', content)

    # Convert <tip></tip> to **Tip:**
    content = re.sub(r'<tip></tip>', '**Tip:**', content)

    # Convert <alert></alert> to **Warning:**
    content = re.sub(r'<alert></alert>', '**Warning:**', content)

    # Remove <footnotes>...</footnotes> tags but keep content
    content = re.sub(r'</?footnotes>', '', content)

    # Remove <div> tags but keep content
    content = re.sub(r'<div[^>]*>', '', content)
    content = re.sub(r'</div>', '', content)

    # Clean up multiple blank lines (more than 2 -> 2)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # Remove trailing whitespace from lines
    content = '\n'.join(line.rstrip() for line in content.split('\n'))

    # Strip leading/trailing whitespace from the whole content
    content = content.strip()

    return content


def extract_section(content: str, start: int, end: int) -> str:
    """Extract and clean a section."""
    section = content[start:end]

    # Remove the leading --- separator if present at the very start
    section = section.lstrip()
    if section.startswith('---'):
        section = section[3:].lstrip()

    # Remove trailing --- separator
    section = section.rstrip()
    if section.endswith('---'):
        section = section[:-3].rstrip()

    return clean_content(section)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    input_file = Path(sys.argv[1]).expanduser()
    output_dir = Path(sys.argv[2]).expanduser()

    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read the input file
    content = input_file.read_text(encoding='utf-8')

    # Find section boundaries
    boundaries = find_section_boundaries(content)

    print(f"Found {len(boundaries)} sections:")

    # Extract and write each section
    for filename, start, end in boundaries:
        section_content = extract_section(content, start, end)

        # Skip empty sections (like "Library Guidelines" which is just a header)
        if len(section_content.strip().split('\n')) <= 2:
            print(f"  Skipping {filename} (empty section)")
            continue

        output_path = output_dir / filename
        output_path.write_text(section_content + '\n', encoding='utf-8')

        # Count lines for reporting
        line_count = len(section_content.split('\n'))
        print(f"  {filename}: {line_count} lines")

    print(f"\nFiles written to: {output_dir}")


if __name__ == "__main__":
    main()
