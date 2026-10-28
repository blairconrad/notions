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
from urllib.parse import quote

from bs4 import BeautifulSoup, Comment
from markdown_it import MarkdownIt
from markdown_it.token import Token
from pygments import highlight as pygments_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name
from pygments.util import ClassNotFound

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


# Heading levels listed in the side TOC. "1-2" keeps h1 section dividers
# (e.g. "Part I", "Part II") alongside their nested h2 headings, and stops
# there so the side nav doesn't descend into every sub-heading. The
# document's own h1 title is dropped separately (drop_title_heading).
TOC_MAX_LEVEL = 2
# An explicit [TOC] marker lists every level in --safe mode (python-markdown's
# toc default); in standard mode it uses TOC_MAX_LEVEL, like the side nav.
SAFE_TOC_MAX_LEVEL = 6
TOC_MARKER = "[TOC]"


def make_highlighter(theme: dict, noclasses: bool):
    """Pygments highlighter for fenced code: returns a <div class="codehilite"> block.

    noclasses=True (--safe) inlines the colours as style="..." attributes;
    otherwise the token classes are styled by pygments_css() in the <style> block.
    """
    formatter = HtmlFormatter(
        cssclass="codehilite",
        noclasses=noclasses,
        style=theme["pygments_style"],
        wrapcode=True,
    )

    def highlight(code: str, lang: str, _attrs: str) -> str:
        try:
            lexer = get_lexer_by_name(lang) if lang else TextLexer()
        except ClassNotFound:
            lexer = TextLexer()
        return pygments_highlight(code, lexer, formatter)

    return highlight


# python-markdown's toc de-duplicates ids by bumping a trailing _N (or adding _1).
ID_COUNT_RE = re.compile(r"^(.*)_([0-9]+)$")
ANCHOR_HTML_RE = re.compile(r"^</?a[\s>]", re.IGNORECASE)


def unique_id(slug: str, used: set[str]) -> str:
    """Replicate python-markdown's toc duplicate-id algorithm (e.g. rate_1 -> rate_2)."""
    while slug in used or not slug:
        m = ID_COUNT_RE.match(slug)
        slug = f"{m.group(1)}_{int(m.group(2)) + 1}" if m else f"{slug}_1"
    used.add(slug)
    return slug


def heading_text(inline: Token) -> str:
    """Plain text of a heading; line breaks (multi-line setext headings) count as spaces."""
    parts = []
    for child in inline.children:
        if child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
    return "".join(parts)


def assign_heading_ids(state) -> None:
    """markdown-it core rule: give each heading the same #id python-markdown's toc did.

    Wikilinks to headings (see build_heading_slug_map) depend on these ids.
    Collects (level, id, inline token) for every heading into env["headings"].
    """
    used: set[str] = set()
    headings = state.env.setdefault("headings", [])
    for i, token in enumerate(state.tokens):
        if token.type != "heading_open":
            continue
        inline = state.tokens[i + 1]
        slug = unique_id(slugify(heading_text(inline)), used)
        token.attrSet("id", slug)
        headings.append((int(token.tag[1:]), slug, inline))


def new_parser() -> MarkdownIt:
    """CommonMark with tables, strikethrough and heading ids."""
    md = MarkdownIt("commonmark")
    md.enable(["table", "strikethrough"])
    md.core.ruler.push("heading_ids", assign_heading_ids)
    return md


def toc_label_html(md: MarkdownIt, env: dict, inline: Token) -> str:
    """Heading text as HTML for a TOC entry, minus links (the entry is itself a link)."""
    children = [
        child
        for child in inline.children
        if child.type not in ("link_open", "link_close")
        and not (child.type == "html_inline" and ANCHOR_HTML_RE.match(child.content))
    ]
    return md.renderer.renderInline(children, md.options, env)


def build_toc_tokens(md: MarkdownIt, env: dict, max_level: int) -> list[dict]:
    """Nest the collected headings (levels <= max_level) into a TOC token tree."""
    roots: list[dict] = []
    stack: list[dict] = []
    for level, slug, inline in env.get("headings", []):
        if level > max_level:
            continue
        node = {
            "level": level,
            "id": slug,
            "html": toc_label_html(md, env, inline),
            "children": [],
        }
        while stack and stack[-1]["level"] >= level:
            stack.pop()
        (stack[-1]["children"] if stack else roots).append(node)
        stack.append(node)
    return roots


