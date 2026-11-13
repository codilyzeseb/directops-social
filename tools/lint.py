#!/usr/bin/env python3
"""Check a post against the house rules before it goes to Metricool.

    python3 tools/lint.py posts/<id>-<slug>

Reads post.json and slides.html in that folder. Exits 1 on any ERROR.
This is a floor, not the review: it cannot hear a sentence that sounds
like an advert, so read the copy aloud as well.
"""
import html
import json
import re
import struct
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BANNED_WORDS = [
    "quote", "quotes", "chatbot", "chatbots", "bot", "bots", "ai agent", "ai agents",
    "cheap", "beta", "no obligation", "guaranteed results", "guarantee", "guaranteed",
    "imagine", "game-changer", "game changer", "gamechanger", "revolutionise", "revolutionize",
    "revolutionary", "unlock", "unlocks", "seamless", "seamlessly", "elevate", "elevates",
    "cutting-edge", "cutting edge",
    # German equivalents
    "kostenvoranschlag", "unverbindlich", "billig", "garantiert", "garantie",
    "stellen sie sich vor", "revolutionär", "nahtlos", "bahnbrechend",
]
# the landing page is in the "Sie" form; a "du" in German copy is an error
GERMAN_DU = re.compile(r"\b(du|dich|dir|dein|deine|deinen|deinem|deiner|euch|euer|eure)\b", re.I)
PRICE = re.compile(r"(€|\$|£|\bCHF\b|\bAED\b|\bEUR\b|\bUSD\b)\s?\d|\d[\d.,']*\s?(€|\$|£|CHF\b|AED\b|EUR\b|USD\b|euros?\b|francs?\b|dirhams?\b)", re.I)
URL = re.compile(r"https?://\S+")
HASHTAG = re.compile(r"(?<!\w)#\w+")
LANDING = {"en": "systems.directops.ai/", "de": "systems.directops.ai/de"}

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_text(label, text, lang):
    low = text.lower()
    for w in BANNED_WORDS:
        if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low):
            err(f"{label}: banned word or phrase '{w}'")
    if "—" in text or "–" in text or " -- " in text:
        err(f"{label}: contains an em or en dash")
    if "!" in text:
        err(f"{label}: contains an exclamation mark")
    if PRICE.search(text):
        err(f"{label}: looks like a price ({PRICE.search(text).group(0)!r})")
    if lang == "de" and GERMAN_DU.search(text):
        err(f"{label}: German copy uses the du form ({GERMAN_DU.search(text).group(0)!r}); the brand uses Sie")
    if re.search(r"[ \t]+\n|\n{3,}", text):
        warn(f"{label}: trailing spaces or more than one blank line")
    if any("  " in line for line in text.split("\n")):
        warn(f"{label}: double space")


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    folder = Path(sys.argv[1])
    root = folder.resolve().parents[1]
    post = json.loads((folder / "post.json").read_text(encoding="utf-8"))
    pid, lang = post["id"], post.get("language", "en")

    ig = post["instagram"]
    fb = post["facebook"]

    # words
    check_text("instagram caption", ig["caption"], lang)
    check_text("instagram first comment", ig.get("first_comment", ""), lang)
    check_text("facebook caption", URL.sub("", fb["caption"]), lang)
    for i, alt in enumerate(post["alt"], 1):
        check_text(f"alt text {i}", alt, lang)
        if len(alt) > 1000:
            err(f"alt text {i}: longer than 1000 characters")
    slides = folder / "slides.html"
    if slides.exists():
        raw = slides.read_text(encoding="utf-8")
        raw = re.sub(r"<!--.*?-->|<style.*?</style>|<title>.*?</title>", " ", raw, flags=re.S)
        text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        check_text("image text", re.sub(r"\s+", " ", text), lang)
        if post.get("example") and "Example" not in text and "Beispiel" not in text:
            err("image text: an example conversation must carry the 'Example' label")

    # instagram
    ig_tags = HASHTAG.findall(ig["caption"]) + HASHTAG.findall(ig.get("first_comment", ""))
    if len(ig_tags) > 5:
        err(f"instagram: {len(ig_tags)} hashtags in caption plus first comment (limit 5)")
    if len(set(t.lower() for t in ig_tags)) != len(ig_tags):
        err("instagram: duplicate hashtag")
    if URL.search(ig["caption"]):
        err("instagram caption: contains a URL (links live in the bio)")
    if len(ig["caption"]) > 2200:
        err("instagram caption: longer than 2200 characters")

    # facebook
    fb_tags = HASHTAG.findall(fb["caption"]) + HASHTAG.findall(fb.get("first_comment", ""))
    if len(fb_tags) > 2:
        err(f"facebook: {len(fb_tags)} hashtags (limit 2)")
    # One link per Facebook post. It sits in the caption on at most two posts a
    # month (Meta is testing a cap on link posts) and in the first comment otherwise.
    cap_links = URL.findall(fb["caption"])
    com_links = URL.findall(fb.get("first_comment", ""))
    links = cap_links + com_links
    if len(links) != 1:
        err(f"facebook: expected exactly one link across caption and first comment, found {len(links)}")
    placement = fb.get("link_placement")
    if placement not in ("caption", "first_comment"):
        err("facebook: link_placement must be 'caption' or 'first_comment'")
    elif (placement == "caption") != bool(cap_links):
        err(f"facebook: link_placement says {placement} but the link is elsewhere")
    check_text("facebook first comment", URL.sub("", fb.get("first_comment", "")), lang)
    for link in links:
        u = urlparse(link.rstrip(".,)"))
        q = parse_qs(u.query)
        want = {"utm_source": "facebook", "utm_medium": "organic", "utm_campaign": "social_autopilot", "utm_content": pid}
        for k, v in want.items():
            if q.get(k) != [v]:
                err(f"facebook link: {k} should be '{v}', found {q.get(k)}")
        if (u.netloc + u.path) != LANDING[lang].rstrip("/") and (u.netloc + u.path) != LANDING[lang]:
            err(f"facebook link: {u.netloc + u.path} is not the {lang} landing page")

    # media
    media = post["media"]
    if not media:
        err("no media")
    if len(media) != len(post["alt"]):
        err(f"{len(media)} media files but {len(post['alt'])} alt texts")
    if post["format"] == "carousel" and not 3 <= len(media) <= 8:
        err(f"carousel has {len(media)} slides (3 to 8)")
    for m in media:
        p = root / m
        if not p.exists():
            err(f"media missing: {m}")
        elif png_size(p) != (1080, 1350):
            err(f"media {m} is {png_size(p)}, expected 1080x1350")

    # schedule
    when = datetime.fromisoformat(post["scheduled"]["dateTime"])
    if post["scheduled"]["timezone"] != "Asia/Dubai":
        err("schedule timezone must be Asia/Dubai (the brand's Metricool timezone)")
    else:
        when = when.replace(tzinfo=timezone(timedelta(hours=4)))
        if when <= datetime.now(timezone.utc):
            err("scheduled time is in the past")

    # truth
    if post.get("claims"):
        for c in post["claims"]:
            if not (c.get("source_url") and c.get("checked")):
                err(f"claim without a checked source: {c.get('claim')!r}")
    if post.get("signed_by_sebastian") and not post.get("bank_note"):
        err("signed 'Sebastian, Direct Ops' but no bank/notes.md entry is referenced")

    for w in warnings:
        print("warn :", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{pid}: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
