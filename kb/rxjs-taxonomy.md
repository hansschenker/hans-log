---
type: concept
title: RxJS Operator Taxonomy — The 22-Axis Fingerprint Model
description: every operator is a point in a 22-axis behavior space — lossy/lossless is one axis, and confused operators are neighbors differing on a single axis
resource: https://claude.ai/share/7be433c6-31f0-4851-be17-bc82d0e52a7d
tags: [rxjs, operators, taxonomy, fingerprint, category-theory, claude]
timestamp: 2026-08-15
---

# RxJS Operator Taxonomy — The 22-Axis Fingerprint Model

## TL;DR

An RxJS operator is not a trick with a name — it is a point in a ~22-dimensional behavior space, and mastery means reading and writing that "fingerprint" fluently in both directions. The model explains why operators get confused: `throttle*` vs `audit*` differ on exactly one axis (which event in the window survives), and `switchMap` vs `exhaustMap` share 21 of 22 positions, differing only in backpressure strategy (cancel vs ignore) — neighbors in fingerprint space, not different animals. The axes are orthogonal as dimensions but not all jointly satisfiable (some combinations are contradictions, some axes only activate given others), which makes the taxonomy a dependent type system rather than a flat checklist — and the session ended by producing a fingerprint template, an `operator-fingerprint` CLI, and a formal taxonomy paper.

## Key Concepts

- **The six time-based families in one table** — the conversation's starting point:

  | Familie | Ausgabe | Welches Event | Timer-Reset? |
  |---|---|---|---|
  | `throttle*` | T | Erstes (leading) | nein |
  | `audit*` | T | Letztes im Fenster | nein |
  | `debounce*` | T | Letztes vor Stille | **ja** |
  | `sample*` | T | Letztes bekanntes (externer Trigger) | nein |
  | `buffer*` | `T[]` | Alle gesammelt | nein |
  | `window*` | `Observable<T>` | Alle als Stream | nein |

- **Lossy vs lossless is the most practically important single axis** — `buffer*`/`window*` reshape the stream without loss; `throttle*`/`audit*` enforce bounded, predictable loss; `debounce*` risks *starvation* (a never-quiet source emits nothing at all); `sample*`'s loss depends on notifier-vs-source frequency. Using a lossy operator where correctness needs every value is a category error, not a bug.
- **Value-based loss has the same shape** — an operator is lossy when it has a *selection rule*: time-based operators select by timing, value-based ones by content or position (`filter`, `distinct*`, `first`/`last`/`elementAt`, `takeLast`, `ignoreElements`) — plus value-*triggered* loss in `switchMap` (cancels the active inner) and `exhaustMap` (ignores new outers).
- **The 12 core orthogonal axes** — temporal (immediate/deferred/scheduled), cardinality (1:1, 1:N, N:1, N:M), lossy, statefulness, synchrony, flattening strategy (merge/concat/switch/exhaust), thermal (cold/hot/warm), error strategy (propagate/recover/retry/isolate), completion sensitivity, side-effect safety, backpressure strategy (drop/queue/cancel/ignore), scheduler coupling.
- **Ten more axes complete the space (~22)** — subscription side (eager/lazy), arity (unary/n-ary), value interdependence (`withLatestFrom` vs `combineLatest` vs `zip` semantics), resubscription (`repeat`/`retry`), notification-type handling (`materialize`), scheduler injection, role (creation/pipeable/consumer), referential identity of emissions (matters for OnPush/memoization), termination guarantee (finite/infinite/conditional), emission-ordering guarantee (`concatMap` ordered, `mergeMap` not).
- **Orthogonal axes, constrained space** — no axis implies another (lossy ≢ async, stateful ≢ hot), yet the reachable region is smaller than 2²²: *infinite + complete-dependent* never emits; *N:1* already implies selection. Some axes are vacuous unless another axis activates them (flattening only exists for higher-order operators) — a **dependent type system**, analogous to Haskell's typeclass hierarchy (Monad presupposes Applicative).
- **`reduce` as the coherent fingerprint** — the worked exercise picked one position per axis (deferred, N:1, lossless, stateful, sync, queue, complete-dependent, pure, ...) and `reduce(acc, seed)` scored 22/22 — the catamorphism; `scan` is its anamorphism sibling.
- **`debounceTime`'s fingerprint reveals its edge case** — complete-dependent + lossy means completion *bypasses the silence timer*: `of(1,2,3).pipe(debounceTime(500))` emits `3` immediately. Axis tensions surface the edge cases documentation rarely does.
- **Three artifacts came out of the session** — an interactive HTML fingerprint template (with tension detector and presets), an `operator-fingerprint <name>` Node CLI (13 operators fully fingerprinted, JSON/Markdown output), and a formal paper: *"A Formal Taxonomy of RxJS Operator Behaviour: A 22-Axis Characterisation Framework"* (831 paragraphs — Observable as Functor/Monad, `mergeMap` as bind, why `switchMap` violates associativity, operator families, a 4-step selection algorithm).

## Content

The conversation is a staircase — each answer makes the next question inevitable, which is itself the meta-lesson: the structure was excavated, not constructed.

