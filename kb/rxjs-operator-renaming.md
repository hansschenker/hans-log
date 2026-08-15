---
type: concept
title: RxJS Operator Renaming — The Suffix Grammar
description: "suffix grammar 'keep the root, fix the suffix': curried roots × boundary combinators (NotebookLM)"
resource: D:\Learning-Local-Hanss\Rxjs-Operator-Renaming
tags: [rxjs, operators, naming, dsl, functional, notebooklm]
timestamp: 2026-08-05
---

# RxJS Operator Renaming — The Suffix Grammar

*NotebookLM study set — two reports, a quiz, and flashcards synthesized from the
`Rxjs-Operator-Renaming` export dir, plus the working session log that produced the plan.
Companion artifacts (`RxJS_Operator_Renaming_Plan.mp4` video overview,
`RxJS_Reactive_Grammar.pptx`, and the quiz/flashcard `.pptx` decks) live alongside the markdown
but are not reproduced here.*

## TL;DR

RxJS operator names are *almost* a systematic grammar already — every family has a root plus
variants, and the second word carries the behavior. The plan makes that grammar total: **keep the
first word (the family root), rename only the second word**, drawing suffixes from a closed
vocabulary in which each suffix has exactly one meaning *and predicts the argument type*. The
implementation is a zero-runtime alias layer where roots are **curried functions** and suffixes
are **first-class boundary combinators** (`time`, `count`, `whileTrue`, `until`, `on`, `when`,
`toggle`), so `take(time(450))` dispatches to the official `takeUntil(timer(450))`. The payoff is
that the operator set stops being an *enumeration* and becomes a *generator*: root × boundary
produces coherent operators RxJS never shipped.

## Key Concepts

- **Core rule — "keep the root, fix the suffix."** Roots (`map`, `filter`, `take`, `buffer`,
  `window`, `throttle`…) are preserved as a **docs bridge**: the first word still finds the
  concept on rxjs.dev. Only the second word is normalized.
- **Suffix = type contract.** Reading the name tells you what argument the operator wants —
  a duration, a count, a predicate, a notifier, or a factory.
- **The closed suffix vocabulary:**

  | Suffix | Argument | Meaning |
  |---|---|---|
  | `time` | `ms` (number) | a fixed clock duration drives the boundary |
  | `count` | `n` (number) | a fixed number of values drives the boundary |
  | `whileTrue` | predicate | continue *as long as* the condition holds (`while` is a reserved JS keyword) |
  | `until` | `signal$` | a notifier ends it — **terminal, fires once** |
  | `on` | `signal$` | acts **each time** the notifier emits — repeating trigger |
  | `when` | factory | *you* create the boundary signal, per cycle or per value |
  | `toggle` | open/close | acts **between** explicit open and close signals |

  Plus `With` (join/extend), `Map`, `All` (flatten), `By` (key selector), `OnComplete`.
- **Roots × boundaries, not a name list.** Each root is a curried function that dispatches on the
  boundary's tag to the exact official operator. Two-word names are just **named partial
  applications**: `bufferOn = s$ => buffer(on(s$))`. Invalid pairings like `map(time(5))` are
  compile errors via overloads on the discriminated union.
- **Zero runtime cost.** The FP layer is construction sugar only — runtime semantics are always
  the official RxJS implementation.
- **The four flattening roots are sacred.** `concat` / `switch` / `merge` / `exhaust` are never
  renamed; they *are* the concurrency vocabulary (queue / latest-only / concurrent /
  ignore-while-busy).
- **The timing triad disambiguated** — `Time` = fixed clock, `When` = per-value factory,
  `On` = external repeating observable. This is what makes `debounceTime` / `debounceWhen` /
  `sampleOn` read uniformly.
- **Killing the "fake Until".** `distinctUntilChanged` → `distinctFromPrevious` (there is no
  notifier; it only compares against the immediately preceding value);
  `distinctUntilKeyChanged` → `distinctFromPreviousBy`.
- **Hidden completion made explicit.** Aggregates emit nothing until the source finishes, so
  they get `OnComplete`: `reduceOnComplete`, `countOnComplete`, `maxOnComplete`,
  `minOnComplete`, `toArrayOnComplete`, `takeLastOnComplete`.
