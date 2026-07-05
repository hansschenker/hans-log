---
slug: i-spent-a-day-with-anthropic-engineers-heres
title: I Spent a Day With Anthropic Engineers. Here's Their REAL Workflow.
channel: Ray Amjad
date: 2026-07-05
videoId: hMgB1bjkI7o
url: https://www.youtube.com/watch?v=hMgB1bjkI7o
type: summary
language: en
---

# I Spent a Day With Anthropic Engineers. Here's Their REAL Workflow.

## TL;DR

Field notes from a Code with Claude event in Tokyo just after Fable 5's release: there is no secret internal workflow — "everyone at Anthropic is living in the future, but in 4 different futures," each engineer running their own experiment. What they converge on instead: no spec-driven frameworks (describe → interview → plan → execute → verify → review), heavy investment in automatic verification environments at the surface where a user actually meets the change, and catching edge cases through repeated code-review rounds at the end rather than a perfect spec at the start.

## Key Concepts

- **Four different futures** — no unified internal workflow; multi-agent stacks, Claude CoWork, vanilla terminal all coexist; one shared best practice: reviewer agent ≠ builder agent (avoid bias)
- **Central transcript vault** — all internal sessions flow into a system for cross-analysis; personal tip: raise `cleanupPeriodDays` in settings.json (default 30 deletes local transcripts)
- **No spec frameworks** — nobody used OpenSpec/SpecKit/BMAD; flow is describe feature → constraints → model interviews you → mockup → plan mode → implement → review
- **"The map is not the territory"** — a strict spec forces the agent down a wrong path when codebase reality deviates; trust the agent to adapt
- **Shed old scaffolding** — with Fable 5 he deleted CLAUDE.md, memory, and skills on some projects and got ~95% results from plain descriptions; A/B test your workflow against the raw model
- **Automatic verification environments** — ask "where does the user meet this change?" (browser → Claude in Chrome/Playwright; API → agent calls the endpoint; terminal → agent drives a terminal); recordings/GIFs delivered to Slack
- **Edge cases at the end** — `/code-review` at max effort for big features, multiple rounds until the reviewer is silent; Codex reviews beat Greptile/CodeRabbit in his own audit
- **Loopify everything** — issue-finding loops feed a backlog, cloud agents open 20–30 PRs, auto-merge ordered by blast radius; Slack as the decision surface
- **Junior vs senior** — seniors don't prompt better, they *read output* better: lived experience spots wrong conclusions and hidden assumptions juniors wave through
- **Insight seeding** — one high-signal insight as the first message of a *fresh* chat acts like a Minecraft world seed; fan out 30–50 variations, saturates ~50–60k tokens; a curated library of seeds is exceptionally valuable

## Summary

The author arrived expecting to extract the perfect internal workflow from Anthropic engineers and found the opposite: everyone is living in a different future, running their own experiment — crazy multi-agent stacks, Claude CoWork, plain terminal — and nobody claims to have it figured out. The few genuinely shared practices are structural: keep the reviewer agent separate from the builder agent, and pipe every session transcript into a central vault so patterns can be analyzed across the org (his personal takeaway: raise `cleanupPeriodDays` in settings.json so your own transcripts survive past the 30-day default and you can mine them later).

**Against spec-maximalism.** None of the engineers he spoke to used spec-driven frameworks like OpenSpec, SpecKit, or BMAD. The common flow is lighter: describe the feature, state a few constraints, let the model interview you, maybe pick a design mockup, then plan mode → implementation → code review. He frames specs on an axis — at the extreme, a spec with every safeguard and edge case is just "code written in English." The engineer's aphorism "the map is not the territory" captures why: a strict spec forces the agent to keep following a plan even where the codebase contradicts it, producing worse results than trusting the agent to adapt. As models improve, yesterday's scaffolding becomes today's ceiling: he deleted CLAUDE.md files, memory files, and skills on some projects post-Fable-5 and plain descriptions got him ~95% there. His recommendation is empirical — run the same task through your current elaborate workflow and through the raw model, and compare.

**Verification over specification.** The single biggest lesson: invest in automatic verification environments. Internally, changes to the Claude desktop app are automatically verified by computer-use agents on cloud containers. The organizing question is *where does a user actually meet this change* — a browser (verify with Claude in Chrome or Playwright), an API surface (agent makes real requests), a terminal (agent drives one). He rebuilt his own project so every PR triggers browser verification with a screen recording, delivered as a GIF to Slack. The composite workflow he observed: describe (with interviewing/prototyping) → constraints → plan → execute → verify end-to-end at the user's surface → code review.

**Edge cases at the end, not the beginning.** Spec-first breaks on contact with the real codebase; better to start fuzzy, let the agent navigate the code, build the PR, and let repeated code reviews catch the surprises. He runs `/code-review` at max reasoning effort for big features (medium for small ones) and loops review→fix 2–3 times — one PR went ~12 rounds with Codex's reviewer before it fell silent. When he had Claude audit whether Greptile or CodeRabbit had ever said anything useful across his past PRs, the conclusion was "not really" — Codex reviews won. Sometimes review reveals the change itself was wrong, and the right move is discarding the PR for an architectural fix rather than a local one.

**Loopification.** Since the event his organizing question is "how much of my work can become a loop?" One loop continuously probes his app and files issues; cloud agents on a dedicated server work the backlog around the clock, opening 20–30 PRs that auto-merge in order of blast radius (loops currently capped at small changes, <500 lines). Codex's Chronicle research preview screenshots his screen and proposes *new* loops — e.g., mine PostHog session replays for rage-clicks and propose UI fixes. The end state he's aiming for: loops run in environments he has prepared, report to Slack, and Slack becomes his decision surface.

**The human differential.** Asked what still separates seniors from juniors when both use frontier models, engineers answered: not prompting — output reading. Seniors' lived experience flags wrong conclusions and hidden assumptions; juniors read the same output and see nothing wrong. The gap is closing, and the deadpan endgame ("I'm going to retire") acknowledges it. Related: his "insight seeding" practice — paste one high-signal insight as the first message of a fresh chat (a seed, like a Minecraft world seed), ask for implications and 30–50 variations, and treat it as a slot machine: mostly garbage, occasionally a gem deeper than the original. Fresh chats only — idea generation saturates after ~50–60k tokens and existing-chat pollution kills it. The compounding asset is a curated library of seeds, which in turn justifies ruthless curation of who you follow for insights.
