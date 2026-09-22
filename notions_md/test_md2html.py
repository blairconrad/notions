#!/usr/bin/env python

import pathlib

import pytest
from bs4 import BeautifulSoup

from notions_md import md2html


class TestStripFrontmatter:
    def test_stripsLeadingFrontmatter(self):
        md_text = "---\ntitle: Foo\nstatus: open\n---\n# Heading\n\nBody\n"
        assert md2html.strip_frontmatter(md_text) == "# Heading\n\nBody\n"

    def test_leavesTextWithoutFrontmatterUnchanged(self):
        md_text = "# Heading\n\nBody\n"
        assert md2html.strip_frontmatter(md_text) == md_text

    def test_leavesLaterHorizontalRulesAlone(self):
        md_text = "# Heading\n\nBody\n\n---\n\nMore\n"
        assert md2html.strip_frontmatter(md_text) == md_text


class TestSlugify:
    def test_lowercasesAndDashesSpaces(self):
        assert md2html.slugify("Hello World") == "hello-world"

    def test_dropsPunctuationButKeepsUnderscoresAndHyphens(self):
        assert (
            md2html.slugify("F2. The memory is Oilpan (blink_gc), not decoded pixels")
            == "f2-the-memory-is-oilpan-blink_gc-not-decoded-pixels"
        )

    def test_stripsBackticksAroundInlineCode(self):
        assert md2html.slugify("The `blink_objects` counters") == "the-blink_objects-counters"

    def test_collapsesRepeatedSeparators(self):
        assert md2html.slugify("a---b   c") == "a-b-c"


class TestBuildHeadingSlugMap:
    def test_mapsHeadingTextToSlug(self):
        md_text = "## F1. First finding\n\nBody\n\n## F2. Second finding\n"
        slugs = md2html.build_heading_slug_map(md_text)
        assert slugs == {
            "F1. First finding": "f1-first-finding",
            "F2. Second finding": "f2-second-finding",
        }

    def test_deduplicatesRepeatedHeadingText(self):
        md_text = "## Notes\n\nA\n\n## Notes\n\nB\n"
        slugs = md2html.build_heading_slug_map(md_text)
        # First occurrence wins the base slug; only the first mapping is kept
        # since dict keys are the heading text (duplicates share a key).
        assert slugs["Notes"] == "notes"

    def test_ignoresHashesInsideFencedCodeBlocks(self):
        md_text = "```bash\n# not a heading\necho hi\n```\n\n## Real Heading\n"
        slugs = md2html.build_heading_slug_map(md_text)
        assert slugs == {"Real Heading": "real-heading"}


class TestConvertWikilinks:
    def test_headingLinkWithAlias(self):
        result = md2html.convert_wikilinks(
            "See [[#F1. Some finding|F1]] for details.",
            {"F1. Some finding": "f1-some-finding"},
            None,
        )
        assert result == "See [F1](#f1-some-finding) for details."

    def test_headingLinkWithoutAlias(self):
        result = md2html.convert_wikilinks(
            "See [[#F1. Some finding]] for details.",
            {"F1. Some finding": "f1-some-finding"},
            None,
        )
        assert result == "See [F1. Some finding](#f1-some-finding) for details."

    def test_headingLinkFallsBackToComputedSlugWhenHeadingUnknown(self):
        result = md2html.convert_wikilinks("[[#Unknown Heading]]", {}, None)
        assert result == "[Unknown Heading](#unknown-heading)"

    def test_pageLinkResolvesToSiblingHtmlFile(self, tmp_path):
        src = tmp_path / "notebook.md"
        src.write_text("body", encoding="utf-8")
        (tmp_path / "Other Note.md").write_text("# Other Note", encoding="utf-8")

        result = md2html.convert_wikilinks("[[Other Note|here]]", {}, src)
        assert result == "[here](Other Note.html)"

    def test_pageLinkWithoutAliasUsesPageNameAsText(self, tmp_path):
        src = tmp_path / "notebook.md"
        (tmp_path / "Other Note.md").touch()

        result = md2html.convert_wikilinks("[[Other Note]]", {}, src)
        assert result == "[Other Note](Other Note.html)"

    def test_pageLinkWithNoResolvableTargetFallsBackToPlainText(self, tmp_path):
        src = tmp_path / "notebook.md"
        src.write_text("body", encoding="utf-8")

        result = md2html.convert_wikilinks(
            "See [[xero-cine-per-draw-retention]] (ei-llm-wiki) for background.", {}, src
        )
        assert result == "See xero-cine-per-draw-retention (ei-llm-wiki) for background."

    def test_pageLinkWithNoSrcPathFallsBackToPlainText(self):
        result = md2html.convert_wikilinks("[[Some Page|alias text]]", {}, None)
        assert result == "alias text"

    def test_multipleWikilinksInOneLine(self):
        slugs = {"A": "a", "B": "b"}
        result = md2html.convert_wikilinks("[[#A]] and [[#B|bee]]", slugs, None)
        assert result == "[A](#a) and [bee](#b)"