- **The 8-policy story.** Every operator is documented across **Source, Trigger, Value,
  Cardinality, Time, Concurrency, Cancellation, Termination** — a structured replacement for
  one-sentence operator summaries.
- **Generated operators.** `take(time(ms))` (= `takeUntil(timer(ms))`), `skip(time(ms))`,
  `throttle(count(n))` (first of every block of n), `sample(count(n))` (last of every block of n)
  — semantically coherent cells nobody sat down to invent.

## Content

### 1. The problem: vocabulary soup

RxJS's learning curve is rarely about Observables themselves; the friction is *naming*.
Developers stall on the nuance between `bufferWhen` and `bufferToggle`, or `auditTime` and
`sampleTime`, and end up memorizing the library by trial and error. The names are close to
systematic — but the exceptions poison the pattern:

- **`When` means three different things** — `bufferWhen` (closing-signal factory),
  `delayWhen` (per-value selector), deprecated `retryWhen`.
- **`distinctUntilChanged` has an `Until` with no notifier** at all.
- **Aggregates like `reduce` hide** that they only emit on completion.

The fix is not to replace RxJS but to clarify it, via an **architectural alias layer**.

### 2. Anatomy: curried roots + boundary combinators

| Component | Role | Definition |
|---|---|---|
| **Family root** | the *what* | a curried function defining the core strategy (`take`, `buffer`), dispatching on the tag of the supplied suffix |
| **Boundary suffix** | the *how/when* | a first-class tagged value defining the trigger, limit, or condition |

Writing `take(time(5000))` means the `take` root observes the `time` tag and delegates to the
underlying official implementation. The grammar stays flexible; execution stays identical to the
standard.

```ts
reading$.pipe(take(count(3)))                            // first three: 18 19 20
reading$.pipe(take(whileTrue((v: number) => v < 22)))    // below threshold: 18-21
reading$.pipe(take(until(stop$)))                        // until stop: 18-22
reading$.pipe(take(time(450)))                           // first 450ms — no official takeTime

reading$.pipe(skip(count(7)))                            // 25 26 27
reading$.pipe(skip(whileTrue((v: number) => v < 25)))    // once hot: 25-27
reading$.pipe(skip(until(calibrated$)))                  // after calibration: 21-27
reading$.pipe(skip(time(450)))                           // after 450ms: 22-27
```

### 3. The rename list (surgical — everything else stays official)

Pipeable, flattening, and aggregate operators all keep their first word.

| Official | Vocabulary name | Why |
|---|---|---|
| `debounce` | `debounceWhen` | factory-driven; family now reads `xxxTime` / `xxxWhen` / `xxxOn` uniformly |
| `throttle` | `throttleWhen` | same |
| `audit` | `auditWhen` | same |
| `sample` | `sampleOn` | external repeating trigger |
| `buffer` | `bufferOn` | `on` (repeating) explicitly distinguished from `until` (terminal) |
| `window` | `windowOn` | same |
| `distinctUntilChanged` | `distinctFromPrevious` | removes the `Until` violation |
| `distinctUntilKeyChanged` | `distinctFromPreviousBy` | `By` signals the key selector |
| `ignoreElements` | `ignoreValues` | plain English over jargon |
| `reduce` / `count` / `max` / `min` / `toArray` / `takeLast` | `…OnComplete` | names that hide completion behavior get `OnComplete` |
| `forkJoin` | `whenAllReady` | opaque technical term → descriptive completion-join |
| `shareReplay({bufferSize:1, refCount:true})` | `shareLatest()` | configured wrapper pinning a memory-safe default |

