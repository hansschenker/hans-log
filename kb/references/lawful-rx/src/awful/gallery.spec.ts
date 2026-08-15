/**
 * Awful gallery — each test DEMONSTRATES the violated law with a concrete
 * counterexample (asserting the inequality), and where useful shows the
 * lawful fix passing the same check.
 */
import { describe, it, expect } from 'vitest';
import { Observable, of, concatMap } from 'rxjs';
import {
  fromSpec,
  fromNestedSpec,
  record,
  projectE2,
  streamsEqualE2,
} from '../testkit/testkit';
import {
  mutantRunningSum,
  eagerAudit,
  hoarderSwitch,
  timeTravelerNotes,
  impostorConcatMap,
  snowflakeCombine,
} from './gallery';
import { mapWith } from '../operators/mapWith';
import { flattenConcat } from '../operators/flatten';
import { tag, untag } from '../operators/notes';

const src12 = { events: [{ t: 0, v: 1 }, { t: 10, v: 2 }] };

describe('A1. The Mutant — shared state across subscriptions', () => {
  it('violates referential transparency: second subscription sees first one’s state', () => {
    const piped = fromSpec(src12).pipe(mutantRunningSum());
    const first = projectE2(record(() => piped));
    const second = projectE2(record(() => piped));
    expect(second).not.toEqual(first); // [1,3] then [4,6] — the sum leaked
  });
});

describe('A2. The Eager Beaver — work before subscription', () => {
  it('violates laziness: effect fires at .pipe() time, before any subscriber', () => {
    const log: string[] = [];
    fromSpec(src12).pipe(eagerAudit(log)); // construction only — no subscribe
    expect(log).toEqual(['audit-started']); // ← already ran
  });
});

describe('A3. The Hoarder — leaks inner subscriptions', () => {
  it('violates the resource contract: inner teardown never runs', () => {
    let torn = false;
    const inner = new Observable<number>(() => () => {
      torn = true;
    });
    const sub = of(inner).pipe(hoarderSwitch()).subscribe();
    sub.unsubscribe();
    expect(torn).toBe(false); // ← the leak: a lawful operator would have torn down
  });

  it('violates claimed switch semantics: previous inner keeps emitting (E2)', () => {
    // inner1 slow, inner2 arrives at t=15 — true switch silences inner1 from then on
    const nested = {
      events: [
        { t: 0, v: { events: [{ t: 5, v: 1 }, { t: 30, v: 99 }] } },
        { t: 15, v: { events: [{ t: 0, v: 2 }] } },
      ],
    };
    const recs = projectE2(record(() => fromNestedSpec(nested).pipe(hoarderSwitch())));
    // 99 (from the "cancelled" inner1) still shows up:
    expect(recs).toContainEqual(['N', '99']);
  });
});

describe('A4. The Time Traveler — breaks the notification grammar N* (C|E)?', () => {
  it('violates the round-trip isomorphism: values after complete are lost (E2)', () => {
    const src = { events: [{ t: 0, v: 1 }, { t: 10, v: 2 }, { t: 20, v: 3 }] };
    const lawful = projectE2(record(() => fromSpec(src).pipe(tag(), untag())));
    const awful = projectE2(
      record(() => fromSpec(src).pipe(tag(), timeTravelerNotes(), untag())),
    );
    expect(awful).not.toEqual(lawful); // the held-back last value silently vanishes
  });
});

describe('A5. The Impostor — claims concat, performs merge', () => {
  const source = { events: [{ t: 0, v: 0 }, { t: 10, v: 1 }] };
  const f = (v: number) =>
    v === 0
      ? fromSpec({ events: [{ t: 5, v: 100 }, { t: 50, v: 101 }] }) // slow inner
      : fromSpec({ events: [{ t: 0, v: 200 }] });

  it('violates the claimed μ: output interleaves where concat must not (E2)', () => {
    expect(
      streamsEqualE2(
        () => fromSpec(source).pipe(impostorConcatMap(f)),
        () => fromSpec(source).pipe(concatMap(f)),
      ),
    ).toBe(false); // 100,200,101 vs 100,101,200
  });

  it('the lawful fix: mapWith + flattenConcat matches rxjs concatMap (E2)', () => {
    expect(
      streamsEqualE2(
        () => fromSpec(source).pipe(mapWith(f), flattenConcat()),
        () => fromSpec(source).pipe(concatMap(f)),
      ),
    ).toBe(true);
  });
});

describe('A6. The Snowflake — non-associative combination', () => {
  it('violates associativity: grouping changes the result (E2)', () => {
    const a = { events: [{ t: 0, v: 1 }] };
    const empty = { events: [] as Array<{ t: number; v: number }> };
    expect(
      streamsEqualE2(
        () => snowflakeCombine(snowflakeCombine(fromSpec(a), fromSpec(empty)), fromSpec(empty)),
        () => snowflakeCombine(fromSpec(a), snowflakeCombine(fromSpec(empty), fromSpec(empty))),
      ),
    ).toBe(false); // left grouping doubles twice: 4 vs 2
  });
});
