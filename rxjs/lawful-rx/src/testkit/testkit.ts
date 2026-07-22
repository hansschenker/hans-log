/**
 * lawful-rx testkit
 *
 * Stream specs, fast-check arbitraries, a virtual-time recorder, and the
 * three equivalence relations from the lawful-operator skill:
 *
 *   E1 — values only (multiset, ignores order/timing)
 *   E2 — values + order (default for law claims)
 *   E3 — values + virtual time (strictest; time-sensitive operators)
 *
 * Every law test names its equivalence explicitly, e.g. "associativity (E2)".
 */
import { Observable, of, EMPTY, merge, delay } from 'rxjs';
import { TestScheduler } from 'rxjs/testing';
import * as fc from 'fast-check';
import { expect } from 'vitest';

// ---------- Stream specs (data, not observables — so both law sides consume identical input) ----------

export interface StreamSpec<V = number> {
  /** events at absolute virtual times, strictly unique times per spec tree */
  events: Array<{ t: number; v: V }>;
}

export type NestedSpec = StreamSpec<StreamSpec<number>>;
export type Nested3Spec = StreamSpec<StreamSpec<StreamSpec<number>>>;

/** Build a cold observable from a spec. Completes when the last event has fired. */
export function fromSpec(spec: StreamSpec<number>): Observable<number> {
  if (spec.events.length === 0) return EMPTY;
  return merge(...spec.events.map((e) => of(e.v).pipe(delay(e.t))));
}

export function fromNestedSpec(spec: NestedSpec): Observable<Observable<number>> {
  if (spec.events.length === 0) return EMPTY;
  return merge(...spec.events.map((e) => of(fromSpec(e.v)).pipe(delay(e.t))));
}

export function fromNested3Spec(spec: Nested3Spec): Observable<Observable<Observable<number>>> {
  if (spec.events.length === 0) return EMPTY;
  return merge(...spec.events.map((e) => of(fromNestedSpec(e.v)).pipe(delay(e.t))));
}

// ---------- Arbitraries ----------
// Radix-separated time scales guarantee globally unique absolute event times in
// nested specs (outer*10000 + mid*100 + leaf, each component below the next radix),
// so same-frame ordering ambiguity can never make an E2 comparison flaky.

const arbTimes = (scale: number, maxDistinct: number, maxLen: number) =>
  fc
    .uniqueArray(fc.integer({ min: 0, max: maxDistinct }), { maxLength: maxLen })
    .map((ts) => ts.sort((a, b) => a - b).map((t) => t * scale));

export const arbValue = fc.integer({ min: -9, max: 9 });

/** leaf stream: up to 4 events, times in {0..90} */
export const arbStream: fc.Arbitrary<StreamSpec<number>> = arbTimes(1, 90, 4).chain((ts) =>
  fc.array(arbValue, { minLength: ts.length, maxLength: ts.length }).map((vs) => ({
    events: ts.map((t, i) => ({ t, v: vs[i] })),
  })),
);

/** stream of streams: outer times in {0,100,...,900} */
export const arbNestedStream: fc.Arbitrary<NestedSpec> = arbTimes(100, 9, 3).chain((ts) =>
  fc.array(arbStream, { minLength: ts.length, maxLength: ts.length }).map((inners) => ({
    events: ts.map((t, i) => ({ t, v: inners[i] })),
  })),
);

/** stream of streams of streams: outer times in {0,10000,...,90000} */
export const arbNested3Stream: fc.Arbitrary<Nested3Spec> = arbTimes(10000, 9, 3).chain((ts) =>
  fc.array(arbNestedStream, { minLength: ts.length, maxLength: ts.length }).map((mids) => ({
    events: ts.map((t, i) => ({ t, v: mids[i] })),
  })),
);

/** a pure function number -> stream, as data (lookup table keyed by value) */
export const arbKleisli: fc.Arbitrary<(x: number) => StreamSpec<number>> = fc
  .array(arbStream, { minLength: 19, maxLength: 19 })
  .map((table) => (x: number) => table[((x % 19) + 19) % 19]);

// ---------- Recorder ----------

export type Rec =
  | { t: number; k: 'N'; v: unknown }
  | { t: number; k: 'E' }
  | { t: number; k: 'C' };

/**
 * Run a pipeline under a fresh TestScheduler and record (virtualTime, kind, value).
 * Inside run(), rxjs time operators (delay/timer/...) automatically use virtual time.
 */
export function record<T>(build: () => Observable<T>): Rec[] {
  const ts = new TestScheduler(() => {});
  const recs: Rec[] = [];
  ts.run(() => {
    build().subscribe({
      next: (v) => recs.push({ t: ts.frame, k: 'N', v }),
      error: () => recs.push({ t: ts.frame, k: 'E' }),
      complete: () => recs.push({ t: ts.frame, k: 'C' }),
    });
  });
  return recs;
}

// ---------- Equivalences ----------

const stringify = (v: unknown) => JSON.stringify(v);

/** E1: multiset of next-values + terminal kind */
export function projectE1(recs: Rec[]) {
  return {
    values: recs.filter((r) => r.k === 'N').map((r) => stringify((r as any).v)).sort(),
    terminal: recs.find((r) => r.k !== 'N')?.k ?? null,
  };
}

/** E2: ordered (kind, value) sequence, frames erased */
export function projectE2(recs: Rec[]) {
  return recs.map((r) => (r.k === 'N' ? ['N', stringify(r.v)] : [r.k]));
}

/** E3: ordered (frame, kind, value) sequence */
export function projectE3(recs: Rec[]) {
  return recs.map((r) => (r.k === 'N' ? [r.t, 'N', stringify(r.v)] : [r.t, r.k]));
}

export function expectStreamsEqualE1<T>(a: () => Observable<T>, b: () => Observable<T>) {
  expect(projectE1(record(a))).toEqual(projectE1(record(b)));
}

export function expectStreamsEqualE2<T>(a: () => Observable<T>, b: () => Observable<T>) {
  expect(projectE2(record(a))).toEqual(projectE2(record(b)));
}

export function expectStreamsEqualE3<T>(a: () => Observable<T>, b: () => Observable<T>) {
  expect(projectE3(record(a))).toEqual(projectE3(record(b)));
}

/** boolean variants, for demonstrating *violations* in the awful gallery */
export function streamsEqualE2<T>(a: () => Observable<T>, b: () => Observable<T>): boolean {
  return JSON.stringify(projectE2(record(a))) === JSON.stringify(projectE2(record(b)));
}
