/**
 * Monad law suites for the two flattening strategies — one suite per μ,
 * as required by the lawful-operator skill (an operator parameterized by
 * concurrency gets its laws verified per strategy).
 *
 * Times in nested specs are radix-separated (outer*10000 + mid*100 + leaf),
 * so every absolute emission time is unique and E2 order is deterministic.
 */
import { describe, it } from 'vitest';
import * as fc from 'fast-check';
import { of, OperatorFunction, Observable } from 'rxjs';
import {
  arbStream,
  arbNested3Stream,
  arbKleisli,
  arbValue,
  fromSpec,
  fromNested3Spec,
  fromNestedSpec,
  expectStreamsEqualE2,
  streamsEqualE2,
} from '../testkit/testkit';
import { mapWith } from './mapWith';
import { flattenConcat, flattenMerge } from './flatten';

type Flatten = <T>() => OperatorFunction<Observable<T>, T>;

function monadLawSuite(name: string, flatten: Flatten) {
  describe(`${name} — Monad laws`, () => {
    it('left identity (E2): of(x) |> map(f) |> flatten === f(x)', () => {
      fc.assert(
        fc.property(arbValue, arbKleisli, (x, f) => {
          expectStreamsEqualE2(
            () => of(x).pipe(mapWith((v) => fromSpec(f(v))), flatten()),
            () => fromSpec(f(x)),
          );
        }),
      );
    });

    it('right identity (E2): s |> map(of) |> flatten === s', () => {
      fc.assert(
        fc.property(arbStream, (spec) => {
          expectStreamsEqualE2(
            () => fromSpec(spec).pipe(mapWith((v) => of(v)), flatten()),
            () => fromSpec(spec),
          );
        }),
      );
    });

    it('associativity (E2): flatten |> flatten === map(flatten) |> flatten', () => {
      fc.assert(
        fc.property(arbNested3Stream, (spec) => {
          expectStreamsEqualE2(
            () => fromNested3Spec(spec).pipe(flatten(), flatten()),
            () =>
              fromNested3Spec(spec).pipe(
                mapWith((mid) => mid.pipe(flatten())),
                flatten(),
              ),
          );
        }),
      );
    });
  });
}

monadLawSuite('flattenConcat', flattenConcat);
monadLawSuite('flattenMerge', flattenMerge);

describe('strategies are genuinely different (sanity, not a law)', () => {
  it('there exists a nested stream where concat ≠ merge (E2)', () => {
    // outer emits two inners; first inner is slow — merge interleaves, concat does not
    const nested = {
      events: [
        { t: 0, v: { events: [{ t: 50, v: 1 }, { t: 250, v: 2 }] } },
        { t: 100, v: { events: [{ t: 0, v: 3 }] } },
      ],
    };
    const eq = streamsEqualE2(
      () => fromNestedSpec(nested).pipe(flattenConcat()),
      () => fromNestedSpec(nested).pipe(flattenMerge()),
    );
    if (eq) throw new Error('expected concat and merge to differ on this input');
  });
});
