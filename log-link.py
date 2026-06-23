#!/usr/bin/env python3
"""Append a link entry to hans-log.md.

Usage:
    python log-link.py <url> <topic> <description>

Example:
    python log-link.py https://notebooklm.google.com/notebook/abc123 rxjs "RxJS operators deep dive"
"""
import os, sys, datetime

LOG_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hans-log.md")

def main():
    if len(sys.argv) < 4:
        print("Usage: python log-link.py <url> <topic> <description>")
        sys.exit(1)

    url = sys.argv[1]
    topic = sys.argv[2]
    description = " ".join(sys.argv[3:])
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    item = f"[{description}]({url})"
    row = f"| {now} | link | {topic} | {item} |"

    with open(LOG_MD, "a", encoding="utf-8") as f:
        f.write(row + "\n")

    print(f"Logged: {row}")

if __name__ == "__main__":
    main()
