import { Observable, MonoTypeOperatorFunction } from 'rxjs';

/**
 * filterWhere — custom filter.
 *
 * Structure: Idempotent semilattice
 * Laws (E2): idempotence        filter(p) |> filter(p) === filter(p)
 *            conjunction-merge  filter(p) |> filter(q) === filter(x => p(x) && q(x))
 *            commutativity      filter(p) |> filter(q) === filter(q) |> filter(p)
 */
export function filterWhere<T>(predicate: (value: T) => boolean): MonoTypeOperatorFunction<T> {
  return (source) =>
    new Observable<T>((subscriber) => {
      const sub = source.subscribe({
        next: (v) => {
          let keep: boolean;
          try {
            keep = predicate(v);
          } catch (err) {
            subscriber.error(err);
            return;
          }
          if (keep) subscriber.next(v);
        },
        error: (e) => subscriber.error(e),
        complete: () => subscriber.complete(),
      });
      return () => sub.unsubscribe();
    });
}

/**
 * distinctByKey — drop values whose key was already seen.
 *
 * Structure: Idempotent (a projection): applying it twice === once (E2).
 *
 * Note the state (`seen`) lives INSIDE the subscribe function — one Set per
 * subscription. Hoisting it out is exactly awful A1, the Mutant.
 */
export function distinctByKey<T, K>(key: (value: T) => K): MonoTypeOperatorFunction<T> {
  return (source) =>
    new Observable<T>((subscriber) => {
      const seen = new Set<K>();
      const sub = source.subscribe({
        next: (v) => {
          const k = key(v);
          if (!seen.has(k)) {
            seen.add(k);
            subscriber.next(v);
          }
        },
        error: (e) => subscriber.error(e),
        complete: () => subscriber.complete(),
      });
      return () => sub.unsubscribe();
    });
}
