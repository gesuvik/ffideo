#!/usr/bin/env python3
"""Zero-dependency structural checks for the FFideo static site."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = sorted(ROOT.glob("*.html"))
EXPECTED_CNAME = "ffideo.gesuvik.lol"
PLACEHOLDERS = {"__GITHUB_RELEASE_ZIP_URL__", "__CHECKOUT_URL__"}


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.lang: str | None = None
        self.title_seen = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang")
        if tag == "title":
            self.title_seen = True
        if values.get("id"):
            self.ids.add(values["id"] or "")
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, value))


def check() -> list[str]:
    errors: list[str] = []
    parsed: dict[Path, ReferenceParser] = {}

    if not HTML_FILES:
        return ["No HTML files found."]

    for page in HTML_FILES:
        parser = ReferenceParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parsed[page] = parser
        if parser.lang != "en":
            errors.append(f"{page.name}: expected default html lang='en'")
        if not parser.title_seen:
            errors.append(f"{page.name}: missing title")

    for page, parser in parsed.items():
        for attribute, reference in parser.references:
            split = urlsplit(reference)
            if split.scheme in {"http", "https", "mailto", "tel", "data"} or reference.startswith("//"):
                continue
            path_text = unquote(split.path)
            target = page if not path_text else (page.parent / path_text).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(f"{page.name}: {attribute} escapes site root: {reference}")
                continue
            if path_text and not target.exists():
                errors.append(f"{page.name}: missing local target: {reference}")
                continue
            if split.fragment and target.suffix == ".html":
                target_parser = parsed.get(target)
                if target_parser and split.fragment not in target_parser.ids:
                    errors.append(f"{page.name}: missing fragment #{split.fragment} in {target.name}")

    cname = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
    if cname != EXPECTED_CNAME:
        errors.append(f"CNAME: expected {EXPECTED_CNAME!r}, found {cname!r}")

    config = (ROOT / "assets" / "config.js").read_text(encoding="utf-8")
    for token in PLACEHOLDERS:
        if token not in config:
            errors.append(f"assets/config.js: missing centralized placeholder {token}")

    for page in HTML_FILES:
        text = page.read_text(encoding="utf-8")
        if "https://" in text or "http://" in text:
            errors.append(f"{page.name}: absolute web URL found; use centralized config or relative assets")

    return errors


def main() -> int:
    errors = check()
    if errors:
        print("Static checks failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"Static checks passed: {len(HTML_FILES)} HTML pages; local references, fragments, CNAME, and URL placeholders verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
