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

End-of-day log. Capture today's work across all 3 goals in one shot.

Steps:
1. Read `hans-log.md` — note if today's date section already exists and what's already there
2. Read all 3 plan files (davos-trail, claude-mastery, rxjs-course) — get the current active step for each goal as context for what was planned today
3. Show the user this prompt and wait for their free-form replies:

```
End of day — [date]. What did you do today?

sport (davos-trail):   [current planned session — e.g. "Wed trail 25k 1000m"]
claude (mastery):      [current phase/lessons — e.g. "Phase 1 lectures 31-45"]
rxjs (course):         [current module/task — e.g. "Module 2 creation operators"]
other (yt, ai, etc.):  
```

4. For each goal/area the user filled in, create a log entry with the matching tag:
   - sport → `fit` tag
   - claude → `ai` tag with `ai-claude-` slug prefix
   - rxjs → `rxjs` tag
   - YouTube videos → `yt` tag (title | url)
   - YouTube playlists → `ytl` tag (title | url)
   - Other AI tools → `ai` tag with appropriate slug prefix
5. Add all entries under today's date section in `## Manual Entries` (create `### YYYY-MM-DD Weekday` if it doesn't exist yet; append if it does)
6. Commit all changes and push

Skip any goal/area the user left blank. Use the plan file's current step wording to fill in the slug and topic if the user was brief.
</important>

<important if="the user says 'show last N entries', 'show last N [tag] entries', or 'push it'">

- `show last N entries` — display N most recent entries from `## Manual Entries` in `hans-log.md` as a table: #, Date, Tag, Entry
- `show last N [tag] entries` — same, filtered by that tag
- `push it` — run `git push` on the hans-log repo
</important>
