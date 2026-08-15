---
type: concept
title: RxJS Operator Combinators — Deriving the Operator Zoo
description: operators are unary functions, so Braithwaite's combinators apply verbatim — pipe is B, identity is I, and flattenWith derives the whole *Map family from one shape
tags: [rxjs, fp, combinators, operators, composition, library-design]
timestamp: 2026-08-15
---

# RxJS Operator Combinators — Deriving the Operator Zoo

## TL;DR

Braithwaite's combinator method transfers to RxJS without modification, because a pipeable operator already *is* the thing his combinators operate on: a unary function, `OperatorFunction<A, B> = (source: Observable<A>) => Observable<B>`. That makes the free-function `pipe()` the B combinator (it composes operators into operators, no source involved), `identity` the I combinator, and endo-operators a **monoid** under `pipe`/`identity`. The showpiece derivation: one combinator, `flattenWith`, manufactures the entire flattening family — `mergeMap`/`concatMap`/`switchMap`/`exhaustMap` collapse into *one shape × one policy argument*, which is the [22-axis taxonomy](./rxjs-taxonomy.md)'s "one-axis neighbors" and the [suffix grammar](./rxjs-operator-renaming.md)'s "keep the root, fix the suffix" executed in code. The one genuinely new constraint over plain-JS combinators: operator combinators must respect **subscription semantics**, and the fingerprint axes say exactly what each combinator preserves.

## Key Concepts

- **The type-level unlock** — `OperatorFunction<A, B>` is a unary function between observables; `MonoTypeOperatorFunction<T>` is an endomorphism. Everything in [JavaScript Combinators](./javascript-combinators.md) about unary functions applies one level up, verbatim.
- **`pipe` the free function is the composition combinator** — `pipe(op1, op2)` (no source!) returns a new operator. `const debouncedSearch = pipe(debounceTime(300), distinctUntilChanged(), switchMap(call))` is an operator built purely from operators — B/`compose` in reading order.
- **`identity` is the unit** — RxJS exports it precisely to be the do-nothing operator; `pipe()` with no arguments returns it.
- **Endo-operators form a monoid** — `pipe` is associative, `identity` is the two-sided unit: the operations-plus-laws pattern of [universal algebra](./universal-algebra.md), with the laws available as refactoring licenses (re-group pipelines freely).
- **Two combinator levels** — Level 1: combinators on *operators* (`pipe`, `identity`, `when`, `around`); Level 2: combinators on *operator factories* (curried data-last functions like `map`), where flip/partial application reshape configuration — `map: (f) => OperatorFunction` is itself Braithwaite's data-last design, as [Module 03 of the payoff course](./rxjs-from-fp-js-to-rxjs.md) teaches.
- **The `flattenWith` derivation** (the centerpiece):

  ```ts
  const flattenWith =
    <A, B>(flatten: OperatorFunction<Observable<B>, B>) =>
    (project: (a: A) => Observable<B>): OperatorFunction<A, B> =>
      pipe(map(project), flatten);

  const mergeMap_   = flattenWith(mergeAll());
  const concatMap_  = flattenWith(concatAll());
  const switchMap_  = flattenWith(switchAll());
  const exhaustMap_ = flattenWith(exhaustAll());
  ```

  `flattenWith` plays the role `leftApply` played in Braithwaite's talk: extract the repeated shape (`map` then flatten), and four "different" operators become one combinator applied to four concurrency policies.
- **A candidate basic set**:

  | Combinator | Shape | Analog |
  |---|---|---|
  | `identity` | `src => src` | I |
  | `pipe(...)` | operator composition | B / `compose` |
  | `flattenWith(policy)` | family-maker for `*Map` | `leftApply` |
  | `when(cond, op)` | `cond ? op : identity` | the `provided` decorator |
  | `liftInner(op)` | `map(inner$ => inner$.pipe(op))` | functor lift, one level up |
  | `around(before, after)` | `op => pipe(tap(before), op, tap(after))` | before/after/around advice |
  | `applyN(n, op)` | `pipe(...Array(n).fill(op))` | iterate/power |

- **`liftInner` has no plain-function ancestor** — it lifts an operator to act *inside* a higher-order observable: `window$.pipe(liftInner(take(3)), mergeAll())` = "apply this operator per burst." A combinator that only exists because streams nest.
- **Operator decorators** — the advice family from the [House deck](./javascript-combinators.md) lands directly: `withRetry = (n) => (op) => pipe(op, retry(n))`, guarded operators via `when`, logging via `around`. Decorators vary an operator; combinators compose them.
- **The RxJS-specific law: respect subscription semantics** — a combinator that subscribes to its source twice breaks cold/unicast assumptions ([heritage](./rxjs-heritage.md) territory). This is the interesting part, not a footnote: the [fingerprint axes](./rxjs-taxonomy.md) specify what each combinator *preserves* — composing lossless operators is lossless, `around` preserves every axis, `withRetry` changes resubscription semantics, `flattenWith` inherits its loss profile from its policy argument. Combinator laws + axis preservation would be a genuinely novel treatment of RxJS.

