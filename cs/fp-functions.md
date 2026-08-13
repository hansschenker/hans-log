---
slug: fp-functions
title: crocks Functions — the whole library index, by category
date: 2026-08-13
tags: [cs, fp, javascript, crocks, point-free, predicates, reference]
source: cs
---

## TL;DR

The map of everything crocks ships outside its ADTs: six categories, roughly 145 functions —
combinators (argument plumbing), helpers (the big general-purpose bag), logic (predicate
combinators), predicates (`* -> Boolean`), point-free functions (auto-curried, data-last
dispatchers over the ADTs), and transformations (`xToY` conversions between datatypes). The
categories, not the alphabetical lists, are the thing to learn — each one answers a different
question, and knowing which category your problem lives in is most of the work of finding the
function.

## Key Concepts

- **Six categories, each with a distinct job:**

  | Category | Signature shape | Answers |
  |---|---|---|
  | Combinators | functions → functions | "how do arguments reach my function?" |
  | Helpers | mixed | "is this common thing already written?" |
  | Logic | predicates → predicates | "how do I combine conditions?" |
  | Predicates | `* -> Boolean` | "what is this value?" |
  | Point-free | data-last, curried | "how do I operate on an ADT without unwrapping?" |
  | Transformations | `xToY` | "how do I get from one ADT to another?" |

- **Point-free means auto-curried and data-last.** The docs' framing: "a way to really get the most
  out of re-usability in JavaScript is to take what is called a point-free approach." Data-last is
  the deliberate design that makes partial application useful — and the reason `flip` exists in the
  combinators for the APIs that get it backwards.
- **Predicates are `* -> Boolean`, full stop** — "used with the many predicate based functions that
  ship with crocks." They're inputs to `safe`, `ifElse`, `when`, `filter`, `propSatisfies`, not
  usually called directly.
- **The predicate list is two lists in disguise:** ordinary JS type checks (`isArray`, `isString`,
  `isNumber`, `isDate`, `isPromise`…) *and* typeclass checks (`isFunctor`, `isMonad`, `isMonoid`,
  `isSemigroup`, `isTraversable`, `isSetoid`…). The second group is unusual — it lets you ask "does
  this thing implement the algebra?" at runtime, which is how a library stays polymorphic across
  user-defined ADTs.
- **Transformations exist "to reduce unwanted nesting of similar types."** That's the same
  `Option<Option<T>>` complaint from [[from-option-to-observable]], one level up: when two ADTs
  stack (a `Maybe` inside an `Either`), you convert rather than nest.
- **Logic functions are combinators for predicates** — `and`, `or`, `not`, `implies`, `ifElse`,
  `when`, `unless`. Seven functions that replace most conditional blocks in a pipeline.
- **`mconcat`/`mreduce`/`mconcatMap`/`mreduceMap` live in helpers**, not in monoids — the monoid is
  the *argument*, the fold is the helper. See [[fp-monoids]].

## Content

### 1. Combinators (8)

`applyTo` · `composeB` · `constant` · `converge` · `flip` · `identity` · `psi` · `substitution`

"The glue that holds the mighty house of crocks together." Covered in full in [[fp-combinators]].
Note the index lists these eight, while the combinators page also documents `compose2` — treat the
page, not the index, as authoritative.

### 2. Helper functions (~54)

"All other support functions that are either convenient versions of combinators or not even
combinators at all." The catch-all, and the one worth skimming end-to-end once. Grouped by what
they're for:

- **Composition:** `compose`, `pipe`, `composeK`, `pipeK` (Kleisli — for chain-returning functions),
  `composeP`, `pipeP` (Promise), `composeS`, `pipeS` (Star)
- **Arity & currying:** `curry`, `partial`, `unary`, `binary`, `nAry`, `once`
- **Object/prop access:** `prop`, `propOr`, `getProp`, `getPropOr`, `propPath`, `propPathOr`,
  `getPath`, `getPathOr`, `setProp`, `setPath`, `unsetProp`, `unsetPath`, `assoc`, `dissoc`,
  `assign`, `pick`, `omit`, `objOf`, `mapProps`, `defaultProps`, `toPairs`, `fromPairs`
- **Safety:** `safe`, `safeAfter`, `safeLift`, `tryCatch`, `defaultTo`, `find`
- **Monoid folds:** `mconcat`, `mconcatMap`, `mreduce`, `mreduceMap`, `mapReduce`
- **Applicative lifting:** `liftA2`, `liftA3`, `liftN`
- **Branching & debugging:** `branch`, `fanout`, `tap`, `unit`

### 3. Logic functions (7)

`and` · `or` · `not` · `implies` · `ifElse` · `when` · `unless`

Predicate combinators — "combine [predicates] in some very interesting ways." `when`/`unless` are
the one-sided `ifElse`; `implies` is the material conditional, rarely seen in a JS library and handy
for validation rules ("if present, then must be valid").

### 4. Predicate functions (47) — `* -> Boolean`

- **JS type checks:** `isArray`, `isBoolean`, `isDate`, `isFunction`, `isInteger`, `isIterable`,
  `isMap`, `isNumber`, `isObject`, `isPromise`, `isString`, `isSymbol`
- **Presence & truth:** `isDefined`, `isNil`, `isEmpty`, `isTrue`, `isFalse`, `isTruthy`, `isFalsy`,
  `isSame`, `isSameType`
