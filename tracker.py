#!/usr/bin/env python3
"""hans-log tracker: append newly created files (Local-Learning) and new GitHub
repos (github.com/hansschenker) to hans-log.md. Run hourly. Idempotent."""
import os, sys, json, glob, datetime, urllib.request, re, time

FOLDER_TOPICS = {
    'rxjs': 'rxjs', 'claude': 'ai', 'domain-specific': 'dsl',
    'functional-programming': 'fp', 'state-machine': 'state-machine',
    'a-state': 'state-machine', 'hans-sport': 'fit',
    'cloudflare': 'cloudflare', 'voidzero': 'voidzero', 'void': 'voidzero',
    'tanstack': 'tanstack', 'nuxt': 'nuxt', 'meta-frameworks': 'meta',
    'monorepo': 'monorepo', 'unjs': 'unjs', 'linear': 'linear',
    'hermes': 'hermes', 'recall': 'recall', 'rpc': 'rpc', 'pnpm': 'pnpm',
    'hans-admin': 'admin', 'dell': 'admin', 'animations': 'animations',
    'hans-log': 'meta', 'linq': 'dotnet', 'ai': 'ai',
}

def file_topic(rel_path):
    parts = re.split(r'[/\\]', rel_path)
    if parts and parts[0].startswith('Learning-Local') and len(parts) > 1:
        parts = parts[1:]  # skip the watch-root prefix
    top = parts[0].lower()
    for k, v in FOLDER_TOPICS.items():
        if top.startswith(k):
            return v
    return ''

def repo_topic(name):
    n = name.lower()
    if 'rxjs' in n: return 'rxjs'
    if 'cloudflare' in n or 'fullstack' in n: return 'cloudflare'
    if 'fitness' in n: return 'fit'
    if 'pnpm' in n: return 'pnpm'
    if 'vite' in n or 'rsc' in n: return 'meta'
    return ''

def log(m): print(m, flush=True)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = SCRIPT_DIR
STATE = os.path.join(LOG_DIR, ".hans-log-state.json")
LOG_MD = os.path.join(LOG_DIR, "hans-log.md")

with open(STATE, encoding="utf-8") as f:
    st = json.load(f)

# Locate the watch directories on the current mount.
# 2026-07-18: C:\Users\hanss\Local-Learning was split into three D:\ folders.
WATCH_NAMES = ["Learning-Local-Backup", "Learning-Local-Folio", "Learning-Local-Hanss"]
# Optional: --roots Name1,Name2 scans a subset (chunked runs; state accumulates).
if "--roots" in sys.argv:
    _sel = sys.argv[sys.argv.index("--roots") + 1].split(",")
    WATCH_NAMES = [n for n in WATCH_NAMES if n in _sel]
SKIP_GITHUB = "--no-github" in sys.argv
watches = {}  # name -> path
for _name in WATCH_NAMES:
    for cand in ([os.path.join(os.path.dirname(LOG_DIR), _name)]
                 + [d for pat in ("D:\\" + _name, "/sessions/*/mnt/" + _name)
                    for d in glob.glob(pat)]):
        if os.path.isdir(cand):
            watches[_name] = cand; break
if not watches:
    log("ERROR: no watch folder accessible (tried: %s)" % ", ".join(WATCH_NAMES)); sys.exit(1)
for _name in WATCH_NAMES:
    if _name not in watches:
        log("WARN: watch folder not accessible: %s" % _name)

now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
known_files = st.get("known_files", {})

# One-time migration: legacy keys were relative to the single old watch dir;
# prefix them with the Backup root so all keys are root-qualified.
if not st.get("keys_root_prefixed"):
    _prefixes = tuple(n + "\\" for n in WATCH_NAMES)
    known_files = {(k if k.startswith(_prefixes) else "Learning-Local-Backup\\" + k): v
                   for k, v in known_files.items()}
    st["keys_root_prefixed"] = True

known_roots = set(st.get("known_roots", ["Learning-Local-Backup"]))

PRUNE = ("node_modules", "venv", "dist", "build", "coverage", "__pycache__")

def save_state():
    st["known_files"] = known_files
    st["known_roots"] = sorted(known_roots)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=0, ensure_ascii=False)

