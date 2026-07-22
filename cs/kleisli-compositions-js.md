---
slug: kleisli-compositions-js
title: Kleisli Compositions in JavaScript
date: 2026-07-21
tags: [cs, functional, monads, composition, fp]
source: rxjs
---

# Kleisli Compositions in JavaScript

*Article by Luis Atencio — [medium.com/@luijar](https://medium.com/@luijar/kliesli-compositions-in-javascript-7e1a7218f0c4)*

## TL;DR

Ordinary function composition wants `A → B`, but effectful functions return *wrapped* values
(`A → M B` — a Maybe, Either, Task, or List). **Kleisli composition** (`composeK` / the `>=>` "fish"
arrow) glues such functions together by threading `chain` (a.k.a. `bind`/`flatMap`) between each
step, so failure, absence, and async are handled automatically instead of with nested branching.
Atencio's frame: "expect the worst and hope for the best" — raise the abstraction rather than
abandon FP when effects appear.

## Key Concepts

- **The type mismatch** — `compose(f, g)` needs `g: A → B` and `f: B → C`. Effectful steps are
  `A → M B`, so the wrapped output can't feed the next function directly; naive composition collapses.
- **Kleisli arrow** — a function returning a monadic type (`String → Maybe`, `String → Task`). A
  Kleisli *category* composes effects/monads rather than plain values.
- **`chain` is the glue** — `composeK` inserts `chain` (bind/flatMap) between steps: it reaches into
  the container, pulls the value out, and passes it to the next arrow — dissolving the impedance
  mismatch that breaks plain `compose`.
- **Fantasy Land conformance** — because Maybe/Either/Task/List all implement the same spec, they're
  interchangeable under `composeK`; one composition shape works across many effect types.
- **Bugs are bad data assumptions** — Atencio: ~95% of bugs come from a bad assumption about the
  data, not the code. Monadic composition *forces* explicit edge-case handling.

## Content

**Thesis.** You don't have to drop functional principles the moment you hit I/O, DB access, or
branching. Kleisli composition lets you keep composing declaratively while the monad handles the
effectful "plumbing" (unwrap → apply → rewrap) invisibly.

**Why regular `compose` breaks.** When `read` returns a `Task` but the next function expects a plain
buffer, the types don't line up and composition fails. `composeK` applies `chain` between each step,
so the `Task`/`Maybe`/`Either` context is carried through automatically.

**Pattern 1 — Maybe (safe property access):**
```javascript
const getStateCode = R.composeK(
  R.compose(Maybe.of, R.toUpper),
  maybeProp('state'),
  maybeProp('address'),
  maybeProp('user'),
  maybeParseJson
)
```
Each step returns `Maybe` (`Just` value or `Nothing`). Deep property access never throws on null —
absence propagates safely to the end.

**Pattern 2 — Task + Either (async file processing):**
- `read` → `Task` wrapping an async file read (rejects if the file is missing)
- `check` → inspects buffer length, returns `Task(Either.Right)` on success or `Either.Left` if empty
- `decode` / `words` → continue the chain inside the Task/Either context

```javascript
const processFile = R.composeK(words, decode('utf8'), check, read)
```
One expression encapsulates missing-file, empty-file, decode, and word-count handling — no imperative
`if`/`try` branching.

**Takeaways.** Kleisli composition should be default practice for effectful pipelines: it raises the
abstraction (express the logical flow, let the monad manage effects), makes edge cases explicit, and
— via Fantasy Land — turns Maybe/Either/Task/List into interchangeable building blocks.

## Source

- Original article: https://medium.com/@luijar/kliesli-compositions-in-javascript-7e1a7218f0c4
- Author: Luis Atencio (`@luijar`)
- Code uses Ramda's `R.composeK` and Fantasy Land monads (Maybe, Either, Task).

## Notes

- `composeK` is the "fish" operator `>=>` in point-free clothing — the same `chain`-threading that
  RxJS's `mergeMap`/`concatMap` do for Observables (Observable is itself a monad). Connects directly
  to [[pouchdb-article]], where DB effects are threaded through the Observable monad.
- The mental model "compose the *effects*, not just the values" is the reusable takeaway; it
  generalizes to Promises (`then` is chain-ish) and any Fantasy-Land type.

## Related

- [[pouchdb-article]] — Luis Atencio threading effects through the Observable monad (same author)
- [[javascript-combinators]] — apply/compose/leftApply building blocks that precede monadic composition
- [[rxjs-heritage]] — `SelectMany`/`chain` as the flatten operation behind RxJS concurrency operators
