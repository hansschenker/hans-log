---
type: reference
title: rxjs-fp — A Functional-Style RxJS Built From Scratch
description: "from-scratch functional RxJS: cold core, curried free operators, no prototype patching"
resource: https://github.com/hansschenker/rxjs-fp
tags: [rxjs, fp, operators, library-design, tree-shaking, agentic]
timestamp: 2026-08-05
---

# rxjs-fp — A Functional-Style RxJS Built From Scratch

*Synthesized from the working session log in the `Rxjs-Fp` export dir (Claude + Codex
transcript), not from NotebookLM. The project itself lives at `~/Web/Hans/rxjs-fp` →
`hansschenker/rxjs-fp` (private, Apache-2.0, never published to npm).*

## TL;DR

A from-scratch reimplementation of RxJS in functional style — **not** a wrapper over the official
library. Three commitments drive every decision: a **classic cold Observable core** (no platform
Observable), **no prototype patching** (free curried functions + `pipe`/`compose`), and **one
operator per behavior** (every config key becomes its own function). The result is 149 exports
and 351 tests where importing a single operator costs **1,453 B against 31,164 B** for the whole
library. All three real bugs found during the build were **lifecycle** bugs, not operator logic —
and the most valuable artifact is the honest pros/cons ledger, which names what the free-function
style actually costs: dot-completion, call-site ergonomics, and a multiplied API surface.

## Key Concepts

- **Cold classic core.** `Observable` + `Subscriber`/`Subscription` with **LIFO teardown**, free
  `pipe`/`compose`, and a shared `operate` helper that every operator is built on. Choosing the
  classic cold core over the platform Observable cut the dependency on the WPT conformance suite
  — which means lifecycle correctness is owned entirely by hand-written tests.
- **No prototype patching + `sideEffects: false`.** Free functions, so bundlers can drop what
  isn't imported. Measured, not estimated: `pipe, of, map` → **1,453 B**; all 149 exports →
  **31,164 B** (4.6%). The single-operator cost barely moved as the surface grew from 29 to 149.
- **One operator per behavior.** Config keys became distinct functions rather than option bags:
  `bufferCount(size, startEvery?)`, `mergeMapConcurrent(fn, n)`, `takeWhileInclusive`,
  `retry`/`retryDelay`, `timeout`/`timeoutWith`, `timer`/`interval`, `distinctBounded`/
  `distinctReset`, and `first()`/`last()` with **no predicate parameter** — you compose `filter`
  in front instead. `buffer` alone became five operators.
- **No alias splits.** Where a split would have produced only an alias, it wasn't added:
  `auditTime` already *is* trailing `throttleTime`, so there is no `throttleTrailing`.
- **`operate` is the leverage point.** Once it existed, `map`/`filter`/`scan`/`skip`/`takeWhile`
  are four or five lines each, and try/catch-to-stream-error comes for free. Fixing one bug in
  `operate` fixed five operators at once.
- **The early-linking rule** — the one genuinely subtle thing in the codebase: an operator must
  create and link its upstream `Subscriber` *before* subscribing, which is why
  `Observable.subscribe` accepts an existing `Subscriber`.
- **Collection abstraction.** `collectByCount` / `collectByTime` / `collectBySelector` /
  `collectByToggle` drive ten buffer/window operators over one `Collection` interface —
  `next` / `close` / `discard` / `fail`.
- **Composition replaces parameters.** Fewer argument combinations to implement, document, and
  test; pure callbacks (predicates, mappers, comparators, reducers) are testable outside streams.
- **Partial application → domain vocabulary.** `compose(onlySubmitted, prepare, atMost(4, saveOne))`
  is itself an operator, applicable to any compatible source. RxJS code stops being anonymous
  plumbing and becomes a small vocabulary of reusable transformations.
- **Naming rule: never repeat the context.** Inside a domain module the context is given —
  `onlySubmitted()`, not `onlySubmittedOrders()`. The `X` is the *rule the step enforces*, never
  the domain noun.
