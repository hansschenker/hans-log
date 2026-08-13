---
slug: js-fp
title: JavaScript — Functional Programming for JavaScript Developers (Packt code repo)
date: 2026-08-13
tags: [cs, fp, javascript, packt, course, code-samples]
source: cs
---

## TL;DR

The **code repository** for a Packt learning-path bundle — three modules stitched into one product,
27 chapters of runnable samples, MIT-licensed. It is not the text: the repo carries only the
examples, and the modules aren't even named inside it. Worth having as a source of working ES5/ES6-era
sample code, with the actual FP material concentrated in Module 3; Modules 1–2 are general JavaScript
and design patterns that build up to it.

## Key Concepts

- **It's a bundle, not a book.** Packt learning paths splice several existing titles into numbered
  "Modules"; this repo exposes them only as `Module 1` / `Module 2` / `Module 3`, with no titles or
  authors given per module.
- **Chapter coverage is uneven** — Module 1 has `Chapter01–09`, Module 3 has `Chapter01–07`, but
  Module 2 skips `Chapter01`, `Chapter02` and `Chapter11`. Chapters with no accompanying code simply
  aren't there, so a missing folder isn't a broken repo.
- **The README's outcome list is the only description of the arc**, and it reads as a progression:
  basic language constructs → functions, closures, object-oriented features → DOM manipulation and
  ES6 → concurrency and performance → design patterns → currying and function composition →
  reactive patterns and dependency injection → immutable data structures and pure functions.
- **FP arrives last.** Currying, composition, immutability, purity and reactive patterns are the
  *end* of that list — the same late-and-motivated ordering [[fp-guide]] uses, and the opposite of
  a reference like [[fp-functions]].
- **MIT licensed**, with the usual Packt extras (free DRM-free PDF for print/Kindle owners, feedback
  form).

## Content

### What's actually in the repo

| Module | Chapter folders | Present |
|---|---|---|
| Module 1 | `Chapter01` – `Chapter09` | 9, contiguous |
| Module 2 | `Chapter03` – `Chapter10`, `Chapter12` – `Chapter14` | 11, with `01`, `02`, `11` absent |
| Module 3 | `Chapter01` – `Chapter07` | 7, contiguous |

Top level otherwise holds only `README.md`, `License` (MIT), `.gitignore`, `.gitattributes`.

### How to use it

Since the modules are unlabelled and the prose isn't included, the repo is best treated as a
**sample-code quarry** rather than a course to work through:

- Module 3's seven chapters are where currying, composition, immutability and pure functions live —
  that's the part that overlaps [[fp-guide]] and the crocks material.
- Modules 1–2 cover general JavaScript and design patterns; useful mainly if a specific pattern
  implementation is wanted, less so as FP study.
- Expect ES5/ES6-era idioms throughout. Read it for the shape of the solution, not for current style.

## Claude Summary

_(Scaffolded from the repo's README and directory listing — the prose text isn't in the repo, so
this note describes the artifact, not the book's content. Nothing read chapter by chapter.)_

## NLM

_(none)_

## Recall.ai

_(none)_

## Source

- **Repo:** <https://github.com/PacktPublishing/JavaScript--Functional-Programming-for-JavaScript-Developers>
- **Used for this note:** the repo README (product description, outcome list, license) and the
  GitHub contents API for the top-level and per-module directory listings
- Module titles/authors are **not** stated anywhere in the repo — deliberately not guessed here

## Notes

- **Lowest-value entry of 2026-08-13, and that's fine.** Code without its prose is a reference, not
  a path. If the FP material is wanted properly, [[fp-guide]] is free, complete, and better
  sequenced; this repo is where to look when a *working example* of something is needed.
- **Module 3 is the only part worth a real pass**, and the question to ask while reading it is
  whether it says anything [[fp-guide]] doesn't. If not, drop the entry to reference-only status.
- **The outcome list is a useful sanity check on course design** — it puts "reactive patterns" and
  "immutable data structures" *after* currying and composition, which matches the ordering
  [[rxjs-from-fp-js-to-rxjs]] is built on. Independent confirmation that FP-before-streams is the
  conventional sequence, not just a personal preference.
- **Gap to verify:** whether Module 2's missing `Chapter01`/`02`/`11` are genuinely code-free
  chapters or an upload omission. Only matters if that module turns out to be worth using.
- Not read; treat every claim above as being about the repository, not the book.

## Related

- [[fp-guide]] — the free, better-sequenced version of the same path to FP
- [[js-functional-programming-nlm]] — the 12-module NotebookLM FP-in-JavaScript course
- [[fp-functions]] · [[fp-combinators]] · [[fp-monoids]] — the crocks reference side
- [[rxjs-from-fp-js-to-rxjs]] — the same concepts rebuilt on streams
- [[typescript-workshop]] — the other course-repo entry of the same week
