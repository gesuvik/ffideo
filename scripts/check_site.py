#!/usr/bin/env python3
"""Zero-dependency structural checks for the FFideo static site."""

from __future__ import annotations

import argparse
import ipaddress
import re
import socket
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = sorted(ROOT.glob("*.html"))
EXPECTED_HTML = {
    "index.html",
    "install.html",
    "privacy.html",
    "eula.html",
    "refunds.html",
    "success.html",
}
EXPECTED_CNAME = "ffideo.gesuvik.lol"
CHECKOUT_PLACEHOLDER = "__CHECKOUT_URL__"
PLACEHOLDER_PATTERN = re.compile(r"__[A-Z0-9_]+__")
CONFIG_ENTRY_PATTERN = re.compile(r'^\s*([A-Za-z][A-Za-z0-9]*):\s*"([^"]+)"', re.MULTILINE)
RELEASE_ZIP_URL = "https://github.com/gesuvik/ffideo/releases/download/v1.0.0/FFideo-1.0.0.zip"
RELEASE_PAGE_URL = "https://github.com/gesuvik/ffideo/releases/tag/v1.0.0"
ALLOWED_EXTERNAL_HOSTS = {"github.com", "lemonsqueezy.com"}
ALLOWED_EXTERNAL_SUFFIXES = (".githubusercontent.com", ".lemonsqueezy.com")
FORBIDDEN_COPY = {
    "if checkout becomes available": "replace conditional checkout copy with the definitive offer",
    "when checkout opens": "replace conditional checkout copy with the definitive offer",
    "polar": "remove the superseded commerce provider",
}


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.config_links: list[dict[str, str | None]] = []
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
        if values.get("data-config-link"):
            self.config_links.append(values)
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, value))


def public_text_files() -> list[Path]:
    files = list(HTML_FILES)
    files.extend(sorted((ROOT / "assets").glob("*.js")))
    files.extend(sorted((ROOT / "assets").glob("*.css")))
    files.extend(sorted((ROOT / "release-docs").glob("*.md")))
    files.extend([ROOT / "README.md", ROOT / "robots.txt", ROOT / "CNAME"])
    return [path for path in files if path.exists()]


def parse_config(config_text: str) -> dict[str, str]:
    return dict(CONFIG_ENTRY_PATTERN.findall(config_text))


def external_url_policy_error(url: str) -> str | None:
    split = urlsplit(url)
    host = (split.hostname or "").lower()
    if split.scheme != "https" or not host:
        return "URL must use HTTPS and include a host"
    if split.username or split.password:
        return "URL credentials are not allowed"
    try:
        if split.port not in {None, 443}:
            return "only the default HTTPS port is allowed"
    except ValueError as error:
        return str(error)
    if host not in ALLOWED_EXTERNAL_HOSTS and not host.endswith(ALLOWED_EXTERNAL_SUFFIXES):
        return f"host is not approved: {host}"
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError as error:
        return f"host resolution failed: {error}"
    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if not ip.is_global:
            return f"host resolves to a non-public address: {ip}"
    return None


class ApprovedRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):  # type: ignore[no-untyped-def]
        failure = external_url_policy_error(new_url)
        if failure:
            raise URLError(f"unsafe redirect: {failure}")
        return super().redirect_request(request, file_pointer, code, message, headers, new_url)


def external_url_error(url: str) -> tuple[str, str] | None:
    policy_failure = external_url_policy_error(url)
    if policy_failure:
        return ("unsafe external URL", policy_failure)

    headers = {"User-Agent": "FFideo-site-check/1.0"}
    opener = build_opener(ApprovedRedirectHandler())
    for method in ("HEAD", "GET"):
        request_headers = headers | ({"Range": "bytes=0-0"} if method == "GET" else {})
        request = Request(url, headers=request_headers, method=method)
        try:
            with opener.open(request, timeout=15) as response:
                if response.status >= 400:
                    return ("unreachable external URL", f"HTTP {response.status}")
                return None
        except HTTPError as error:
            if method == "HEAD" and error.code in {403, 405}:
                continue
            return ("unreachable external URL", f"HTTP {error.code}")
        except (URLError, TimeoutError, OSError) as error:
            return ("unreachable external URL", str(error.reason if isinstance(error, URLError) else error))
    return ("unreachable external URL", "request failed")


