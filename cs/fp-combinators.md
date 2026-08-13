---
slug: fp-combinators
title: crocks Combinators — applyTo, composeB, converge, psi, substitution & friends
date: 2026-08-13
tags: [cs, fp, javascript, combinators, crocks, point-free, combinatory-logic]
source: cs
---

## TL;DR

crocks ships the classical combinatory-logic birds as ordinary JavaScript functions — `identity`,
`constant`, `composeB`, `flip`, `applyTo`, `substitution`, `converge`, `psi`, `compose2` — each a
tiny higher-order function that rearranges *how arguments reach a function* rather than doing any
work itself. They're the plumbing that makes point-free code possible: once you can compose, flip,
fork and re-feed arguments without naming them, the intermediate variables disappear.

## Key Concepts

- **A combinator does no work.** Every one of these is pure argument choreography — nothing is
  computed, only routed. That's why they're the substrate under point-free style rather than a
  feature of it.
- **`identity :: a -> a`** — returns its input unchanged. The docs call it "a workhorse": it's the
  default branch, the no-op transform, and the identity element for `Endo` composition in
  [[fp-monoids]].
- **`constant :: a -> () -> a`** — "pass it any value and it will give you back a function that will
  return that same value no matter what you pass it." The way to drop an argument.
- **`composeB :: (b -> c) -> (a -> b) -> a -> c`** — composition of exactly two functions, read as
  *"f after g"*. The binary primitive that variadic `compose` generalises.
- **`flip :: (a -> b -> c) -> b -> a -> c`** — swaps the first two parameters. The fix for the
  recurring curry problem where the API puts context first and data last, but partial application
  wants the opposite.
- **`applyTo :: a -> (a -> b) -> b`** (the **Thrush**) — inverts application: "give it a value and it
  will give you back a function ready to take a function." This is what lets you hold the *data*
  fixed and vary the *function*:

  ```js
  const getPrices = compose(applyTo(prices), map)
  getPrices(discount(10))
  //=> [ 4.49, 26.99, 14.39 ]
  ```

- **`substitution :: (a -> b -> c) -> (a -> b) -> a -> c`** — one value feeds *both* slots of a
  binary function, one of them via a transform first. The shape behind "compare a thing to something
  derived from itself."
- **`converge :: (b -> c -> d) -> (a -> b) -> (a -> c) -> a -> d`** — fork one input through two
  branches, then merge. The canonical uses are averaging (`sum` and `length` over the same array)
  and assembling a full name from parts.
- **`psi :: (b -> b -> c) -> (a -> b) -> a -> a -> c`** — "the sister of `converge`": takes *two*
  arguments, runs each through the *same* unary function, merges the results. This is Haskell's
  `on` — `compare \`on\` fst` — and the natural way to write equality/validation over a projected
  field.
- **`compose2 :: (c -> d -> e) -> (a -> c) -> (b -> d) -> a -> b -> e`** — a binary function with
  each of its two arguments pre-mapped by its own unary function.

### The combinatory-logic names

