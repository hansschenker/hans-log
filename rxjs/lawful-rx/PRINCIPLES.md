# lawful-rx — Verified Laws

One line per operator, per the lawful-operator skill (Step 5). Equivalence relations: E1 values-only, E2 values+order (default), E3 values+virtual-time.

- `mapWith`: Functor(E2) — identity, composition; hygiene ✓
- `andThen`: Monoid(E2, identity=EMPTY) — associativity, left/right identity; hygiene ✓
- `flattenConcat`: Monad(E2) — left/right identity, associativity; hygiene ✓
- `flattenMerge`: Monad(E2) — left/right identity, associativity; hygiene ✓
- `filterWhere`: Idempotent semilattice(E2) — idempotence, conjunction-merge, commutativity; hygiene ✓
- `distinctByKey`: Idempotent(E2) — projection; hygiene ✓
- `tag`/`untag`: Isomorphism(E2) — round-trip both directions, incl. erroring streams; hygiene ✓

Awful gallery (`src/awful/`): A1 Mutant, A2 Eager Beaver, A3 Hoarder, A4 Time Traveler, A5 Impostor, A6 Snowflake — each with a counterexample test demonstrating the broken law and a pointer to the lawful fix.

Design decisions:

- E2 is the default equivalence for all law claims (rxjs-full convention). No operator here claims E3; none is time-sensitive by design.
- Nested-stream arbitraries use radix-separated times (outer×10000 + mid×100 + leaf, components below the next radix), so every absolute emission time is unique — E2 comparisons can never be flaky on same-frame ordering.
- Monad laws are verified once per flattening strategy; switch/exhaust are deliberately excluded from the monad claims (cancellation breaks associativity) — see A3/A5 for what claiming them anyway looks like.