def check(*, check_external: bool = False) -> list[str]:
    errors: list[str] = []
    parsed: dict[Path, ReferenceParser] = {}

    found_html = {page.name for page in HTML_FILES}
    missing_html = EXPECTED_HTML - found_html
    if missing_html:
        errors.append(f"Missing expected HTML pages: {', '.join(sorted(missing_html))}")

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

    config_path = ROOT / "assets" / "config.js"
    config_text = config_path.read_text(encoding="utf-8")
    config = parse_config(config_text)
    expected_config = {
        "releaseZipUrl": RELEASE_ZIP_URL,
        "releasePageUrl": RELEASE_PAGE_URL,
    }
    for key, expected_value in expected_config.items():
        actual_value = config.get(key)
        if actual_value != expected_value:
            errors.append(f"assets/config.js: expected {key}={expected_value!r}, found {actual_value!r}")

    checkout_value = config.get("checkoutUrl")
    if checkout_value is None:
        errors.append("assets/config.js: missing checkoutUrl")

    for key, value in config.items():
        if PLACEHOLDER_PATTERN.fullmatch(value):
            if key != "checkoutUrl" or value != CHECKOUT_PLACEHOLDER:
                errors.append(f"assets/config.js: unapproved placeholder for {key}: {value}")
            continue
        split = urlsplit(value)
        if split.scheme != "https" or not split.netloc:
            errors.append(f"assets/config.js: {key} must be an absolute HTTPS URL or approved placeholder")
            continue
        if check_external:
            failure = external_url_error(value)
            if failure:
                failure_kind, failure_detail = failure
                errors.append(f"assets/config.js: {failure_kind} for {key}: {value} ({failure_detail})")

    for page, parser in parsed.items():
        for attrs in parser.config_links:
            key = attrs.get("data-config-link") or ""
            if key not in config:
                errors.append(f"{page.name}: unknown data-config-link key {key!r}")
                continue
            if PLACEHOLDER_PATTERN.fullmatch(config[key]):
                if attrs.get("aria-disabled") != "true":
                    errors.append(f"{page.name}: placeholder-backed {key} link must be statically aria-disabled")
                if attrs.get("tabindex") != "-1":
                    errors.append(f"{page.name}: placeholder-backed {key} link must use tabindex=-1")

    placeholder_locations: list[tuple[str, str]] = []
    for path in public_text_files():
        text = path.read_text(encoding="utf-8")
        for token in PLACEHOLDER_PATTERN.findall(text):
            placeholder_locations.append((path.relative_to(ROOT).as_posix(), token))
        lowered = text.lower()
        for phrase, action in FORBIDDEN_COPY.items():
            if phrase in lowered:
                errors.append(f"{path.relative_to(ROOT)}: {action}; found {phrase!r}")

    allowed_placeholder_locations = [
        [],
        [("assets/config.js", CHECKOUT_PLACEHOLDER)],
    ]
    if placeholder_locations not in allowed_placeholder_locations:
        rendered = ", ".join(f"{path}:{token}" for path, token in placeholder_locations) or "none"
        errors.append(
            "Placeholders must be limited to the single centralized checkout value in "
            f"assets/config.js; found {rendered}"
        )

    for page in HTML_FILES:
        text = page.read_text(encoding="utf-8")
        if "https://" in text or "http://" in text:
            errors.append(f"{page.name}: absolute web URL found; use centralized config or relative assets")

    index_text = (ROOT / "index.html").read_text(encoding="utf-8").lower()
    for required in ("us$4.99", "one-time purchase", "five free exports"):
        if required not in index_text:
            errors.append(f"index.html: definitive offer is missing {required!r}")

    success_path = ROOT / "success.html"
    if success_path.exists():
        success_text = success_path.read_text(encoding="utf-8").lower()
        for required in ("license key", "activate pro", "paste", "install.html", 'data-config-link="releasezipurl"'):
            if required not in success_text:
                errors.append(f"success.html: missing post-purchase guidance or link {required!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-external",
        action="store_true",
        help="request every configured public HTTPS URL in addition to structural checks",
    )
    args = parser.parse_args()
    errors = check(check_external=args.check_external)
    if errors:
        print("Static checks failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(
        f"Static checks passed: {len(HTML_FILES)} HTML pages; local links, fragments, "
        "centralized URLs, placeholders, and checkout guidance verified"
        f"{' with external URL requests' if args.check_external else ''}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
