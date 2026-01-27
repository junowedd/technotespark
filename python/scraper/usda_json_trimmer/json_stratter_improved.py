#!/usr/bin/env python3
import json
import sys
from pathlib import Path

"""
json_stratter_improved.py

Pretty-print the structural hierarchy of a JSON file
into a readable tree format and write it to an output file.

Usage:
  python json_stratter_improved.py input.json output.txt
  python json_stratter_improved.py input.json output.txt --max-depth 5
"""

def write_structure(data, outfile, indent=0, max_depth=None):
    if max_depth is not None and indent >= max_depth:
        outfile.write("  " * indent + "...\n")
        return

    if isinstance(data, dict):
        for key, value in data.items():
            outfile.write("  " * indent + f"{key}\n")
            write_structure(value, outfile, indent + 1, max_depth)

    elif isinstance(data, list):
        outfile.write("  " * indent + "[list]\n")
        if data:
            write_structure(data[0], outfile, indent + 1, max_depth)


def main():
    if len(sys.argv) < 3:
        print("Usage: python json_stratter_improved.py <input.json> <output.txt> [--max-depth N]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    max_depth = None
    if "--max-depth" in sys.argv:
        idx = sys.argv.index("--max-depth")
        try:
            max_depth = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            print("--max-depth requires an integer value")
            sys.exit(1)

    with input_file.open() as f:
        data = json.load(f)

    with output_file.open("w", encoding="utf-8") as out:
        out.write(f"JSON Structure for: {input_file.name}\n")
        out.write("=" * 40 + "\n")
        write_structure(data, out, indent=0, max_depth=max_depth)

    print(f"Structure written to: {output_file}")


if __name__ == "__main__":
    main()
