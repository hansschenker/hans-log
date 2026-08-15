---
type: article
title: Erik Meijer — Subject/Observer is Dual to Iterator (the Rx Duality)
description: the two-page paper where Rx is derived, not designed — dualize IEnumerable/IEnumerator mechanically and IObservable/IObserver falls out
resource: D:\Learning-Local-Backup\Rxjs\_docs\meijer.duality.pdf
tags: [rxjs, duality, category-theory, observables, iterables, rx-net, frp]
timestamp: 2026-08-15
---

# Erik Meijer — Subject/Observer is Dual to Iterator (the Rx Duality)

## TL;DR

Meijer's two-page paper (Microsoft, ~2010) is the mathematical birth certificate of Rx: take the Iterator pattern's `IEnumerable<T>`/`IEnumerator<T>`, mechanically swap the arguments and results of every method signature ("taking the definition of categorical duality from Wikipedia literally"), streamline, and the Observer pattern's `IObservable<T>`/`IObserver<T>` falls out — including the exact `OnNext`/`OnError`/`OnCompleted` contract RxJS still uses. The kicker is that the two patterns had never been recognized as duals ("the standard design pattern literature does not even list Iterator and Observer as related patterns"), and that the math-derived interfaces are *better* than hand-designed observer APIs: `Subscribe` returning an `IDisposable` is what makes stateless operator composition possible at all.

## Key Concepts

- **Duality as "buy one, get one free"** — the paper opens with De Morgan (`!(a && b) == !a || !b`) and lists the CS duals: call-by-value/call-by-name, induction/co-induction, least/greatest fixed points, algebras/co-algebras. Dualize a known structure and you get a second structure with all its theory for free.
- **The starting point** — `IEnumerable<T>.GetEnumerator()` and `IEnumerator<T>` with `bool MoveNext()` (which can also throw) and `T Current`. The precise return type of `MoveNext` is the disjoint sum **`bool + Exception`** — that observation is what makes the derivation land exactly on Rx's three notifications.
- **The mechanical derivation** — swap arguments and results of all method signatures (keeping only the `IDisposable` aspect invariant), then streamline: the redundant `OnCompleted(bool)` becomes `OnCompleted()` (dual of signaling "no more values" by returning false), and the write-only `OnNext` property becomes a method. Result: `Subscribe(IObserver<T>): IDisposable` + `OnNext(T)` / `OnError(Exception)` / `OnCompleted()` — the grammar `next* (error | complete)?` is *derived*, not designed.
- **Math beat convention** — classic observer APIs remove observers via `deleteObserver(o)`/`Add`/`Remove` delegates, which forces observables to track their subscribers. Disposing the subscription handle instead delegates that responsibility to the source, so combinators like `Where` are **completely stateless** — the paper shows the full `Observable.Create`/`Observer.Create` implementation, plus `GetMouseMoves` wrapping a .NET mouse event with teardown in the closure (the ancestral `fromEvent`).
- **Rx vs FRP: shed time, parameterize concurrency** — classic FRP models behaviors as continuous functions over time (efficient implementation "still an open research problem", the paper notes); Rx "completely sheds the notion of time from the notion of reactivity" and is parameterized over concurrency via `IScheduler` (`Now`, `Schedule(work)`, `Schedule(work, dueTime)`) instead.
- **Not just dual — isomorphic** — pull-based and push-based streams convert into each other: pull→push must *add* concurrency (so `Subscribe` doesn't block while pushing), push→pull must *remove* it (block `MoveNext` until the next value arrives). Concurrency is exactly the difference between the two worlds.
- **The open questions** — where the math dictates concurrency's essential role, and whether `IScheduler` awaits its own "strike of lightning" derivation like `IObservable` got.

## Content

**The derivation, step by step.** Start from the Iterator pattern:

```csharp
interface IEnumerable<out T> { IEnumerator<T> GetEnumerator(); }
interface IEnumerator<out T> : IDisposable {
  bool MoveNext();   // can also throw — really returns bool + Exception
  T Current { get; }
}
```

Dualize mechanically — every input becomes an output, every output an input — and streamline the two artifacts of the raw swap. What emerges is:

```csharp
interface IObservable<out T> { IDisposable Subscribe(IObserver<T> observer); }
interface IObserver<in T> {
  void OnNext(T value);
  void OnError(Exception exception);
  void OnCompleted();
}
```

Read the correspondence: consumer-pulls-`MoveNext` becomes producer-pushes-`OnNext`; `MoveNext` returning `false` becomes `OnCompleted()`; `MoveNext` throwing becomes `OnError(e)`; `GetEnumerator`'s disposal becomes `Subscribe`'s disposal. Every piece of RxJS's Observer contract is the mirror image of something every programmer already knows from `for...of`.

**Why the derived design wins.** Because `Subscribe` hands back a disposal handle, an operator like `Where` needs no bookkeeping: it creates a fresh observable that, on subscribe, subscribes to its source with an anonymous filtering observer and passes the disposal straight through. Statefulness bottoms out only at genuine sources (an event with a listener list) — everything between source and consumer is a stateless function. This is the structural reason RxJS operator chains compose freely.

**The philosophical claim.** The paper's closing move separates Rx from the FRP tradition: reactivity is not about time, it is about *who has control* — and the pull/push isomorphism prices the conversion in exactly one currency, concurrency. That framing is what later notes in this bundle build on: the pull/push table in [RxJS Heritage](./rxjs-heritage.md), the pull side shipped as a library in [IxJS](./interactive-rx.md), and the axis space of [the operator taxonomy](./rxjs-taxonomy.md), where entire axes (backpressure) exist only on the push side of this duality.

## Source

- `D:\Learning-Local-Backup\Rxjs\_docs\meijer.duality.pdf` — "Subject/Observer is Dual to Iterator", Erik "Head in the Box" Meijer, Microsoft (2 pages; full text read for this note)
- Companion material in the same `_docs` dir: `Notes from the Rx talk erik eijer.pdf`, `Rxjs is based on Linq and Rx.net.txt`; further Meijer files in `D:\Learning-Local-Backup\Rxjs\Rxjs-course-files-onedrive\OneDrive_1_6-3-2026\` (fp-, parsers-, rx-historically-, asyncIterable-erik-meijer.txt) and `D:\Learning-Local-Hanss\Erik-Meijer-Domains\Domains_a4.pdf` — not yet mined

## Notes

- This is the **rxjs-course Module 1 keystone**: the whole heritage story (LINQ grammar + Rx.NET temporal semantics) rests on this 2-page derivation. Teaching idea straight from the paper: derive `IObserver` live from `IEnumerator` on a whiteboard — students watch `next*/error|complete` fall out of `bool + Exception`.
- The "isomorphic, priced in concurrency" point is the deep version of "pull naturally avoids backpressure" — worth quoting when the course reaches flow control.
- The unmined Meijer files above (esp. `rx-historically-found-erik-meijer.txt` and `Domains_a4.pdf`) could become follow-up notes if Module 1 needs more depth.

## Related

- [RxJS Heritage — from LINQ and Rx.NET](./rxjs-heritage.md) — the lineage story this paper anchors mathematically
- [IxJS — Interactive Extensions for JavaScript](./interactive-rx.md) — the pull side of the duality, shipped as a library
- [From Options to Observables — a monadic journey](./from-option-to-observable.md) — the Observable as the last stop of the monadic journey this duality grounds
- [RxJS Operator Taxonomy — The 22-Axis Fingerprint Model](./rxjs-taxonomy.md) — the behavior axes that only exist on the push side

---

Part of: [RxJS](./rxjs.md)