class TestMdToHtml:
    def test_convertsHeadingWikilinkToWorkingAnchor(self):
        md_text = "## F1. Some finding\n\nSee [[#F1. Some finding|F1]] above.\n"
        output = md2html.md_to_html(md_text, title="t")
        soup = BeautifulSoup(output, "html.parser")

        heading = soup.find(["h1", "h2", "h3", "h4", "h5", "h6"], string="F1. Some finding")
        link = soup.find("a", string="F1")

        assert heading is not None and heading.get("id")
        assert link["href"] == f"#{heading['id']}"

    def test_noLiteralWikilinkSyntaxLeftInOutput(self):
        md_text = "## F1. Some finding\n\nSee [[#F1. Some finding|F1]] and [[Elsewhere]].\n"
        output = md2html.md_to_html(md_text, title="t")
        assert "[[" not in output and "]]" not in output

    def test_pageWikilinkResolvesRelativeToSourceFile(self, tmp_path):
        src = tmp_path / "notebook.md"
        (tmp_path / "Other Note.md").touch()
        md_text = "See [[Other Note]].\n"

        output = md2html.md_to_html(md_text, title="t", src_path=src)
        soup = BeautifulSoup(output, "html.parser")
        link = soup.find("a", string="Other Note")

        assert link["href"] == "Other Note.html"

    def test_mermaidBlockStillRendersWithWikilinksPresent(self):
        md_text = "[[#Heading]]\n\n```mermaid\ngraph TD; A-->B;\n```\n\n## Heading\n"
        output = md2html.md_to_html(md_text, title="t")
        assert '<div class="mermaid">' in output
        assert "graph TD" in output


class TestMdToHtmlSafe:
    def test_convertsHeadingWikilinkAndKeepsHeadingIdForAnchor(self):
        md_text = "## F1. Some finding\n\nSee [[#F1. Some finding|F1]] above.\n"
        output = md2html.md_to_html_safe(md_text, title="t")
        soup = BeautifulSoup(output, "html.parser")

        heading = soup.find(["h3", "h4"], string="F1. Some finding")
        link = soup.find("a", string="F1")

        assert heading is not None and heading.get("id")
        assert link["href"] == f"#{heading['id']}"

    def test_classAttributeStillStrippedFromHeadings(self):
        md_text = "## Heading\n\nBody\n"
        output = md2html.md_to_html_safe(md_text, title="t")
        soup = BeautifulSoup(output, "html.parser")
        heading = soup.find(["h3", "h4"])
        assert heading.get("class") is None

    def test_unresolvedPageWikilinkFallsBackToPlainTextNotBrokenLink(self, tmp_path):
        src = tmp_path / "notebook.md"
        md_text = "See [[some-external-page]] for background.\n"

        output = md2html.md_to_html_safe(md_text, title="t", src_path=src)
        assert "[[" not in output
        assert "some-external-page" in output


class TestConvert:
    def test_writesHtmlFileWithResolvedWikilinks(self, tmp_path):
        src = tmp_path / "notebook.md"
        src.write_text(
            "## F1. Some finding\n\nSee [[#F1. Some finding|F1]].\n", encoding="utf-8"
        )
        dst = tmp_path / "notebook.html"

        md2html.convert(src, dst)

        output = dst.read_text(encoding="utf-8")
        assert "[[" not in output
        assert 'href="#f1-some-finding"' in output
