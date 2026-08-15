import { describe, it } from 'vitest';
import * as fc from 'fast-check';
import { arbStream, fromSpec, expectStreamsEqualE2 } from '../testkit/testkit';
import { filterWhere, distinctByKey } from './filterWhere';

const arbPred = fc.func(fc.boolean());
const arbKey = fc.func(fc.integer({ min: 0, max: 3 }));

describe('filterWhere — Idempotent semilattice laws', () => {
  it('idempotence (E2): filter(p) |> filter(p) === filter(p)', () => {
    fc.assert(
      fc.property(arbStream, arbPred, (spec, p) => {
        expectStreamsEqualE2(
          () => fromSpec(spec).pipe(filterWhere(p), filterWhere(p)),
          () => fromSpec(spec).pipe(filterWhere(p)),
        );
      }),
    );
  });

  it('conjunction-merge (E2): filter(p) |> filter(q) === filter(p ∧ q)', () => {
    fc.assert(
      fc.property(arbStream, arbPred, arbPred, (spec, p, q) => {
        expectStreamsEqualE2(
          () => fromSpec(spec).pipe(filterWhere(p), filterWhere(q)),
          () => fromSpec(spec).pipe(filterWhere((x) => p(x) && q(x))),
        );
      }),
    );
  });

  it('commutativity (E2): filter(p) |> filter(q) === filter(q) |> filter(p)', () => {
    fc.assert(
      fc.property(arbStream, arbPred, arbPred, (spec, p, q) => {
        expectStreamsEqualE2(
          () => fromSpec(spec).pipe(filterWhere(p), filterWhere(q)),
          () => fromSpec(spec).pipe(filterWhere(q), filterWhere(p)),
        );
      }),
    );
  });
});

describe('distinctByKey — idempotence (a projection)', () => {
  it('idempotence (E2): distinct(k) |> distinct(k) === distinct(k)', () => {
    fc.assert(
      fc.property(arbStream, arbKey, (spec, k) => {
        expectStreamsEqualE2(
          () => fromSpec(spec).pipe(distinctByKey(k), distinctByKey(k)),
          () => fromSpec(spec).pipe(distinctByKey(k)),
        );
      }),
    );
  });
});
