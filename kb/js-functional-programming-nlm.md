---
type: course
title: Functional Programming in JavaScript — 12-Module NotebookLM Course
description: NLM-authored 12-module video course — expression-orientation to Functional FizzBuzz, the source course the RxJS payoff course rebuilds on streams
resource: C:\Users\hanss\Web\javascript\js-functional-programming-nlm
tags: [fp, javascript, course, notebooklm, teaching, closures, currying, laziness]
timestamp: 2026-08-15
---

# Functional Programming in JavaScript — 12-Module NotebookLM Course

## TL;DR

Hans's 12-module video course on functional programming in plain JavaScript, authored with NotebookLM (the `nlm` in the folder name) and narrated via a TTS/transcription pipeline — a pure content repository (scripts, transcripts, slides, rendered videos; no code, no build). The curriculum is a strict prerequisite chain from expression-orientation to a Functional FizzBuzz capstone, taught at unusual depth: closures via execution contexts and the heap, currying vs partial application, recursion against the reality of missing TCO, product types and cons lists built from pure closures, functor laws, laziness via thunks, falsiness as a zero-allocation Maybe, and referential transparency with its safe-mutation loophole. It is the source course that [From FP-JS to RxJS](./rxjs-from-fp-js-to-rxjs.md) rebuilds concept-for-concept on streams.

## Key Concepts

- **The curriculum arc** (each module a prerequisite of the next): 01 Expression-Orientation → 02 First-Class Functions & Closure Capture → 03 Currying and Arity → 04 Recursion as the Iteration Primitive → 05 Product Types via Objects & Closures → 06 The Cons List → 07 Higher-Order Transformations → 08 Strictness vs. Laziness → 09 Coercion/Falsiness as a Maybe Substitute → 10 Referential Transparency and the Boundary → 11 Iteration vs. Recursion Mechanics → 12 The Grand Synthesis (Functional FizzBuzz).
- **Rigid script template** — every module: one-paragraph abstract, five video segments (each with Objective / Visual Prompt / Script-Narrative-Outline), and a 5-question quiz (A–D options, no published answer keys). Plain text despite the `.md` extension — bare-line headings, the format the RxJS payoff course deliberately mirrors so both courses read side by side.
- **The house style is the syllabus** — the code rules *are* the FP discipline being taught: everything an expression (ternaries, `&&`/`||`, `??` — never `if`/`switch`/loops in functional code); data-last curried unary functions (`f => xs => ...`); cons lists from closures/pairs, not arrays; laziness via thunks (`() => lazyRange(low + 1)`) because JS has no TCO; the string monoid + falsiness as a zero-allocation Maybe (`(fizz(n) + buzz(n)) || n`); and the "1% boundary" — all side effects isolated at the program edge (`printStream`).
- **Mechanics over folklore** — Module 02 teaches closures through execution contexts, activation records, and heap-managed lexical scope; Module 04 confronts "highly volatile" purely recursive JS head-on; Module 11 closes with the historic compiler proofs that loops and tail recursion contain each other.
- **Data from first principles** — Module 05 eliminates objects and arrays entirely, representing data as pure heap-allocated closures (with the categorical product laws tested); Module 06 builds the cons list from Module 05's `pair`, studies structural sharing, and shows how the asymmetric cost profile dictates functional algorithm design.
- **The honest Maybe compromise** — Module 09 leverages JavaScript's coercion/falsiness to *bypass* the formal Maybe monad, and analyzes the architectural trade-off openly (the payoff course later fixes the confessed empty-string bug with `EMPTY`/`defaultIfEmpty`).
- **The performance loophole** — Module 10's centerpiece: the exact conditions under which internally mutable code stays observably pure — referential transparency as an optimization license, not just a purity rule.
- **Known content gaps** — some scripts reference code lost in generation ("We define lazyRange as:" followed by nothing, notably in Module 12) and carry citation artifacts; filling those snippets in house style is the standing editing task.

## Content

