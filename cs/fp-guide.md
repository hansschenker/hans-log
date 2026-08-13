---
slug: fp-guide
title: Professor Frisby's Mostly Adequate Guide to Functional Programming
date: 2026-08-13
tags: [cs, fp, javascript, currying, composition, functors, monads, monoids]
source: cs
---

## TL;DR

The book-length version of the road that today's other entries only sketch: it starts from first-class
functions and walks — chapter by chapter, each one earning the next — through purity, currying,
composition, types, and containers until monads and monoids arrive as the obvious conclusion rather
than as mystical objects. It is the canonical FP-in-JavaScript text (CC BY-SA, by Brian Lonsdorf /
@DrBoolean), and its distinctive move is *motivation before formalism*: you feel the pain that each
abstraction removes before you learn its name.

## Key Concepts

- **The arc is the argument.** Ch. 1–5 build the toolkit (first-class functions → purity → currying →
  composition), Ch. 6 spends it on a real app, Ch. 7 adds types, Ch. 8–13 climb the container ladder
  (functor → monad → applicative → natural transformation → traversable → monoid). No chapter is
  optional scaffolding; each is the answer to a problem posed by the one before.
- **Purity as the enabling constraint**, not a moral stance — same input, same output, no observable
  side effects, which is what makes the later composition laws hold at all.
- **Currying is the precondition for point-free code.** You cannot compose functions cleanly until
  they are unary; currying is the structure that makes `compose(f, g, h)` possible.
- **"Coding by composing"** — programs as `f∘g∘h` pipelines rather than statement sequences, the same
  idea [[rxjs-pipe-compose]] examines from the RxJS side.
- **Hindley-Milner as documentation** (Ch. 7) — type signatures as the cheapest specification, and the
  route to "parametricity": what a function *can't* do, given only its signature.
- **"Tupperware"** (Ch. 8) is the pedagogical hinge — the container/functor chapter. Wrapping a value
  and mapping inside the wrapper is introduced as a mundane containment trick, and the whole monad
  edifice then follows from taking it seriously.
- **"Monadic Onions"** (Ch. 9) — nesting is the problem, `join`/`chain` is the answer. Exactly the
  `Option<Option<T>>` motivation used in [[from-option-to-observable]], reached from the container
  side rather than the null-check side.
- **Applicatives (Ch. 10)** for combining independent wrapped values, where monads' sequencing is
  stronger than needed.
- **Monoids "bring it all together" (Ch. 13)** — the closing chapter, not the opening one: an
  associative binary operation plus an identity, generalising concat/sum/product/max. The same
  structure the crocks `Prod` docs in [[fp-monoids]] present as an API.
- **Appendices A–C** ship the actual support functions, algebraic structures, and point-free
  utilities — the book is executable, with an npm package (`@mostly-adequate/support`) behind the
  exercises.

## Content

### Structure

| Ch. | Title | What it earns |
|---|---|---|
| 1 | What Ever Are We Doing? | the seagull-program motivation |
| 2 | First Class Functions | functions as values, the ground floor |
| 3 | Pure Happiness with Pure Functions | purity, and why it buys everything later |
| 4 | Currying | unary functions, partial application |
| 5 | Coding by Composing | `compose`, point-free style, associativity |
| 6 | Example Application | the toolkit spent on something real |
| 7 | Hindley-Milner and Me | signatures as documentation, parametricity |
| 8 | Tupperware | containers and functors — the hinge chapter |
| 9 | Monadic Onions | nesting, `join`/`chain`, monads |
| 10 | Applicative Functors | combining independent effects |
| 11 | Transform Again, Naturally | natural transformations |
| 12 | Traversing the Stone | traversable, turning structures inside out |
| 13 | Monoids bring it all together | associativity + identity as the closing frame |

Appendices: **A** Essential Functions Support · **B** Algebraic Structures Support · **C** Point-free
Utilities.

### Why the ordering matters

The guide's pedagogy is the reason to prefer it over a reference: abstractions arrive *late* and
*motivated*. Monads are Ch. 9, after five chapters of composition have made the nesting problem
unavoidable; monoids are Ch. 13, after the reader has met a dozen concrete monoids without the name.
This is the inverse of the usual "here is a monad, here are the laws" presentation — and it is the
same instinct behind [[from-option-to-observable]], where the speaker explicitly refuses the
category-theory definition and teaches by example instead.

### Practical notes

- Examples are ES6-era, with a support package (`npm i @mostly-adequate/support`) providing the
  helper functions and algebraic structures used in exercises.
- Best read online via Gitbook (side-bar navigation, in-browser exercises); PDF and EPUB are
  published as release artifacts.
- The repo's own README warns the local build setup "is now a bit old and thus, you may run into
  various issues when building this locally" — read online or grab a release rather than fighting
  the toolchain.

## Claude Summary

_(Scaffolded from the log entry plus the repo's own table of contents and README — the Content
section above is the synthesis. Not yet read chapter by chapter.)_

## NLM

_(none)_

## Recall.ai

_(none)_

## Source

- **Repo:** <https://github.com/MostlyAdequate/mostly-adequate-guide>
- **Author:** Brian Lonsdorf (@DrBoolean), community-maintained under the MostlyAdequate org
- **License:** Creative Commons Attribution-ShareAlike 4.0 International
- **Files used for this scaffold:** `SUMMARY.md` (table of contents), `README.md` (reading options,
  support package, license, build caveat)

## Notes

- **This is the spine the other 2026-08-13 entries hang off.** The crocks docs
  ([[fp-combinators]], [[fp-monoids]], [[fp-functions]]) are the *reference* for the same concepts;
  this is the *narrative*. Read the guide for order and motivation, hit crocks when you need the API.
- **Ch. 8–9 is the pairing to make with the monad talk.** [[from-option-to-observable]] arrives at
  `flatMap` from the practical side (nested null checks in a repository); Tupperware/Monadic Onions
  arrives from the container side (`Option<Option<T>>` as a shape problem). Teaching both framings
  back-to-back is probably the strongest version of that lesson for
  [[rxjs-from-fp-js-to-rxjs]].
- **Ch. 13 answers a question the RxJS material keeps raising** — why `reduce`, `concat`, `merge` and
  `max` feel like the same operation. Monoid, arriving last, is the retroactive explanation.
- **Open question for the course:** the guide never reaches streams. The natural extension is a
  Ch. 14-that-doesn't-exist — "Traversing time" — which is precisely the gap
  [[rxjs-from-fp-js-to-rxjs]] is meant to fill. Worth checking whether the guide's chapter order
  survives the jump to Observables, or whether time forces a different sequence.
- Not yet read end-to-end; this note is structure-and-intent only. Fill Content per chapter as they
  get read.

## Related

- [[from-option-to-observable]] — the same path to monads, told in 30 minutes from the null-check side
- [[fp-monoids]] — crocks `Prod`, the API view of Ch. 13
- [[fp-combinators]] — crocks combinator helpers, the API view of Ch. 4–5
- [[fp-functions]] — crocks point-free function index, the API view of Appendix C
- [[js-fp]] — Packt FP-for-JS-developers course repo, the video-course counterpart
- [[js-functional-programming-nlm]] — the 12-module NotebookLM FP course
- [[rxjs-from-fp-js-to-rxjs]] — the same 12 concepts rebuilt on streams
- [[rxjs-pipe-compose]] — composition in the RxJS layer
- [[universal-algebra]] — operations-and-laws framing behind functors, monads, monoids