## Content

**Why this works at all.** Braithwaite's derivation machinery assumes nothing about its functions except that they are unary and composable. RxJS's pipeable-operator refactor (v5.5+) made every operator exactly that. The consequence is easy to miss because `.pipe()` the *method* dominates usage: the *free function* `pipe` is a combinator library's core export hiding in the standard library, and any pipeline fragment you can name is already a custom operator — no `Observable.lift`, no subclassing, just function composition.

**Derive, don't catalog.** The RxJS operator surface (~100 operators) reads as a zoo until the combinator lens factors it: the `*Map` family is `flattenWith` × four policies; the `*All` family supplies those policies; rate-limiters are one shape × a timing policy (the [taxonomy](./rxjs-taxonomy.md)'s finding that `throttle*`/`audit*`/`debounce*` differ on single axes); `pluck` was literally `map` ∘ property access until RxJS deprecated it in favor of writing the composition yourself. The teaching consequence mirrors [the Braithwaite note](./javascript-combinators.md): derive `flattenWith` once, and the operator families read as inevitable rather than memorized.

**What a spike would look like** — natural home: the [rxjs-fp](./rxjs-fp.md) repo (curried free operators, no prototype patching, tree-shakeable):

1. `combinators.ts` exporting the basic set above with strict types;
2. a demo deriving `switchMap` from `flattenWith(switchAll())` and asserting behavioral equivalence against the built-in on marble tests;
3. Vitest property checks for the monoid laws (`pipe(a, pipe(b, c))` ≡ `pipe(pipe(a, b), c)`, `pipe(identity, op)` ≡ `op` ≡ `pipe(op, identity)`);
4. an axis-preservation table per combinator, mechanically checkable against the fingerprint model.

**Course placement.** This is the bridge between [payoff-course Module 03](./rxjs-from-fp-js-to-rxjs.md) (`map(fn)` as partial application; the arity-1 constraint as the load-bearing wall — the very constraint that makes operators combinable) and the taxonomy's proposed "Module X" (the fingerprint model): a module that *derives* the operator zoo from ~7 combinators before fingerprinting it.

## Source

- Original synthesis (Claude Code session, 2026-08-15), building directly on Reginald Braithwaite's "JavaScript Combinators" derivation ([note](./javascript-combinators.md)) and the RxJS pipeable-operator API (`pipe`, `identity`, `OperatorFunction` — rxjs.dev). The `flattenWith` factorization mirrors the documented equivalence `mergeMap(f)` ≡ `map(f)` + `mergeAll()`.

## Notes

- **Spike landed 2026-08-15**: `src/operators/combinators.ts` in rxjs-fp implements the set (`identityOperator`, `when`, `flattenWith`, `liftInner`, `around`, `applyN`; `compose` already existed as the repo's B combinator), with an 11-test spec covering the monoid laws (associativity + both identity laws), `flattenWith` rebuilding `mergeMap` and `switchMap` (including cancellation parity under fake timers), and each combinator's behavior. Full suite 362 tests green.
- Open question worth its own exploration: is there a `liftInner`-style combinator for *time* (lifting an operator to act on windows/buffers uniformly), and does it relate to `windowTime` + `liftInner` + `mergeAll` the way `flattenWith` relates to the `*Map` family?

## Related

- [JavaScript Combinators — Deriving leftApply, rightApply, and Friends](./javascript-combinators.md) — the plain-function original this note lifts to operators
- [crocks Combinators — applyTo, composeB, converge, psi, substitution & friends](./fp-combinators.md) — the library-grade combinator catalog on the value level
- [RxJS Operator Taxonomy — The 22-Axis Fingerprint Model](./rxjs-taxonomy.md) — the axis space; combinators as axis-preserving maps
- [RxJS Operator Renaming — The Suffix Grammar](./rxjs-operator-renaming.md) — the naming layer `flattenWith` implements in code
- [rxjs-fp — A Functional-Style RxJS Built From Scratch](./rxjs-fp.md) — the implementation home for the spike
- [From FP-JS to RxJS — The RxJS Payoff Course](./rxjs-from-fp-js-to-rxjs.md) — Module 03's arity-1 constraint is what makes operators combinable

---

Part of: [RxJS](./rxjs.md) · [Functional Programming](./functional-programming.md)
