# Hans Log — Claude Code Instructions

Personal knowledge log: daily entries, structured notes, and 3-goal weekly focus tracker.

Notes live in one directory per tag: `yt/`, `ai/`, `rxjs/`, `cs/`, `fit/`, `age/`, `health/`. The old `notes/` directory is retired.

## Goals & Plans

| Goal | Target | Plan file |
|---|---|---|
| davos-trail | 2026-07-26 | `D:/Learning-Local-Backup/Hans-Sport/Running/davos-trail-plan.md` |
| claude-mastery | 2026-08-31 | `C:/Users/hanss/Claude/claude-mastery/claude-mastery-plan.md` |
| rxjs-course | 2026-09-30 | `D:/Learning-Local-Backup/Rxjs/Rxjs-Deep-Dive-Course/rxjs-course-plan.md` |

## Startup: Daily Briefing

At the start of every session, automatically run this briefing without being asked:

1. Read `hans-log.md` → find yesterday's entries under `## Manual Entries` → display them
2. Read all 3 plan files above → show the current active step for each goal
3. If yesterday has NO section under `## Manual Entries`, gather evidence (run `python yt-scan.py`, check recent Activity rows and git commits) and offer to backfill yesterday — drafts only, Hans approves before anything is written
4. Schedule the auto-draft checks: create recurring cron jobs at 08:57, 11:57 and 14:57 local, each with prompt "auto-draft check" (skip any that already exist in this session — check with CronList). Cron jobs are session-bound, so this re-creates them each session

Output format:

**Daily Briefing — [date]**

**Yesterday's log**
- [entries from previous day]

