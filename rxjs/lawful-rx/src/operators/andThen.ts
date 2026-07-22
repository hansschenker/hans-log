import { Observable, MonoTypeOperatorFunction, Subscription } from 'rxjs';

/**
 * andThen — sequential composition of two streams (concat as a binary op).
 *
 * Structure: Monoid over Observable<T> with EMPTY as identity
 * Laws (E2): associativity   (a ⧺ b) ⧺ c === a ⧺ (b ⧺ c)
 *            left identity   EMPTY ⧺ a === a
 *            right identity  a ⧺ EMPTY === a
 *
 * Hygiene: second stream is only subscribed after the first completes
 * (laziness); teardown cancels whichever leg is active.
 */
export function andThen<T>(second: Observable<T>): MonoTypeOperatorFunction<T> {
  return (first) =>
    new Observable<T>((subscriber) => {
      let secondSub: Subscription | null = null;
      const firstSub = first.subscribe({
        next: (v) => subscriber.next(v),
        error: (e) => subscriber.error(e),
        complete: () => {
          secondSub = second.subscribe(subscriber);
        },
      });
      return () => {
        firstSub.unsubscribe();
        secondSub?.unsubscribe();
      };
    });
}
