import { Observable, OperatorFunction } from 'rxjs';

/**
 * mapWith — custom 1:1 transform, built from scratch.
 *
 * Structure: Functor
 * Laws (E2): identity        map(x => x) === id
 *            composition     map(f) |> map(g) === map(x => g(f(x)))
 *
 * Hygiene: all state per-subscription (none needed); errors in f are
 * channeled to error(), teardown delegates to the source subscription.
 */
export function mapWith<T, R>(f: (value: T) => R): OperatorFunction<T, R> {
  return (source) =>
    new Observable<R>((subscriber) => {
      const sub = source.subscribe({
        next: (v) => {
          let r: R;
          try {
            r = f(v);
          } catch (err) {
            subscriber.error(err);
            return;
          }
          subscriber.next(r);
        },
        error: (e) => subscriber.error(e),
        complete: () => subscriber.complete(),
      });
      return () => sub.unsubscribe();
    });
}
