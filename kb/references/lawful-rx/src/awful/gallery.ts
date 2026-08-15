/**
 * The awful-operator gallery — A1..A6 from the lawful-operator skill.
 *
 * Every operator here is DELIBERATELY broken. Each has a companion test in
 * gallery.spec.ts that demonstrates the violated law with a concrete
 * counterexample, and names the lawful fix.
 */
import { Observable, OperatorFunction, MonoTypeOperatorFunction, Subscription } from 'rxjs';
import { flattenMerge } from '../operators/flatten';
import { mapWith } from '../operators/mapWith';
import { Note } from '../operators/notes';

/**
 * A1. The Mutant — shared mutable state across subscriptions.
 * `sum` lives OUTSIDE the Observable constructor: every subscriber shares it.
 * Law broken: referential transparency — two subscriptions to the same
 * pipeline are not two independent executions.
 * Fix: move `let sum` inside the subscribe function (see distinctByKey).
 */
export function mutantRunningSum(): OperatorFunction<number, number> {
  let sum = 0; // ← the sin
  return (source) =>
    new Observable<number>((subscriber) =>
      source.subscribe({
        next: (v) => {
          sum += v;
          subscriber.next(sum);
        },
        error: (e) => subscriber.error(e),
        complete: () => subscriber.complete(),
      }),
    );
}

/**
 * A2. The Eager Beaver — side effect at pipeline CONSTRUCTION time.
 * `pipe(eagerAudit(log))` writes to the log before anyone subscribes.
 * Law broken: laziness — "a pipeline is a value".
 * Fix: wrap the effect in the Observable constructor (or defer()).
 */
export function eagerAudit(log: string[]): MonoTypeOperatorFunction<number> {
  return (source) => {
    log.push('audit-started'); // ← the sin: runs at .pipe() time
    return source;
  };
}

/**
 * A3. The Hoarder — a switch-like operator that never unsubscribes the
 * previous inner. Algebraically invisible under E1/E2 value checks on
 * short-lived inners — which is why it survives review.
 * Law broken: switch cancel semantics (E3) + resource contract.
 * Fix: unsubscribe the previous inner before subscribing the next
 * (see flattenMerge's teardown for the bookkeeping pattern).
 */
export function hoarderSwitch<T>(): OperatorFunction<Observable<T>, T> {
  return (source) =>
    new Observable<T>((subscriber) => {
      const hoard: Subscription[] = []; // ← never released
      let activeInners = 0;
      let outerDone = false;
      const outerSub = source.subscribe({
        next: (inner) => {
          // claims switch semantics, but the previous inner keeps running
          activeInners++;
          hoard.push(
            inner.subscribe({
              next: (v) => subscriber.next(v),
              error: (e) => subscriber.error(e),
              complete: () => {
                activeInners--;
                if (outerDone && activeInners === 0) subscriber.complete();
              },
            }),
          );
        },
        error: (e) => subscriber.error(e),
        complete: () => {
          outerDone = true;
          if (activeInners === 0) subscriber.complete();
        },
      });
      return () => outerSub.unsubscribe(); // ← inners not torn down either
    });
}

/**
 * A4. The Time Traveler — violates the notification grammar N* (C|E)?.
 * Works at the Note level so the corruption is observable: it moves the
 * completion note BEFORE the last value note.
 * Law broken: tag |> timeTravel |> untag ≠ tag |> untag (round-trip iso).
 */
export function timeTravelerNotes<T>(): MonoTypeOperatorFunction<Note<T>> {
  return (source) =>
    new Observable<Note<T>>((subscriber) => {
      let held: Note<T> | null = null;
      return source.subscribe({
        next: (note) => {
          if (note.kind === 'N') {
            if (held) subscriber.next(held);
            held = note; // hold back the latest value...
          } else {
            subscriber.next(note); // ← ...emit terminal note first (the sin)
            if (held) subscriber.next(held); // value AFTER complete: dropped downstream
            subscriber.complete();
          }
        },
        error: (e) => subscriber.error(e),
        complete: () => subscriber.complete(),
      });
    });
}

/**
 * A5. The Impostor — documented as concat-flattening, implemented as merge.
 * Law broken: the CLAIMED μ's semantics — outputs interleave under load,
 * so tests written against the documented concat ordering fail.
 * Fix: pick ONE strategy, document it, law-test that one.
 */
export function impostorConcatMap<T, R>(
  f: (value: T) => Observable<R>,
): OperatorFunction<T, R> {
  // "concatMap" in the docs, mergeMap in the code:
  return (source) => source.pipe(mapWith(f), flattenMerge());
}

/**
 * A6. The Snowflake — non-associative combination: special-cases its left
 * operand (doubles its values). Grouping changes the result.
 * Law broken: associativity — users can no longer extract sub-pipelines.
 * Fix: make the binary op treat both operands uniformly (see andThen),
 * or exclude it from the lawful API surface.
 */
export function snowflakeCombine(
  a: Observable<number>,
  b: Observable<number>,
): Observable<number> {
  return new Observable<number>((subscriber) => {
    let aDone = false;
    let bDone = false;
    const subA = a.subscribe({
      next: (v) => subscriber.next(v * 2), // ← left bias: the sin
      error: (e) => subscriber.error(e),
      complete: () => {
        aDone = true;
        if (bDone) subscriber.complete();
      },
    });
    const subB = b.subscribe({
      next: (v) => subscriber.next(v),
      error: (e) => subscriber.error(e),
      complete: () => {
        bDone = true;
        if (aDone) subscriber.complete();
      },
    });
    return () => {
      subA.unsubscribe();
      subB.unsubscribe();
    };
  });
}
