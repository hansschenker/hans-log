---
type: topic
title: Functional Programming
description: FP in JavaScript/TypeScript — currying, composition, combinators, monoids, monads, and the road from Option to Observable
tags: [combinators, elm, fp, monads, monoids]
timestamp: 2026-08-15
---

The FP foundation under the RxJS work: crocks, the Mostly Adequate Guide, Kleisli composition, and the monadic journey that ends at Observables.

## Courses

- [JavaScript — Functional Programming for JavaScript Developers (Packt code repo)](./js-fp.md) — Packt course code repo
- [Functional Programming in JavaScript — 12-Module NotebookLM Course](./js-functional-programming-nlm.md) — NLM-authored 12-module video course — expression-orientation to Functional FizzBuzz, the source course the RxJS payoff course rebuilds on streams
- [From FP-JS to RxJS — The RxJS Payoff Course](./rxjs-from-fp-js-to-rxjs.md) — the RxJS payoff course — the same 12 FP-in-JavaScript concepts, one per module, rebuilt on streams with runnable strict-TS demos

## Videos

- [Effects as Data | Richard Feldman | Reactive 2015](./effects-as-data-richard-feldman-reactive-2015.md) — modeling side effects as data, the Elm architecture

## Concepts

- [From Options to Observables — a monadic journey (Miłosz Piechocki, WarsawJS](./from-option-to-observable.md) — Option monad → Observable, a monadic journey (NotebookLM)
- [JavaScript Combinators — Deriving leftApply, rightApply, and Friends](./javascript-combinators.md) — Braithwaite's derivation — partial application decomposes a function's interface outside-in, and repeated extraction ends at named combinators like C
- [RxJS Operator Combinators — Deriving the Operator Zoo](./rxjs-operator-combinators.md) — operators are unary functions, so Braithwaite's combinators apply verbatim — pipe is B, identity is I, and flattenWith derives the whole *Map family from one shape
- [Pipe vs Compose — Point-Free Composition in RxJS FP Architecture](./rxjs-pipe-compose.md) — Point-Free Composition in RxJS FP Architecture — currying, point-free style, hybrid FP-RxJS case study (NotebookLM)
- [Universal Algebra — Operations + Laws as a General Theory](./universal-algebra.md) — an algebra is just a set with operations satisfying equational laws — the single lens behind monoids, functor laws, and lawful APIs

## Articles

- [Kleisli Compositions in JavaScript](./kleisli-compositions-js.md) — Luis Atencio on Kleisli composition in JS

## References

- [crocks Combinators — applyTo, composeB, converge, psi, substitution & friends](./fp-combinators.md) — combinator helpers (composeB, substitution, applyTo) in the crocks FP library
- [crocks Functions — the whole library index, by category](./fp-functions.md) — index of crocks' point-free helper functions
- [Professor Frisby's Mostly Adequate Guide to Functional Programming](./fp-guide.md) — the classic FP-in-JavaScript book, currying → monads
- [crocks Monoids — Prod, and the shared empty/concat interface](./fp-monoids.md) — multiplicative monoid, concat/empty laws in the crocks library
- [rxjs-fp — A Functional-Style RxJS Built From Scratch](./rxjs-fp.md) — from-scratch functional RxJS: cold core, curried free operators, no prototype patching
