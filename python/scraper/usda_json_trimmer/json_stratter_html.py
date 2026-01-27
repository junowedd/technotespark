#!/usr/bin/env python3
import json
import sys
from pathlib import Path

"""
json_stratter_html.py

Generate an interactive HTML tree view of a JSON structure.

Usage:
  python json_stratter_html.py input.json output.html
"""

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JSON Structure Viewer</title>
<style>
  body {
    font-family: Arial, sans-serif;
    margin: 40px;
  }
  ul {
    list-style-type: none;
    margin-left: 20px;
    padding-left: 20px;
    border-left: 1px solid #ccc;
  }
  li {
    margin: 4px 0;
  }
  .list {
    color: #555;
    font-style: italic;
  }
</style>
</head>
<body>
<h1>JSON Structure</h1>
"""

HTML_FOOTER = """
</body>
</html>
"""

def render_html(data, out):
    if isinstance(data, dict):
        out.write("<ul>")
        for key, value in data.items():
            out.write(f"<li><strong>{key}</strong>")
            render_html(value, out)
            out.write("</li>")
        out.write("</ul>")
    elif isinstance(data, list):
        out.write("<ul><li class='list'>[list]</li>")
        if data:
            render_html(data[0], out)
        out.write("</ul>")


def main():
    if len(sys.argv) != 3:
        print("Usage: python json_stratter_html.py <input.json> <output.html>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    with input_file.open() as f:
        data = json.load(f)

    with output_file.open("w", encoding="utf-8") as out:
        out.write(HTML_HEADER)
        render_html(data, out)
        out.write(HTML_FOOTER)

    print(f"HTML tree written to: {output_file}")


if __name__ == "__main__":
    main()