**Deliberately kept:** bare `take(3)` / `skip(2)` (a numeric argument is self-evident — no
`takeCount` pedantry; it's an implicit `count` boundary), and `delay` as-is since `delayWhen`
already disambiguates it. **Excluded entirely:** deprecated operators — `retryWhen` (use
`retry({delay})`), `mapTo`, `pluck` (use `map` with property access), `publish*`, `*MapTo`,
`timeoutWith`, `toPromise` (use `firstValueFrom` / `lastValueFrom`). Scheduler operators like
`observeOn` are **not** renamed: their `On` refers to a scheduler, not a signal, so they sit
outside the grammar.

### 4. Why this is the FP move

The deep property: this isn't a list of operators, it's **a closed set of primitives plus a
composition rule**, with the operator list falling out as the product. The original RxJS API is
an *enumeration* — someone had to think of `bufferToggle` and ship it. The grammar is a
*generator*: roots × boundaries, where the official API is just the cells someone already named.

What makes it open-ended is that the matrix still has **unfilled but semantically coherent
cells**. Nobody invented `throttleCount` — but once `throttle` means *emit then suppress during a
window* and `count(n)` means *a fixed number of values is the window*, the combination already
has exactly one sensible meaning. The grammar did the design work. Same effect as any good
algebra — monoids, parser combinators, lenses: start with the smallest lawfully-composing pieces
and the library writes itself outward.

This is also why *keep the first name* beat full renames like `keepLatest`: full renames produce
a **bigger enumeration**; roots-plus-boundaries produce a **smaller generator**. Fewer things to
learn, more things expressible.

Currently `throttle(count(3))` is deliberately a compile error — only combinations with
unambiguous semantics are enabled. Extending the dispatch in `roots.ts` cell by cell is exactly
the kind of change the architecture makes cheap.

### 5. Implementation status

- **Package**: one `catalog.ts` as the single source of truth, from which operator modules,
  migration tables, and docs derive. Pure re-exports where names are unchanged; partial
  applications for new names; `boundaries.ts` / `roots.ts` as the core.
- **Tests**: Vitest identity + marble + type-level tests, plus a **collision test against real
  rxjs exports** (avoiding the "mergeAll lesson" — aliases must never shadow official exports).
  35 tests passing.
- **Samples**: `samples/take-skip.ts` and `samples/buffer.ts` cover both flavors of the algebra
  (take/skip's four boundaries, buffer's five, including both generated time operators). Output
  is fully deterministic; the demo dogfoods the vocabulary in its own plumbing
  (`interval(100).pipe(take(count(10)))`).
- **Docs**: `src/docs.ts` renders 14 pages + the sidebar JSON from the catalog;
  `npm run generate:docs` writes into `~/rxjs-vitepress-ds` following the site's Atlas pattern.
- **In rxjs-vitepress-ds**: a `vocabulary/` section — overview page with the suffix-grammar and
  flattening-strategy tables, 12 family pages, and an Excluded page with replacements. Each
  operator renders as an `ROperatorCard` with its dispatch example and full 8-policy story table.
  `config.mts` imports `vocabulary-sidebar.json` and adds a Vocabulary nav entry. Build passes.
  ⚠️ **These rxjs-vitepress-ds changes are still uncommitted** in that repo.

## Quiz

1. Why was `distinctUntilChanged` renamed to `distinctFromPrevious`? → `Until` is reserved for
   terminal boundaries that fire once, which doesn't match repeating value comparison
2. Concurrency policy of `exhaust`? → Ignores new work while an inner is active; values arriving
   in that window are dropped
3. `Trigger` policy of the `audit` family? → The first value opens a window; emission occurs when
   the boundary signal fires or the duration elapses
4. Why `forkJoin` → `whenAllReady`? → The official name is opaque and doesn't describe waiting
   for completion
5. Which operator does the vocabulary generate that RxJS never shipped? → `take(time(ms))`
6. `Cancellation` policy of `delay`? → Unsubscribing cancels all currently scheduled future
   emissions
7. `on` vs `when`? → `on` takes an existing notifier Observable; `when` takes a factory that
   creates a new signal per cycle
8. `Cardinality` of the `sample` family? → Many source values become at most one value per
   sampling tick
9. `take(whileTrue(p))` when `p` first returns false? → The source is cancelled immediately
10. `shareLatest` wraps what? → `shareReplay({ bufferSize: 1, refCount: true })`
11. Which strategy is "queue in order — one inner at a time, new work waits"? → `concat`
12. `Time` policy of `takeLastOnComplete`? → Output happens only upon source completion
13. Suffix for joining/extending the source (e.g. `withLatestFrom`)? → `With`
14. Why `whileTrue` and not `while`? → `while` is a reserved keyword in JavaScript/TypeScript
15. `Concurrency` policy for `toggle` boundaries in buffer/window? → Multiple collections or
    windows may be open at the same time
16. `Trigger` policy of `debounce`? → A value's silence period ends without a newer value arriving
17. `Termination` of `delay` on source error? → Errors are forwarded immediately, bypassing
    scheduled delays
18. Why do aggregates get `OnComplete`? → To explicitly declare they produce no output until the
    source completes
19. "Emits a value, then suppresses until the signal you created for it fires"? → `throttleWhen`
20. Result of `sample(count(3))`? → Emits the last value of every block of 3 source values
21. "All next values dropped; only error and complete forwarded"? → `ignoreValues`
22. `scan` vs `reduceOnComplete` cardinality? → `scan` emits one output per source value;
    `reduceOnComplete` emits one total output
23. `debounceTime` when the source completes mid-silence? → The pending value is emitted
    immediately before completion
24. `Value` policy of `distinctFromPreviousBy`? → Values kept only when the *selected key*
    changed vs. the previous emission
25. "A source next is accepted only when no inner is active; otherwise ignored"? → `exhaustMap`
26. `take(until(stop$))` resolves to? → `takeUntil(stop$)`
27. `Concurrency` of `switchMap`? → Only the latest inner is active; previous subscriptions are
    cancelled

## Flashcards

**Grammar**
- Core principle? → Keep the first word (family root), rename only the second word (suffix)
- `time` / `count` → a fixed clock duration / a fixed number of values drives the boundary
- `whileTrue` → continue as long as a predicate holds (`while` is reserved in JS)
- `until` vs `on` → `until` is terminal and fires once; `on` is a repeating trigger
- `when` → a user-supplied factory creates the boundary signal per cycle or per value
- `toggle` → acts between explicit open and close signals
- `With` / `All` / `By` → join-or-extend / flatten a higher-order Observable by the root strategy /
  compare-or-group by a selected key
- Curried root? → A function taking a boundary combinator and dispatching to an official operator
- Bare root + number (`take(3)`)? → An implicit `count` boundary
- Why isn't `observeOn` renamed? → Its `On` refers to a *scheduler*, not a signal — outside the grammar

**Alias map**
- `distinctFromPrevious` → `distinctUntilChanged`; `distinctFromPreviousBy` → `distinctUntilKeyChanged`
- `ignoreValues` → `ignoreElements`; `whenAllReady` → `forkJoin`
- `reduceOnComplete` → `reduce`; `toArrayOnComplete` → `toArray`; `takeLastOnComplete` → `takeLast`
- `bufferOn` → partial application of `buffer`; `windowOn` → `window` with `on(signal$)`
- `sampleOn` → `sample`; `debounceWhen` → `debounce`; `throttleWhen` → `throttle`; `auditWhen` → `audit`
- `shareLatest` → pins `shareReplay({ bufferSize: 1, refCount: true })`
- Replacements: `pluck` → `map` + property access; `toPromise` → `firstValueFrom`/`lastValueFrom`;
  `retryWhen` → `retry({ delay })`

**Sacred strategies**
- The four? → `concat`, `switch`, `merge`, `exhaust`
- `concat` → queue in order, one inner at a time, new work waits
- `switch` → keep latest; a new source value cancels the previous inner
- `merge` → run concurrently; inners may overlap
- `exhaust` → ignore while busy; new source values dropped until the active inner completes

**8-policy framework**
- `Trigger` → the condition closing a collection cycle, suppression window, or timing period
- `Cardinality` → the relationship between number of source values and number of results
- `take(time(5000))` → keeps values for the duration, then completes
- `skip(time(ms))` → drops values for a duration, then forwards everything
- `throttle(count(3))` / `sample(count(3))` → first / last value of every block of 3
- `takeLastOnComplete` trigger, `last` trigger, `endWith` trigger → source completion
- `first` cancellation → source cancelled immediately after the first match
- `single` on a second match → errors immediately and cancels the source
- `find` vs `findIndex` → emits the value itself vs. the numeric index
- `startWith` time → initial values emit synchronously on subscription, then source timing takes over
- `withLatestFrom` trigger → only the primary source emitting produces output
- `delay` time / `delayWhen` cancellation → fixed forward shift / unsubscribing cancels all pending
- `timeout` trigger → a deadline fires before the required emission occurs
- `map` / `scan` / `pairwise` cardinality → 1:1 / one output per source value (running accumulator) /
  two adjacent values → one `[previous, current]` pair
- `groupBy` concurrency → many grouped observables active at once
- `mergeScan` vs `switchScan` → async updates may overlap vs. only the latest survives
- `expand` value → mapped to an Observable whose values are recursively fed back into the projection
- `catchError` trigger / `retry` time → a source error activates recovery / immediate or configured delay
- `tap` cardinality → one input notification produces exactly one output notification
- `finalize` trigger → the stream ends via completion, error, or unsubscription
- `share` trigger → the first subscriber starts the shared subscription
- `bufferToggle` value / `bufferWhen` flush → values between an open and its close collected into
  arrays / when a signal from the closing-signal factory emits
- `windowCount` concurrency → windows may overlap if a start interval is configured
- `debounceTime` / `throttleTime` / `auditTime` / `sampleTime` → fixed silence passes /
  values in the suppression window are dropped, not buffered / latest value in the window emitted
  at its close / a periodic timer tick
- `distinct` source → each value flows with memory of *all* previously seen values
- `elementAt` termination → completes after the indexed value, or errors if the index is never reached

## Source

- **Local exports dir:** `D:/Learning-Local-Hanss/Rxjs-Operator-Renaming/`
- **Markdown files used:** `RxJS Reimagined_ How a _Suffix Grammar_ Makes Reactive Programming
  Click.md`, `The Suffix Logic Manual_ Decoding the Language of Operators.md`, `RxJS-Quiz.md`,
  `RxJS-Flashcards.md`, `rxjs-operator-renaming.txt` (working session log)
- **Companion artifacts (not reproduced):** `RxJS_Operator_Renaming_Plan.mp4` (video overview),
  `RxJS_Reactive_Grammar.pptx`, `RxJS-Quiz.pptx`, `RxJS-Flashcards.pptx`
- **Repo:** https://github.com/hansschenker/rxjs-operator-renaming

## Notes

- The strongest idea here isn't any single rename — it's the shift from **enumeration to
  generator**. Once suffixes are values rather than name fragments, the API surface becomes
  `roots × boundaries`, and the official operator list is revealed as an arbitrary subset of a
  regular grid. That reframing is worth more than the alias layer itself.
- `OnComplete` on aggregates is the rename with the highest teaching value. "Why does my `reduce`
  never fire?" on an infinite stream is a classic beginner wall, and the name now answers it.
- Deliberately *not* renaming `take(3)` shows good taste: the grammar is applied where it removes
  ambiguity, not everywhere it could be applied mechanically.
- The docs bridge constraint (keep the root so rxjs.dev still works) is what makes this teachable
  rather than a fork of the vocabulary. It's the same reason the four flattening roots are frozen.
- Open thread: the empty matrix cells (`throttle(count(n))`, `sample(count(n))`) are compile
  errors today. Worth deciding which deserve to exist while working through the course material.
- **Loose end:** the generated `vocabulary/` section in `rxjs-vitepress-ds` is still uncommitted
  in that repo.

## Related

- [A Formal Taxonomy of RxJS Observables](./rxjs-observable-taxonomy.md) — the semantics layer this grammar names; cold/hot ⟂ unicast/multicast
- [I switched a map and you'll never guess what happened next - Pete Darwin, Shai Reznik, Mike Brocchi](./rxjs-switchmap-deep-dive.md) — the `switch` strategy's cancellation policy in practice
- [#74 Subjects in RxJS  | Understanding Observables & RxJS | A Complete Angular Course](./rxjs-74-subjects.md) — multicasting, the machinery behind `shareLatest`
- [RxJS Heritage — from LINQ and Rx.NET](./rxjs-heritage.md) — where the operator names came from in the first place

---

Part of: [RxJS](./rxjs.md)
