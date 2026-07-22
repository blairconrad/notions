"""Convert one or more Markdown files to standalone HTML with Mermaid diagram support.

Usage:
    md2html file.md [file2.md ...]
    md2html file.md -o output.html

Output is written alongside the source file with a .html extension unless -o is given.
Mermaid fenced code blocks are rendered via CDN.
"""

import argparse
import html
import pathlib
import re
import sys

import markdown

CSS = """
body { font-family: sans-serif; max-width: 960px; margin: 2em auto; line-height: 1.6; color: #222; }
h1, h2, h3, h4, h5, h6 { margin-top: 1.4em; }
code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-size: 0.92em; }
pre { background: #f4f4f4; padding: 1em; overflow: auto; border-radius: 4px; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; margin: 1em 0; }
td, th { border: 1px solid #ccc; padding: 0.4em 0.8em; }
th { background: #f0f0f0; }
blockquote { border-left: 4px solid #ccc; margin: 0; padding: 0.2em 1em; color: #555; }
.mermaid { text-align: center; margin: 1.5em 0; }
"""

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"


def md_to_html(md_text: str, title: str = "") -> str:
    body = markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "toc", "pymdownx.tilde"],
    )

    def replace_mermaid(m: re.Match) -> str:
        return f'<div class="mermaid">\n{html.unescape(m.group(1))}\n</div>'

    body = re.sub(
        r'<code class="language-mermaid">(.*?)</code>',
        replace_mermaid,
        body,
        flags=re.DOTALL,
    )
    body = re.sub(
        r'<pre>\s*(<div class="mermaid">.*?</div>)\s*</pre>',
        r"\1",
        body,
        flags=re.DOTALL,
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
  <script src="{MERMAID_CDN}"></script>
</head>
<body>
{body}
</body>
</html>"""


def convert(src: pathlib.Path, dst: pathlib.Path) -> None:
    md_text = src.read_text(encoding="utf-8")
    title = src.stem.replace("-", " ").replace("_", " ")
    output = md_to_html(md_text, title=title)
    dst.write_text(output, encoding="utf-8")
    print(f"  {src} -> {dst}")


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Markdown file(s) to standalone HTML with Mermaid support."
    )
    parser.add_argument("inputs", nargs="+", metavar="FILE.md", help="Input Markdown file(s)")
    parser.add_argument("-o", "--output", metavar="FILE.html",
                        help="Output path (only valid when a single input file is given)")
    args = parser.parse_args()

    if args.output and len(args.inputs) > 1:
        print("error: -o/--output can only be used with a single input file", file=sys.stderr)
        sys.exit(1)

    for src_str in args.inputs:
        src = pathlib.Path(src_str)
        if not src.exists():
            print(f"error: file not found: {src}", file=sys.stderr)
            sys.exit(1)
        dst = pathlib.Path(args.output) if args.output else src.with_suffix(".html")
        convert(src, dst)


if __name__ == "__main__":
    cli()