**1. Comparison → loss.** Comparing the six time-based families (`throttle*`, `audit*`, `debounce*`, `sample*`, `buffer*`, `window*`) surfaces the first deep split: `buffer*`/`window*` are lossless grouping (same logic, different output type — `T[]` for batching vs `Observable<T>` for reactive sub-pipelines like `.pipe(max())`), while the other four are lossy in characteristically different ways. `debounce*` is the only family that resets its timer on every event ("warte auf Stille"), and the only one that can starve entirely.

**2. Loss → axes.** Asking "which *value-based* operators are lossy" generalizes loss into a selection-rule pattern, and asking "what other characteristics exist" opens the axis catalog: synchrony, cardinality, statefulness, flattening strategy, thermal, error strategy, backpressure, completion behavior, side-effect safety — then rigorously separated into 12 *truly orthogonal* axes (dropping derived ones like "higher-order", which is just 1:N cardinality on the input type, or "unicast/multicast", which is the thermal axis renamed).

**3. Axes → completeness → 22.** Pressing "is this complete?" adds ten structural axes (subscription side, arity, interdependence, resubscription, notification handling, scheduler injection, role, referential identity, termination, ordering) — with the honest caveat that any finite axis set is a projection: operators are functions over time-indexed sequences with effects, so a truly complete characterization needs the type-theoretic/categorical model (which is where the Functor/Monad framing of [From Options to Observables](./from-option-to-observable.md) connects back in).

**4. The fingerprint, both directions.** Fingerprint-to-operator: choose one position per axis and find the operator — `reduce` fits 22/22. Operator-to-fingerprint: `debounceTime` forced through all 22 axes, exposing its flush-on-complete edge case and the collapse of axes 12/18 (its scheduler coupling *is* its injection point). The direction *name → axes* is the more revealing one: every axis demands a concrete answer, nothing hides behind intuition.

**5. Why confusion happens: neighborhood.** The families that trip people up are nearest neighbors in the space — `throttle*`/`audit*` differ on one axis (leading vs trailing survivor), `debounce*` differs from both on one axis (timer reset), `switchMap`/`exhaustMap` share 21 of 22 positions. One-axis differences produce silently different behavior under load; that is why the wrong flattening choice causes race conditions that only appear under concurrency.

**6. Structure → artifacts.** The taxonomy solidified into an operator template (identity + 22 axes in four blocks + tension detector + marble diagram), the `operator-fingerprint` CLI over 13 operators, and the formal paper with the full axis table, fingerprint catalogue, orthogonality/dependency analysis, operator families, a selection procedure with worked examples (search input → `debounceTime`, save button → `exhaustMap`), and the category-theory chapter (`reduce` as catamorphism, `scan` as anamorphism, `mergeMap` as bind).

## Claude Summary

Source is itself a Claude chat (2026-03-27); the full arc, condensed: compare six time-based families → which are lossy → which value-based operators are lossy → what other characteristics exist → which axes are truly orthogonal (12) → is the set complete (no — 22, still a projection) → fingerprint-to-operator exercise (`reduce`, 22/22) → operator-to-fingerprint (`debounceTime`) → takeaways → operator template (HTML + Markdown) → `operator-fingerprint` CLI → formal taxonomy paper (docx, 831 paragraphs). Closing insight: the axes form an implicit algebra — satisfiable, unsatisfiable, and vacuously-satisfied position combinations — so the real structure is a dependent type, and the next rigor step would be a denotational semantics in Haskell/Agda with the axes as type-level constraints.

## Source

- Claude chat (2026-03-27): https://claude.ai/share/7be433c6-31f0-4851-be17-bc82d0e52a7d
- Read via the rendered share page (the chat also produced local artifacts: HTML template, Markdown template, `operator-fingerprint.mjs` CLI, and the taxonomy paper docx — not in this repo)

## Notes

- The chat itself proposed the course placement: a **"Module X: The Operator Fingerprint Model"** sitting between the category-theory foundations and production patterns (axes → dependent types → fingerprinting → selection → edge cases → Observable as Monad). Strong candidate for the rxjs-course operator-reference spine.
- The backpressure axis (drop/queue/cancel/ignore) is the same design-choice framing as in [RxJS Heritage](./rxjs-heritage.md) — this note supplies the formal space around that single axis.
- The one-axis-difference explanation of `switchMap`/`exhaustMap` confusion pairs with the suffix-grammar view in [RxJS Operator Renaming](./rxjs-operator-renaming.md): renaming fixes the vocabulary, fingerprints fix the semantics.
- Where the CLI + paper artifacts live locally is worth recording here once found.

## Related

- [RxJS Heritage — from LINQ and Rx.NET](./rxjs-heritage.md) — the four flattening policies and backpressure-as-design-choice this taxonomy formalizes
- [A Formal Taxonomy of RxJS Observables](./rxjs-observable-taxonomy.md) — the sibling taxonomy for Observables (cold/hot ⟂ unicast/multicast); this note does the same for operators
- [RxJS Operator Renaming — The Suffix Grammar](./rxjs-operator-renaming.md) — naming layer over the same operator space
- [From Options to Observables — a monadic journey](./from-option-to-observable.md) — the Functor/Monad framing the axis model bottoms out in
- [rxjs-fp — A Functional-Style RxJS Built From Scratch](./rxjs-fp.md) — a from-scratch library where the fingerprint model could guide operator design

---

Part of: [RxJS](./rxjs.md)
