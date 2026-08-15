---
type: course
title: From FP-JS to RxJS — The RxJS Payoff Course
description: the RxJS payoff course — the same 12 FP-in-JavaScript concepts, one per module, rebuilt on streams with runnable strict-TS demos
resource: https://github.com/hansschenker/rxjs-from-fp-js-to-rxjs
tags: [rxjs, fp, course, teaching, typescript, streams]
timestamp: 2026-08-15
---

# From FP-JS to RxJS — The RxJS Payoff Course

## TL;DR

Hans's own 12-module course that cashes in the three explicit promises the **Functional Programming in JavaScript** course made about RxJS: that curried unary pipelines are "the exact design methodology powering functional pipelines in libraries like RxJS" (3.5), that the Observable is the cure for JavaScript's missing tail calls (4.5), and the literal "Real-World Parallel: RxJS Operator Functions" (7.5). Each module mirrors its FP-course counterpart one-to-one — same concept, lifted from single values to values over time — with a `script.md` (5 video segments + quiz, same plain-text format as the source course) and a `demo.ts` whose five sections run every claim in the script. The recurring sentence pattern is the course's engine: *"In the JavaScript course you X; in RxJS this becomes Y."*

## Key Concepts

- **The payoff structure** — the FP course teaches a concept on plain JavaScript; this course re-teaches the *same* concept on streams, so RxJS arrives as a consequence rather than a new topic. Twelve concepts, twelve modules, 1:1.
- **The full mapping** (from the README):

  | # | FP-in-JS module | RxJS module | Key APIs |
  |---|---|---|---|
  | 01 | Expression-Orientation | The Pipeline as an Expression | `of`, `map`, `filter`, `iif`, `pipe` |
  | 02 | First-Class Functions & Closure Capture | First-Class Streams and Producer Closures | `Observable`, `defer`, `finalize` |
  | 03 | Currying and Arity | Operator Factories and the Unary Pipeline | `pipe`, `map`, `MonoTypeOperatorFunction` |
  | 04 | Recursion as the Iteration Primitive | Recursion Without a Stack | `range`, `reduce`, `generate`, `expand` |
  | 05 | Product Types via Objects & Closures | Products of Streams and Data as Behavior | `zip`, `combineLatest`, `new Observable` |
  | 06 | The Cons List | The Stream as a List in Time | `EMPTY`, `concat`, `defer`, `first`, `skip` |
  | 07 | Higher-Order Transformations | Operators, Functor Laws, and Higher-Order Streams | `map`, `toArray`, `concatMap`, `mergeMap` |
  | 08 | Strictness vs. Laziness | Cold Observables and Subscription-Time Evaluation | `defer`, `tap`, `generate`, `take` |
  | 09 | Coercion/Falsiness as a Maybe Substitute | EMPTY as an Honest Nothing | `EMPTY`, `filter`, `defaultIfEmpty` |
  | 10 | Referential Transparency and the Boundary | Pure Declarations and the subscribe Boundary | `scan`, `tap`, `shareReplay` |
  | 11 | Iteration vs. Recursion Mechanics | Where the Loop Lives | `queueScheduler`, `observeOn`, `generate` |
  | 12 | The Grand Synthesis (Functional FizzBuzz) | FizzBuzz as a Stream | `range`, `zip`, `repeat`, `map`, `take` |

- **"Declarations denote; subscribe does"** — Module 01's split is the course's load-bearing rule: banning statements (FP course) becomes banning logic from `subscribe`, so every transformation is an operator expression denoting an Observable. The rest of the course is variations on it.
- **The "1% boundary" rule enforced in code** — demos are strict TypeScript, no `any`, framework-free, deterministic, self-terminating; `console.log` appears only in subscribe observers and labeled `tap` calls — the course practices the purity discipline it teaches.
- **Honest measurements, not assertions** — where an analogy has limits, the scripts say so: recursive `concat`/`defer` stream construction dies silently around **400 cells**; flat producers (`range`, `generate`) handle **millions**; the raw recursive `queueScheduler.schedule` trampoline handles **millions**. Measured on this machine, not claimed.
- **The Church-encoding twist (Module 05)** — the FP course built `pair = a => b => f => f(a)(b)`; the RxJS module's payoff is that the Observable itself is the Church encoding at architectural scale: a producer closure that yields its values only as calls to a consumer.
- **A list in time has no index (Module 06)** — `EMPTY` is Nil, `concat(of(head), tail$)` is Cons; every FP lesson survives the port and one gets sharper teeth.
- **The no-modulo FizzBuzz remix (Module 12)** — the capstone closes with a program no array-bound version can write: the fizz/buzz rules expressed as positions in repeating cycles zipped against the numbers, and a genuinely infinite FizzBuzz cut off by its consumer.

