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


def _token(level, id_, children=None):
    return {"level": level, "id": id_, "html": id_, "children": children or []}


class TestDropTitleHeading:
    def test_dropsFirstTopLevelTokenPromotingItsChildren(self):
        tokens = [
            _token(1, "title", children=[_token(2, "intro-section")]),
            _token(1, "part-i"),
            _token(1, "part-ii", children=[_token(2, "f1")]),
        ]
        result = md2html.drop_title_heading(tokens)
        assert [t["id"] for t in result] == ["intro-section", "part-i", "part-ii"]

    def test_returnsEmptyListWhenTitleHasNoSiblingsOrChildren(self):
        tokens = [_token(1, "title")]
        assert md2html.drop_title_heading(tokens) == []

    def test_leavesTokensUnchangedWhenNoTitleLevelPresent(self):
        tokens = [_token(2, "section-one"), _token(2, "section-two")]
        assert md2html.drop_title_heading(tokens) == tokens

    def test_leavesEmptyListUnchanged(self):
        assert md2html.drop_title_heading([]) == []


class TestRenderToc:
    def test_rendersNestedListWithTitleSpan(self):
        tokens = [_token(1, "part-i", children=[_token(2, "f1")])]
        html = md2html.render_toc(tokens, "Contents")
        soup = BeautifulSoup(html, "html.parser")

        assert soup.find("div", class_="toc") is not None
        assert soup.find("span", class_="toctitle").text == "Contents"
        top_li = soup.find("ul").find("li", recursive=False)
        assert top_li.find("a", recursive=False)["href"] == "#part-i"
        assert [a["href"] for a in top_li.find("ul").find_all("a")] == ["#f1"]

    def test_returnsEmptyStringForNoTokens(self):
        assert md2html.render_toc([], "Contents") == ""


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
        assert result == "[here](Other%20Note.html)"

    def test_pageLinkWithoutAliasUsesPageNameAsText(self, tmp_path):
        src = tmp_path / "notebook.md"
        (tmp_path / "Other Note.md").touch()

        result = md2html.convert_wikilinks("[[Other Note]]", {}, src)
        assert result == "[Other Note](Other%20Note.html)"

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

        assert link["href"] == "Other%20Note.html"

    def test_mermaidBlockStillRendersWithWikilinksPresent(self):
        md_text = "[[#Heading]]\n\n```mermaid\ngraph TD; A-->B;\n```\n\n## Heading\n"
        output = md2html.md_to_html(md_text, title="t")
        assert '<div class="mermaid">' in output
        assert "graph TD" in output

    def test_autoGeneratesTocFromHeadings(self):
        md_text = "# Top\n\nIntro\n\n## Section One\n\nBody\n\n## Section Two\n\nMore\n"
        output = md2html.md_to_html(md_text, title="t")
        soup = BeautifulSoup(output, "html.parser")

        toc = soup.find("div", class_="toc")
        assert toc is not None
        toc_links = [a["href"] for a in toc.find_all("a")]
        # The document title (h1) is excluded; only the h2 sections are listed.
        assert toc_links == ["#section-one", "#section-two"]
        # The TOC must come before the document content, not after it.
        assert output.index('class="toc"') < output.index("<h1")

    def test_tocExcludesSubHeadingsBelowTwoLevelsDeep(self):
        md_text = (
            "# Top\n\n## Section One\n\n### Sub-section\n\nBody\n\n## Section Two\n"
        )
        output = md2html.md_to_html(md_text, title="t")
        soup = BeautifulSoup(output, "html.parser")

        toc = soup.find("div", class_="toc")
        toc_links = [a["href"] for a in toc.find_all("a")]
        assert toc_links == ["#section-one", "#section-two"]
        assert "#sub-section" not in toc_links

    def test_tocRetainsPartLevelHeadingsWithNestedSections(self):
        md_text = (
            "# Notebook Title\n\n## Where this stands\n\n"
            "# Part I - Method\n\n"
            "# Part II - Findings\n\n## F1. First\n\n## F2. Second\n"
        )
        output = md2html.md_to_html(md_text, title="t")
        soup = BeautifulSoup(output, "html.parser")

        toc = soup.find("div", class_="toc")
        top_lis = toc.find("ul").find_all("li", recursive=False)
        top_level_links = [li.find("a", recursive=False)["href"] for li in top_lis]
        assert top_level_links == ["#where-this-stands", "#part-i-method", "#part-ii-findings"]

        part_two_li = next(li for li in top_lis if li.find("a", recursive=False)["href"] == "#part-ii-findings")
        nested_links = [a["href"] for a in part_two_li.find("ul").find_all("a")]
        assert nested_links == ["#f1-first", "#f2-second"]

    def test_noTocWhenOnlyTitleHeadingPresent(self):
        md_text = "# Top\n\nJust an intro, no sections.\n"
        output = md2html.md_to_html(md_text, title="t")
        assert 'class="toc"' not in output
        assert 'class="page-layout"' not in output

    def test_tocIsSideBySideWithContentNotStackedAbove(self):
        md_text = "# Top\n\n## Section One\n\nBody\n"
        output = md2html.md_to_html(md_text, title="t")
        soup = BeautifulSoup(output, "html.parser")

        layout = soup.find("div", class_="page-layout")
        assert layout is not None
        children = [c for c in layout.find_all(recursive=False)]
        assert [c.get("class") for c in children] == [["toc"], ["content"]]
        assert children[1].find("h1") is not None

    def test_doesNotDuplicateTocWhenMarkerAlreadyPresent(self):
        md_text = "[TOC]\n\n## Section One\n\nBody\n"
        output = md2html.md_to_html(md_text, title="t")
        assert output.count('class="toc"') == 1

    def test_noTocWhenNoHeadings(self):
        md_text = "Just a paragraph, no headings here.\n"
        output = md2html.md_to_html(md_text, title="t")
        assert 'class="toc"' not in output
        assert 'class="page-layout"' not in output

    def test_addsScrollSpyScriptWhenTocPresent(self):
        md_text = "# Top\n\n## Section One\n\nBody\n"
        output = md2html.md_to_html(md_text, title="t")
        assert "IntersectionObserver" in output

    def test_noScrollSpyScriptWhenNoToc(self):
        md_text = "Just a paragraph, no headings here.\n"
        output = md2html.md_to_html(md_text, title="t")
        assert "IntersectionObserver" not in output


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

    def test_doesNotAddTableOfContents(self):
        md_text = "# Top\n\n## Section One\n\nBody\n\n## Section Two\n\nMore\n"
        output = md2html.md_to_html_safe(md_text, title="t")
        assert "toc" not in output.lower()

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