- **`pipe` vs `compose`.** `pipe(source$, op1, op2)` runs a pipeline on a source;
  `compose(op1, op2)` builds a new reusable operator. `compose` does not replace `pipe`.

## Content

### 1. What exists

Six planned phases became thirteen. The final surface:

| Layer | Contents |
|---|---|
| **Core** | cold `Observable`, `Subscriber`/`Subscription` (LIFO teardown), free `pipe`/`compose`, `operate`, `EmptyError`, `TimeoutError` |
| **Creation (9)** | `of`, `from`, `defer`, `timer`, `interval`, `fromEvent`, `throwError`, `EMPTY`, `NEVER` |
| **Combination** | `merge`, `concat`, `combineLatest`, `zip` (tuple types preserved) |
| **Operators (~100+)** | transform, higher-order, filter, error/effect, timing, buffer/window, multicasting |
| **Interop** | promise bridges, async-iteration helpers incl. `bufferedValuesFrom` |

149 exports, 351 tests across 22 files, 17+ commits, CI green on five gates: prettier, eslint,
`tsc --noEmit`, vitest, build.

### 2. The three real bugs — all lifecycle

**① Early linking.** `operate` registered the upstream subscription only *after*
`source.subscribe()` returned, so during a synchronous emission an operator had no handle to
close upstream. `take(2)` over a synchronous source let the producer run to completion — the
`subscriber.closed` guards in `of`/`from` had **never worked**. The fix: create the upstream
`Subscriber` first, link it to the downstream teardown, *then* subscribe.

The same flaw sat in `mergeMap`/`switchMap`/`exhaustMap`/`takeUntil` for their inner sources, and
the symptom had already been visible — this dance, shipped as "the price of synchronous inners":

```ts
let subscription: Subscription | undefined;
let done = false;
const finish = () => { done = true; if (subscription) inners.delete(subscription); };
subscription = inner.subscribe({ complete: finish });
if (!done) inners.add(subscription);
```

Creating the Subscriber first deleted the whole thing:

```ts
const innerSubscriber = new Subscriber<R>({ complete: () => inners.delete(innerSubscriber) });
inners.add(innerSubscriber);
inner.subscribe(innerSubscriber);
```

**The lesson worth keeping:** awkward code in three separate operators was evidence about the
*core*, not about the operators. The fix removed code rather than adding it — and the test that
caught it was the kind you skip as "obviously fine."

**② `ConnectableObservable` reset.** It reset when the source terminated but not when its
connection was unsubscribed, so a ref-counted `share` reattached to a spent Subject and could
never restart. Two failing tests, one root cause — surfaced only because the test asserted
"restarts after every subscriber leaves" rather than just "shares."

A third failure in the same batch was the *test* being wrong: `share()` over a synchronous source
**does** restart per subscriber, because the ref count hits zero before the second subscriber
arrives. Split into two tests asserting both facts, so the surprising one is pinned rather than
hidden.

**③ `expandConcurrent` stack growth.** Projecting from inside the inner subscriber's `next`
handler nested ~6 frames per recursion level; 50,000 levels blew the stack. Fixed with a
trampoline — values queued, projected by one FIFO drain loop, so depth is constant regardless of
recursion depth. Verified non-vacuous by stashing the fix and confirming the test fails. One
semantic change named rather than left implicit: projection order is now **FIFO (breadth-first)**
rather than depth-first — the same trade upstream RxJS Next made, for the same reason.

**Later, an external review pass** (Codex) found two more error-channel leaks and a scalability
bug: `bufferToggle`/`windowToggle` closing selectors and `sequenceEqual` comparators threw
*outside* the stream contract (escaping via `reportUnhandledError` instead of
`subscriber.error()`), and synchronous `retry`/`repeat` resubscribed recursively — `retry(100000)`
stopped at ~1,745 attempts and delivered **neither** error nor completion. All fixed with guards
and a resubscription trampoline; 298 tests at that point.