## Content

**Why this course exists.** The source course ([FP in JavaScript (NotebookLM)](./js-functional-programming-nlm.md)) kept issuing IOUs about RxJS — three explicit promises across Modules 3.5, 4.5, and 7.5. This repo is the redemption: rather than teaching RxJS from its API surface, it re-runs the twelve FP concepts a learner already owns and shows each one *becoming* an RxJS mechanism.

**The arc.** Modules 01–03 port the syntactic discipline: expression-orientation becomes the pipe/subscribe split; first-class functions become first-class Observables with producer closures re-invoked cold per subscriber; hand-curried data-last helpers (`f => xs => xs.map(f)`) become `map(fn)` itself — an operator factory returning a first-class `OperatorFunction`, with pipe proven to be nested application and the arity-1 constraint identified as the load-bearing wall of the whole API.

Modules 04–06 port the data structures: the tail-call wall (`sum(200000)` dying with a `RangeError`) is cured by relocating the loop into the producer where the stack cannot see it (`range` + `reduce` as the catamorphism, `generate` as accumulator-passing style, `expand` as genuine stream recursion); product types become `zip` with map-destructuring as projections; the cons list becomes `cons(head, tail$) = concat(of(head), tail$)` — a list in time.

Modules 07–09 port the semantics: the functor laws are verified empirically on live emissions and the course climbs the rung the list course could not reach — functions returning whole streams, flattened by `concatMap`/`mergeMap`; the thunk (`() => heavyCompute()`) becomes RxJS's default posture (cold = suspended computation); the FP course's falsiness-Maybe (with its confessed empty-string bug) is *fixed on screen* — absence as non-emission, `defaultIfEmpty` as `||` done right, triggered by emptiness of the stream instead of falsiness of a value, monoid algebra intact with `concat` as operation and `EMPTY` as identity.

Modules 10–12 port the discipline and close: referential transparency works on whole pipeline declarations (inert until subscribe — with `shareReplay` as the optimization license and `scan` as the `runST` loophole); "where does the loop live" is answered mechanically (producers iterate flatly, `queueScheduler` ships the hand-built trampoline as a library primitive) with exact measurements of which stack problems the cure solves and which it does not; and FizzBuzz collapses eleven modules of machinery into one expression — `range(1, 100).pipe(map(fizzbuzz)).subscribe(...)` — with the `(fizz(n) + buzz(n)) || n` monoid-and-fallback core preserved character for character.

**Format.** Each `Module NN/` holds `script.md` (deliberately mirroring the source course's bare-lines format so the two courses read side by side — 5 video segments with Objective / Visual Prompt / Script per segment, plus a 5-question quiz) and `demo.ts` (five sections corresponding 1:1 to the five segments). Run with `npm run module:NN`, `npm run all`, `npm run typecheck` (Node ≥ 24).

## Source

- GitHub: https://github.com/hansschenker/rxjs-from-fp-js-to-rxjs (own repo, built 2026-08-11)
- Local: `C:\Users\hanss\Web\Hans\rxjs-from-fp-js-to-rxjs` — README + all 12 `script.md` module intros read for this note

## Notes

- This is the graph's most-wanted node (10 broken links pointed here before it was written) — the bridge between the [Functional Programming](./functional-programming.md) and [RxJS](./rxjs.md) hubs.
- Direct feeder for the **rxjs-course** goal: Module 03 (operator factories) and 07 (functor laws) overlap the planned operator-reference; the honest-limits measurements (400-cell recursive cons death vs. millions via `generate`/trampoline) are ready-made "where the analogy breaks" content.
- The measurement-driven convention ("measured on this machine rather than asserted") is worth adopting course-wide — same spirit as the [22-axis fingerprint model](./rxjs-taxonomy.md)'s tension detector: claims must be checkable.

## Related

- [FP in JavaScript (NotebookLM course)](./js-functional-programming-nlm.md) — the source course whose twelve concepts this one rebuilds (not yet written)
- [Professor Frisby's Mostly Adequate Guide to Functional Programming](./fp-guide.md) — the classic book behind the FP concepts
- [From Options to Observables — a monadic journey](./from-option-to-observable.md) — the talk-sized version of the same journey, monad by monad
- [rxjs-fp — A Functional-Style RxJS Built From Scratch](./rxjs-fp.md) — the library-side companion: building functional RxJS rather than teaching it
- [Pipe vs Compose — Point-Free Composition in RxJS FP Architecture](./rxjs-pipe-compose.md) — deep dive on the composition mechanics Module 03 teaches

---

Part of: [RxJS](./rxjs.md) · [Functional Programming](./functional-programming.md)
