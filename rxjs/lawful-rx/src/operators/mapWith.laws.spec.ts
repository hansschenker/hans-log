import { describe, it } from 'vitest';
import * as fc from 'fast-check';
import { arbStream, fromSpec, expectStreamsEqualE2 } from '../testkit/testkit';
import { mapWith } from './mapWith';

const arbFn = fc.func(fc.integer({ min: -100, max: 100 }));

describe('mapWith — Functor laws', () => {
  it('identity (E2): map(x => x) === id', () => {
    fc.assert(
      fc.property(arbStream, (spec) => {
        expectStreamsEqualE2(
          () => fromSpec(spec).pipe(mapWith((x) => x)),
          () => fromSpec(spec),
        );
      }),
    );
  });

  it('composition (E2): map(f) |> map(g) === map(g ∘ f)', () => {
    fc.assert(
      fc.property(arbStream, arbFn, arbFn, (spec, f, g) => {
        expectStreamsEqualE2(
          () => fromSpec(spec).pipe(mapWith(f), mapWith(g)),
          () => fromSpec(spec).pipe(mapWith((x) => g(f(x)))),
        );
      }),
    );
  });
});
