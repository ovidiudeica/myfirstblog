"""Validate generated blog metadata using only the Python standard library."""
import argparse
import json
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

SITE = "https://ovidiudeica.github.io/myfirstblog"
IMAGE = SITE + "/assets/images/og-preview-sharp.png"
ALT = "My First Blog homepage preview"
TITLE = "Welcome to my blog"
PUBLISHED = "2020-07-05T00:00:00+00:00"
HOME_DESCRIPTION = (
    "My First Blog is a simple personal website made with Jekyll and the Minima "
    "theme as a GitHub Learning Lab exercise. Hosted on GitHub Pages, it includes "
    "an introductory post from July 2020."
)
PAGES = {
    "index.html": (SITE + "/", HOME_DESCRIPTION, "website", "summary_large_image"),
    "2020/07/05/my-first-blog-post.html": (
        SITE + "/2020/07/05/my-first-blog-post.html", "Testing", "article", "summary"
    ),
}


class Head(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.meta = defaultdict(list)
        self.raw = defaultdict(list)
        self.canonicals = []
        self.canonical_tags = []
        self.title = ""
        self.json_ld = []
        self.in_head = self.in_title = self.in_json = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        if tag == "meta":
            key = attrs.get("property") or attrs.get("name")
            if key:
                self.meta[key].append(attrs.get("content", ""))
                self.raw[key].append(self.get_starttag_text())
        elif tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonicals.append(attrs.get("href", ""))
            self.canonical_tags.append(self.get_starttag_text())
        elif tag == "title":
            self.in_title = True
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_json = True
            self.json_ld.append("")

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        elif tag == "title":
            self.in_title = False
        elif tag == "script":
            self.in_json = False

    def handle_data(self, data):
        if self.in_head and self.in_title:
            self.title += data
        if self.in_head and self.in_json:
            self.json_ld[-1] += data


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(html, filename):
    url, description, kind, card = PAGES[filename]
    head = Head(html)
    require(head.canonicals == [url], "canonical must be unique and exact")
    require(head.title == TITLE + " | My First Blog", "document title changed")
    for key, values in head.meta.items():
        if key.startswith(("og:", "twitter:", "article:")):
            require(len(values) == 1, f"duplicate metadata: {key}")
    expected = {
        "og:url": url, "og:title": TITLE, "og:description": description,
        "description": description, "og:site_name": "My First Blog", "og:type": kind,
        "og:image": IMAGE, "og:image:width": "1200", "og:image:height": "627",
        "og:image:alt": ALT, "twitter:card": card, "twitter:title": TITLE,
        "twitter:image": IMAGE, "twitter:image:alt": ALT,
    }
    for key, value in expected.items():
        require(head.meta.get(key) == [value], f"{key}: expected one {value!r}")
    if kind == "article":
        require(head.meta.get("article:published_time") == [PUBLISHED],
                "article publication date changed")
        require(len(head.json_ld) == 1, "expected one article JSON-LD block")
        data = json.loads(head.json_ld[0])
        require(data.get("@type") == "BlogPosting", "article JSON-LD type changed")
        for key in ("datePublished", "dateModified"):
            require(data.get(key) == PUBLISHED, f"JSON-LD {key} changed")
    else:
        require("article:published_time" not in head.meta,
                "homepage must not acquire an article publication date")
    return head


def negative_tests(html, filename):
    head = validate(html, filename)
    image_tag = head.raw["og:image"][0]
    canonical = head.canonical_tags[0]
    og_url = head.raw["og:url"][0]
    mutations = {
        "missing og:image": html.replace(image_tag, "", 1),
        "relative image": html.replace(image_tag, image_tag.replace(IMAGE, "/assets/images/og-preview-sharp.png"), 1),
        "missing image baseurl": html.replace(image_tag, image_tag.replace("/myfirstblog/", "/"), 1),
        "duplicated image baseurl": html.replace(image_tag, image_tag.replace("/myfirstblog/", "/myfirstblog/myfirstblog/"), 1),
        "wrong canonical": html.replace(canonical, canonical.replace(SITE, SITE + "/wrong"), 1),
        "wrong og:url": html.replace(og_url, og_url.replace(SITE, SITE + "/wrong"), 1),
        "conflicting duplicate OG": html.replace("</head>", '<meta property="og:title" content="Wrong title"></head>', 1),
        "duplicate canonical": html.replace("</head>", canonical + "</head>", 1),
        "wrong image dimensions": html.replace(head.raw["og:image:width"][0], '<meta property="og:image:width" content="600">', 1),
    }
    if filename != "index.html":
        mutations["changed publication date"] = html.replace(PUBLISHED, "2021-07-05T00:00:00+00:00")
    for label, broken in mutations.items():
        require(broken != html, f"negative fixture did not change HTML: {label}")
        try:
            validate(broken, filename)
        except ValueError:
            continue
        raise ValueError(f"negative regression not detected: {filename}: {label}")
    return len(mutations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?", default="_site")
    parser.add_argument("--negative-tests", action="store_true")
    args = parser.parse_args()
    count = 0
    for filename in PAGES:
        html = (Path(args.site) / filename).read_text(encoding="utf-8")
        validate(html, filename)
        if args.negative_tests:
            count += negative_tests(html, filename)
        print(f"PASS: {filename}: canonical, OG, Twitter and publication metadata")
    if args.negative_tests:
        print(f"PASS: {count} negative regression cases rejected")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Metadata regression failed: {error}")
