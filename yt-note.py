#!/usr/bin/env python3
"""yt-note: fetch a YouTube video's transcript and save it as a note in youtube/.

Usage:
    python yt-note.py <youtube-url> [slug]

Pulls title/channel via YouTube oEmbed (no API key) and the caption track via
youtube-transcript-api, then writes youtube/<slug>.md with frontmatter and the
transcript in readable paragraphs. Slug defaults to a slugified title.
"""
import os, sys, re, json, datetime, urllib.request
from urllib.parse import urlparse, parse_qs

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "youtube")
PARA_CHARS = 700  # start a new paragraph after roughly this many characters

def video_id(url):
    u = urlparse(url)
    if u.netloc.endswith("youtu.be"):
        return u.path.lstrip("/").split("/")[0]
    if "/shorts/" in u.path:
        return u.path.split("/shorts/")[1].split("/")[0]
    v = parse_qs(u.query).get("v")
    if v:
        return v[0]
    sys.exit("ERROR: could not extract video id from: " + url)

def slugify(title, max_words=8):
    words = re.sub(r"[^a-z0-9 ]", "", title.lower()).split()
    return "-".join(words[:max_words]) or "untitled"

def fetch_meta(vid):
    try:
        with urllib.request.urlopen(
                "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v="
                + vid + "&format=json", timeout=15) as r:
            oe = json.load(r)
        return oe.get("title", ""), oe.get("author_name", "")
    except Exception as e:
        print("WARN: oEmbed failed (%s), continuing without title" % e)
        return "", ""

def fetch_transcript(vid):
    from youtube_transcript_api import YouTubeTranscriptApi
    langs = ["en", "en-US", "en-GB", "de"]
    try:                                   # v1.x API
        api = YouTubeTranscriptApi()
        try:
            fetched = api.fetch(vid, languages=langs)
        except Exception:
            tl = api.list(vid)             # fall back to whatever exists
            fetched = next(iter(tl)).fetch()
        return [s.text for s in fetched], getattr(fetched, "language_code", "")
    except AttributeError:                 # pre-1.0 API
        from youtube_transcript_api import YouTubeTranscriptApi as A
        try:
            snips = A.get_transcript(vid, languages=langs)
        except Exception:
            tl = A.list_transcripts(vid)
            snips = next(iter(tl)).fetch()
        return [s["text"] for s in snips], ""

def paragraphs(snippets):
    paras, cur = [], ""
    for s in snippets:
        t = re.sub(r"\s+", " ", s.replace("\n", " ")).strip()
        if not t or t.startswith("["):     # [Music], [Applause] ...
            continue
        cur = (cur + " " + t).strip()
        if len(cur) >= PARA_CHARS and t.endswith((".", "!", "?")):
            paras.append(cur); cur = ""
    if cur:
        paras.append(cur)
    return paras

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    url = sys.argv[1]
    vid = video_id(url)
    title, author = fetch_meta(vid)
    slug = sys.argv[2] if len(sys.argv) > 2 else slugify(title or vid)

    snippets, lang = fetch_transcript(vid)
    paras = paragraphs(snippets)
    words = sum(len(p.split()) for p in paras)

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, slug + ".md")
    if os.path.exists(path):
        print("WARN: overwriting existing", path)

    today = datetime.date.today().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("slug: %s\n" % slug)
        f.write("title: %s\n" % (title or "(unknown)"))
        f.write("channel: %s\n" % (author or "(unknown)"))
        f.write("date: %s\n" % today)
        f.write("videoId: %s\n" % vid)
        f.write("url: https://www.youtube.com/watch?v=%s\n" % vid)
        f.write("type: transcript\n")
        if lang:
            f.write("language: %s\n" % lang)
        f.write("---\n\n# %s\n\n" % (title or vid))
        f.write("## TL;DR\n\n_(to be filled)_\n\n")
        f.write("## Transcript\n\n")
        f.write("\n\n".join(paras) + "\n")

    print("saved: youtube/%s.md (%d words, %d paragraphs)" % (slug, words, len(paras)))
    print("title: %s | channel: %s" % (title, author))

if __name__ == "__main__":
    main()