**Today's focus**
| Goal | Next step |
|---|---|
| sport (davos-trail) | [current week's remaining sessions] |
| claude (mastery) | [current phase + next lessons to watch] |
| rxjs (course) | [current module + next task] |

---

<important if="the user says 'log [tag]: ...' to add a new log entry">

Add the entry to `hans-log.md` under `## Manual Entries` (newest day first), then commit and push.

There are two input variants depending on whether the entry has a local file or a URL:

**File-based tags (ai, rxjs, cs, fit, age, health):**
- Input: `log [tag]: [title] | [file path] | [topic] | [description max 80 chars]`
- Stored: `- [tag] | [slug] | [title] — [description] | [topic] | [tag]/[slug].[ext]`
- Workflow: copy file → scaffold note → commit+push

**URL-based tags (yt, ytl):**
- Input: `log [tag]: [title] | [url] | [topic] | [description max 80 chars]`
- Stored: `- [tag] | [slug] | [title] — [description] | [topic] | [url]`
- Workflow: write log entry → commit+push (no file to copy; URL is stored inline)

Mnemonic: **ta-ti-urlfi-to-de** → `log tag: title | url-or-file | topic | description`

For file-based entries, run this 3-step workflow automatically:
1. Copy the file from `[file path]` into `[tag]/[slug].[ext]` (preserve the original file extension)
2. Scaffold `[tag]/[slug].md` — synthesize TL;DR, Key Concepts, and Content from the copied file
3. Commit both files and push
If no file path is given, skip steps 1–2 and only commit the log entry.

| Tag | Covers | Slug prefix | URL or file |
|---|---|---|---|
| `yt` | YouTube video watched | — | URL |
| `ytl` | YouTube playlist created | `ytl-` | URL |
| `ai` | All AI work (Claude, Google, OpenAI) | `ai-claude-`, `ai-google-`, `ai-openai-` | file |
| `rxjs` | RxJS course work | — | file |
| `cs` | Computer science (algorithms, systems, languages, theory) | — | file |
| `fit` | Running/strength | — | file |
| `age` | Healthy aging, longevity | — | file |
| `health` | Healthy lifestyle, food | — | file |

**`yt` example:**
```
log yt: RxJS switchMap Explained | https://www.youtube.com/watch?v=rUZ9CjcaCEw | RxJS | when to cancel vs merge inner observables
```
Stored as: `- yt | rxjs-switchmap-explained | RxJS switchMap Explained — when to cancel vs merge inner observables | RxJS | https://www.youtube.com/watch?v=rUZ9CjcaCEw`

**`ytl` example:**
```
log ytl: RxJS Operators Playlist | https://www.youtube.com/playlist?list=PLxxxxx | RxJS | curated list of RxJS operator deep dives
```
Stored as: `- ytl | ytl-rxjs-operators | RxJS Operators Playlist — curated list of RxJS operator deep dives | RxJS | https://www.youtube.com/playlist?list=PLxxxxx`

For `ai` entries, start the slug with the provider prefix: `ai-claude-[topic]`, `ai-google-[topic]`, `ai-openai-[topic]`. The `gai` and `claude` tags are retired — use `ai` with the `ai-google-` / `ai-claude-` slug prefix instead.

Input shorthand for `ai` entries: the title may lead with the provider prefix, e.g. `log ai: ai-claude Agentic RAG | ...` → slug `ai-claude-agentic-rag`, stored title "Agentic RAG" (prefix moves into the slug, stripped from the title). If no prefix is given, infer the provider from context.
</important>

<important if="the user says 'note [slug]', 'add note:', or 'show note'">

Notes live in the tag directory of their log entry: `[tag]/[slug].md`.

- `note [slug]` — create `[tag]/[slug].md` pre-filled from the matching log entry using the template below
- `add note: [slug] | [section] | [file path]` (section = claude/nlm/recall/notes) — read the file at `[file path]` and paste its content into that section of `[tag]/[slug].md`. Must be a local file path — URLs won't work for authenticated services like Recall.ai or NotebookLM; export the content as a file first.
- `show note [slug]` — find and display `[tag]/[slug].md`

Note file structure:

Frontmatter: `slug`, `title`, `date`, `tags`, `source` (yt/ytl/ai/rxjs/fit)

Sections in order:
- **TL;DR** — 2–3 sentence synthesis
- **Key Concepts** — bullet list
- **Content** — synthesized content merging the best from all 3 artifacts
- **Claude Summary** — full Claude summary content or link
- **NLM** — full NotebookLM study guide content or link
- **Recall.ai** — full Recall.ai summary content or link
- **Source** — original url
- **Notes** — own thoughts, insights, connections
- **Related** — `[[slug]]` links to related notes
</important>

<important if="the user says 'log eod'">

End-of-day log. The primary source is **`~/Daily/daily.txt`** (`C:/Users/hanss/Daily/daily.txt`) — Hans's capture inbox. Rather than typing each item, `log eod` reads today's section of daily.txt and drafts one hans-log entry per record. Entries stay tag-driven; the 3 goal plans only provide hints for any extra fit/ai/rxjs lines.

**daily.txt format:** dated sections headed `Mo 14:14 20.07.2026` (`weekday time DD.MM.YYYY`), followed by comma-separated records. The standard record is:

```
header, link, description
```

Legacy records may put the link last (`header, note, link`); `daily-scan.py` finds the link by pattern (URL or local path), not position, so both parse.

Steps:
1. Run `python daily-scan.py` → prints today's records as `header / link / desc`, skipping any whose header is already in `hans-log.md` (dedup — re-running is safe). Use `--date DD.MM.YYYY` for another day, `--all` to include already-logged items.
2. Draft one entry per **new** record, mapping each field:
   - `header` → slug (slugified) **and** title
   - `description` → the entry description
   - `link` → the stored resource (URL or local path, kept as-is)
   - **tag** → infer from the header/link (`interactive-rx`/`rxjava-*`/`rxjs-taxonomy` → `rxjs`, `claude`/`claude.ai` → `ai` with an `ai-claude-` slug, etc.). Flag any ambiguous call in the draft.
   - Stored line: `- [tag] | [slug] | [title] — [description] | [topic] | [link]`
3. Show all drafts as a numbered list and ask **"Log these? (all / numbers / corrections)"** — never write without approval.
4. After approval: add entries under today's `### YYYY-MM-DD Weekday` section in `## Manual Entries` (create it if absent, newest day first; append if it exists).
5. Ask once: **"Anything else today not in daily.txt?"** (fit runs, offline work). For each free-form line the user gives, create an entry with that tag (`ai` entries get the `ai-claude-` / `ai-google-` / `ai-openai-` slug prefix). Read the 3 plan files only if needed to fill slug/topic wording for these extras.
6. Commit all changes and push.
</important>

<important if="the user says 'show last N entries', 'show last N [tag] entries', or 'push it'">

- `show last N entries` — display N most recent entries from `## Manual Entries` in `hans-log.md` as a table: #, Date, Tag, Entry
- `show last N [tag] entries` — same, filtered by that tag
- `push it` — run `git push` on the hans-log repo
</important>

<important if="the user or a scheduled task says 'auto-draft check', 'evening auto-draft', or 'draft eod'">

Three times daily (~09:00, ~12:00, ~15:00) a scheduled task triggers this — small incremental batches instead of one big end-of-day dump. Draft log entries from evidence gathered since the last check, then ask — never log without approval.

1. Run `python yt-scan.py` → `yt`/`ytl` candidates from Chrome history (the mark cursor keeps checks incremental)
2. Read today's Activity rows in `hans-log.md` (tracker) and `git log --since=midnight --oneline` in this repo; read the 3 plan files for context on what was planned
3. Draft one entry per tag with evidence, in stored format, shown as a numbered list. Skip anything already logged today — if nothing new since the last check, say so briefly and stop
4. Ask: "Log these? (all / numbers / corrections)" and wait. On approval: add the entries under today's section, run `python yt-scan.py --mark`, commit and push
</important>

<important if="the user says 'scan yt'">

YouTube consumption scan from Chrome history.

1. Run `python yt-scan.py` (`--days N` if the user names a window). It lists videos (→ `yt`) and playlists (→ `ytl`) visited since the last mark, skipping anything already in `hans-log.md`
2. Show the candidates as two numbered tables; the user picks by number which to log
3. Create the entries for the picks under today's date (title + URL from the scan; synthesize topic/description, ask only if unclear). Playlists in history are merely *visited* — confirm which ones the user actually created before tagging `ytl`
4. Run `python yt-scan.py --mark` to advance the cursor, then commit and push
</important>

<important if="the user says 'yt note [url]'">

Fetch a YouTube video's transcript and save a SUMMARY note in `yt/[slug].md`. The full transcript never goes into the repo.

1. Run `python yt-note.py [url]` — names the note after the video title (slugified, first 8 words). It writes the raw transcript to a temp file and scaffolds `yt/[slug].md` with empty TL;DR / Key Concepts / Summary sections; both paths are printed
2. Read the temp transcript and fill the note: TL;DR (2–3 sentences), Key Concepts (bullets), Summary (the video's actual argument in structured prose — skip sponsor segments)
3. If the video isn't in `hans-log.md` yet, also add a `yt` log entry pointing to `yt/[slug].md`
4. Commit and push

Requires the `youtube-transcript-api` pip package (installed 2026-07-04). Videos without captions will fail — report that plainly.
</important>
