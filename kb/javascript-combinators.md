---
type: concept
title: JavaScript Combinators — Deriving leftApply, rightApply, and Friends
description: Braithwaite's derivation — partial application decomposes a function's interface outside-in, and repeated extraction ends at named combinators like C
resource: D:\Learning-Local-Hanss\Javascript-Combinators
tags: [cs, fp, javascript, combinators, partial-application, currying, decorators]
timestamp: 2026-08-15
---

# JavaScript Combinators — Deriving leftApply, rightApply, and Friends

## TL;DR

Reginald Braithwaite's "JavaScript Combinators" talk earns combinators instead of listing them: start from an everyday `pluck(collection, property)`, notice a function's parameter list is an *interface* that can be decomposed, partially apply it both ways (`pluckFrom`, `pluckWith`), extract the repeated pattern into `leftApply`/`rightApply`, keep mechanically extracting — and named combinatory-logic birds fall out at the bottom (`C`, the flip). The lesson is that combinators are not exotic vocabulary but the fixed points of ordinary refactoring: **partial application decomposes a function from the outside-in** (its interface), where extracting sub-functions decomposes it inside-out (its implementation). Two Seth House decks in the same folder frame the material — combinators/decorators as a review of *JavaScript Allongé*, and a reactive-programming intro showing where the road leads: Rx.

## Key Concepts

- **A function's parameters are an interface** — `pluck(collection, property)` has a two-part interface; decomposing that interface is a design act, not just a call convention.
- **Two partial applications, two designs** — `pluckFrom(collection)(property)` (data-first) vs `pluckWith(property)(collection)` (data-last): the same function decomposed in both directions. Data-last is the shape pipelines want — the convention the whole crocks/RxJS world standardizes on.
- **Extract until named combinators appear** — the talk's signature move, step by step:

  ```javascript
  let leftApply  = (fn, a) => (b) => fn(a, b);
  let rightApply = (fn, b) => (a) => fn(a, b);

  let pluckFrom = (collection) => leftApply(pluck, collection);
  let pluckFrom = leftApply(leftApply, pluck);            // extract again
  let pluckFrom = leftApply(leftApply, leftApply)(pluck); // and again

  // the residue, named:
  let Istarstar = (a) => (b) => (c) => a(b, c);   // leftApply(leftApply, leftApply)
  let C         = (a) => (b) => (c) => a(c, b);   // leftApply(leftApply, rightApply)

  let pluckFrom = Istarstar(pluck);
  let pluckWith = C(pluck);   // C is flip — swap the argument order
  ```

- **Outside-in vs inside-out decomposition** — the folder's mind map splits it cleanly: *Implementation (inside-out)*: extracting functions, smaller functions, identifying actors; *Interface (outside-in)*: partial application, currying, decomposing arguments. Combinators live on the interface side.
- **Combinator, defined** — (UtahJS deck) higher-order *pure* functions that take only functions as arguments and return a function; `compose(a, b) = c => a(b(c))` is the archetype.
- **Partial application in production shape** — `var post = applyLeft(xhr, 'POST')`, `var getJSON = applyRight(xhr, jsonHeaders)`: one general `xhr(method, path, data, headers)` decomposed into an API surface.
- **Decorators as the impure sibling** — a decorator takes one function and returns a variation of it: `maybe` (skip on null), `fluent` (return `this`), and the advice family `before`/`after`/`around`/`provided` — "AKA aspect-oriented programming, AKA Lisp Flavors".
- **The map(parseInt) trap, solved combinator-style** — `['1','2','3'].map(parseInt)` yields `[1, NaN, NaN]` (index becomes radix); `map(applyLast(parseInt, 10))` fixes the interface mismatch by decomposition instead of a wrapper lambda.
- **The road ends at Rx** — the companion Open West 2016 deck ("Reactive Programming: A Practical Introduction", same author) presents Rx as "a unified API for sync & async operations" with the Perlis motto — 100 functions on one data structure — the combinator philosophy applied to streams.

## Content

**The derivation is the content.** Where the crocks docs ([fp-combinators](./fp-combinators.md)) present `composeB`, `applyTo`, and substitution as a finished catalog, Braithwaite's talk shows *where such a catalog comes from*: refactoring pressure. Each extraction step is boring and mechanical; the surprise is only at the end, when the leftover shapes turn out to be the classic birds of combinatory logic — `C` (flip) hiding inside `leftApply(leftApply, rightApply)`. That makes this note the pedagogical front door to the crocks catalog: derive two combinators once, and the other twenty read as inevitable rather than arbitrary.

**Decorators complete the picture.** The UtahJS deck (Seth House, 2013, structured as a review of Braithwaite's *JavaScript Allongé*) adds the practical taxonomy: pure combinators for *composition* (`compose`, `applyLeft`/`applyRight`, currying — the `converter.curry('km', 1.60936)` unit-conversion family) and decorators for *variation* (`maybe`-guarded setters, `fluent` chainable methods, admin-guarded deletes) — with functional mixins (raganwald's method-combinators, Twitter Flight) as the framework-scale application.

**Same folder, next chapter.** The second House deck pitches reactive programming with the exact API families this bundle's RxJS notes formalize — filtering/transforming/collecting/combining operators as combinators over one stream type. The through-line from `pluckWith` to `pipe(map, filter)` is direct: data-last curried unary functions are what make both compose.

## Source

- `D:\Learning-Local-Hanss\Javascript-Combinators\` — `javascript-combinators.txt` (the core derivation, extracted from Reginald Braithwaite's talk; full talk as `Reginald Braithwaite - JavaScript Combinators.mp4`, not watched end-to-end), `presentation-utahjs.pdf` (Seth House, UtahJS 2013 — full text read), `presentation-frp-intro.pdf` (Seth House, Open West 2016 — skimmed), plus NotebookLM mind-map exports (`.png`/`.mm`/`.json`).

## Notes

- Teaching gold for the rxjs-course: the derive-don't-catalog approach is exactly how Module 03 of [the payoff course](./rxjs-from-fp-js-to-rxjs.md) treats `map(fn)` as partial application — this talk supplies the missing prequel showing the extraction mechanics live.
- `C` here = crocks' `flip`; `Istarstar` is uncurried application curried — worth a cross-reference table in the course's combinator segment.

## Related

- [crocks Combinators — applyTo, composeB, converge, psi, substitution & friends](./fp-combinators.md) — the finished catalog this talk derives the front door to
- [Kleisli Compositions in JavaScript](./kleisli-compositions-js.md) — composition when functions return wrapped values, the next step up
- [Professor Frisby's Mostly Adequate Guide to Functional Programming](./fp-guide.md) — the other classic FP-JS book, same territory as *JavaScript Allongé*
- [Functional Programming in JavaScript — 12-Module NotebookLM Course](./js-functional-programming-nlm.md) — data-last curried unary style as house rule
- [From FP-JS to RxJS — The RxJS Payoff Course](./rxjs-from-fp-js-to-rxjs.md) — Module 03: `map(fn)` as partial application, the derivation's stream-side payoff

---

Part of: [Functional Programming](./functional-programming.md)