crocks names `applyTo` as the Thrush; the rest of the correspondence is the standard
combinatory-logic vocabulary (Smullyan's birds), useful when reading FP literature that uses the
letters rather than the words — my annotation, not the docs':

| crocks | Classic | Definition |
|---|---|---|
| `identity` | **I** (idiot) | `x` |
| `constant` | **K** (kestrel) | `x → y → x` |
| `substitution` | **S** (starling) | `f g x → f x (g x)` |
| `composeB` | **B** (bluebird) | `f g x → f (g x)` |
| `flip` | **C** (cardinal) | `f x y → f y x` |
| `applyTo` | **T** (thrush) | `x f → f x` |
| `converge` | **Φ** (phoenix) | `f g h x → f (g x) (h x)` |
| `psi` | **Ψ** | `f g x y → f (g x) (g y)` |

S, K and I alone are Turing-complete — the SKI calculus — which is the deeper reason this handful of
functions keeps reappearing: they're a basis, not a grab-bag.

## Content

### What these are for

Point-free style has one hard requirement: every value must reach its function without being named.
Composition (`composeB`) handles the linear case — output of one into input of the next. Everything
else in this list handles the *non*-linear cases:

| Situation | Combinator |
|---|---|
| output → next input | `composeB` |
| one input, two branches, then merge | `converge` |
| two inputs, same projection on both, then merge | `psi` |
| two inputs, a different projection on each | `compose2` |
| one input used raw *and* transformed | `substitution` |
| argument order doesn't match the curry | `flip` |
| hold the data, vary the function | `applyTo` |
| drop the argument entirely | `constant` |
| pass it through untouched | `identity` |

Read as a table, the set stops being arbitrary: it's a systematic enumeration of the ways a value
can reach a binary function.

### The `applyTo` example, unpacked

```js
const getPrices = compose(applyTo(prices), map)
getPrices(discount(10))
//=> [ 4.49, 26.99, 14.39 ]
```

`map` is curried, so `map(discount(10))` is a function `[Price] -> [Price]` — but `prices` is the
value we want fixed. `applyTo(prices)` produces a function that *takes a function* and applies it to
`prices`, so composing it after `map` yields "given a per-item transform, give me the transformed
price list." The data is baked in; the operation is the parameter. That inversion is the whole trick.

## Claude Summary

_(Scaffolded from the crocks docs — the Content section is the synthesis. Not yet exercised in
code.)_

## NLM

_(none)_

## Recall.ai

_(none)_

## Source

- **Page logged:** <https://crocks.dev/docs/functions/combinators.html>
- Combinatory-logic table above is standard FP vocabulary, added by me — only "Thrush" for
  `applyTo` appears in the crocks docs
- Sibling crocks entries: [[fp-monoids]], [[fp-functions]]

## Notes

- **Slug collision worth knowing:** there is an older `fp-combinators` entry in the log (2025-01,
  under the retired `fp` tag) pointing at a TutorChase explainer — *"what are combinators"* — a
  different resource with the same slug. This note covers the crocks page only. If the older one
  ever gets a note, it needs a distinct slug.
- **This is the API view of [[fp-guide]] Ch. 4–5.** Currying and "coding by composing" are where the
  book earns these; crocks hands them over as a list. The book explains *why* you'd want `flip`;
  crocks tells you it exists.
- **`psi` = `on` is the highest-value item here.** Sorting/grouping/equality by a projected field is
  everyday work, and `psi(equals, prop('id'))` says it in one line. Worth committing to memory even
  if the rest stay as reference.
- **`applyTo` is the one that unlocks reading other people's point-free code** — the inversion
  (fix the data, vary the function) is unintuitive until seen once, and it shows up constantly in
  Ramda-style pipelines.
- **Open thread for RxJS:** `converge` and `psi` are the static-time analogues of what
  `combineLatest` + `map` does over streams — fork one source, transform each branch, merge with a
  combining function. If that correspondence holds cleanly it's a good bridge lesson for
  [[rxjs-from-fp-js-to-rxjs]]: the same shape, once over values and once over time.
- Not yet exercised in code; next step is rewriting one existing utility point-free using
  `converge`/`psi` to see whether it actually reads better or just shorter.

## Related

- [[fp-guide]] — Ch. 4 Currying, Ch. 5 Coding by Composing, Appendix C Point-free Utilities
- [[fp-monoids]] — `Endo`, where `identity` is the empty element
- [[fp-functions]] — the wider crocks point-free function index
- [[rxjs-pipe-compose]] — `pipe` vs `compose`, the same composition question in RxJS
- [[universal-algebra]] — operations-and-laws framing
- [[from-option-to-observable]] — the ADT side of the same library ecosystem
- [[js-functional-programming-nlm]] — the 12-module FP-in-JavaScript course
