# Hans Log — Claude Code Instructions

## Startup: Daily Briefing

At the start of every session, automatically run this briefing without being asked:

1. **Yesterday's log** — read `hans-log.md`, find the most recent day's entries under `## Manual Entries`, and display them
2. **Today's focus** — read all 3 plan files and show the current active step for each goal:
   - Sport: `C:/Users/hanss/Local-Learning/Hans-Sport/Running/davos-trail-plan.md` — show current week's remaining sessions
   - Claude: `C:/Users/hanss/Claude/claude-mastery/claude-mastery-plan.md` — show current phase and next lessons to watch
   - RxJS: `C:/Users/hanss/Local-Learning/Rxjs/Rxjs-Deep-Dive-Course/rxjs-course-plan.md` — show current module status and next task

Format the briefing like this:

---
**Daily Briefing — [date]**

**Yesterday's log**
- [entries from previous day]

**Today's focus**
| Goal | Next step |
|---|---|
| sport (davos-trail) | [current week session] |
| claude (mastery) | [current phase + next lessons] |
| rxjs (course) | [current module + next task] |
---

## Logging

When the user says "log [tag]: [description]", add an entry under today's date in `## Manual Entries` (newest day first), commit, and push. Format:
```
- [tag] | [slug] | [description] | [path or url if given]
```

**YouTube videos** use the `yt` tag. Format:
```
- yt | [slug] | [video title] — [one-liner on what you learned] | [youtube url]
```
Example: `log yt: RxJS switchMap deep dive — when to use switchMap vs mergeMap for HTTP requests | https://youtube.com/watch?v=...`

When the user says "push it", run `git push` on the hans-log repo.

## Goals & Plans

| Goal | Target | Plan |
|---|---|---|
| davos-trail | 2026-07-26 | C:/Users/hanss/Local-Learning/Hans-Sport/Running/davos-trail-plan.md |
| claude-mastery | 2026-08-31 | C:/Users/hanss/Claude/claude-mastery/claude-mastery-plan.md |
| rxjs-course | 2026-09-30 | C:/Users/hanss/Local-Learning/Rxjs/Rxjs-Deep-Dive-Course/rxjs-course-plan.md |