NESTED_LIST_WITH_FENCE = (
    "1. **First**\n"
    "2. **Second**\n"
    "   1. Run:\n"
    "      ```\n"
    "      logTrace io.undertow\n"
    "      ```\n"
    "   2. Next\n"
    "3. **Third**\n"
)

BOTH_RENDERERS = pytest.mark.parametrize("render", [md2html.md_to_html, md2html.md_to_html_safe])


def render_soup(render, md_text):
    return BeautifulSoup(render(md_text, title="t"), "html.parser")


def direct_item_texts(list_tag):
    return [li.get_text(" ", strip=True) for li in list_tag.find_all("li", recursive=False)]


class TestNestedListsAndFences:
    @BOTH_RENDERERS
    def test_threeSpaceIndentedSublistIsNested(self, render):
        soup = render_soup(render, NESTED_LIST_WITH_FENCE)

        outer = soup.find("ol")
        assert len(outer.find_all("li", recursive=False)) == 3
        inner = outer.find_all("li", recursive=False)[1].find("ol")
        assert [text.split()[0] for text in direct_item_texts(inner)] == ["Run:", "Next"]

    @BOTH_RENDERERS
    def test_fencedBlockInsideListItemIsABlockNotInlineCode(self, render):
        soup = render_soup(render, NESTED_LIST_WITH_FENCE)

        pre = soup.find("pre")
        assert pre is not None and pre.find_parent("li") is not None
        assert "logTrace io.undertow" in pre.get_text()

    @BOTH_RENDERERS
    def test_twoSpaceBulletNestingIsNestedThreeDeep(self, render):
        soup = render_soup(render, "- a\n  - b\n    - c\n- d\n")
        assert soup.find("ul").find("ul").find("ul") is not None

    @BOTH_RENDERERS
    def test_closingFenceWithTrailingWhitespaceEndsTheFence(self, render):
        soup = render_soup(render, "```\ncode\n```  \t\n- a\n  - b\n")
        assert soup.find("ul").find("ul") is not None

    @BOTH_RENDERERS
    def test_indentedCodeWithListSyntaxStaysCode(self, render):
        soup = render_soup(render, "para\n\n    - literal\n      - child\n")
        assert soup.find("ul") is None
        assert "- literal" in soup.find("pre").get_text()

    @BOTH_RENDERERS
    def test_fenceOpenedOnListMarkerLineIsLiteral(self, render):
        soup = render_soup(render, "- ```\n  - x\n    - y\n  ```\n")
        assert soup.find("pre") is not None
        assert soup.find("ul").find("ul") is None

    @BOTH_RENDERERS
    def test_topLevelFenceIndentedUpToThreeSpacesIsLiteral(self, render):
        soup = render_soup(render, " ```\n - x\n   - y\n ```\n")
        assert soup.find("pre") is not None and soup.find("ul") is None

    @BOTH_RENDERERS
    def test_emptyListItemStillParentsNestedItems(self, render):
        soup = render_soup(render, "- \n  - child\n")
        assert soup.find("ul").find("ul") is not None

    @BOTH_RENDERERS
    def test_inlineCodeSpanOfThreeBackticksIsNotAFenceOpener(self, render):
        soup = render_soup(render, "```example```\n- a\n  - b\n")
        assert soup.find("pre") is None
        assert soup.find("ul").find("ul") is not None

    @BOTH_RENDERERS
    def test_rawPreBlockContentsAreLeftLiteral(self, render):
        soup = render_soup(render, "<pre>\n- a\n  - b\n</pre>\n")
        # The leading newline is the source's own (browsers drop it after <pre>).
        assert "- a\n  - b\n" in soup.find("pre").get_text()

    @BOTH_RENDERERS
    def test_fencedBlockIsASingleHighlightedPreInCodehiliteWrapper(self, render):
        soup = render_soup(render, "```python\nx = 1\n```\n")
        assert len(soup.find_all("pre")) == 1
        assert soup.find("pre").parent.name == "div"

    @BOTH_RENDERERS
    def test_lazyContinuationLineKeepsListContext(self, render):
        soup = render_soup(render, "- item\ncontinuation\n  - child\n")
        assert soup.find("ul").find("ul") is not None

    @BOTH_RENDERERS
    def test_thematicBreakIsNotAListMarker(self, render):
        soup = render_soup(render, "- - -\n\n  paragraph\n")
        assert soup.find("hr") is not None
        assert soup.find("pre") is None


