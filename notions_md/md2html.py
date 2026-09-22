"""Convert one or more Markdown files to standalone HTML.

Two output modes, both themed (default theme: blue-topaz; --theme plain for a
neutral palette), with syntax-highlighted (Pygments) fenced code blocks:

  Standard (default): full HTML document with a <style> block (generated from
  the selected theme) and Mermaid diagram support via CDN <script>. Intended
  for local viewing in a browser.

  Safe (--safe): same standalone document, but the content itself uses only
  inline style="..." attributes (no <style> block, no <script>), and is run
  through a sanitizer that strips <script>/<style>/<iframe>/<form>/<input>
  and similar tags, event-handler attributes, and javascript: hrefs. This
  produces HTML that is safe to paste into ServiceNow Work Notes / Internal
  Notes fields (which only allow a restricted tag set and reject <style>/
  <script>). Mermaid diagrams cannot render in this mode (no <script>
  allowed), so fenced ```mermaid``` blocks are left as plain code and a
  warning is printed.

Obsidian-style [[wikilinks]] (with an optional |alias) are also converted:
[[#Heading text]] links to a heading anchor in the same document, and
[[Page name]] links to a sibling Page name.html if Page name.md exists next
to the source file, otherwise it's rendered as plain text (its target can't
be resolved, e.g. a reference into another vault).

Standard mode also adds a sticky side table of contents (from the document's
headings) unless the source already places a [TOC] marker itself. --safe mode
never adds one, since ServiceNow output has no <style> block to support it
and the collapsed h3/h4 heading levels would make it redundant.

Usage:
    md2html file.md [file2.md ...]              # standard, blue-topaz theme
    md2html file.md -o output.html
    md2html file.md --theme plain                # standard, neutral palette
    md2html file.md --safe                       # ServiceNow-safe styling (theme: blue-topaz)
    md2html file.md --safe --theme plain         # ServiceNow-safe styling, neutral palette

Output is written alongside the source file with a .html extension unless -o is given.
"""

import argparse
import html
import pathlib
import re
import sys
import unicodedata

import markdown
from bs4 import BeautifulSoup, Comment
from pygments.formatters import HtmlFormatter

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"

# Highlights whichever TOC entry corresponds to the section currently in
# view. Watches each heading the TOC links to and marks its link "active"
# once the heading crosses a band near the top of the viewport (the -70%
# bottom rootMargin keeps that band thin, so normally only one heading is
# "current" at a time even with short sections).
TOC_SCROLLSPY_JS = """
<script>
(function () {
  var links = document.querySelectorAll('.toc a[href^="#"]');
  if (!links.length) return;
  var targets = [];
  links.forEach(function (a) {
    var el = document.getElementById(a.getAttribute('href').slice(1));
    if (el) targets.push([el, a]);
  });
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var match = targets.find(function (t) { return t[0] === entry.target; });
      if (!match) return;
      links.forEach(function (a) { a.classList.remove('active'); });
      match[1].classList.add('active');
    });
  }, { rootMargin: '0px 0px -70% 0px', threshold: 0 });
  targets.forEach(function (t) { observer.observe(t[0]); });
})();
</script>
"""

# YAML frontmatter (--- ... --- at the very start of the file) is metadata,
# not content, so it's stripped before conversion in both modes.
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n.*?\n---[ \t]*\n?", re.DOTALL)


def strip_frontmatter(md_text: str) -> str:
    return FRONTMATTER_RE.sub("", md_text, count=1)


# codehilite (fenced ```lang blocks) intercepts every fenced code block,
# including ```mermaid ones, before we ever see a "language-mermaid" class to
# detect. So mermaid blocks are pulled out of the raw Markdown text up front
# and spliced back in as <div class="mermaid"> after conversion.
MERMAID_FENCE_RE = re.compile(r"^```mermaid[ \t]*\n(.*?)^```[ \t]*$\n?", re.DOTALL | re.MULTILINE)
MERMAID_PLACEHOLDER = "\uE000MERMAID_BLOCK_{index}\uE000"
MERMAID_PLACEHOLDER_RE = re.compile(r"<p>\uE000MERMAID_BLOCK_(\d+)\uE000</p>")


