import { Observable, OperatorFunction, Subscription } from 'rxjs';

/**
 * flattenConcat — μ for the concat monad: one inner at a time, FIFO queue.
 *
 * Structure: Monad (join). Laws (E2), one suite per strategy:
 *   left identity   of(x) |> map(f) |> flatten === f(x)
 *   right identity  s |> map(of) |> flatten === s
 *   associativity   sss |> flatten |> flatten === sss |> map(flatten) |> flatten
 *
 * Hygiene: exactly one inner subscription live; queue drained in order;
 * teardown cancels outer + active inner and drops the queue.
 */
export function flattenConcat<T>(): OperatorFunction<Observable<T>, T> {
  return (source) =>
    new Observable<T>((subscriber) => {
      const queue: Observable<T>[] = [];
      let active = false;
      let outerDone = false;
      let innerSub: Subscription | null = null;

      const startNext = (): void => {
        const next = queue.shift();
        if (!next) {
          active = false;
          if (outerDone) subscriber.complete();
          return;
        }
        active = true;
        innerSub = next.subscribe({
          next: (v) => subscriber.next(v),
          error: (e) => subscriber.error(e),
          complete: () => startNext(),
        });
      };

      const outerSub = source.subscribe({
        next: (inner) => {
          queue.push(inner);
          if (!active) startNext();
        },
        error: (e) => subscriber.error(e),
        complete: () => {
          outerDone = true;
          if (!active) subscriber.complete();
        },
      });

      return () => {
        outerSub.unsubscribe();
        innerSub?.unsubscribe();
        queue.length = 0;
      };
    });
}

/**
 * flattenMerge — μ for the merge monad: all inners concurrently.
 *
 * Structure: Monad (join). Same three laws as flattenConcat, verified
 * separately (SKILL.md: one suite per flattening strategy).
 *
 * Hygiene: inner subscriptions tracked and released on completion;
 * teardown cancels outer + all live inners (contrast: awful A3, the Hoarder).
 */
export function flattenMerge<T>(): OperatorFunction<Observable<T>, T> {
  return (source) =>
    new Observable<T>((subscriber) => {
      let activeInners = 0;
      let outerDone = false;
      const inners = new Subscription();

      const outerSub = source.subscribe({
        next: (inner) => {
          activeInners++;
          inners.add(
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

      return () => {
        outerSub.unsubscribe();
        inners.unsubscribe();
      };
    });
}
