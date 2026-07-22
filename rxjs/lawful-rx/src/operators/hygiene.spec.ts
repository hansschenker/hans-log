/**
 * Subscription hygiene — not algebraic, but per the skill: half the gallery
 * entries are hygiene failures in disguise. Verified for every operator.
 */
import { describe, it, expect } from 'vitest';
import { Observable, of } from 'rxjs';
import { mapWith } from './mapWith';
import { andThen } from './andThen';
import { flattenConcat, flattenMerge } from './flatten';
import { filterWhere, distinctByKey } from './filterWhere';
import { tag, untag } from './notes';

function neverWithTeardown(onTeardown: () => void): Observable<number> {
  return new Observable<number>(() => onTeardown);
}

describe('subscription hygiene: teardown propagates on unsubscribe', () => {
  it('mapWith tears down its source', () => {
    let torn = false;
    neverWithTeardown(() => (torn = true))
      .pipe(mapWith((x) => x))
      .subscribe()
      .unsubscribe();
    expect(torn).toBe(true);
  });

  it('filterWhere / distinctByKey tear down their source', () => {
    let a = false;
    let b = false;
    neverWithTeardown(() => (a = true)).pipe(filterWhere(() => true)).subscribe().unsubscribe();
    neverWithTeardown(() => (b = true)).pipe(distinctByKey((x) => x)).subscribe().unsubscribe();
    expect(a && b).toBe(true);
  });

  it('andThen tears down the active leg (first, then second)', () => {
    let first = false;
    neverWithTeardown(() => (first = true))
      .pipe(andThen(of(1)))
      .subscribe()
      .unsubscribe();
    expect(first).toBe(true);

    let second = false;
    of(1)
      .pipe(andThen(neverWithTeardown(() => (second = true))))
      .subscribe()
      .unsubscribe();
    expect(second).toBe(true);
  });

  it('flattenConcat tears down outer and active inner (contrast: awful A3)', () => {
    let inner = false;
    of(neverWithTeardown(() => (inner = true)))
      .pipe(flattenConcat())
      .subscribe()
      .unsubscribe();
    expect(inner).toBe(true);
  });

  it('flattenMerge tears down all live inners (contrast: awful A3)', () => {
    let i1 = false;
    let i2 = false;
    of(
      neverWithTeardown(() => (i1 = true)),
      neverWithTeardown(() => (i2 = true)),
    )
      .pipe(flattenMerge())
      .subscribe()
      .unsubscribe();
    expect(i1 && i2).toBe(true);
  });

  it('tag / untag tear down their source', () => {
    let a = false;
    let b = false;
    neverWithTeardown(() => (a = true)).pipe(tag()).subscribe().unsubscribe();
    neverWithTeardown(() => (b = true)).pipe(tag(), untag()).subscribe().unsubscribe();
    expect(a && b).toBe(true);
  });
});