def render_markdown(md_text: str, theme: dict, safe: bool) -> tuple[str, list[dict], bool]:
    """Render Markdown to (HTML body, side-nav TOC tree, whether a [TOC] marker was expanded)."""
    md = new_parser()

    def expand_toc_marker(state) -> None:
        """Replace a paragraph that is just [TOC] with the rendered table of contents."""
        max_level = SAFE_TOC_MAX_LEVEL if safe else TOC_MAX_LEVEL
        tokens = state.tokens
        i = 0
        while i + 2 < len(tokens):
            opening, inline, closing = tokens[i : i + 3]
            if (
                opening.type == "paragraph_open"
                and inline.type == "inline"
                and inline.content.strip() == TOC_MARKER
                # A [TOC] reference-link definition makes this a link, not the marker.
                and all(child.type == "text" for child in inline.children)
                and closing.type == "paragraph_close"
            ):
                toc = Token("html_block", "", 0)
                toc.content = render_toc(build_toc_tokens(md, state.env, max_level), "Contents") + "\n"
                tokens[i : i + 3] = [toc]
                state.env["toc_placed"] = True
            i += 1

    md.core.ruler.push("toc_marker", expand_toc_marker)

    highlight = make_highlighter(theme, noclasses=safe)

    # Rendered here rather than via markdown-it's `highlight` option, which
    # only accepts output starting with "<pre" and would wrap our
    # <div class="codehilite"> in a second <pre><code>.
    def render_fence(self, tokens, idx, options, env):
        token = tokens[idx]
        lang = token.info.strip().split(maxsplit=1)[0] if token.info.strip() else ""
        if lang == "mermaid":
            if safe:
                env["mermaid_skipped"] = True
            else:
                # Source is left unescaped, as before: mermaid diagrams use tags like <br/>.
                return f'<div class="mermaid">\n{token.content}</div>\n'
        return highlight(token.content, lang, "")

    def render_code_block(self, tokens, idx, options, env):
        return highlight(tokens[idx].content, "", "")

    md.add_render_rule("fence", render_fence)
    md.add_render_rule("code_block", render_code_block)
    # ~~text~~ was <del> under python-markdown; markdown-it emits <s>.
    md.add_render_rule("s_open", lambda self, tokens, idx, options, env: "<del>")
    md.add_render_rule("s_close", lambda self, tokens, idx, options, env: "</del>")

    env: dict = {}
    body = md.render(md_text, env)
    if env.get("mermaid_skipped"):
        print(
            "warning: mermaid fenced code block(s) found, but --safe mode cannot "
            "render Mermaid (no <script> allowed); left as plain code.",
            file=sys.stderr,
        )
    return body, build_toc_tokens(md, env, TOC_MAX_LEVEL), env.get("toc_placed", False)


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
    """Map each heading's literal text to the #id it gets when rendered.

    Parses with the same parser and id allocation as rendering, so headings
    nested in lists or hidden in code blocks are counted exactly as they are
    in the output. Runs of whitespace in the text are collapsed to one space.
    """
    env: dict = {}
    new_parser().parse(md_text, env)
    slug_map: dict[str, str] = {}
    for _level, slug, inline in env.get("headings", []):
        slug_map.setdefault(" ".join(inline.content.split()), slug)
    return slug_map


def convert_wikilinks(
    md_text: str, heading_slugs: dict[str, str], src_path: pathlib.Path | None
) -> str:
    def repl(m: re.Match) -> str:
        target = m.group(1).strip()
        alias = m.group(2).strip() if m.group(2) else None

        if target.startswith("#"):
            heading = " ".join(target[1:].split())
            slug = heading_slugs.get(heading) or slugify(heading)
            text = alias or heading
            return f"[{text}]({''.join(('#', slug))})"

        display = alias or target
        if src_path is not None:
            candidate = src_path.parent / f"{target}.md"
            if candidate.exists():
                return f"[{display}]({quote(candidate.with_suffix('.html').name)})"
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
    body, toc_tokens_raw, toc_placed = render_markdown(md_text, theme, safe=False)

    # A [TOC] marker is expanded in place by render_markdown. Notebooks rarely
    # add one, so otherwise build a sticky side nav automatically, unless the
    # document has no (non-title) headings at all.
    toc_tokens = drop_title_heading(toc_tokens_raw)
    toc_html = render_toc(toc_tokens, "Contents")
    if toc_html and not toc_placed:
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

    raw_body, _, _ = render_markdown(md_text, theme, safe=True)

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
