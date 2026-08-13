# Hans Log — Workflow Explained

_Written 2026-08-13. Describes the current (tag-driven, daily.txt-based) workflow._

The log has settled into a three-layer pipeline — **capture → entry → note** — where each layer has
its own file and its own trigger.

## 1. The shape

| Layer | Lives in | Role |
|---|---|---|
| Capture | `~/Daily/daily.txt` | Raw inbox — you type `header, link, description` during the day |
| Entry | `hans-log.md` → `## Manual Entries` | One line per item, newest day first — the index |
| Note | `[tag]/[slug].md` | The synthesized artifact, one file per entry that deserves one |

Content is filed **by tag, not by goal**: `yt/ ai/ rxjs/ cs/ fit/ age/ health/`. The old flat
`notes/` directory is gone, and so are the `gai`/`claude` tags — all AI work is now `ai` with a
provider slug prefix (`ai-claude-`, `ai-google-`, `ai-openai-`).

Every entry is the same grammar — **ta-ti-urlfi-to-de**:

```
- [tag] | [slug] | [title] — [description] | [topic] | [url-or-file-path]
```

### Tags

| Tag | Covers | Link type |
|---|---|---|
| `yt` | YouTube video watched | URL |
| `ytl` | YouTube playlist created (slug prefix `ytl-`) | URL |
| `ai` | All AI work — Claude, Google, OpenAI (slug prefix `ai-claude-` / `ai-google-` / `ai-openai-`) | file |
| `rxjs` | RxJS course work | file |
| `cs` | Computer science — algorithms, systems, languages, theory | file |
| `fit` | Running / strength | file |
| `age` | Healthy aging, longevity | file |
| `health` | Healthy lifestyle, food | file |

## 2. Four ways an entry gets created

- **`log [tag]: ...`** — single item, typed directly. If the link is a local file, it's copied into
  `[tag]/[slug].[ext]` and a note is scaffolded next to it; if it's a URL, the URL is stored inline
  and there's nothing to copy.
- **`log eod`** — the batch path. `daily-scan.py` reads today's section of `daily.txt`, dedups
  against `hans-log.md` by header, and prints what's new; the tag is inferred from each
  header/link, one line is drafted per record, and **nothing is written before approval**.
- **`auto-draft check`** — the same drafting, three times a day (08:57 / 11:57 / 14:57) off cron,
  so entries accrue in small batches instead of one evening dump. Evidence there comes from
  `yt-scan.py`, today's Activity rows, and `git log --since=midnight`.
- **`scan yt`** — Chrome history sweep for watched videos and playlists; a mark cursor keeps it
  incremental. Playlists get confirmed as actually *created* before they're tagged `ytl`.

Everything drafted is shown as a numbered list and waits for **"all / numbers / corrections"**.
Nothing is written on inference alone.

## 3. Notes, and the NotebookLM rule

`note [slug]` scaffolds, `add note: [slug] | [section] | [file]` pastes an export in,
`show note [slug]` displays. Notes have a fixed spine:

> TL;DR → Key Concepts → Content → Claude Summary → NLM → Recall.ai → Source → Notes → Related

**NotebookLM material is built from the local export directory, never the URL** — the notebook is
login-gated, so exports (reports, chats, quiz, mindmap, code) are downloaded into a topic-named
folder under `D:/Learning-Local-Hanss/`. Only the `.md` and `.pptx` exports are read; the
`.mp4`/`.pdf`/`.zip`/`.png`/`.mm`/`.json` bulk is ignored. TL;DR / Key Concepts / Content are
synthesized fresh; each report and chat is preserved (condensed but faithful) under **NLM**; the
local dir and the exact filenames used go in **Source**.

`yt note [url]` is the parallel case for video: `yt-note.py` fetches the transcript to a temp file
and scaffolds `yt/[slug].md` — only the summary lands in the repo, never the full transcript.

## 4. The loop closes at session start

Each session opens with the **daily briefing** — yesterday's entries, the current step from each of
the three goal plans (davos-trail, claude-mastery, rxjs-course), and an offer to backfill yesterday
if it has no section. The cron jobs get re-created each session because they're session-bound.

The net effect: `daily.txt` absorbs everything with near-zero friction during the day, `log eod`
turns it into structured entries with one approval, and only the items worth deepening get promoted
into a real note with cross-links.

## 5. How dedup works (and the bug it used to have)

`log eod` must never skip an item silently: a wrongly-skipped record never reaches the drafts, so
it is never seen again. Dedup therefore compares **whole slugs**, and errs toward showing an item.

- The header from `daily.txt` is slugified (`Agentic RAG` → `agentic-rag`).
- `hans-log.md` is indexed by the **slug field** of each entry — the second pipe-separated field —
  not searched as one blob of text.
- A match requires slug equality, with the documented provider prefixes (`ai-claude-`,
  `ai-google-`, `ai-openai-`, `ytl-`) tolerated on the stored side, so header `agentic-rag` still
  matches a stored `ai-claude-agentic-rag`. Skipped items print what they matched.
- Entry lines predating the `- tag | slug | ...` format aren't indexed, so anything they cover
  reappears as a draft to reject rather than vanishing.

Until 2026-08-13 the check was a plain substring test against the whole file, which skipped `js-fp`
because it occurs inside `rxjs-fp`. `test-daily-scan.py` now covers that case and its neighbours
(`combinators` inside `fp-combinators`, bare fragments, case folding, prefix tolerance).

## 6. Scripts

| Script | Used by |
|---|---|
| `daily-scan.py` | `log eod` — parses today's `daily.txt` section, dedups by header |
| `yt-scan.py` | `scan yt`, `auto-draft check` — Chrome history sweep, `--mark` advances the cursor |
| `yt-note.py` | `yt note [url]` — transcript fetch + note scaffold |
| `log-entry.py` | manual entry append (`python log-entry.py tag [description] [url]`) |
| `test-daily-scan.py` | tests for the above — `python test-daily-scan.py`, exits non-zero on failure |
| `tracker.py`, `weekly-digest.py`, `generate-topics.py`, `log-link.py` | adjacent tooling — activity tracker, digests, `topics/` generation, link handling |