### 3. Killing the buffer/window duplication

The concrete motivator: a `windowCount` cleanup landed and had **no way to reach `bufferCount`**,
which still carried the same shape. `bufferCount` and `windowCount` implemented the same
`count % startEvery` arithmetic twice; `buffer`/`bufferWhen`/`window`/`windowWhen` shared notifier
logic across four files.

The fix was four shared drivers over a `Collection` interface, making each of the ten operators
one line:

```ts
export function bufferCount<T>(size: number, startEvery: number = size): OperatorFunction<T, T[]> {
  return collectByCount(size, startEvery, bufferCollector<T>());
}
```

**The interesting part** — buffers and windows must differ in *exactly one place*, and it wasn't
where expected. `next` + `close` isn't enough; the interface also needs `discard()`. **A window is
published when it opens; a buffer when it closes.** That asymmetry is inherent (a window has to
exist before it can receive anything) and only surfaces on an empty source — upstream RxJS has it
too: `bufferCount` on empty emits nothing, `windowCount` on empty emits one empty window. So
`close()` means *a boundary was reached, emit*, and `discard()` means *released without reaching
one* — for a buffer, drop; for a window, still complete the published Subject. `fail()` is the
third member: a window forwards the error into its Subject, a buffer just drops its values.

Cost: 611 lines across ten files → 529 across ten plus two shared. The line saving is modest; the
structural one isn't — the drift can't happen again. Bundle impact nil.

### 4. The pros/cons ledger

**What it buys**

- Composition replaces parameters — `first()` takes no predicate because `filter` exists.
- One helper centralized the hard part; lifecycle correctness lives in one file rather than
  smeared across ninety.
- Tree-shaking and import-order guarantees that are real and measurable.
- Honest signatures that compound as a codebase ages.

**What it costs**

- **Call-site ergonomics are worse.** `pipe(source, map(f), filter(p))` puts the source inside
  the parens; `source.pipe(…)` reads better and method chaining better still. This showed up
  concretely — Prettier reformatted dozens of test call sites into multi-line blocks that would
  have been one line with a method.
- **You lose dot-completion.** With prototype methods, typing `source.` lists everything. With
  free functions you must already know the name to import it — a real discoverability loss over a
  149-export surface, falling hardest on newcomers, *exactly the people a config object was
  arguably protecting*.
- **The split multiplied the surface** — 149 exports against upstream's ~97. Every split trades
  "read the options" for "know the operator exists."
- **It duplicated implementations** (the con weighted heaviest, and the one later fixed).
- **The type system fights the shape at the edges** — `zipWith`/`combineLatestWith` prepend the
  source to a tuple of inputs, which is sound but not expressible; both needed erasing casts, and
  the tests passed while typecheck failed. `pipe`'s overload ladder stops at nine operators.
- **Not migratable.** Every call site changes shape and some semantics moved (`repeat` counts
  differently, `scan`/`reduce` require seeds). A codemod could do the syntax but not the semantics.

**Where it lands:** decisively worth it for libraries and bundle-sensitive apps; least worth it
for exploratory work and teams with RxJS muscle memory.

### 5. The samples layer

Five domains, each demoed live end-to-end: **orders** (invoice batch with per-item recovery),
**search autocomplete** (7 keystrokes → exactly 2 searches), **upload queue** (retry then reject
without killing the queue), **Angular form autosave** (saving → failed → saved), **websocket
ticker** (3 connections, 2 failure modes, direction history surviving reconnects).

Then a two-tier extraction into `samples/shared-operators.ts` — the distinction that matters:

- **Tier 1, shared *logic*** — `recoverFailure(toFallback)` owned the
  `error instanceof Error ? error.message : String(error)` normalization duplicated ~8 times;
  `failAfterSilence(ms)` / `retryAfter(attempts, delayMs)`; `until(stop$)`.
