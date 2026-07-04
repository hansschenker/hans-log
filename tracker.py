#!/usr/bin/env python3
"""hans-log tracker: append newly created files (Local-Learning) and new GitHub
repos (github.com/hansschenker) to hans-log.md. Run hourly. Idempotent."""
import os, sys, json, glob, datetime, urllib.request, re

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
    top = re.split(r'[/\\]', rel_path)[0].lower()
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

# Locate the watch directory on the current mount.
# Folder was renamed/moved over time; try known names in order.
WATCH_NAMES = ["Learning-Local-Backup", "Local-Learning"]
watch = ""
for _name in WATCH_NAMES:
    cand_local = os.path.join(os.path.dirname(LOG_DIR), _name)
    if os.path.isdir(cand_local):
        watch = cand_local; break
    cand = glob.glob("/sessions/*/mnt/" + _name)
    if cand:
        watch = cand[0]; break
if not watch or not os.path.isdir(watch):
    log("ERROR: watch folder not accessible (tried: %s)" % ", ".join(WATCH_NAMES)); sys.exit(1)

now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
known_files = st.get("known_files", {})
new_files = []
for root, dirs, fs in os.walk(watch):
    for fn in fs:
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, watch).replace("/", "\\")
        if rel not in known_files:
            try: mt = os.path.getmtime(full)
            except OSError: mt = 0
            new_files.append(rel); known_files[rel] = mt

# GitHub: newest first; new = created_at after baseline and name unseen.
known_repos = set(st.get("known_repos", []))
baseline = st.get("repo_baseline_time", st.get("created"))
new_repos = []
try:
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
st["known_repos"] = sorted(known_repos)
st["repo_baseline_time"] = baseline
st["last_scan"] = now
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(st, f, indent=0, ensure_ascii=False)

log("Scan %s: +%d files, +%d repos" % (now, len(new_files), len(new_repos)))
for rel in sorted(new_files): log("  file: " + rel)
for nm, _ in new_repos: log("  repo: " + nm)
