#!/usr/bin/env python3
"""
Collect public r/nba comments into data/nba_candidates.csv.

Timeboxed on purpose -- this is not a scraping project. It reads Reddit's
public RSS feeds only (no login, no API key), sleeps between requests to stay
polite, and stops after a fixed number of threads.

    python scripts/collect_nba.py              # defaults
    python scripts/collect_nba.py --threads 30 --sleep 7

The output is a pool of CANDIDATES to read and pick from. It is not
labels.csv. Copy the posts you keep into labels.csv yourself.
"""

import argparse
import csv
import html
import re
import sys
import time
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

import requests

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) takemeter-coursework/0.1"
ATOM = {"a": "http://www.w3.org/2005/Atom"}
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "nba_candidates.csv"

LISTINGS = [
    "https://www.reddit.com/r/nba/top/.rss?t=week&limit=50",
    "https://www.reddit.com/r/nba/top/.rss?t=month&limit=50",
    "https://www.reddit.com/r/nba/hot/.rss?limit=50",
]

SKIP_AUTHORS = {"/u/AutoModerator", "/u/nba_bot", "/u/NBA_MOD"}
MIN_WORDS = 8          # one-word "lol" replies carry no label signal
MAX_WORDS = 250        # walls of text get truncated at 128 tokens anyway


class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "br", "li"):
            self.parts.append(" ")


def to_text(content_html: str) -> str:
    parser = _Text()
    parser.feed(html.unescape(content_html or ""))
    text = " ".join("".join(parser.parts).split())
    return text.replace("&nbsp;", " ").strip()


def fetch(url: str, sleep: float, retries: int = 3) -> ET.Element | None:
    for attempt in range(retries):
        r = requests.get(url, headers={"User-Agent": UA}, timeout=20)
        if r.status_code == 200 and r.content.strip():
            return ET.fromstring(r.content)
        wait = sleep * (attempt + 2)
        print(f"  [{r.status_code}] backing off {wait:.0f}s", file=sys.stderr)
        time.sleep(wait)
    return None


def thread_links(sleep: float) -> list[tuple[str, str]]:
    seen, out = set(), []
    for url in LISTINGS:
        feed = fetch(url, sleep)
        time.sleep(sleep)
        if feed is None:
            continue
        for entry in feed.findall("a:entry", ATOM):
            link = entry.find("a:link", ATOM).get("href")
            title = entry.findtext("a:title", default="", namespaces=ATOM)
            m = re.search(r"/comments/([a-z0-9]+)/", link)
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                out.append((link, title))
    return out


def comments(thread_url: str, sleep: float) -> list[dict]:
    feed = fetch(thread_url.rstrip("/") + "/.rss?limit=100&sort=top", sleep)
    if feed is None:
        return []
    rows = []
    for entry in feed.findall("a:entry", ATOM):
        eid = entry.findtext("a:id", default="", namespaces=ATOM)
        if not eid.startswith("t1_"):          # t3_ is the post itself
            continue
        author = entry.findtext("a:author/a:name", default="", namespaces=ATOM)
        if author in SKIP_AUTHORS:
            continue
        text = to_text(entry.findtext("a:content", default="", namespaces=ATOM))
        words = len(text.split())
        if text in ("[deleted]", "[removed]") or not (MIN_WORDS <= words <= MAX_WORDS):
            continue
        rows.append({"text": text, "source_url": entry.find("a:link", ATOM).get("href")})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threads", type=int, default=30)
    ap.add_argument("--sleep", type=float, default=7.0)
    args = ap.parse_args()

    links = thread_links(args.sleep)
    print(f"{len(links)} threads found, reading {min(args.threads, len(links))}")

    seen, pool = set(), []
    for i, (link, title) in enumerate(links[: args.threads], 1):
        got = comments(link, args.sleep)
        fresh = [r for r in got if r["text"] not in seen]
        for r in fresh:
            seen.add(r["text"])
            r["thread"] = title
        pool.extend(fresh)
        print(f"  {i:>2}/{args.threads}  +{len(fresh):<3} total {len(pool):<4} {title[:60]}")
        time.sleep(args.sleep)

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["text", "thread", "source_url"])
        w.writeheader()
        w.writerows(pool)
    print(f"\nWrote {len(pool)} candidates to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
