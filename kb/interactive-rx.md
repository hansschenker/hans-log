---
type: reference
title: IxJS — Interactive Extensions for JavaScript
description: the pull-based dual of RxJS — LINQ-style operators over Iterable/AsyncIterable, where the consumer controls the pace
resource: https://github.com/ReactiveX/IxJS
tags: [rxjs, ixjs, iterables, async-iterables, pull-based, linq, duality]
timestamp: 2026-08-15
---

# IxJS — Interactive Extensions for JavaScript

## TL;DR

IxJS is RxJS's pull-based sibling from the same ReactiveX family: the same LINQ-style operator grammar (`map`, `filter`, `reduce`, `pipe`) applied to `Iterable` and `AsyncIterable` instead of `Observable`. The split is the pull/push duality itself — Rx is for event-based workflows where the *producer* pushes at its own rate; Ix is for I/O-style workflows where the *consumer* pulls when ready, which is why backpressure simply doesn't arise (the consumer sets the pace by iterating). "Interactive" vs "Reactive" is the original Microsoft naming for exactly this pull/push pair.

## Key Concepts

- **One grammar, two duals** — IxJS composes synchronous and asynchronous *collections* with Array#extras-style operators; RxJS composes *event streams*. Same operator vocabulary, opposite control flow.
- **Core types** — `Iterable` (via `Symbol.iterator`, consumed with `for...of`) and `AsyncIterable` (via `Symbol.asyncIterator`, consumed with `for await...of`); `IterableX`/`AsyncIterableX` are the prototype-enhanced variants for direct method chaining without importing each operator.
- **When Ix, when Rx** — Ix for I/O operations where you as the consumer pull data when you are ready; Rx for event-based workflows where data is pushed at the producer's rate. Wrong pick = fighting the control flow.
- **Backpressure dissolves under pull** — the docs don't discuss backpressure because they don't need to: on-demand consumption means the consumer's iteration speed *is* the flow control. (The push side has to *design* a strategy instead — see [RxJS Heritage](./rxjs-heritage.md).)
- **Pipeable, tree-shakeable style** — `from(source()).pipe(filter(...), map(...))`, mirroring modern RxJS:

  ```javascript
  import { from } from 'ix/iterable';
  import { filter, map } from 'ix/iterable/operators';

  const results = from(gen()).pipe(
    filter(x => x % 2 === 0),
    map(x => x * x)
  );
  for (const item of results) console.log(item);
  ```

- **Lineage** — Ix.NET was Microsoft's pull-based companion to Rx.NET (LINQ to Objects extended); IxJS carries that into JavaScript under the ReactiveX org, shipped as the `ix` npm package with TS/CJS/ESM/UMD builds.

## Content

**The effect quadrant.** The cleanest way to place IxJS is the classic sync/async × one/many grid — Ix owns the pull column that plain values and Promises leave open:

| | one value | many values |
|---|---|---|
| **sync (pull)** | `T` | `Iterable<T>` — **Ix** |
| **async (pull)** | — | `AsyncIterable<T>` — **Ix** |
| **async (push)** | `Promise<T>` | `Observable<T>` — **Rx** |

`AsyncIterable` is the interesting middle: asynchronous like an Observable, but the consumer still pulls — each `for await...of` step *requests* the next value. That makes it the natural type for paginated APIs, file/stream reading, and database cursors, where producing faster than consumption would only waste memory.

**Duality in practice.** The [RxJS Heritage](./rxjs-heritage.md) note carries the theory table — `IEnumerable`/`IEnumerator` (consumer pulls) as the dual of `IObservable`/`IObserver` (producer pushes), with the consequence "pull naturally avoids backpressure; push requires explicit flow control to survive." IxJS is that left column shipped as a library: the same `pipe` composition, deferred execution (nothing runs until iterated — the pull mirror of "nothing runs until subscribed"), and the same operator names, but every RxJS backpressure decision (drop/queue/cancel/ignore) becomes a non-question.

**Async iteration ergonomics.** `from()` lifts standard iterables, generators, Promise iterators, or other AsyncIterables into the Ix world; `AsyncIterable` supports both `for await...of` and `.forEach()` with `.catch()` error handling.

## Source

- GitHub: https://github.com/ReactiveX/IxJS (README) — npm package `ix`

## Notes

- Direct **rxjs-course Module 1** material: IxJS is the *living* pull side of the Meijer duality — the heritage story (LINQ → Ix.NET/Rx.NET → IxJS/RxJS) can be demonstrated with runnable code on both sides of the dual.
- Great contrast device for the backpressure section: show the same pipeline in Ix (no flow-control needed) and Rx (must choose drop/queue/cancel/ignore) — the fingerprint axes that vanish under pull make the [22-axis taxonomy](./rxjs-taxonomy.md) sharper.
- `AsyncIterable` is also what modern JS runtimes hand you for streams (Node readable streams are async-iterable) — a practical hook for the course's I/O examples.

## Related

- [RxJS Heritage — from LINQ and Rx.NET](./rxjs-heritage.md) — the pull/push duality table this library embodies
- [RxJS Operator Taxonomy — The 22-Axis Fingerprint Model](./rxjs-taxonomy.md) — the backpressure and synchrony axes that dissolve under pull
- [erik-meijer](./erik-meijer.md) — Iterable/Observable duality as the mathematical root (not yet written)
- [From Options to Observables — a monadic journey](./from-option-to-observable.md) — the same one-grammar-many-contexts idea, monad by monad

---

Part of: [RxJS](./rxjs.md)