def extract_mermaid_blocks(md_text: str) -> tuple[str, list[str]]:
    """Replace ```mermaid fences with placeholder paragraphs; return text + block contents."""
    blocks: list[str] = []

    def repl(m: re.Match) -> str:
        blocks.append(m.group(1))
        return f"\n{MERMAID_PLACEHOLDER.format(index=len(blocks) - 1)}\n\n"

    return MERMAID_FENCE_RE.sub(repl, md_text), blocks


def restore_mermaid_blocks(body_html: str, blocks: list[str]) -> str:
    def repl(m: re.Match) -> str:
        return f'<div class="mermaid">\n{blocks[int(m.group(1))]}</div>'

    return MERMAID_PLACEHOLDER_RE.sub(repl, body_html)


MD_EXTENSIONS = ["fenced_code", "codehilite", "tables", "sane_lists", "toc", "pymdownx.tilde"]

# toc extension's default [TOC] marker (must be alone on its own line); used
# to detect whether the source already placed it explicitly.
TOC_MARKER_RE = re.compile(r"^\[TOC\][ \t]*$", re.MULTILINE)

# ---------------------------------------------------------------------------
# Obsidian-style [[wikilinks]].
#
# Two shapes are handled, both with an optional |alias:
#   [[#Heading text|alias]]  - link to a heading within this same document.
#   [[Page name|alias]]      - link to another note; resolved to a sibling
#                              .html file if the matching .md exists next to
#                              the source file, otherwise rendered as plain
#                              text (there's nowhere for it to point).
#
# Converted to plain Markdown link syntax *before* the file is handed to the
# markdown library, so normal link rendering (and --safe sanitizing) applies.
# ---------------------------------------------------------------------------

WIKILINK_RE = re.compile(r"\[\[([^\[\]|]+)(?:\|([^\[\]]+))?\]\]")

# Fenced code blocks are excluded before scanning for ATX headers below, so
# a '#' comment inside a shell/Python code sample isn't mistaken for a heading.
FENCE_RE = re.compile(r"^```.*?^```[ \t]*$\n?", re.DOTALL | re.MULTILINE)
ATX_HEADER_RE = re.compile(r"^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$", re.MULTILINE)


def slugify(text: str) -> str:
    """Replicate python-markdown's 'toc' extension default (ASCII) slugify.

    Wikilinks to headings need to resolve to the same #id the toc extension
    assigns to that heading, so the anchor actually lands on the target.
    """
    value = unicodedata.normalize("NFKD", text)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


def build_heading_slug_map(md_text: str) -> dict[str, str]:
    """Map each heading's literal text to the #id toc will give it.

    Mirrors toc's de-duplication of repeated headings (id, id_1, id_2, ...).
    """
    slug_map: dict[str, str] = {}
    seen: dict[str, int] = {}
    for m in ATX_HEADER_RE.finditer(FENCE_RE.sub("", md_text)):
        text = m.group(1).strip()
        base_slug = slugify(text)
        count = seen.get(base_slug, 0)
        seen[base_slug] = count + 1
        slug_map.setdefault(text, base_slug if count == 0 else f"{base_slug}_{count}")
    return slug_map


def convert_wikilinks(
    md_text: str, heading_slugs: dict[str, str], src_path: pathlib.Path | None
) -> str:
    def repl(m: re.Match) -> str:
        target = m.group(1).strip()
        alias = m.group(2).strip() if m.group(2) else None

        if target.startswith("#"):
            heading = target[1:].strip()
            slug = heading_slugs.get(heading) or slugify(heading)
            text = alias or heading
            return f"[{text}]({''.join(('#', slug))})"

        display = alias or target
        if src_path is not None:
            candidate = src_path.parent / f"{target}.md"
            if candidate.exists():
                return f"[{display}]({candidate.with_suffix('.html').name})"
        # No resolvable target (e.g. a reference into another vault/wiki):
        # fall back to plain text rather than leaving literal [[...]] behind.
        return display

    return WIKILINK_RE.sub(repl, md_text)

# ---------------------------------------------------------------------------
# --safe mode style palettes (inline styles only; no <style> block allowed).
# ---------------------------------------------------------------------------