class TestInlineFormatting:
    @BOTH_RENDERERS
    def test_doubleTildeBecomesDel(self, render):
        soup = render_soup(render, "keep ~~drop~~ keep\n")
        assert soup.find("del").get_text() == "drop"
        assert soup.find("s") is None

    @BOTH_RENDERERS
    def test_orderedListMayDirectlyFollowAParagraphLine(self, render):
        soup = render_soup(render, "**Steps**:\n1. one\n2. two\n")
        assert direct_item_texts(soup.find("ol")) == ["one", "two"]


def heading_ids(soup):
    return [h["id"] for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]


def hrefs(soup):
    return [a["href"] for a in soup.find_all("a", href=True)]


def wikilink_href(soup):
    """href of the link in the body paragraph (the side TOC also links to headings)."""
    return soup.find("p").find("a")["href"]


class TestHeadingIdsAndToc:
    @BOTH_RENDERERS
    def test_multiLineSetextHeadingIdTreatsLineBreakAsSpace(self, render):
        soup = render_soup(render, "First line\nsecond line\n---\n\nSee [[#First line second line]].\n")
        assert heading_ids(soup) == ["first-line-second-line"]
        assert wikilink_href(soup) == "#first-line-second-line"

    @BOTH_RENDERERS
    def test_wikilinkTargetsTheHeadingTheParserNumbered(self, render):
        # The first "Notes" heading is nested in a list item, which a regex over
        # the source wouldn't see; the second must still be Notes_1.
        soup = render_soup(render, "- parent\n  ## Notes\n\n## Notes!\n\n[[#Notes!]]\n")
        assert heading_ids(soup) == ["notes", "notes_1"]
        assert wikilink_href(soup) == "#notes_1"

    @BOTH_RENDERERS
    def test_wikilinkIgnoresHeadingLookalikesInIndentedFences(self, render):
        # Content lines of an indented fence may start at column 0.
        soup = render_soup(render, "  ```\n## Notes\n  ```\n\n## Notes!\n\n[[#Notes!]]\n")
        assert heading_ids(soup) == ["notes"]
        assert wikilink_href(soup) == "#notes"

    @BOTH_RENDERERS
    def test_duplicateIdsBumpAnExistingNumericSuffix(self, render):
        soup = render_soup(render, "## Rate_1\n\n## Rate_1!\n")
        assert heading_ids(soup) == ["rate_1", "rate_2"]

    @BOTH_RENDERERS
    def test_headingsWithNoSluggableTextGetNumberedIds(self, render):
        soup = render_soup(render, "## !!!\n\n## ???\n")
        assert heading_ids(soup) == ["_1", "_2"]

    def test_tocEntryDoesNotNestTheHeadingsLinkInsideItsOwnAnchor(self):
        soup = render_soup(md2html.md_to_html, "# T\n\n## [Docs](https://example.com)\n\n## B\n")
        entry = soup.find("div", class_="toc").find("a", href="#docs")
        assert entry.find("a") is None
        assert entry.get_text() == "Docs"

    def test_tocEntryUnwrapsRawHtmlAnchorsToo(self):
        soup = render_soup(md2html.md_to_html, '# T\n\n## <a href="https://example.com">Docs</a> now\n\n## B\n')
        entry = soup.find("div", class_="toc").find("a", href="#docs-now")
        assert entry.find("a") is None
        assert entry.get_text() == "Docs now"

    @BOTH_RENDERERS
    def test_indentedCodeBlockGetsTheHighlightWrapper(self, render):
        soup = render_soup(render, "para\n\n    x = 1\n")
        pre = soup.find("pre")
        assert pre.parent.name == "div"
        assert "x = 1" in pre.get_text()

    def test_explicitTocMarkerIncludesTheTitleHeading(self):
        soup = render_soup(md2html.md_to_html, "[TOC]\n\n# Title\n\n## A\n")
        toc = soup.find("div", class_="toc")
        assert [a["href"] for a in toc.find_all("a")] == ["#title", "#a"]
        assert soup.find("div", class_="page-layout") is None

    def test_tocMarkerLookalikeInsideRawScriptIsLeftAlone(self):
        md_text = '[TOC]\n\n# T\n\n<script>\nconst example = "<p>[TOC]</p>";\n</script>\n'
        output = md2html.md_to_html(md_text, title="t")
        assert output.count('class="toc"') == 1
        assert 'const example = "<p>[TOC]</p>";' in output

    def test_safeModeExpandsExplicitTocMarkerThroughAllLevels(self):
        md_text = "[TOC]\n\n# T\n\n## A\n\n### B\n\n#### C\n"
        soup = render_soup(md2html.md_to_html_safe, md_text)
        assert hrefs(soup) == ["#t", "#a", "#b", "#c"]
        assert "[TOC]" not in soup.get_text()

    def test_safeModeWithoutMarkerAddsNoToc(self):
        soup = render_soup(md2html.md_to_html_safe, "# T\n\n## A\n")
        assert hrefs(soup) == []