# --baseline <RootName>: resumable, time-budgeted first scan of a moved-in root.
# Registers existing files WITHOUT log rows (moved content is not new activity).
# Run repeatedly until it prints "baseline complete".
if "--baseline" in sys.argv:
    broot = sys.argv[sys.argv.index("--baseline") + 1]
    if broot not in watches:
        log("ERROR: root not accessible: %s" % broot); sys.exit(1)
    if broot in known_roots:
        log("baseline complete: %s (already known)" % broot); sys.exit(0)
    prog = st.setdefault("baseline_progress", {}).setdefault(broot, {"pending": [""]})
    pending = prog["pending"]
    wpath = watches[broot]
    t0, added, dirs_done = time.time(), 0, 0
    while pending and time.time() - t0 < 33:
        sub = pending.pop()
        try:
            entries = list(os.scandir(os.path.join(wpath, sub) if sub else wpath))
        except OSError:
            continue
        for e in entries:
            rp = (sub + "\\" + e.name) if sub else e.name
            try: is_dir = e.is_dir(follow_symlinks=False)
            except OSError: continue
            if is_dir:
                if not e.name.startswith(".") and e.name not in PRUNE:
                    pending.append(rp)
            else:
                if (broot + "\\" + rp) not in known_files:
                    known_files[broot + "\\" + rp] = 0; added += 1
        dirs_done += 1
    if pending:
        save_state()
        log("baseline in progress: %s — +%d files this run, %d dirs pending; run again"
            % (broot, added, len(pending))); sys.exit(0)
    known_roots.add(broot)
    st["baseline_progress"].pop(broot, None)
    save_state()
    log("baseline complete: %s (+%d files this run, no log rows)" % (broot, added))
    sys.exit(0)

# Normal scan: time-budgeted and resumable (mount I/O can be slow; a partial
# scan saves its pending-directory stack and continues on the next run).
BUDGET = float(sys.argv[sys.argv.index("--budget") + 1]) if "--budget" in sys.argv else 33.0
t0 = time.time()
new_files = []
scan_pending = st.setdefault("scan_pending", {})
for wname, wpath in watches.items():
    if wname not in known_roots:
        log("SKIP %s: pending baseline — run: python tracker.py --baseline %s" % (wname, wname))
        continue
    pending = scan_pending.get(wname) or [""]
    while pending and time.time() - t0 < BUDGET:
        sub = pending.pop()
        try:
            entries = list(os.scandir(os.path.join(wpath, sub) if sub else wpath))
        except OSError:
            continue
        for e in entries:
            rp = (sub + "\\" + e.name) if sub else e.name
            try: is_dir = e.is_dir(follow_symlinks=False)
            except OSError: continue
            if is_dir:
                if not e.name.startswith(".") and e.name not in PRUNE:
                    pending.append(rp)
            else:
                key = wname + "\\" + rp
                if key not in known_files:
                    known_files[key] = 0
                    new_files.append(key)
    if pending:
        scan_pending[wname] = pending
        log("PARTIAL scan: %s — %d dirs pending, continues next run" % (wname, len(pending)))
    else:
        scan_pending.pop(wname, None)

# GitHub: newest first; new = created_at after baseline and name unseen.
known_repos = set(st.get("known_repos", []))
baseline = st.get("repo_baseline_time", st.get("created"))
new_repos = []
try:
    if SKIP_GITHUB:
        raise RuntimeError("skipped (--no-github)")
    req = urllib.request.Request(
        "https://api.github.com/users/%s/repos?per_page=100&sort=created&direction=desc" % st["github_user"],
        headers={"User-Agent": "hans-log-tracker"})
    repos = json.load(urllib.request.urlopen(req, timeout=30))
    for r in repos:
        nm, ca = r.get("name"), r.get("created_at", "")
        if nm and nm not in known_repos and ca > baseline:
            new_repos.append((nm, ca)); known_repos.add(nm)
            if ca > baseline: baseline = ca
except Exception as e:
    log("WARN: GitHub fetch failed: %s" % e)

# Append rows.
rows = []
for rel in sorted(new_files):
    rows.append("| %s | file | %s | `%s` |" % (now, file_topic(rel), rel))
for nm, ca in sorted(new_repos, key=lambda x: x[1]):
    rows.append("| %s | repo | %s | [%s](https://github.com/%s/%s) (created %s) |"
                % (now, repo_topic(nm), nm, st["github_user"], nm, ca[:10]))
if rows:
    with open(LOG_MD, "a", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")

# Persist state.
st["known_files"] = known_files
st["known_roots"] = sorted(known_roots)
st["known_repos"] = sorted(known_repos)
st["repo_baseline_time"] = baseline
st["last_scan"] = now
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(st, f, indent=0, ensure_ascii=False)

log("Scan %s: +%d files, +%d repos" % (now, len(new_files), len(new_repos)))
for rel in sorted(new_files): log("  file: " + rel)
for nm, _ in new_repos: log("  repo: " + nm)