DEFAULT_THEME = "blue-topaz"

# "plain": neutral, professional style.
# "blue-topaz" (default): colors lifted from the Obsidian "Blue Topaz" theme's
# default light color scheme (https://github.com/PKM-er/Blue-Topaz_Obsidian-css),
# reading the actual --h1..--h6/--background-primary/--text-normal/
# --simple-blue-1 hex/hsl values out of theme.css and converting to hex.
THEMES = {
    "plain": {
        "outer": (
            "font-family:HelveticaNeue-Light,'Helvetica Neue Light','Helvetica Neue',"
            "Helvetica,Arial,sans-serif; font-weight:300; "
            "line-height:1.6; color:#333;"
        ),
        "h3": (
            "font-weight:300; font-size:1.4em; line-height:1.2; "
            "margin-top:1.2em; margin-bottom:0.4em; color:#333;"
        ),
        "h4": (
            "font-weight:300; font-size:1.15em; line-height:1.2; "
            "margin-top:1em; margin-bottom:0.3em; color:#333;"
        ),
        # Full h1-h6 gradient for standard (non-safe) mode, where each level
        # can have distinct styling instead of being collapsed to h3/h4.
        "headings": {
            1: "font-weight:300; line-height:1.2; margin-top:1.4em; margin-bottom:0.5em; color:#222;",
            2: "font-weight:300; line-height:1.2; margin-top:1.3em; margin-bottom:0.45em; color:#2b2b2b;",
            3: "font-weight:300; line-height:1.2; margin-top:1.2em; margin-bottom:0.4em; color:#333;",
            4: "font-weight:300; line-height:1.2; margin-top:1.1em; margin-bottom:0.35em; color:#3d3d3d;",
            5: "font-weight:300; line-height:1.2; margin-top:1em; margin-bottom:0.3em; color:#484848;",
            6: "font-weight:300; line-height:1.2; margin-top:1em; margin-bottom:0.3em; color:#555; text-transform:uppercase; letter-spacing:0.03em;",
        },
        "hr": "height:1px; border:none; background-color:#ddd; margin:1em 0;",
        "toc_box": (
            "border:1px solid #ddd; border-radius:4px; padding:0.75em 1.25em; "
            "margin:0 0 1.5em 0; background:#f7f7f7;"
        ),
        "toc_title": "font-weight:600; color:#333;",
        "toc_active": "color:#3498db; font-weight:600;",
        "blockquote": (
            "margin:0.5em 0 1em 0; padding-left:1em; "
            "border-left:3px solid rgba(0,0,0,0.1); color:#555; font-style:italic;"
        ),
        "pre": (
            "padding:0.5em 1em; "
            "font-family:Consolas,Monaco,'Andale Mono',monospace; "
            "font-size:0.85em; line-height:1.5; white-space:pre-wrap;"
        ),
        "inline_code": (
            "font-family:Consolas,Monaco,'Andale Mono',monospace; font-size:80%; "
            "vertical-align:baseline; background:#f5f2f0; padding:0.1em 0.3em;"
        ),
        # Syntax highlighting (codehilite/Pygments) for fenced code blocks.
        "pygments_style": "friendly",
        "code_chrome": "border-radius:4px; margin:1em 0; overflow:auto;",
        "table": "width:100%; border-collapse:collapse; font-size:0.95em;",
        "th": (
            "padding:0.25em 0.5em; text-align:left; "
            "border-bottom:2px solid #ddd; font-weight:600;"
        ),
        "td": "padding:0.25em 0.5em;",
        "tr_even": "background:#fff;",
        "tr_odd": "background:#f7f7f7;",
        "link": "color:#3498db; text-decoration:none; border-bottom:1px solid #3498db;",
    },
    "blue-topaz": {
        "outer": (
            "font-family:HelveticaNeue-Light,'Helvetica Neue Light','Helvetica Neue',"
            "Helvetica,Arial,sans-serif; "
            "line-height:1.6; color:#0e0e0e; background:#ffffff; padding:0.5em;"
        ),
        # Headings use the theme's h1-h6 blue gradient (dark navy -> light sky
        # blue); ServiceNow work notes should stay within h3/h4, so h3 gets
        # the h1 color (top-level) and h4 gets the h3 color (sub-level).
        "h3": (
            "font-weight:600; font-size:1.4em; line-height:1.3; "
            "margin-top:1.2em; margin-bottom:0.4em; color:#08377D;"
        ),
        "h4": (
            "font-weight:600; font-size:1.15em; line-height:1.3; "
            "margin-top:1em; margin-bottom:0.3em; color:#0E63B9;"
        ),
        # Full h1-h6 gradient for standard (non-safe) mode: colors and sizes
        # taken directly from the Obsidian "Blue Topaz" theme's default light
        # color scheme (--h1..--h6-color and --h1..--h6-size in theme.css).
        "headings": {
            1: "font-weight:600; font-size:1.5625em; line-height:1.3; margin-top:1.4em; margin-bottom:0.5em; color:#08377D;",
            2: "font-weight:600; font-size:1.4375em; line-height:1.3; margin-top:1.3em; margin-bottom:0.45em; color:#004FA8;",
            3: "font-weight:600; font-size:1.3125em; line-height:1.3; margin-top:1.2em; margin-bottom:0.4em; color:#0E63B9;",
            4: "font-weight:600; font-size:1.1875em; line-height:1.3; margin-top:1.1em; margin-bottom:0.35em; color:#3482C5;",
            5: "font-weight:600; font-size:1.0625em; line-height:1.3; margin-top:1em; margin-bottom:0.3em; color:#5AA0E2;",
            6: "font-weight:600; font-size:1em; line-height:1.3; margin-top:1em; margin-bottom:0.3em; color:#89B9E6;",
        },
        "hr": "height:1px; border:none; background-color:#7d7d7d; margin:1em 0;",
        "toc_box": (
            "border:1px solid #42A1FA; border-radius:4px; padding:0.75em 1.25em; "
            "margin:0 0 1.5em 0; background:rgba(66,161,250,0.06);"
        ),
        "toc_title": "font-weight:600; color:#08377D;",
        "toc_active": "color:#0E63B9; font-weight:600;",
        "blockquote": (
            "margin:0.5em 0 1em 0; padding:0.4em 1em; "
            "border-left:3px solid #42A1FA; background:#d5d5d52c; "
            "color:#0e0e0e; font-style:italic;"
        ),
        "pre": (
            "padding:0.5em 1em; "
            "font-family:Consolas,Monaco,'Andale Mono',monospace; "
            "line-height:1.5; white-space:pre-wrap;"
        ),
        "inline_code": (
            "font-family:Consolas,Monaco,'Andale Mono',monospace; "
            "vertical-align:baseline; background:#e6e6e671; "
            "color:#e95d00;"
        ),
        # Syntax highlighting (codehilite/Pygments) for fenced code blocks.
        "pygments_style": "catppuccin-latte",
        "code_chrome": "border-radius:4px; margin:1em 0; overflow:auto;",
        "table": "width:100%; border-collapse:collapse; font-size:0.95em;",
        "th": (
            "padding:0.25em 0.5em; text-align:left; "
            "border-bottom:2px solid #42A1FA; font-weight:600; "
            "background:rgba(66,161,250,0.1); color:#0e0e0e;"
        ),
        "td": "padding:0.25em 0.5em; color:#0e0e0e;",
        "tr_even": "background:#ffffff;",
        "tr_odd": "background:#f1f1f176;",
        "link": "color:#42A1FA; text-decoration:none; border-bottom:1px solid #42A1FA;",
    },
}

