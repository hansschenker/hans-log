import { describe, it } from 'vitest';
import * as fc from 'fast-check';
import { EMPTY, Observable } from 'rxjs';

const empty = EMPTY as Observable<number>;
import { arbStream, fromSpec, expectStreamsEqualE2 } from '../testkit/testkit';
import { andThen } from './andThen';

describe('andThen — Monoid laws (identity: EMPTY)', () => {
  it('associativity (E2): (a ⧺ b) ⧺ c === a ⧺ (b ⧺ c)', () => {
    fc.assert(
      fc.property(arbStream, arbStream, arbStream, (sa, sb, sc) => {
        const [a, b, c] = [sa, sb, sc].map((s) => () => fromSpec(s));
        expectStreamsEqualE2(
          () => a().pipe(andThen(b())).pipe(andThen(c())),
          () => a().pipe(andThen(b().pipe(andThen(c())))),
        );
      }),
    );
  });

  it('left identity (E2): EMPTY ⧺ a === a', () => {
    fc.assert(
      fc.property(arbStream, (spec) => {
        expectStreamsEqualE2(
          () => empty.pipe(andThen(fromSpec(spec))),
          () => fromSpec(spec),
        );
      }),
    );
  });

  it('right identity (E2): a ⧺ EMPTY === a', () => {
    fc.assert(
      fc.property(arbStream, (spec) => {
        expectStreamsEqualE2(
          () => fromSpec(spec).pipe(andThen(empty)),
          () => fromSpec(spec),
        );
      }),
    );
  });
});
