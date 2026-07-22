import { Observable, OperatorFunction } from 'rxjs';

/**
 * tag / untag — materialize/dematerialize pair over a tiny Note algebra.
 *
 * Structure: Isomorphism between Observable<T> and Observable<Note<T>>
 * Laws (E2): round-trip  tag |> untag === id
 *            round-trip  untag |> tag === id   (on well-formed note streams)
 *
 * The Note grammar mirrors the Observable contract: N* (C | E)?
 * Awful A4 (the Time Traveler) is precisely an operator that breaks this
 * grammar — the round-trip law is how you catch it.
 */
export type Note<T> =
  | { kind: 'N'; value: T }
  | { kind: 'E'; error: unknown }
  | { kind: 'C' };

export function tag<T>(): OperatorFunction<T, Note<T>> {
  return (source) =>
    new Observable<Note<T>>((subscriber) => {
      const sub = source.subscribe({
        next: (value) => subscriber.next({ kind: 'N', value }),
        error: (error) => {
          subscriber.next({ kind: 'E', error });
          subscriber.complete();
        },
        complete: () => {
          subscriber.next({ kind: 'C' });
          subscriber.complete();
        },
      });
      return () => sub.unsubscribe();
    });
}

export function untag<T>(): OperatorFunction<Note<T>, T> {
  return (source) =>
    new Observable<T>((subscriber) => {
      const sub = source.subscribe({
        next: (note) => {
          switch (note.kind) {
            case 'N':
              subscriber.next(note.value);
              break;
            case 'E':
              subscriber.error(note.error);
              break;
            case 'C':
              subscriber.complete();
              break;
          }
        },
        error: (e) => subscriber.error(e),
        complete: () => subscriber.complete(),
      });
      return () => sub.unsubscribe();
    });
}
