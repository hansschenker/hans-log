#!/usr/bin/env python3
"""yt-scan: list new YouTube videos/playlists from Chrome history as log candidates.

Reads Chrome's History SQLite DB (via a temp copy, so a running Chrome is fine),
collects youtube watch/playlist visits since the saved cursor, skips anything
already logged in hans-log.md, and prints candidates for `yt` / `ytl` entries.

Usage:
    python yt-scan.py            # show candidates since last --mark (default: 7 days back)
    python yt-scan.py --days 3   # override the lookback window
    python yt-scan.py --mark     # advance the cursor to now (run after logging picks)
"""
import os, sys, re, json, shutil, sqlite3, tempfile, time, datetime
from urllib.parse import urlparse, parse_qs

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(SCRIPT_DIR, ".hans-log-state.json")
LOG_MD = os.path.join(SCRIPT_DIR, "hans-log.md")
HISTORY = os.path.expanduser(
    "~/AppData/Local/Google/Chrome/User Data/Default/History")
CHROME_EPOCH_OFFSET = 11644473600  # seconds between 1601-01-01 and 1970-01-01
DEFAULT_DAYS = 7

def to_chrome(unix_s):
    return int((unix_s + CHROME_EPOCH_OFFSET) * 1_000_000)

def from_chrome(t):
    return datetime.datetime.fromtimestamp(t / 1_000_000 - CHROME_EPOCH_OFFSET)

def clean_title(t):
    t = re.sub(r"^\(\d+\)\s*", "", t or "")          # "(10769) " notification counter
    return re.sub(r"\s*-\s*YouTube$", "", t).strip()

def load_state():
    with open(STATE, encoding="utf-8") as f:
        return json.load(f)

def save_state(st):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=1)

def main():
    st = load_state()

    if "--mark" in sys.argv:
        st["yt_scan_cursor"] = to_chrome(time.time())
        save_state(st)
        print("yt-scan cursor set to now (%s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        return

    days = DEFAULT_DAYS
    if "--days" in sys.argv:
        days = float(sys.argv[sys.argv.index("--days") + 1])
        cursor = to_chrome(time.time() - days * 86400)
    else:
        cursor = st.get("yt_scan_cursor") or to_chrome(time.time() - days * 86400)

    if not os.path.exists(HISTORY):
        print("ERROR: Chrome history not found at", HISTORY); sys.exit(1)
    tmp = os.path.join(tempfile.gettempdir(), "yt-scan-history.db")
    shutil.copy2(HISTORY, tmp)

    db = sqlite3.connect(tmp)
    rows = db.execute(
        """SELECT url, title, last_visit_time, visit_count FROM urls
           WHERE last_visit_time > ?
             AND (url LIKE '%youtube.com/watch%' OR url LIKE '%youtube.com/playlist%')
           ORDER BY last_visit_time""", (cursor,)).fetchall()
    db.close()

    already_logged = ""
    if os.path.exists(LOG_MD):
        with open(LOG_MD, encoding="utf-8") as f:
            already_logged = f.read()

    videos, playlists = {}, {}
    for url, title, t, n in rows:
        q = parse_qs(urlparse(url).query)
        title = clean_title(title)
        if "/playlist" in url and q.get("list"):
            key, bucket, canon = q["list"][0], playlists, \
                "https://www.youtube.com/playlist?list=" + q["list"][0]
        elif q.get("v"):
            key, bucket, canon = q["v"][0], videos, \
                "https://www.youtube.com/watch?v=" + q["v"][0]
        else:
            continue
        if key in already_logged:
            continue  # already in hans-log.md
        cur = bucket.get(key)
        if cur is None:
            bucket[key] = {"url": canon, "title": title, "t": t, "n": n}
        else:
            cur["t"] = max(cur["t"], t)
            cur["n"] = max(cur["n"], n)
            if title and not cur["title"]:
                cur["title"] = title

    since = from_chrome(cursor).strftime("%Y-%m-%d %H:%M")
    if not videos and not playlists:
        print("No new YouTube candidates since %s." % since)
        return

    print("YouTube candidates since %s (videos: %d, playlists: %d)\n"
          % (since, len(videos), len(playlists)))
    if videos:
        print("-- videos (tag: yt) --")
        for i, v in enumerate(sorted(videos.values(), key=lambda x: x["t"]), 1):
            print("%2d. %s | %dx | %s\n    %s" % (
                i, from_chrome(v["t"]).strftime("%Y-%m-%d %H:%M"),
                v["n"], v["title"] or "(no title)", v["url"]))
    if playlists:
        print("\n-- playlists (tag: ytl, confirm they are yours) --")
        for i, p in enumerate(sorted(playlists.values(), key=lambda x: x["t"]), 1):
            print("P%d. %s | %dx | %s\n    %s" % (
                i, from_chrome(p["t"]).strftime("%Y-%m-%d %H:%M"),
                p["n"], p["title"] or "(no title)", p["url"]))
    print("\nAfter logging your picks, run: python yt-scan.py --mark")

if __name__ == "__main__":
    main()
