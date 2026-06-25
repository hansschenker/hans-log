# Hans Log — Claude Code Instructions

Personal knowledge log: daily entries, structured notes, and 3-goal weekly focus tracker.

## Goals & Plans

| Goal | Target | Plan file |
|---|---|---|
| davos-trail | 2026-07-26 | `C:/Users/hanss/Local-Learning/Hans-Sport/Running/davos-trail-plan.md` |
| claude-mastery | 2026-08-31 | `C:/Users/hanss/Claude/claude-mastery/claude-mastery-plan.md` |
| rxjs-course | 2026-09-30 | `C:/Users/hanss/Local-Learning/Rxjs/Rxjs-Deep-Dive-Course/rxjs-course-plan.md` |

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

**Input format (all tags):** `log [tag]: [title] | [file path] | [topic] | [description max 80 chars]`

**Stored format (all tags):** `- [tag] | [slug] | [title] — [description] | [topic] | notes/[slug].[ext]`

After writing the log entry, run this 3-step workflow automatically:
1. Copy the file from `[file path]` into `notes/[slug].[ext]` (preserve the original file extension)
2. Scaffold `notes/[slug].md` — synthesize TL;DR, Key Concepts, and Content from the copied file
3. Commit both files and push
If no file path is given, skip steps 1–2 and only commit the log entry.

| Tag | Covers | Slug prefix |
|---|---|---|
| `yt` | YouTube video | — |
| `ai` | All AI work (Claude, Google, OpenAI) | `ai-claude-`, `ai-google-`, `ai-openai-` |
| `rxjs` | RxJS course work | — |
| `sport` | Running/strength | — |

For `ai` entries, start the slug with the provider prefix: `ai-claude-[topic]`, `ai-google-[topic]`, `ai-openai-[topic]`. The `gai` tag is retired — use `ai` with `ai-google-` slug prefix instead.
</important>

<important if="the user says 'note [slug]', 'add note:', or 'show note'">

- `note [slug]` — create `notes/[slug].md` pre-filled from the matching log entry using the template below
- `add note: [slug] | [section] | [file path]` (section = claude/nlm/recall/notes) — read the file at `[file path]` and paste its content into that section of `notes/[slug].md`. Must be a local file path — URLs won't work for authenticated services like Recall.ai or NotebookLM; export the content as a file first.
- `show note [slug]` — read and display `notes/[slug].md`

Note file structure:

Frontmatter: `slug`, `title`, `date`, `tags`, `source` (yt/gai/ai/rxjs/sport)

Sections in order:
- **TL;DR** — 2–3 sentence synthesis
- **Key Concepts** — bullet list
- **Content** — synthesized content merging the best from all 3 artifacts
- **Claude Summary** — full Claude summary content or link
- **NLM** — full NotebookLM study guide content or link
- **Recall.ai** — full Recall.ai summary content or link
- **Source** — original url
- **Personal Notes** — own thoughts, insights, connections
- **Related** — `[[slug]]` links to related notes
</important>

<important if="the user says 'show last N entries', 'show last N [tag] entries', or 'push it'">

- `show last N entries` — display N most recent entries from `## Manual Entries` in `hans-log.md` as a table: #, Date, Tag, Entry
- `show last N [tag] entries` — same, filtered by that tag
- `push it` — run `git push` on the hans-log repo
</important>
