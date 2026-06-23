#!/usr/bin/env python3
"""Print a weekly digest of hans-log entries grouped by topic.

Usage:
    python weekly-digest.py          # current week (Mon–today)
    python weekly-digest.py -1       # last week
    python weekly-digest.py 2026-06-16  # week starting on this date
"""
import os, sys, re, datetime
from collections import defaultdict

LOG_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hans-log.md")

def week_range(offset=0, start_date=None):
    if start_date:
        monday = start_date
    else:
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(weeks=offset)
    sunday = monday + datetime.timedelta(days=6)
    return monday, sunday

def parse_args():
    args = sys.argv[1:]
    if not args:
        return week_range(0)
    if args[0].startswith('-') and args[0][1:].lstrip('-').isdigit():
        return week_range(int(args[0]))
    try:
        d = datetime.date.fromisoformat(args[0])
        d = d - datetime.timedelta(days=d.weekday())  # snap to Monday
        return week_range(start_date=d)
    except ValueError:
        pass
    return week_range(0)

def in_range(date_str, start, end):
    try:
        d = datetime.date.fromisoformat(date_str[:10])
        return start <= d <= end
    except:
        return False

with open(LOG_MD, encoding='utf-8') as f:
    content = f.read()

start, end = parse_args()

# ── Parse Manual Entries ──────────────────────────────────────────────────────
manual = defaultdict(list)  # topic -> [entry_text]
in_manual = False
cur_date = None

for line in content.splitlines():
    if line.strip() == '## Manual Entries':
        in_manual = True; continue
    if in_manual and line.startswith('## '):
        in_manual = False; continue
    if not in_manual:
        continue
    m = re.match(r'^### (\d{4}-\d{2}-\d{2})', line)
    if m:
        cur_date = m.group(1); continue
    if line.startswith('- ') and cur_date and in_range(cur_date, start, end):
        parts = [p.strip() for p in line[2:].split('|')]
        tag = parts[0].lower().split('-')[0] if parts else 'other'
        manual[tag].append(line[2:].strip())

# ── Parse Activity table ──────────────────────────────────────────────────────
auto = defaultdict(list)   # topic -> [item_text]
auto_types = defaultdict(lambda: defaultdict(int))  # topic -> type -> count

for line in content.splitlines():
    m = re.match(r'^\| (20\d\d-\d\d-\d\dT\S+) \| (\w+) \| (\w*) \| (.*) \|$', line)
    if not m:
        continue
    ts, rtype, topic, item = m.group(1), m.group(2), m.group(3), m.group(4).strip()
    if not in_range(ts, start, end):
        continue
    t = topic or 'other'
    auto_types[t][rtype] += 1
    if rtype in ('repo', 'link'):
        auto[t].append(f'[{rtype}] {item}')

# ── Render ────────────────────────────────────────────────────────────────────
days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
print(f'\n{"="*60}')
print(f'  Weekly Digest: {start} {days[start.weekday()]} – {end} {days[end.weekday()]}')
print(f'{"="*60}\n')

all_topics = sorted(set(list(manual.keys()) + list(auto.keys())))

if not all_topics:
    print('No entries found for this week.\n')
    sys.exit(0)

for topic in all_topics:
    m_entries = manual.get(topic, [])
    a_entries = auto.get(topic, [])
    a_counts  = auto_types.get(topic, {})
    total = len(m_entries) + sum(a_counts.values())
    label = topic.upper() if topic else 'OTHER'
    print(f'  {label}  ({total} entries)')
    print(f'  {"-"*40}')

    if m_entries:
        print('  Manual:')
        for e in m_entries:
            print(f'    -{e}')

    if a_counts:
        parts = []
        if a_counts.get('file'): parts.append(f"{a_counts['file']} new files")
        if a_counts.get('repo'): parts.append(f"{a_counts['repo']} new repo(s)")
        if a_counts.get('link'): parts.append(f"{a_counts['link']} link(s)")
        print(f'  Auto-tracked: {", ".join(parts)}')
        for e in a_entries:
            print(f'    -{e}')

    print()

total_all = sum(len(v) for v in manual.values()) + sum(sum(v.values()) for v in auto_types.values())
print(f'  Total: {total_all} entries across {len(all_topics)} topic(s)\n')