- **Typeclass checks:** `isAlt`, `isAlternative`, `isApplicative`, `isApply`, `isBifunctor`,
  `isCategory`, `isChain`, `isContravariant`, `isExtend`, `isFoldable`, `isFunctor`, `isMonad`,
  `isMonoid`, `isPlus`, `isProfunctor`, `isSemigroup`, `isSemigroupoid`, `isSetoid`, `isTraversable`
- **Property checks:** `hasProp`, `hasProps`, `hasPropPath`, `propEq`, `propSatisfies`, `pathEq`,
  `pathSatisfies`

The typeclass group doubles as a vocabulary list for the algebra hierarchy — reading it top to
bottom is a decent map of what [[fp-guide]] Ch. 8–13 builds.

### 5. Point-free functions (46)

Auto-curried, data-last, dispatching over crocks ADTs *and* plain JS collections:

- **Functor / monad / applicative:** `map`, `chain`, `bichain`, `ap`, `alt`, `bimap`, `contramap`,
  `promap`, `extend`, `sequence`, `traverse`, `nmap`
- **Folding & combining:** `fold`, `foldMap`, `reduce`, `reduceRight`, `concat`, `empty`, `merge`
- **List-ish:** `head`, `tail`, `init`, `last`, `cons`, `filter`, `reject`
- **Pair / Tuple:** `fst`, `snd`, `swap`, `project`, `first`, `second`
- **Extraction & running:** `option`, `either`, `coalesce`, `valueOf`, `run`, `runWith`, `evalWith`,
  `execWith`, `read`, `race`
- **Comparison & misc:** `equals`, `compareWith`, `both`, `log`

### 6. Transformation functions (32) — `xToY`

"Mostly used to reduce unwanted nesting of similar types." The set is essentially a conversion
matrix over `Async`, `Either`, `First`, `Last`, `Maybe`, `Result`, plus `List`/`Array`, `Tuple` and
`Writer`/`Pair`:

| From ↓ | to Async | to Either | to First | to Last | to Maybe | to Result | to Array/List |
|---|---|---|---|---|---|---|---|
| Either | ✓ | — | ✓ | ✓ | ✓ | ✓ | — |
| First | ✓ | ✓ | — | ✓ | ✓ | ✓ | — |
| Last | ✓ | ✓ | ✓ | — | ✓ | ✓ | — |
| Maybe | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ (array, list) |
| Result | ✓ | ✓ | ✓ | ✓ | ✓ | — | — |
| Async | → Promise | — | — | — | — | — | — |

Plus the plain structural ones: `arrayToList`, `listToArray`, `tupleToArray`, `writerToPair`.

Reading the matrix rather than the alphabetical list makes the design obvious: the six
failure/optionality types are mutually convertible, because which one you want depends on whether
you need a reason (`Either`/`Result`), a choice (`First`/`Last`), mere presence (`Maybe`), or
asynchrony (`Async`) — and that answer changes as a value moves through a pipeline.

## Claude Summary

_(Scaffolded from the crocks docs — the categorisation and groupings within each category are mine;
the function lists are the docs'. Not yet exercised in code.)_

## NLM

_(none)_

## Recall.ai

_(none)_

## Source

- **Page logged:** <https://crocks.dev/docs/functions/> (index — lists combinators, helpers and
  logic functions; the other three categories are linked, not listed)
- **Also used:** `/docs/functions/predicate-functions.html`, `/docs/functions/pointfree-functions.html`,
  `/docs/functions/transformation-functions.html`
- Sibling crocks entries: [[fp-combinators]] (category 1 in full), [[fp-monoids]] (the monoids the
  `mconcat`/`mreduce` helpers consume)

## Notes

- **This note is a map, not a lesson.** Its use is "which category does my problem live in" —
  the answer then narrows ~145 functions to a dozen. Worth re-reading before reaching for lodash out
  of habit.
- **The typeclass predicates are the sleeper feature.** `isMonad`, `isMonoid`, `isSemigroup` as
  runtime checks are what let generic helpers accept user-defined ADTs. Nothing in [[fp-guide]]
  covers this — it's a library-design concern the book doesn't reach.
- **`implies` is worth stealing** even outside crocks: validation rules are overwhelmingly
  "if this field is present, then it must satisfy X", and spelling that as `implies` rather than
  `!a || b` reads far better.
- **Kleisli composition (`composeK`/`pipeK`) is the missing link to the monad talk.** Composing
  functions that each return a monad is exactly what `flatMap` chaining does by hand in
  [[from-option-to-observable]] — `pipeK` is that pattern extracted into a combinator. Likely the
  cleanest way to show a class *why* `chain` composes where `map` doesn't.
- **Open thread for RxJS:** the transformation matrix is the static-time version of the interop
  functions in RxJS (`from` over Promise/Array/Iterable, `firstValueFrom` back out). Same idea —
  the effect you want changes as the value moves — and worth naming that way in
  [[rxjs-from-fp-js-to-rxjs]].
- Not yet exercised in code; the practical next step is picking five helpers to actually adopt
  (`safe`, `tryCatch`, `propPathOr`, `ifElse`, `mreduce` are the likely candidates) rather than
  trying to absorb the whole surface.

## Related

- [[fp-combinators]] — category 1, in full
- [[fp-monoids]] — the monoids behind `mconcat`/`mreduce`
- [[fp-guide]] — the narrative these functions are the reference for
- [[from-option-to-observable]] — `chain`/`flatMap` and the nesting problem the transforms address
- [[rxjs-pipe-compose]] — `pipe` vs `compose`, both present here as helpers
- [[universal-algebra]] — the algebra vocabulary behind the typeclass predicates
- [[js-fp]] · [[js-functional-programming-nlm]] — the course-shaped counterparts
