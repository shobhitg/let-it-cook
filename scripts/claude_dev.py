#!/usr/bin/env python3
"""List, fetch, and check claude.dev blog posts for the playbook skill. Stdlib only.

usage: python3 -I scripts/claude_dev.py COMMAND
  list             every post in the claude.dev RSS feed, newest first
  new              feed posts that have no digest in skills/playbook/posts/
  fetch [SLUG...]  save each post's text to .cache/posts/ (default: every post with a digest)
  check-quotes     fail if any > "quote" in the skill is missing from its cached post
"""
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path

FEED = "https://claude.dev/rss.xml"
ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "playbook"
POSTS = SKILL / "posts"  # one digest per post; a digest's existence marks the post as read
CACHE = ROOT / ".cache" / "posts"  # full post text, gitignored


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "let-it-cook-refresh"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def feed():
    posts = []
    for item in ET.fromstring(get(FEED)).iter("item"):
        link = item.findtext("link", "").strip()
        posts.append({
            "slug": link.rstrip("/").rsplit("/", 1)[-1],
            "url": link,
            "title": item.findtext("title", "").strip(),
            "date": parsedate_to_datetime(item.findtext("pubDate")).date().isoformat(),
            "category": item.findtext("category", "").strip(),
        })
    return sorted(posts, key=lambda post: post["date"], reverse=True)


class PostText(HTMLParser):
    """Markdown-ish text of a post page, from its <h1> up to the "Related posts" footer."""

    SKIP = {"script", "style", "svg", "noscript", "nav", "button"}
    OPEN = {
        "p": "\n\n", "div": "\n", "section": "\n", "li": "\n- ", "tr": "\n|", "td": " ", "th": " ",
        "br": "\n", "blockquote": "\n\n> ", "figcaption": "\n\n",
    }
    CLOSE = {"td": " |", "th": " |", "p": "\n", "li": "\n", **{f"h{n}": "\n" for n in range(1, 5)}}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skipping, self.started, self.done, self.pre = [], 0, False, False, False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skipping += 1
        self.started = self.started or tag == "h1"
        if not self.started or self.done or self.skipping:
            return
        if tag in ("h1", "h2", "h3", "h4"):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "pre":
            self.pre = True
            self.out.append("\n\n```\n")
        elif tag == "code" and not self.pre:
            self.out.append("`")
        else:
            self.out.append(self.OPEN.get(tag, ""))

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skipping = max(0, self.skipping - 1)
            return
        if not self.started or self.done or self.skipping:
            return
        if tag == "pre":
            self.pre = False
            self.out.append("\n```\n\n")
        elif tag == "code" and not self.pre:
            self.out.append("`")
        else:
            self.out.append(self.CLOSE.get(tag, ""))

    def handle_data(self, data):
        if not self.started or self.done or self.skipping:
            return
        if data.strip() == "Related posts":
            self.done = True
            return
        self.out.append(data if self.pre else re.sub(r"\s+", " ", data))


def post_text(page):
    parser = PostText()
    parser.feed(page)
    lines, in_code = [], False
    for line in "".join(parser.out).splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        if "░" not in line:  # the page's reading-progress bar
            lines.append(line.rstrip() if in_code else " ".join(line.split()))
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def normalized(text):
    plain = {"‘": "'", "’": "'", "“": '"', "”": '"', "—": "-", "–": "-", "\xa0": " "}
    text = text.translate(str.maketrans(plain))
    return " ".join(text.split()).lower()


def check_quotes():
    sources = {path.stem: normalized(path.read_text()) for path in CACHE.glob("*.md")}
    everything = " ".join(sources.values())
    problems = 0
    for doc in sorted(SKILL.rglob("*.md")):
        # A digest's quotes must come from its own post; anything else may quote any post.
        haystack = sources.get(doc.stem, "") if doc.parent == POSTS else everything
        if doc.parent == POSTS and not haystack:
            print(f"NO CACHED SOURCE  {doc.relative_to(ROOT)}  (run: fetch {doc.stem})")
            problems += 1
            continue
        for quote in re.findall(r'^> "(.+)"\s*$', doc.read_text(), re.M):
            if normalized(quote) not in haystack:
                print(f"NOT IN SOURCE  {doc.relative_to(ROOT)}: {quote[:100]}")
                problems += 1
    print(f"{problems} problem(s)" if problems else "every quote found in its source")
    return 1 if problems else 0


def main(argv):
    command, args = (argv[0], argv[1:]) if argv else ("", [])
    if command in ("list", "new"):
        for post in feed():
            if command == "list" or not (POSTS / f"{post['slug']}.md").exists():
                print(f"{post['date']}  {post['slug']}  [{post['category']}]  {post['title']}")
    elif command == "fetch":
        CACHE.mkdir(parents=True, exist_ok=True)
        for slug in args or sorted(path.stem for path in POSTS.glob("*.md")):
            url = f"https://claude.dev/blog/{slug}/"
            body = post_text(get(url))
            (CACHE / f"{slug}.md").write_text(f"<!-- {url} -->\n\n{body}")
            print(f".cache/posts/{slug}.md  {len(body.split())} words")
    elif command == "check-quotes":
        return check_quotes()
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
