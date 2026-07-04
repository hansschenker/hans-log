# Hans Log — Claude Code Instructions

Personal knowledge log: daily entries, structured notes, and 3-goal weekly focus tracker.

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

**File-based tags (ai, rxjs, fit, age, health):**
- Input: `log [tag]: [title] | [file path] | [topic] | [description max 80 chars]`
- Stored: `- [tag] | [slug] | [title] — [description] | [topic] | notes/[slug].[ext]`
- Workflow: copy file → scaffold note → commit+push

**URL-based tags (yt, ytl):**
- Input: `log [tag]: [title] | [url] | [topic] | [description max 80 chars]`
- Stored: `- [tag] | [slug] | [title] — [description] | [topic] | [url]`
- Workflow: write log entry → commit+push (no file to copy; URL is stored inline)

Mnemonic: **ta-ti-urlfi-to-de** → `log tag: title | url-or-file | topic | description`

For file-based entries, run this 3-step workflow automatically:
1. Copy the file from `[file path]` into `notes/[slug].[ext]` (preserve the original file extension)
2. Scaffold `notes/[slug].md` — synthesize TL;DR, Key Concepts, and Content from the copied file
3. Commit both files and push
If no file path is given, skip steps 1–2 and only commit the log entry.

| Tag | Covers | Slug prefix | URL or file |
|---|---|---|---|
| `yt` | YouTube video watched | — | URL |
| `ytl` | YouTube playlist created | `ytl-` | URL |
| `ai` | All AI work (Claude, Google, OpenAI) | `ai-claude-`, `ai-google-`, `ai-openai-` | file |
| `rxjs` | RxJS course work | — | file |
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

- `note [slug]` — create `notes/[slug].md` pre-filled from the matching log entry using the template below
- `add note: [slug] | [section] | [file path]` (section = claude/nlm/recall/notes) — read the file at `[file path]` and paste its content into that section of `notes/[slug].md`. Must be a local file path — URLs won't work for authenticated services like Recall.ai or NotebookLM; export the content as a file first.
- `show note [slug]` — read and display `notes/[slug].md`

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

End-of-day log. Capture today's work across all tags in one shot. Entries are tag-driven, not goal-driven — the 3 goal plans only provide hints for the fit/ai/rxjs lines; any tag can be logged whether or not it relates to a goal.

Steps:
1. Read `hans-log.md` — note if today's date section already exists and what's already there
2. Read all 3 plan files (davos-trail, claude-mastery, rxjs-course) — use each current active step as the hint on its tag line
3. Show the user this compact prompt and wait for their free-form replies. Do NOT print one line per tag — the user only reports what actually happened:

```
End of day — [date]. What did you do today?
One line per activity: [tag]: [what happened]   (tags: fit, ai, rxjs, age, health, yt, ytl)
Plan context: fit [current session] · ai [current step] · rxjs [current task]
```

4. For each line the user replies with, create a log entry with that tag (`ai` entries get the provider slug prefix, e.g. `ai-claude-`)
5. Add all entries under today's date section in `## Manual Entries` (create `### YYYY-MM-DD Weekday` if it doesn't exist yet; append if it does)
6. Commit all changes and push

Only tags the user mentions become entries — most days won't cover all tags. Use the plan file's current step wording to fill in slug and topic if the user was brief.
</important>

<important if="the user says 'show last N entries', 'show last N [tag] entries', or 'push it'">

- `show last N entries` — display N most recent entries from `## Manual Entries` in `hans-log.md` as a table: #, Date, Tag, Entry
- `show last N [tag] entries` — same, filtered by that tag
- `push it` — run `git push` on the hans-log repo
</important>

<important if="the user says 'scan yt'">

YouTube consumption scan from Chrome history.

1. Run `python yt-scan.py` (`--days N` if the user names a window). It lists videos (→ `yt`) and playlists (→ `ytl`) visited since the last mark, skipping anything already in `hans-log.md`
2. Show the candidates as two numbered tables; the user picks by number which to log
3. Create the entries for the picks under today's date (title + URL from the scan; synthesize topic/description, ask only if unclear). Playlists in history are merely *visited* — confirm which ones the user actually created before tagging `ytl`
4. Run `python yt-scan.py --mark` to advance the cursor, then commit and push
</important>

<important if="the user says 'yt note [url]'">

Fetch a YouTube video's transcript into `youtube/[slug].md`.

1. If the video is already logged in `hans-log.md`, reuse that entry's slug: `python yt-note.py [url] [slug]`. Otherwise run `python yt-note.py [url]` (slug derived from title)
2. The script writes frontmatter + transcript in paragraphs, with an empty TL;DR section — read the transcript and fill in the TL;DR (5–8 sentences, the video's actual argument, skip sponsor segments)
3. If the video isn't in `hans-log.md` yet, also add a `yt` log entry pointing to `youtube/[slug].md`
4. Commit and push

Requires the `youtube-transcript-api` pip package (installed 2026-07-04). Videos without captions will fail — report that plainly.
</important>
