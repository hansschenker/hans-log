# lawful-rx

Property-tested, algebraically lawful custom RxJS operators — course material for Rxjs-Deep-Dive. Every operator is built from scratch (`new Observable`), classified by algebraic structure, and ships a `*.laws.spec.ts` suite that property-tests its laws with fast-check under virtual time.

Core principle: **a law is a refactoring guarantee** — every law an operator satisfies is a transformation users may safely perform on their pipelines.

## Run

```
npm install
npm test        # 33 tests: law suites + hygiene + awful gallery
```

## Layout

```
src/testkit/testkit.ts     stream specs, fast-check arbitraries, virtual-time
                           recorder, E1/E2/E3 equivalence relations
src/operators/             lawful operators + law suites + hygiene tests
  mapWith        Functor        (identity, composition)
  andThen        Monoid         (associativity, identities w/ EMPTY)
  flatten        Monad ×2       (concat + merge strategies, 3 laws each)
  filterWhere    Semilattice    (idempotence, conjunction-merge, commutativity)
  distinctByKey  Idempotent     (projection)
  notes          Isomorphism    (tag/untag round-trips, incl. errors)
src/awful/                 the awful-operator gallery A1–A6: deliberately
                           broken operators + tests proving each violation
PRINCIPLES.md              declared laws, equivalences, design decisions
```

## The testkit idea

Law sides must consume *identical* input, so test streams are plain data (`StreamSpec`: events at virtual times), turned into observables only inside each side. A recorder subscribes under a fresh `TestScheduler` and captures `(frame, kind, value)`; equivalences project the recording:

- **E1** values-only (multiset) — `merge` is commutative here
- **E2** values + order — the default for every law claim in this repo
- **E3** values + exact virtual time — for time-sensitive operators

A law test always names its equivalence: `associativity (E2)`.