# Tags that must never appear in ServiceNow-safe output.
FORBIDDEN_TAGS = {
    "button",
    "embed",
    "form",
    "iframe",
    "input",
    "link",
    "meta",
    "object",
    "script",
    "style",
}


def pygments_css(theme: dict) -> str:
    """CSS for codehilite-highlighted code blocks (standard mode only)."""
    formatter = HtmlFormatter(style=theme["pygments_style"], cssclass="codehilite")
    defs = formatter.get_style_defs(".codehilite")
    # Drop the bare "pre { line-height: ... }" rule pygments emits: it isn't
    # scoped to .codehilite and would clash with our own <pre> chrome rule.
    lines = [ln for ln in defs.splitlines() if not ln.strip().startswith("pre ")]
    return "\n".join(lines)


def build_css(theme: dict) -> str:
    """Turn a theme's inline-style fragments into a real <style> block for standard mode.

    Unlike --safe mode (which must collapse h1-h6 down to h3/h4 for
    ServiceNow), standard mode gives every heading level its own styling via
    the theme's "headings" gradient.
    """
    heading_rules = "\n".join(
        f"h{level} {{ {style} }}" for level, style in sorted(theme["headings"].items())
    )
    return f"""
body {{ max-width: 1400px; margin: 2em auto; padding: 0 2em; {theme["outer"]} }}
{heading_rules}
hr {{ {theme["hr"]} }}
blockquote {{ {theme["blockquote"]} }}
.codehilite {{ {theme["code_chrome"]} }}
pre {{ {theme["pre"]} }}
pre code {{ background: none; padding: 0; color: inherit; font-family: inherit; }}
code {{ {theme["inline_code"]} }}
table {{ {theme["table"]} }}
th {{ {theme["th"]} }}
td {{ {theme["td"]} }}
tr:nth-child(even) {{ {theme["tr_even"]} }}
tr:nth-child(odd) {{ {theme["tr_odd"]} }}
a {{ {theme["link"]} }}
.mermaid {{ text-align: center; margin: 1.5em 0; }}
.page-layout {{ display: flex; align-items: flex-start; gap: 2.5em; }}
.page-layout > .content {{ flex: 1 1 auto; min-width: 0; max-width: 900px; order: 1; }}
.toc {{ {theme["toc_box"]} flex: 0 0 280px; position: sticky; top: 1.5em;
  max-height: calc(100vh - 3em); overflow-y: auto; order: 2; }}
.toc .toctitle {{ {theme["toc_title"]} display: block; margin-bottom: 0.4em; }}
.toc ul {{ margin: 0.2em 0 0 0; padding-left: 0; list-style: none; }}
.toc li {{ padding-left: 1.2em; text-indent: -1.2em; }}
.toc a {{ text-decoration: none; border-bottom: none; }}
.toc a.active {{ {theme["toc_active"]} }}
@media (max-width: 900px) {{
  .page-layout {{ display: block; }}
  .toc {{ position: static; max-height: none; margin-bottom: 1.5em; }}
}}
{pygments_css(theme)}
"""


