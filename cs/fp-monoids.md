---
slug: fp-monoids
title: crocks Monoids — Prod, and the shared empty/concat interface
date: 2026-08-13
tags: [cs, fp, javascript, monoids, crocks, algebra]
source: cs
---

## TL;DR

crocks defines a monoid as *any ADT providing both `empty` and `concat`* — that's the whole
contract, and `Prod` is the smallest instance of it: wrap a number, `concat` multiplies, `empty` is
`1`. The library ships ten of them over booleans, objects, functions, `Maybe` and numbers, all
behind the same three instance functions, which is what lets one set of helpers (`mconcat`,
`mreduce`, and their `Map` variants) fold *any* list of values by simply naming which monoid to
use.

## Key Concepts

- **The contract is two functions.** A monoid is "a means to represent a binary operation, usually
  locked down to a specific type"; crocks treats any ADT with `empty` and `concat` as one. All
  monoids expose `empty` on the *constructor*, plus instance `valueOf`, `empty`, `concat`.
- **`empty` is the identity, not "nothing".** Concatenating `empty` to any value returns that other
  value — which is why `Prod.empty()` is `1` and not `0`. Getting this wrong silently annihilates
  the fold.
- **The operation must be associative** — `(a·b)·c = a·(b·c)` — which is what makes folding a list
  order-independent and, in principle, parallelisable.
- **`Prod :: Number -> Prod Number`** — multiplication over numbers, identity `1`. Defensive
  constructor: `Prod(undefined)`, `NaN` and `null` all yield `Prod 1`, i.e. the identity, so a bad
  value can't poison the product.
- **Ten monoids, one interface** — the point of the table below is that `All`/`Any` (booleans),
  `Assign` (objects), `Endo` (functions), `First`/`Last` (`Maybe`), and `Max`/`Min`/`Prod`/`Sum`
  (numbers) are interchangeable at the call site.
- **`Endo` is the interesting one** — function composition as a monoid, identity = the identity
  function. That's the same associativity that makes `compose(f, g, h)` unambiguous in
  [[fp-guide]] Ch. 5.
- **`First`/`Last` over `Maybe`** turn "take the first present value" into a fold — the monoid form
  of a null-coalescing chain, and a neat bridge to the `Option` material in
  [[from-option-to-observable]].
- **The payoff is the helpers.** Monoids are rarely used one `.concat()` at a time; they're passed
  *as an argument* to a fold:
  - `mconcat  :: Monoid m, Foldable f => m -> f a -> m a`
  - `mreduce  :: Monoid m, Foldable f => m -> f a -> a`
  - `mconcatMap :: Monoid m, Foldable f => m -> (b -> a) -> f b -> m a`
  - `mreduceMap :: Monoid m, Foldable f => m -> (b -> a) -> f b -> a`

  `mconcat*` keeps the result wrapped in the monoid; `mreduce*` returns the bare value. The `Map`
  variants transform each element on the way in, so you don't pre-`map` the list.

## Content

### `Prod` in full

```js
Prod(100)
//=> Prod 100

Prod(undefined)   // also NaN, null
//=> Prod 1

Prod.empty()
//=> Prod 1

Prod(5).concat(Prod(4))
//=> Prod 20

Prod(5).equals(Prod(5))
//=> true

Prod(4).valueOf()
//=> 4
```

Type: `Prod :: Number -> Prod Number`. Identity: `1` — "when the value it provides is `concat`ed to
any other value, it will return the other value."

### The ten monoids

| Monoid | Type | `concat` does | `empty` is |
|---|---|---|---|
| `All` | Boolean | logical AND | `true` |
| `Any` | Boolean | logical OR | `false` |
| `Assign` | Object | object merge | `{}` |
| `Endo` | Function | function composition | identity function |
| `First` | Maybe | first `Just` wins | `Nothing` |
| `Last` | Maybe | last `Just` wins | `Nothing` |
| `Max` | Number | maximum | `-Infinity` |
| `Min` | Number | minimum | `Infinity` |
| `Prod` | Number | multiplication | `1` |
| `Sum` | Number | addition | `0` |

Note how each identity is exactly the value that "does nothing" under its operation — `-Infinity`
for `Max`, `Infinity` for `Min`, `{}` for merge, `Nothing` for first/last. Reading the column
top-to-bottom is the fastest way to internalise what an identity element *is*.

### Why this shape matters

The reason all ten look alike is the reason monoids are worth naming at all: once "combine a list
down to one value" is expressed as `mreduce(SomeMonoid, list)`, choosing sum vs product vs max vs
"first non-empty" becomes a one-word change at the call site, with no rewriting of the fold. The
abstraction isn't the individual monoid — it's the interchangeability.

## Claude Summary

_(Scaffolded from the crocks docs — the Content section is the synthesis. Not yet exercised in
code.)_

## NLM

_(none)_

## Recall.ai

_(none)_

## Source

- **Page logged:** <https://crocks.dev/docs/monoids/Prod.html>
- **Also used:** <https://crocks.dev/docs/monoids/> (the monoid index and shared interface),
  <https://crocks.dev/docs/functions/helpers.html> (`mconcat` / `mconcatMap` / `mreduce` /
  `mreduceMap` signatures)
- crocks is the FP ADT library the other 2026-08-13 crocks entries point at:
  [[fp-combinators]], [[fp-functions]]

## Notes

- **This is the API view of [[fp-guide]] Ch. 13.** The book puts "Monoids bring it all together"
  *last*, after a dozen concrete instances have been met without the name; crocks presents the same
  material as a table on day one. Read in that order — narrative first, table as reference — the
  table stops looking arbitrary.
- **The identity column is the actual lesson.** `Max.empty() === -Infinity` is the kind of thing
  that looks like trivia until you fold an empty list and need the answer to be *neutral*. Worth an
  exercise: for each of the ten, predict `empty` before reading it.
- **`Endo` is the link to composition.** Function composition being a monoid is why
  [[rxjs-pipe-compose]] can claim `pipe`/`compose` differ only in direction and intent — the
  associativity that makes a composition chain unambiguous is monoid associativity.
- **Open thread for RxJS:** `merge`, `concat` and `reduce` on Observables feel monoid-shaped
  (empty = `EMPTY`, concat = `concat`). Worth checking whether Observable-under-`concat` actually
  satisfies the laws, and whether saying so out loud makes the operator zoo in
  [[rxjs-from-fp-js-to-rxjs]] easier to teach — this is the same "one root, many names" problem as
  [[rxjs-operator-renaming]].
- Not yet exercised in code; next step is a small script folding the same list through `Sum`,
  `Prod`, `Max` and `First` via `mreduce` to feel the call-site interchangeability.

## Related

- [[fp-guide]] — Ch. 13 "Monoids bring it all together", the narrative version
- [[fp-combinators]] — crocks combinator helpers
- [[fp-functions]] — crocks point-free function index
- [[universal-algebra]] — algebra as operations plus laws, the frame monoids sit in
- [[from-option-to-observable]] — `Maybe`/`Option` semantics behind `First` and `Last`
- [[rxjs-pipe-compose]] — composition and associativity in the RxJS layer
- [[js-functional-programming-nlm]] — the 12-module FP-in-JavaScript course
