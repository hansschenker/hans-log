import { describe, it } from 'vitest';
import * as fc from 'fast-check';
import { concat, throwError, defer } from 'rxjs';
import { arbStream, fromSpec, expectStreamsEqualE2 } from '../testkit/testkit';
import { tag, untag } from './notes';

describe('tag/untag — Isomorphism laws', () => {
  it('round-trip (E2): tag |> untag === id, completing streams', () => {
    fc.assert(
      fc.property(arbStream, (spec) => {
        expectStreamsEqualE2(
          () => fromSpec(spec).pipe(tag(), untag()),
          () => fromSpec(spec),
        );
      }),
    );
  });

  it('round-trip (E2): tag |> untag === id, erroring streams', () => {
    fc.assert(
      fc.property(arbStream, (spec) => {
        const src = () => concat(fromSpec(spec), defer(() => throwError(() => new Error('boom'))));
        expectStreamsEqualE2(() => src().pipe(tag(), untag()), src);
      }),
    );
  });

  it('round-trip (E2): untag |> tag === id on well-formed note streams', () => {
    fc.assert(
      fc.property(arbStream, (spec) => {
        // well-formed note stream by construction: anything out of tag()
        const notes = () => fromSpec(spec).pipe(tag());
        expectStreamsEqualE2(() => notes().pipe(untag(), tag()), notes);
      }),
    );
  });
});
