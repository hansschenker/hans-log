#!/usr/bin/env python3
"""daily-scan: parse a day's records from Daily/daily.txt as hans-log candidates.

daily.txt is a capture inbox grouped into dated sections. A section header looks
like `Mo 14:14 20.07.2026` (weekday time DD.MM.YYYY); the records under it are
comma-separated and follow the standard:

    header, link, description

Legacy records may put the link last (`header, note, link`), so the link is
found by pattern (URL or local path), not by position. This script prints the
parsed records for the target day (default: today) so `log eod` can draft one
hans-log entry per item; anything whose header is already in hans-log.md is
flagged as already logged.

Dedup compares whole slugs, not substrings: the header is slugified and matched
against the slug field of each hans-log entry. A plain substring test would skip
`js-fp` because it occurs inside `rxjs-fp` — a silent loss, since a false skip
never reaches the drafts.

Usage:
    python daily-scan.py                 # records for today
    python daily-scan.py --date 20.07.2026   # records for a specific day
    python daily-scan.py --all           # include items already in hans-log.md
"""
import os, re, sys, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_MD = os.path.join(SCRIPT_DIR, "hans-log.md")
DAILY = os.path.expanduser("~/Daily/daily.txt")

# `Mo 14:14 20.07.2026` — weekday, time, DD.MM.YYYY
HEADER_RE = re.compile(r"^\s*[A-Za-z]{2,3}\s+\d{1,2}:\d{2}\s+(\d{1,2}\.\d{1,2}\.\d{4})\s*$")
RESOURCE_RE = re.compile(r"^(https?://|www\.|~|/|[A-Za-z]:[\\/])")

# A daily.txt header may omit the prefix the stored slug carries, e.g. header
# `agentic-rag` logged as `ai-claude-agentic-rag`.
SLUG_PREFIXES = ("ai-claude-", "ai-google-", "ai-openai-", "ytl-")


def is_resource(s):
    return bool(RESOURCE_RE.match(s.strip()))


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.strip().lower()).strip("-")


def logged_slugs(text):
    """Slugs already stored in hans-log.md.

    Entries are `- [tag] | [slug] | [title] — [desc] | [topic] | [link]`, so the
    slug is the second pipe-separated field. Lines that predate the format are
    simply not indexed — an unmatched item shows up as a draft for Hans to
    reject, which is recoverable; a wrongly skipped one disappears silently.
    """
    slugs = set()
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("-"):
            continue
        fields = [f.strip() for f in s.lstrip("- ").split("|")]
        if len(fields) >= 2 and fields[1]:
            slugs.add(fields[1].lower())
    return slugs


def match_logged(header, slugs):
    """Return the logged slug this header duplicates, or "" if it is new."""
    h = slugify(header)
    if not h:
        return ""
    if h in slugs:
        return h
    for p in SLUG_PREFIXES:
        if p + h in slugs:
            return p + h
    return ""


def parse_record(line):
    """Return (header, link, description) from one comma-separated record."""
    parts = [p.strip() for p in line.split(",")]
    header = parts[0]
    rest = [p for p in parts[1:] if p]
    link, desc = "", []
    for p in rest:
        if not link and is_resource(p):
            link = p
        else:
            desc.append(p)
    return header, link, ", ".join(desc)


def section_for(date_str):
    """Yield record lines under the section whose header matches date_str."""
    if not os.path.exists(DAILY):
        print("ERROR: daily.txt not found at", DAILY); sys.exit(1)
    with open(DAILY, encoding="utf-8") as f:
        lines = f.read().splitlines()
    in_section = False
    for line in lines:
        m = HEADER_RE.match(line)
        if m:
            # normalise 20.7.2026 -> 20.07.2026 for comparison
            got = "%02d.%02d.%04d" % tuple(int(x) for x in m.group(1).split("."))
            in_section = (got == date_str)
            continue
        if in_section:
            s = line.strip()
            if not s or set(s) <= set("-="):   # blank or divider
                continue
            yield s


def main():
    argv = sys.argv[1:]
    show_all = "--all" in argv
    if "--date" in argv:
        raw = argv[argv.index("--date") + 1]
    else:
        raw = datetime.date.today().strftime("%d.%m.%Y")
    date_str = "%02d.%02d.%04d" % tuple(int(x) for x in raw.split("."))

    slugs = set()
    if os.path.exists(LOG_MD):
        with open(LOG_MD, encoding="utf-8") as f:
            slugs = logged_slugs(f.read())

    records = list(section_for(date_str))
    if not records:
        print("No daily.txt section found for %s." % date_str)
        return

    new, logged = [], []
    for line in records:
        header, link, desc = parse_record(line)
        hit = "" if show_all else match_logged(header, slugs)
        if hit:
            logged.append((header, hit))
        else:
            new.append((header, link, desc))

    print("Daily items for %s (%d records, %d new):\n" % (
        date_str, len(records), len(new)))
    for i, (header, link, desc) in enumerate(new, 1):
        print("%2d. %s\n    link: %s\n    desc: %s" % (
            i, header, link or "(none)", desc or "(none)"))
    if logged:
        print("\nAlready in hans-log.md (skipped, use --all to include):")
        for header, hit in logged:
            extra = "" if hit == slugify(header) else "  (logged as: %s)" % hit
            print("  - %s%s" % (header, extra))


if __name__ == "__main__":
    main()
