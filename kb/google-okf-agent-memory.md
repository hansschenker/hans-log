---
type: video
title: "Google OKF + Claude : Why We Stopped Using RAG"
description: agent memory as a folder of linked markdown files — OKF standardizes it; files + grep beat vector DBs
resource: https://www.youtube.com/watch?v=l46NJXUL4PM
tags: [okf, agent-memory, agents, claude, knowledge-graphs, markdown, rag]
timestamp: 2026-08-15
channel: "Cloud Codes"
language: en
---

# Google OKF + Claude : Why We Stopped Using RAG

## TL;DR

The best long-term memory for an AI agent is not a vector database but a folder of plain markdown files the agent reads at session start and writes back to at session end. Claude Code proved this in practice (it shipped a local vector store and ripped it out because grep over real files beat embeddings), and in June 2026 Google standardized it as the Open Knowledge Format: one file per concept, a tiny YAML index card on top, ordinary markdown links turning the flat folder into a knowledge graph. This note is the design source for hans-log's own `kb/` bundle.

## Key Concepts

- **LLMs have no memory** — every request is a blank slate; close the session and the context is gone. Memory is something you deliberately give an agent.
- **The RAG/vector-DB patch** — chunk documents, embed to points in high-dimensional space, retrieve by cosine similarity. But *closest is not correct*: answers get split across chunks or drowned out by look-alikes, and a vector is unreadable — you can't open, diff, or hand-fix one.
- **Claude Code ripped out its vector store** — Boris Cherny: agentic search (grep, list, open real files) turned out simpler, cheaper, and more accurate than any embedding index. For precise facts, exact search wins — grep finds *all* call sites in milliseconds; similarity finds the 10 that merely felt close.
- **Files as memory** — CLAUDE.md for standing instructions, memory files that grow with the project; all of it lives in git, so every learned fact is a reviewable diff, revertible, approvable in a PR.
- **OKF (Open Knowledge Format)** — published by the Google Cloud data team in June 2026; a bundle is just a directory tree of markdown files. Only one frontmatter field is required (`type`); `title`, `description`, `resource`, `tags`, `timestamp` are the recommended index card an agent can scan without reading a single body.
- **Links are the real magic** — concepts reference each other with plain markdown links; the flat folder quietly becomes a graph, "the same shape you would draw on a whiteboard, except the agent can read it."
- **Progressive disclosure** — each folder can carry an `index.md` menu; the agent reads the menu and opens only what it needs. 10,000 files of knowledge, a handful touched per task.
- **`log.md`** — a dated history of changes, so the memory remembers how its facts got there.
- **Three rules** — minimally opinionated (only `type` required); producer and consumer are independent; it's a format, not a platform (no account, no SDK, no owner).
- **Portable brain** — hand the same folder to Gemini or any homegrown agent and it reads the exact same memory.
- **Honest limits** — v0.1 is a month-old draft; a format can't save bad content (someone still curates); and vector search still shines for millions of unstructured docs and fuzzy semantic questions. What changed is the *default*: files and search first, vector DB as the deliberate special case.

## Summary

The video opens with the wound: give a brilliant agent a real task, close the window, and tomorrow it has amnesia — every decision and hard-won detail wiped. For years the industry patched this with vector databases: slice knowledge into chunks, embed each chunk as a long list of numbers, and retrieve by fuzzy similarity. But retrieval *guesses*. It hands back the chunks that look mathematically close to the question and hopes the answer is in there. The paragraph you needed may be split across two chunks or outranked by one that merely shares words, and you can never see why — a vector can't be opened, diffed, or corrected by hand, and you run a whole extra service (re-embedding on every edit) to get approximations of what a folder of files would have told you exactly.

The twist is that Claude Code tried exactly this — a local vector database baked in — and removed it. Plain agentic search over real files (grep, list, open) proved simpler, cheaper, and more accurate. If you want every place a function is called, grep gives you all of them exactly; cosine similarity gives you the ten that felt close. So Claude Code's memory is files you already own — CLAUDE.md loaded at the top of every session, memory files that grow as the agent learns — and because it's files, the agent's memory lives in git: every learned fact is a diff you can review, a bad fact is one revert away.

In June 2026 Google made that pattern official with the Open Knowledge Format. A bundle is nothing more than a directory of markdown files — the file's path is its identity, "that is the whole database." Each concept file has two halves: a YAML index card on top (only `type` is required; title, one-line description, a resource link, tags, and a timestamp are recommended — small queryable fields an agent can scan without reading a single body, "the index card in front of the essay") and free-form markdown below. The real magic is the links: one concept points to the next with an ordinary markdown link, and the folder becomes a graph — the orders table points to the customers table, a playbook points to the alert it fixes. Per-folder `index.md` menus give progressive disclosure (read the menu, open only what you need), and `log.md` keeps a dated history of what changed. Three rules hold it together: minimally opinionated, producer/consumer independence, and format-not-platform.

Wired into Claude Code, you point the agent at the bundle from CLAUDE.md; from then on the folder is its long-term memory — when it learns something new it writes a fresh file, links it in, and appends a line to the log. And because OKF is a standard, the brain travels: Gemini or any other agent reads the same folder. The honest caveats: v0.1 is a draft with early tooling; a format cannot save messy content — someone still has to curate the brain; and vector search remains the right tool for millions of unstructured documents and fuzzy semantic queries. What changed is the default: files and exact search are now the first choice for agent memory, and the vector database is the special case you reach for on purpose.

## Source

https://www.youtube.com/watch?v=l46NJXUL4PM — Cloud Codes

## Notes

This video (plus the [OKF spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)) directly shaped the 2026-08-15 reorganization of hans-log: all notes now live flat in `kb/` with the OKF index card, markdown-link graph, topic hubs, and `index.md` menu.

## Related

- [I Spent a Day With Anthropic Engineers. Here's Their REAL Workflow.](./i-spent-a-day-with-anthropic-engineers-heres.md) — the same "plain files, plain search" philosophy from inside Anthropic
- [Build Agentic RAG With Claude Code](./build-agentic-rag-with-claude-code.md) — the agentic-search-over-files approach applied to codebase RAG
- [RAG Explained in 14 Minutes | 10 RAG Patterns Every AI Engineer Must Know (2026)](./rag-explained-in-14-minutes-10-rag-patterns.md) — the vector-retrieval world OKF positions itself against
- ["Knowledge Graphs — Lecture 1: Knowledge Representation with Graphs (1.1–1.7)"](./kg-lecture-1-knowledge-representation-with-graphs.md) — the formal theory behind "links turn files into a graph"

---

Part of: [AI Engineering](./ai-engineering.md) · [Claude Code](./claude-code.md) · [Knowledge Graphs & Ontologies](./knowledge-graphs.md) · [RAG](./rag.md)