- **Tier 2, shared *vocabulary* only** — `waitFor` (debounce), `onlyChanged` (distinct),
  `latest` (switch), `atMost` (bounded concurrency). No logic of their own; extraction buys
  consistency, not deduplication.
- **Stays per-domain** — the `onlyX` predicate filters, `mapXToY` projections, and the verb+`One`
  journeys (`searchOne`, `autosaveOne`, `uploadOneFileResiliently`). Their entire value is the
  domain predicate behind a business name; a generic `only(predicate)` is just `filter` again.

That turns the teaching story into three layers: RxJS primitive → shared policy vocabulary →
domain binding.

### 6. LINQ ↔ RxJS category mapping

*(from `LINQ categories.txt` in the same dir)*

- **LINQ categories:** filtering, projection, aggregation, generation, concatenation,
  partitioning, grouping, joining, set operations, quantifiers, conversion, sorting.
- **RxJS categories:** creation, transformation, filtering, combination, flattening/higher-order
  mapping, reduction/aggregation, multicasting/sharing, error handling, time/scheduling, utility.
- **Direct maps:** filtering, projection, aggregation, generation, concatenation, partitioning
  (`Where`↔`filter`, `Select`↔`map`, `SelectMany`↔`mergeMap`/`switchMap`, `Take`↔`take`,
  `Skip`↔`skip`, `Count`↔`count`, `Reduce`↔`reduce`).
- **Partial maps:** grouping, joining, set operations, quantifiers, conversion.
- **No natural counterpart:** sorting (done via collection operators in RxJS). Conversely RxJS
  *adds* time control, flattening policies, multicasting, scheduling, cancellation, and error
  recovery — the categories that exist only because values arrive over time.

### 7. Reading order

141 files, but the design is concentrated in six:

1. `src/core/observable.ts` + `subscriber.ts` — the cold contract, ~150 lines. Everything follows.
2. `src/core/operate.ts` — the helper every operator uses; its comment explains the early-linking rule.
3. `src/operators/map.ts` — the smallest complete operator; the shape all others follow.
4. `src/operators/merge-map-concurrent.ts` — the hardest: inner tracking, queueing, teardown.
5. `src/operators/internal/collection.ts` — the buffer/window factoring.
6. `src/subject/subject.ts` — the only hot thing, and the `super()` workaround.

The spec files sit next to their sources; `core/observable.spec.ts` states the cold semantics as
executable claims. `git log --reverse` reads as a build log — each message explains *why*,
including the three bugs.

### 8. Self-identified gaps

1. **Composition-law / property-based tests** — the highest-value gap by a distance. A functional
   design should be easiest to test here, and nothing was written.
2. **Coverage in CI** — 291+ tests with no idea what fraction of branches they touch; the
   `fail()`/`discard()` branches in the boundary drivers are likely unexercised.
3. **A bundle-size budget** — the headline claim was measured by hand, twice. Nothing stops it
   regressing; one accidental import from `index.ts` into a leaf would silently couple everything.
4. **Type-level tests** — the `as never` erasing casts are exactly where a type regression passes
   every runtime test. `expectTypeof` would pin them.
5. **Consumer-reality fixtures** — nobody has installed the packed tarball into a clean directory.
   That's how "builds fine, unusable when published" happens.

Plus two judgment calls left open: no `mergeAll`/`concatAll`/`switchAll` (upstream RxJS Next
dropped them too, but `mergeMap((inner) => inner)` reads poorly), and whether `Subscriber` /
`operate` are supported API or escape hatches.

### 9. On working with a long-running agent

Phases 7–13 came from one sentence — "do the rest of the 118 operators the same way, keep the
same code quality" — producing ~90 operators, seven commits and ~160 tests without further input.
Consistency held across ~150 exports because it was one continuous context rather than sessions
resumed cold, and cross-cutting fixes propagated correctly (the early-linking bug found in `take`
was recognized in four other operators).

