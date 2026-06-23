#!/usr/bin/env python3
"""Generate topics/ folder — one .md file per topic from hans-log.md."""
import os, re
from collections import defaultdict

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hans-log.md')
TOPICS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'topics')
os.makedirs(TOPICS_DIR, exist_ok=True)

with open(LOG, encoding='utf-8') as f:
    content = f.read()

# topic -> list of (date, kind, text)
data = defaultdict(list)

# ── Manual Entries ────────────────────────────────────────────────────────────
in_manual, cur_date = False, None
for line in content.splitlines():
    if line.strip() == '## Manual Entries':
        in_manual = True; continue
    if in_manual and line.startswith('## '):
        in_manual = False; continue
    if not in_manual: continue
    m = re.match(r'^### (\d{4}-\d{2}-\d{2} \w+)', line)
    if m: cur_date = m.group(1); continue
    if line.startswith('- ') and cur_date:
        parts = [p.strip() for p in line[2:].split('|')]
        topic = parts[0].lower() if parts else 'other'
        entry = ' | '.join(parts[1:]) if len(parts) > 1 else parts[0]
        data[topic].append((cur_date, 'manual', entry))

# ── Activity table ────────────────────────────────────────────────────────────
for line in content.splitlines():
    m = re.match(r'^\| (20\d\d-\d\d-\d\d)T\S+ \| (\w+) \| (\w+) \| (.*) \|$', line)
    if not m: continue
    date, kind, topic, item = m.group(1), m.group(2), m.group(3), m.group(4).strip()
    if topic:
        data[topic].append((date, kind, item))

# ── Write one file per topic ──────────────────────────────────────────────────
SKIP = {'', 'other'}
written = []
for topic, entries in sorted(data.items()):
    if topic in SKIP: continue
    # Group by date
    by_date = defaultdict(list)
    for date, kind, text in entries:
        by_date[date].append((kind, text))

    lines = [f'# {topic.upper()}\n',
             f'*All {topic} entries from [hans-log](../hans-log.md) — auto-generated, do not edit.*\n\n']
    for date in sorted(by_date.keys(), reverse=True):
        lines.append(f'## {date}\n')
        for kind, text in by_date[date]:
            prefix = 'file' if kind == 'file' else kind
            lines.append(f'- [{prefix}] {text}\n')
        lines.append('\n')

    path = os.path.join(TOPICS_DIR, f'{topic}.md')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(lines)
    written.append(f'{topic} ({len(entries)} entries)')

print(f'Generated {len(written)} topic files:')
for w in written: print(f'  {w}')
