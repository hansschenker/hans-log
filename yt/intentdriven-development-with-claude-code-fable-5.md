---
slug: intentdriven-development-with-claude-code-fable-5
title: Intent-driven development with Claude Code & Fable 5
channel: Google Cloud Tech
date: 2026-07-07
videoId: 6ERUGFurDHY
url: https://www.youtube.com/watch?v=6ERUGFurDHY
type: summary
language: en
---

# Intent-driven development with Claude Code & Fable 5

## TL;DR

A Google Cloud Tech conversation and live demo with Lydia Hallie (Anthropic's Claude Code team) and YK Sugi (CS Dojo, author of the popular "Claude Code tips" repo) on **intent-driven development** — describing *what* you want built rather than *how*, then owning the verification. Two demos build and then evolve a 3D slingshot game while running Claude Code on Google Cloud's Vertex AI, showcasing voice prompting, auto mode, Claude Design wireframes, and dynamic multi-subagent workflows running on Fable 5.

## Key Concepts

- **Intent-driven development** — express *what* to build, not *how*. Clarity of intent matters more than the "perfect prompt"; if your intent is clear, Claude fills the gaps even with typos.
- **Voice-to-text prompting** — talk instead of type to express intent faster; brainstorming out loud reduces self-editing friction.
- **Broad-first, then deep** — settle architecture and library choices before details. Rule of thumb: *ask more questions when you have less context.*
- **Verification is part of intent** — plan mode, pasted images, and tests are how you verify. The work shifts from ~90% coding / 10% review to ~90% review — being a good reviewer matters more than ever.
- **You own the output** — don't commit everything generated. Review and commit only what's valuable; use draft PRs + feature branches (not direct-to-main) to simulate real code review.
- **Claude Code on Google Cloud / Vertex AI** — install via gcloud SDK + enable Vertex AI API, or the built-in `setup-vertex` wizard. Gives access to Opus 4.6 and Fable 5; models can be pinned to the 1M-context variant.
- **Auto mode** — a middle ground between allow/deny lists: a classifier runs *between* tool calls and only pauses for genuinely dangerous actions. Cuts "permission fatigue," is context-aware (deleting a folder you asked to delete isn't flagged), resists prompt injection, and is far safer than `--dangerously-skip-permissions`. Enabled via an env var, then surfaced with Shift+Tab.
- **Claude Design (research preview)** — generate an editable HTML wireframe / visual plan from prompts, then export it as the spec that drives Claude Code. "Claude Code, but for design."
- **Dynamic workflows** — ask Claude to "use a dynamic workflow" and it writes a JavaScript file orchestrating many subagents: build agents run in parallel (engine, UI, audio, levels/haptics), then integration → review → verify run sequentially. Deterministic, saveable, and re-runnable as a command; per-subagent model choice is editable in the JS (fable/sonnet/opus).
- **Role shift** — the software engineer becomes more of a product manager: owning architecture, features, taste, and high agency rather than syntax. Analogy: you write TypeScript, not the machine code beneath it.
- **"Cloudify" everything** — automate the work you don't enjoy; keep the creative work you do. Claude Code as a universal interface to the computer (research, video/image editing, data) — YK saved $10k using it to compile a realtor email list when buying property. Claude Cowork handles non-technical tasks (email, calendar, flights); Claude Code handles technical.

## Summary

**Framing — intent over prompts.** The hosts open on why Claude Code has changed how engineers build. YK Sugi's "Claude Code tips" repo (8,000+ stars) grew from him using the tool the day it launched — including, quietly, for a job-interview demo whose quality surprised the interviewers. Both guests reframe good AI coding as *intent-driven development*: it isn't about a magic prompt but about knowing exactly what you want and expressing it. YK's top practical lever is **voice-to-text** — talking is faster than typing and gets you out of your own head, and Claude tolerates the resulting typos as long as the intent is clear. Lydia adds that intent includes **verification**: plan mode, pasted images, and structuring the prompt with real software-engineering judgment all shape what Claude actually does. Anthropic's goal is to shrink the friction from "idea" to "deployed website" as close to zero as possible.

**Demo 1 — YK builds a slingshot game on Vertex AI.** After showing the Claude Code + gcloud SDK setup (set project, enable the Vertex AI API, launch Claude against Vertex), YK voice-prompts a 3D slingshot game: fixed camera, drag for x/y, hold-duration for z, front-end only (HTML/JS/CSS). He works broad-first — letting the model propose the stack (Three.js) and physics options, going back and forth to pick a WASM physics library, then narrowing scope to just "a working slingshot, no targets yet." Along the way he shares tips: alias `claude` for speed, keep all projects in one parent folder so the agent can pull elements across them, learn Git + `gh` CLI, verify by *testing behavior* not just reading code, and — crucially — don't push to `main`. He has the agent init a repo, add a trajectory preview, add shatter-on-hit targets, grant a collaborator admin access, then commit to a **feature branch and open a draft PR** to simulate code review before merging.

**Demo 2 — Lydia rebuilds it with Claude Design + workflows on Fable 5.** Lydia starts from a **visual plan** built in Claude Design (research preview): an HTML wireframe of menus, level select, gameplay loop, health/charge bars, haptics, and scoring, which she edits and exports as her spec. She sets up Vertex with the `setup-vertex` wizard, enabling Opus 4.6 and **Fable 5** pinned to 1M context. She then explains **auto mode** — an env-var toggle that inserts a classifier between tool calls, asking only about dangerous operations. It solves the dilemma between constant permission prompts ("permission fatigue") and the reckless `--dangerously-skip-permissions`, is context-dependent, and better catches prompt injection — enabling long autonomous sessions. Finally she uses a **dynamic workflow**: "read this design file and use a dynamic workflow to rebuild the game." Claude generates a JavaScript workflow that fans out parallel build subagents (engine, UI, audio, levels/haptics) followed by sequential integration, review, and verify phases — all on Fable 5. Because it's a real JS file, it's deterministic, can be saved and re-run as a command, and per-subagent models can be swapped in code. The result matches the wireframe closely and turns the prototype into a real multi-level game.

**Bigger ideas — craft, ownership, and scope.** On the recurring "AI writes too much messy code" complaint, both push back the same way: *you're responsible for the output.* If you generate 100k lines you don't have to commit 100k lines — review with AI or by hand, use draft PRs, and only merge what's good. The engineer's role is shifting toward product management: owning architecture and intent while building the right environment (hooks, permissions, sandboxes) around the agent. Lydia's personal setup leans on scheduled/proactive Claude sessions and the GitHub Claude bot that auto-fixes PRs until CI is green. Both describe "cloudifying" life — automating the tedious, keeping the creative (Lydia still hand-makes her keynote slides). YK frames Claude Code as the universal interface to the computer — research, Reddit sweeps, video/image conversion, and the realtor-list trick that saved him $10k — while Claude Cowork covers non-technical work (email, calendar, flights) on the same runtime. Rapid-fire takeaways: AI makes senior developers *more* valuable, reading docs is not dead, and prioritize software architecture over specific language features.