class TestTocMarkerAsReferenceLink:
    @BOTH_RENDERERS
    def test_tocDefinedAsAReferenceLinkStaysALink(self, render):
        soup = render_soup(render, "[TOC]: https://example.com\n\n[TOC]\n\n## A\n")
        link = soup.find("p").find("a")
        assert link["href"] == "https://example.com"
        assert link.get_text() == "TOC"


class TestSafeModeMermaidWarning:
    WARNING = "cannot render Mermaid"

    def warns(self, md_text, capsys):
        md2html.md_to_html_safe(md_text)
        return capsys.readouterr().err.count(self.WARNING)

    def test_warnsForPlainFence(self, capsys):
        assert self.warns("```mermaid\ngraph TD; A-->B;\n```\n", capsys) == 1

    def test_warnsForFenceInsideListItem(self, capsys):
        assert self.warns("- item\n\n  ```mermaid\n  graph TD; A-->B;\n  ```\n", capsys) == 1

    def test_warnsForTildeAndUnclosedFences(self, capsys):
        assert self.warns("~~~mermaid\ngraph TD; A-->B;\n~~~\n", capsys) == 1
        assert self.warns("```mermaid\ngraph TD; A-->B;\n", capsys) == 1

    def test_warnsOnceForSeveralFences(self, capsys):
        md_text = "```mermaid\nA\n```\n\n```mermaid\nB\n```\n"
        assert self.warns(md_text, capsys) == 1

    def test_doesNotWarnForExampleInsideAnotherFence(self, capsys):
        md_text = "````markdown\n```mermaid\ngraph TD; A-->B;\n```\n````\n"
        assert self.warns(md_text, capsys) == 0

    def test_doesNotWarnWithoutMermaid(self, capsys):
        assert self.warns("```python\nprint(1)\n```\n", capsys) == 0


class TestHighlightedBlockFontSize:
    def test_codeInsidePreDoesNotShrinkTheFontAgain(self):
        output = md2html.md_to_html("```python\nprint(1)\n```\n", theme_name="plain")
        soup = BeautifulSoup(output, "html.parser")
        css = soup.find("style").get_text()
        rule = next(line for line in css.splitlines() if line.startswith("pre code"))
        assert "font-size: inherit" in rule
