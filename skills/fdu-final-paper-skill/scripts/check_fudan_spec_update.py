#!/usr/bin/env python3
"""Check whether the local Fudan thesis specification reference may be stale."""

from __future__ import annotations

import argparse
import html.parser
import json
import re
import sys
import urllib.request
from pathlib import Path


DEFAULT_TIMEOUT = 20


class LinkTextParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_link = False
        self._parts: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            self._in_link = True
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._in_link:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._in_link:
            text = " ".join("".join(self._parts).split())
            if text:
                self.links.append(text)
            self._in_link = False


def load_snapshot(reference: Path, snapshot_path: Path | None) -> dict[str, str]:
    if snapshot_path is None:
        snapshot_path = reference.with_name("fudan-spec-snapshot.json")
    if snapshot_path.exists():
        return json.loads(snapshot_path.read_text(encoding="utf-8"))
    return {
        "official_page": "https://gs.fudan.edu.cn/6b/9f/c2806a27551/page.htm",
        "list_page": "https://gs.fudan.edu.cn/2806/list.htm",
        "expected_title": "复旦大学博士、硕士学位论文规范（2026.06修订版）.doc",
        "expected_marker": "2026.06",
    }


def fetch(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "fdu-final-paper-skill-update-check/1.0"},
    )
    with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT) as response:
        data = response.read()
        content_type = response.headers.get("Content-Type", "")
    encoding_match = re.search(r"charset=([\w-]+)", content_type)
    encoding = encoding_match.group(1) if encoding_match else "utf-8"
    return data.decode(encoding, errors="replace")


def extract_link_texts(html: str) -> list[str]:
    parser = LinkTextParser()
    parser.feed(html)
    return parser.links


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


def check_reference(reference: Path, snapshot: dict[str, str]) -> list[str]:
    errors: list[str] = []
    reference_text = reference.read_text(encoding="utf-8")
    for key in ("official_page", "list_page", "expected_title", "expected_marker"):
        value = snapshot.get(key, "")
        if value and value not in reference_text:
            errors.append(f"Reference does not contain snapshot {key}: {value}")
    return errors


def check_online(snapshot: dict[str, str]) -> list[str]:
    warnings: list[str] = []
    expected_title = snapshot["expected_title"]
    expected_marker = snapshot.get("expected_marker", "")

    official_html = fetch(snapshot["official_page"])
    list_html = fetch(snapshot["list_page"])
    official_text = normalized(official_html)
    list_text = normalized(list_html)

    if normalized(expected_title) not in official_text + list_text:
        warnings.append(f"Expected title not found on official pages: {expected_title}")
    if expected_marker and expected_marker not in official_text + list_text:
        warnings.append(f"Expected marker not found on official pages: {expected_marker}")

    candidates = [
        text
        for text in extract_link_texts(list_html)
        if "论文规范" in text or "学位论文" in text or "GB/T" in text
    ]
    unexpected = [text for text in candidates if expected_marker and expected_marker not in text]
    newer_hint = [
        text
        for text in unexpected
        if re.search(r"20(2[7-9]|[3-9]\d)|2026\.(0[7-9]|1[0-2])", text)
    ]
    if newer_hint:
        warnings.append("Possible newer official item(s): " + " | ".join(newer_hint[:5]))

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--fail-on-change", action="store_true")
    args = parser.parse_args()

    reference = args.reference.resolve()
    snapshot = load_snapshot(reference, args.snapshot)

    issues = check_reference(reference, snapshot)
    if not args.offline:
        issues.extend(check_online(snapshot))

    if issues:
        for issue in issues:
            print(f"WARNING: {issue}", file=sys.stderr)
        print("Fudan specification check found possible drift.", file=sys.stderr)
        return 2 if args.fail_on_change else 0

    mode = "offline" if args.offline else "online"
    print(f"Fudan specification check passed ({mode}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
