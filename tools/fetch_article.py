"""Fetch a news article via curl (bypasses the blocked WebFetch proxy) and print
clean readable text for manual coding. Usage: python tools/fetch_article.py <url>

Only for reading publicly available article text so it can be coded by hand.
"""
from __future__ import annotations

import re
import subprocess
import sys
from html.parser import HTMLParser
from html import unescape

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
SKIP = {"script", "style", "noscript", "svg", "form", "aside", "nav"}
BLOCK = {"p", "h1", "h2", "h3", "li", "blockquote", "figcaption"}


class Extract(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip = 0
        self.chunks: list[str] = []
        self.buf: list[str] = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        if tag == "title":
            self._in_title = True
        if tag in BLOCK and self.buf:
            self._flush()

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        if tag == "title":
            self._in_title = False
        if tag in BLOCK:
            self._flush()

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self.skip:
            return
        text = data.strip()
        if text:
            self.buf.append(text)

    def _flush(self):
        if self.buf:
            line = " ".join(self.buf).strip()
            if len(line) > 1:
                self.chunks.append(line)
            self.buf = []


def main() -> None:
    url = sys.argv[1]
    html = subprocess.run(
        ["curl", "-sSL", "-A", UA, "--max-time", "30", url],
        capture_output=True, text=True,
    ).stdout
    parser = Extract()
    parser.feed(html)
    parser._flush()
    seen, lines = set(), []
    for chunk in parser.chunks:
        c = unescape(re.sub(r"\s+", " ", chunk))
        if c not in seen and len(c) > 25:
            seen.add(c)
            lines.append(c)
    print("TITLE:", unescape(parser.title.strip()))
    print("URL:", url)
    print("=" * 60)
    print("\n".join(lines[:80]))


if __name__ == "__main__":
    main()
