#!/usr/bin/env python3
"""Log a manual entry to hans-log.md under today's date section.

Usage:
    python log-entry.py tag [description] [url-or-path]

Examples:
    python log-entry.py rxjs-deep-dive chatgpt https://chatgpt.com/share/...
    python log-entry.py hans-project C:\\Users\\hanss\\Local-Learning\\Recall
    python log-entry.py sport vo2max-training https://youtube.com/...
    python log-entry.py claude master-course-session

Or pass a single daily.tx-style comma-separated string:
    python log-entry.py "rxjs-deep-dive, chatgpt, https://chatgpt.com/share/..."
"""
import os, sys, datetime

LOG_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hans-log.md")
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MANUAL_MARKER = '## Manual Entries'

def today_heading():
    now = datetime.datetime.now()
    return f"### {now.strftime('%Y-%m-%d')} {DAYS[now.weekday()]}"

def build_entry(args):
    raw = ' '.join(args)
    if ',' in raw:
        parts = [p.strip() for p in raw.split(',') if p.strip()]
    else:
        parts = [a.strip() for a in args if a.strip()]
    # Ensure first field is a short topic (no hyphens) — if not, infer it
    if parts and '-' in parts[0]:
        topic = parts[0].split('-')[0]
        parts = [topic] + parts
    return '- ' + ' | '.join(parts)

def main():
    if len(sys.argv) < 2:
        print("Usage: python log-entry.py tag [description] [url-or-path]")
        sys.exit(1)

    entry = build_entry(sys.argv[1:])
    heading = today_heading()

    with open(LOG_MD, encoding='utf-8') as f:
        content = f.read()

    if MANUAL_MARKER not in content:
        print(f"ERROR: '{MANUAL_MARKER}' section not found in hans-log.md")
        sys.exit(1)

    if heading in content:
        # Insert entry right after the existing today heading
        content = content.replace(heading + '\n', heading + '\n' + entry + '\n', 1)
    else:
        # New day: insert heading+entry right after the Manual Entries header
        insert_after = MANUAL_MARKER + '\n\n*'
        header_end = content.find('\n\n', content.find(MANUAL_MARKER) + len(MANUAL_MARKER))
        # Find the end of the subtitle line
        subtitle_end = content.find('\n\n', header_end + 2)
        insert_point = subtitle_end + 2
        content = content[:insert_point] + heading + '\n' + entry + '\n\n' + content[insert_point:]

    with open(LOG_MD, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

    print(f"Logged: {entry}")

if __name__ == '__main__':
    main()