def wrap_document(
    title: str, body_html: str, style_block: str = "", extra_head: str = ""
) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  {style_block}
  {extra_head}
</head>
<body>
{body_html}
</body>
</html>"""


def drop_title_heading(toc_tokens: list[dict]) -> list[dict]:
    """Remove the document's own title (its first top-level heading) from a TOC tree.

    A link back to the top of the page it's already on isn't useful, but
    later top-level (h1) headings are meaningful section dividers (e.g.
    "Part I", "Part II") and must be kept. So only the very first entry is
    dropped, and its own children (headings that appeared before the first
    such divider) are promoted to take its place rather than lost.
    """
    if not toc_tokens or toc_tokens[0]["level"] != 1:
        return toc_tokens
    title, *rest = toc_tokens
    return title["children"] + rest


def render_toc(toc_tokens: list[dict], toc_title: str) -> str:
    """Render a TOC token tree (as produced by the toc extension) to HTML."""

    def render_list(tokens: list[dict]) -> str:
        if not tokens:
            return ""
        items = "".join(
            f'<li><a href="#{t["id"]}">{t["html"]}</a>{render_list(t["children"])}</li>'
            for t in tokens
        )
        return f"<ul>{items}</ul>"

    list_html = render_list(toc_tokens)
    if not list_html:
        return ""
    return f'<div class="toc"><span class="toctitle">{toc_title}</span>{list_html}</div>'


def md_to_html(
    md_text: str,
    title: str = "",
    theme_name: str = DEFAULT_THEME,
    src_path: pathlib.Path | None = None,
) -> str:
    """Standard mode: full document, themed <style> block, Mermaid via CDN script."""
    if theme_name not in THEMES:
        valid = ", ".join(sorted(THEMES))
        raise ValueError(f"Unknown theme '{theme_name}'. Valid options: {valid}")
    theme = THEMES[theme_name]

    md_text = strip_frontmatter(md_text)
    md_text = convert_wikilinks(md_text, build_heading_slug_map(md_text), src_path)
    md_text, mermaid_blocks = extract_mermaid_blocks(md_text)
    md = markdown.Markdown(
        extensions=MD_EXTENSIONS,
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "codehilite"},
            # toc_depth "1-2" keeps h1 section dividers (e.g. "Part I",
            # "Part II") alongside their nested h2 headings, and stops there
            # so the side nav doesn't descend into every sub-heading. The
            # document's own h1 title is dropped separately below.
            "toc": {"title": "Contents", "toc_depth": "1-2"},
        },
    )
    body = md.convert(md_text)
    body = restore_mermaid_blocks(body, mermaid_blocks)

    # The toc extension only inserts its generated TOC where a [TOC] marker
    # appears in the source; since notebooks rarely add one, build a sticky
    # side nav from it automatically here unless the document already placed
    # the marker itself or has no (non-title) headings at all.
    toc_tokens = drop_title_heading(md.toc_tokens)
    toc_html = render_toc(toc_tokens, "Contents")
    if toc_html and not TOC_MARKER_RE.search(md_text):
        body = (
            f'<div class="page-layout">\n{toc_html}\n<div class="content">\n{body}\n</div>\n</div>'
            f"{TOC_SCROLLSPY_JS}"
        )

    return wrap_document(
        title,
        body,
        style_block=f"<style>{build_css(theme)}</style>",
        extra_head=f'<script src="{MERMAID_CDN}"></script>',
    )



def sanitize(soup: BeautifulSoup) -> None:
    """Strip disallowed tags/attributes so output is always ServiceNow-safe."""
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()

    for tag_name in FORBIDDEN_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            # Strip event handlers, and drop 'class' left by markdown
            # extensions since it serves no purpose without a <style> block
            # and ServiceNow output should stay style-only. 'id' is kept:
            # heading ids are still needed as jump targets for in-document
            # anchors (e.g. from converted [[#Heading]] wikilinks).
            if attr.lower().startswith("on") or attr == "class":
                del tag.attrs[attr]

        if tag.name == "a" and "href" in tag.attrs:
            href = tag.attrs["href"].strip()
            if href.lower().startswith("javascript:"):
                del tag.attrs["href"]


def restyle_headings(soup: BeautifulSoup, theme: dict) -> None:
    """Markdown h1-h3 -> ServiceNow h3 (top-level); h4-h6 -> h4 (sub-level)."""
    for level in range(1, 7):
        for tag in soup.find_all(f"h{level}"):
            if level <= 3:
                tag.name = "h3"
                tag["style"] = theme["h3"]
            else:
                tag.name = "h4"
                tag["style"] = theme["h4"]


def restyle_tables(soup: BeautifulSoup, theme: dict) -> None:
    for table in soup.find_all("table"):
        table["style"] = theme["table"]
        for th in table.find_all("th"):
            th["style"] = theme["th"]
        body_rows = (
            table.find("tbody").find_all("tr")
            if table.find("tbody")
            else [tr for tr in table.find_all("tr") if not tr.find("th")]
        )
        for i, tr in enumerate(body_rows):
            tr["style"] = theme["tr_even"] if i % 2 == 0 else theme["tr_odd"]
            for td in tr.find_all("td"):
                td["style"] = theme["td"]


def restyle_codehilite_wrapper(soup: BeautifulSoup, theme: dict) -> None:
    """Style the outer codehilite div while its 'class' attr still identifies it.

    Must run before sanitize() strips 'class', since noclasses=True Pygments
    output already carries the background/color inline (e.g. style="background:
    #fdf6e3") and only the class attribute tells us which divs to add chrome to.
    """
    for div in soup.find_all("div", class_="codehilite"):
        existing = div.get("style", "").rstrip("; ")
        div["style"] = f"{existing}; {theme['code_chrome']}" if existing else theme["code_chrome"]


def restyle_code(soup: BeautifulSoup, theme: dict) -> None:
    for pre in soup.find_all("pre"):
        # Merge with any inline style Pygments already set (noclasses mode
        # adds e.g. "line-height: 125%;"), so highlighting colors survive.
        existing = pre.get("style", "").rstrip("; ")
        pre["style"] = f"{existing}; {theme['pre']}" if existing else theme["pre"]

    for code in soup.find_all("code"):
        if code.find_parent("pre") is None:
            code["style"] = theme["inline_code"]


def restyle_misc(soup: BeautifulSoup, theme: dict) -> None:
    for bq in soup.find_all("blockquote"):
        bq["style"] = theme["blockquote"]
    for hr in soup.find_all("hr"):
        hr["style"] = theme["hr"]
    for a in soup.find_all("a"):
        if a.has_attr("href"):
            a["style"] = theme["link"]


def md_to_html_safe(
    md_text: str,
    title: str = "",
    theme_name: str = DEFAULT_THEME,
    src_path: pathlib.Path | None = None,
) -> str:
    """Safe mode: ServiceNow-safe styling (inline styles only, sanitized, no script)."""
    if theme_name not in THEMES:
        valid = ", ".join(sorted(THEMES))
        raise ValueError(f"Unknown theme '{theme_name}'. Valid options: {valid}")
    theme = THEMES[theme_name]

    md_text = strip_frontmatter(md_text)
    md_text = convert_wikilinks(md_text, build_heading_slug_map(md_text), src_path)
    if MERMAID_FENCE_RE.search(md_text):
        print(
            "warning: mermaid fenced code block(s) found, but --safe mode cannot "
            "render Mermaid (no <script> allowed); left as plain code.",
            file=sys.stderr,
        )

    raw_body = markdown.markdown(
        md_text,
        extensions=MD_EXTENSIONS,
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "noclasses": True,
                "pygments_style": theme["pygments_style"],
            }
        },
    )

    soup = BeautifulSoup(raw_body, "html.parser")
    restyle_codehilite_wrapper(soup, theme)
    sanitize(soup)
    restyle_headings(soup, theme)
    restyle_tables(soup, theme)
    restyle_code(soup, theme)
    restyle_misc(soup, theme)

    fragment = str(soup)
    fragment = re.sub(r"\n{3,}", "\n\n", fragment)
    wrapped_fragment = f'<div style="{theme["outer"]}">\n{fragment}\n</div>'

    return wrap_document(title, wrapped_fragment)


def convert(
    src: pathlib.Path, dst: pathlib.Path, safe: bool = False, theme: str = DEFAULT_THEME
) -> None:
    md_text = src.read_text(encoding="utf-8")
    title = src.stem.replace("-", " ").replace("_", " ")
    output = (
        md_to_html_safe(md_text, title=title, theme_name=theme, src_path=src)
        if safe
        else md_to_html(md_text, title=title, theme_name=theme, src_path=src)
    )
    dst.write_text(output, encoding="utf-8")
    print(f"  {src} -> {dst}")


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Markdown file(s) to standalone HTML, optionally in ServiceNow-safe styling."
    )
    parser.add_argument(
        "inputs", nargs="+", metavar="FILE.md", help="Input Markdown file(s)"
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE.html",
        help="Output path (only valid when a single input file is given)",
    )
    parser.add_argument(
        "--safe",
        action="store_true",
        help="Produce ServiceNow-safe HTML: inline styles only, sanitized, no <style>/<script>/Mermaid",
    )
    parser.add_argument(
        "--theme",
        choices=sorted(THEMES),
        default=DEFAULT_THEME,
        help=f"Style palette (default: '{DEFAULT_THEME}'); applies to both standard and --safe output",
    )
    args = parser.parse_args()

    if args.output and len(args.inputs) > 1:
        print(
            "error: -o/--output can only be used with a single input file",
            file=sys.stderr,
        )
        sys.exit(1)

    for src_str in args.inputs:
        src = pathlib.Path(src_str)
        if not src.exists():
            print(f"error: file not found: {src}", file=sys.stderr)
            sys.exit(1)
        dst = pathlib.Path(args.output) if args.output else src.with_suffix(".html")
        convert(src, dst, safe=args.safe, theme=args.theme)


if __name__ == "__main__":
    cli()
