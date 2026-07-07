---
slug: claude-fable-5-is-back-should-you-still
title: Claude Fable 5 Is BACK! Should You Still Use Opus? (Real Test)
channel: The Cloud Girl
date: 2026-07-07
videoId: 2XhM_8DlgnQ
url: https://www.youtube.com/watch?v=2XhM_8DlgnQ
type: summary
language: en
---

# Claude Fable 5 Is BACK! Should You Still Use Opus? (Real Test)

## TL;DR

A practical walkthrough (The Cloud Girl) of Anthropic's new Fable 5 best-practices guide, aimed at people disappointed that Fable 5 didn't beat Opus 4.8 in their old setups. The core message: Fable 5 isn't a faster, smarter Opus you can drop in — it's a different model built for long, multi-step work, and you get the best out of it by *removing* prompt instructions and setting intent instead of rules. Five patterns are demoed, counted down from #5 to the #1 "cheat code."

## Key Concepts

- **Fable 5 ≠ a better Opus 4.8** — Opus is tuned for short tasks ("summarize this paragraph"); Fable 5 is built for long ones ("audit the codebase, find leaked API keys, fix them, write tests, open a PR"). By default it thinks longer and gathers more context, so old Opus prompts make it over-plan and over-refactor.
- **#5 — Refactor your prompts: remove instructions, don't add.** Opus-era prompts are too prescriptive and actively degrade Fable 5's output. When something's off, the fix is a *leaner* prompt, not more rules.
- **#4 — Use parallel sub-agents / build for async.** Fable 5 dispatches parallel sub-agents more readily than any prior Claude. Delegate independent subtasks and keep working; long-lived sub-agents retain context and save time/cost via cached rates. The one production instruction: *"delegate independent subtasks to sub agents and keep working while they run. Intervene if a sub agent goes off track or is missing relevant context."*
- **#3 — Give Fable 5 a memory system.** It has no memory between conversations by default but performs much better with one — and it can be as simple as a text file. Have it write lessons/preferences to the file, then read+apply them at the start of new sessions.
- **#2 — Use effort levels correctly.** Four levels: **low / medium / high / extra-high**. High is the default; extra-high for the most capability-intensive work; medium/low for routine, fast back-and-forth. Even at **medium, Fable 5 often beats Opus 4.8 at extra-high** — don't default everything to max (it costs more and is slower). Higher effort can over-engineer; counter with *"do the simplest thing that works well. Don't add anything beyond what the task requires."*
- **#1 — Set intent, not rules (the cheat code).** Fable 5's instruction-following is strong enough that one well-planned sentence replaces a whole block of prompt engineering. Describe the *standard* you want and the *reason* behind the request — give context — rather than an exhaustive list of behaviors. Fable 5 figures out the behaviors that serve the intent.

## Summary

The video responds to a wave of confusion: people tried Anthropic's newly released **Fable 5** (alongside Mythus 5), dropped it into their existing Opus 4.8 workflows, and found it *worse* — slower, over-planning, refactoring an entire module when asked to rename a variable. The host's thesis, drawn from Anthropic's just-published best-practices guide, is that this is a category error. Fable 5 is not "Opus but faster and smarter"; it's a different kind of model optimized for long, thorough, multi-step tasks. Point it at a trivial task with a verbose Opus-style prompt and it will over-think, over-explain, and over-build.

She then counts down five patterns. **#5 Refactor prompts and scaffolding:** prompts written for Opus 4.8 are too prescriptive and degrade Fable 5's results, so the counterintuitive fix is to *remove* instructions. A demo shows a lean prompt (write a Python function that picks a random SpongeBob code and prints it with today's date) producing clean output, while a bloated instruction list produces worse, cluttered results. **#4 Parallel sub-agents and async:** Fable 5 spins up parallel sub-agents easily, so you delegate independent subtasks and keep working instead of waiting — demoed with two sub-agents arguing for and against pineapple on pizza, then a third synthesizing. The guidance that unlocks it is a single sentence about delegating and intervening only when a sub-agent drifts.

**#3 Memory system:** Fable 5 starts each conversation blank but improves markedly with a memory file. In the demo, a Bollywood-playlist session records the user's "only '90s golden-era, pre-2000" preference into a memory note; a fresh session that reads the note honors it immediately — one setup, permanent benefit. **#2 Effort levels:** the primary dial for trading intelligence vs. latency vs. cost, with four settings; high is the sensible default, and — crucially — Fable 5 at *medium* frequently beats Opus 4.8 at *extra-high*, so maxing everything just wastes time and money. A villain-origin-story demo contrasts a fast, decent medium response against a richer but slower extra-high one that isn't always worth it; the anti-over-engineering guardrail is "do the simplest thing that works well." **#1 Set intent, not rules:** the pattern that makes the rest work. Where Opus rewarded piling on instructions, Fable 5 fights it — so describe the standard and the *why*, give context, and let the model derive the behaviors. A side-by-side party-planning prompt shows the leaner, intent-first version producing a more personal, better result. The throughline of the whole video: with Fable 5, give the right context and intent, not an exhaustive list of instructions.