**What the repository is.** One folder per module, each holding the editable script (`fp module NN.md` — the source of truth), the spoken narration transcript (`*_cockaoo_transcript_basic.txt`, a rendering of the script, not an independent source), and binary build artifacts produced elsewhere (slides `.pptx`/`.zip`, rendered `.mp4`). Path gotchas are real: every path contains spaces, filenames are inconsistent (Module 12's script is `fp module 12 fizzbuzz.md`), Module 01's `.txt` is a byte-identical duplicate of its `.md`, and Modules 10–12 are missing some artifacts.

**The arc in four movements** *(condensed from the module abstracts)*:

- **Foundation (01–03).** Expression-orientation as a *mechanical prerequisite* for composable software, not a cosmetic choice; then the engine-level truth about first-class functions (execution contexts, activation records, how the heap keeps captured scopes alive); then currying vs partial application disentangled, with ES6 arrows as pure mathematical lambdas.
- **Data (04–06).** Recursion as the iteration primitive against the concrete limits of the runtime; product types from first principles down to pure closures and their categorical laws; the cons list built from `pair`, with structural sharing and the asymmetric cost profile driving algorithm design.
- **Semantics (07–09).** Higher-order transformations — `map` implemented over the hand-rolled cons list, the formal functor laws, and why data-last API design is a *structural requirement* for pipelines; then the big divergence, strict JavaScript vs lazy languages with thunks as the hand-operated escape hatch; then falsiness-as-Maybe with its trade-offs analyzed rather than hidden.
- **Discipline and synthesis (10–12).** Referential transparency, the algebra of optimization, and the safe-mutation loophole; the loops↔recursion containment proofs and where each keeps its state; and the capstone — a mathematically elegant, production-safe Functional FizzBuzz from lazy evaluation + string monoid + falsy fallback + isolated effect boundary.

**Its role in the bundle.** This course is the trunk of the FP cluster: the crocks notes ([monoids](./fp-monoids.md), combinators, functions) supply the library-grade versions of its algebraic structures, [universal algebra](./universal-algebra.md) supplies the operations-plus-laws theory behind its functor/monoid laws, and the [RxJS payoff course](./rxjs-from-fp-js-to-rxjs.md) redeems its three RxJS promises module by module. Before this note, 8 links across the bundle pointed here — the most-wanted unwritten node after the payoff course itself.

## Source

- Local content repo: `C:\Users\hanss\Web\javascript\js-functional-programming-nlm` (not a git repository) — its `CLAUDE.md` (the repo's own precise self-description) plus all twelve module abstracts read for this note. Authored with NotebookLM; narration via TTS pipeline.

## Notes

- The **house-style block is reusable as a style contract** — the same six rules govern code added to either course; worth lifting verbatim into the rxjs-course conventions.
- Standing task in the repo: fill the generation-lost code snippets (Module 12's `lazyRange` and friends) in house style, and sync the Module 01 `.md`/`.txt` duplicate when editing.
- Pipeline note: this plus the payoff course demonstrates the full NLM → script → TTS → video production chain — relevant as a template if the rxjs-course goes the same route.

## Related

- [From FP-JS to RxJS — The RxJS Payoff Course](./rxjs-from-fp-js-to-rxjs.md) — the RxJS port: same 12 concepts rebuilt on streams, promises 3.5/4.5/7.5 redeemed
- [Professor Frisby's Mostly Adequate Guide to Functional Programming](./fp-guide.md) — the classic book covering the same territory with formal Maybe/Either instead of the falsiness compromise
- [crocks Monoids — Prod, and the shared empty/concat interface](./fp-monoids.md) — the string monoid of Module 09/12, library-grade
- [Universal Algebra — Operations + Laws as a General Theory](./universal-algebra.md) — the theory behind the functor laws and monoid identities the course verifies
- [From Options to Observables — a monadic journey](./from-option-to-observable.md) — the Maybe→Observable journey Module 09's compromise gestures toward

---

Part of: [Functional Programming](./functional-programming.md)