**What autonomy did not buy:** judgment about what to build, or the standard to hold it to. The
first twenty minutes were spent planning against the wrong repository; three corrections
redirected the entire project. The recommendation was to build on the platform Observable — the
classic cold core was Hans's override, and it shaped every operator that followed. And the quality
ratchet was almost entirely his: `windowCount`'s parallel arrays, `expand`'s stack growth, the
bounded `distinct`, the buffer/window duplication — all four were flagged as rough edges and
shipped anyway, and became good only on "fix that."

**What running unsupervised cost:** a lint failure reached a commit (the verification chain piped
through `tail`, swallowing the exit code); a README was corrupted by a cp1252 write, caught only
because `prettier --check` happened to fail; an incoherent test landed in `interop.spec.ts`; and
code already judged mediocre got shipped with an honest caveat attached.

> The four "fix that" turns produced more quality improvement than the seven autonomous phases
> did, and the seven autonomous phases produced more code than the four reviews ever could.

The lesson stated at the end: **flagging a weakness is not the same as fixing it.** Five were
flagged; all five turned out cheap to fix and worth fixing. "Honest about a known flaw" felt like
diligence; it was mostly a way of not doing the work.

## Source

- **Local dir:** `D:/Learning-Local-Hanss/Rxjs-Fp/`
- **Files used:** `rxjs-fp.txt` (1302-line Claude + Codex session log), `LINQ categories.txt`
- **Repo:** https://github.com/hansschenker/rxjs-fp — private, Apache-2.0, `private: true`
  guard set, never published to npm (the name is unclaimed there)
- **Working copy:** `~/Web/Hans/rxjs-fp`

## Notes

- This and [RxJS Operator Renaming — The Suffix Grammar](./rxjs-operator-renaming.md) are **the same thesis approached from opposite ends**. Both
  reject option bags for one-operator-per-behavior and make the name carry the contract. But
  renaming keeps official RxJS underneath as a zero-runtime alias layer and *shrinks* the surface
  into a root × boundary **generator**; rxjs-fp reimplements from scratch and *grows* it to 149
  exports by splitting every config key — then runs straight into the duplication a generator
  avoids by construction.
- More striking: rxjs-fp **independently rediscovered the boundary abstraction**.
  `collectByCount` / `collectByTime` / `collectBySelector` / `collectByToggle` *is* the suffix
  grammar's `count` / `time` / `when` / `toggle` — arrived at as a deduplication refactor rather
  than as a naming scheme. Same insight, found twice, under different pressure. That convergence
  is the best evidence either project has that the abstraction is real, and it suggests the
  natural next move: give rxjs-fp the boundary values as its *public* API, not just its internals.
- The `discard()` discovery (window publishes on open, buffer on close) is the sharpest single
  insight in the log — a genuine asymmetry that only an empty-source test can surface, and one
  upstream RxJS carries without ever naming.
- The pros/cons ledger is worth rereading before adopting free-function style anywhere else. The
  dot-completion loss is the argument that's hardest to answer, and it's the one most often waved
  away.
- Reading `git log --reverse` as a build narrative is a good habit to keep for the other projects.

## Related

- [RxJS Operator Renaming — The Suffix Grammar](./rxjs-operator-renaming.md) — the same design thesis as an alias layer over official RxJS
- [A Formal Taxonomy of RxJS Observables](./rxjs-observable-taxonomy.md) — the cold/hot ⟂ unicast/multicast semantics this core implements
- [#74 Subjects in RxJS  | Understanding Observables & RxJS | A Complete Angular Course](./rxjs-74-subjects.md) — Subject and multicasting, the only hot thing in the library
- [I switched a map and you'll never guess what happened next - Pete Darwin, Shai Reznik, Mike Brocchi](./rxjs-switchmap-deep-dive.md) — inner-subscription cancellation, where the early-linking bug lived

---

Part of: [RxJS](./rxjs.md) · [Functional Programming](./functional-programming.md) · [AI Engineering](./ai-engineering.md)
