---
slug: pouchdb-article
title: RxJS & PouchDB — Persistent Data Flows
date: 2026-07-21
tags: [rxjs, pouchdb, persistence, frp, functional]
source: rxjs
---

# RxJS & PouchDB — Persistent Data Flows

*Article by Luis Atencio — [medium.com/@luijar](https://medium.com/@luijar/rxjs-pouchdb-persistent-data-flows-480f503ee41f)*

## TL;DR

Atencio wraps PouchDB's Promise-based, schema-less document API in RxJS Observables so that
persistence becomes just another stage in a reactive pipeline. By adapting DB calls with
`fromPromise()` and events with `fromEvent()`, database orchestration reads almost synchronously,
stays immutable, and pushes all side effects downstream into the subscriber — a "database as an
event source" model that unifies local and remote data.

## Key Concepts

- **Databases as event sources, not isolated concerns** — treating persistence as a stream lets it
  compose with the rest of the reactive graph instead of sitting behind imperative callbacks.
- **Promise → Observable adaptation** — `fromPromise()` lifts PouchDB's `post`/`put`/`bulkDocs`/query
  Promises into the stream; `fromEvent()` lifts lifecycle emitters (e.g. `'created'`).
- **Concurrency policy matters for writes** — `concatMap()` preserves order for dependent/sequential
  writes; `mergeMap()` for independent ones (the same `mergeMap`/`concatMap`/`switchMap`/`exhaustMap`
  choice from [[rxjs-heritage]]).
- **Buffering as a write optimizer** — `bufferCount(20)` batches records into `bulkDocs()` to cut
  network/memory overhead; `bufferWhen()` + `race()` flush on time **or** on `beforeunload`.
- **Immutability + isolated effects** — `timestamp()`, `map()`, `filter()` transform data purely;
  the subscription handler is the single, unidirectional place effects land.

## Content

**Thesis.** Static persistent data (a database) and dynamic reactive streams are usually treated as
separate worlds. Atencio's argument is that wrapping PouchDB in Observables collapses that boundary:
async latency becomes transparent behind the Observable abstraction, and local vs. remote sources
merge into one stream that processes identically regardless of origin.

**Patterns demonstrated:**

1. **Sequential single-record writes** — turn a data array into individual timestamped records and
   `post()` them one at a time with `concatMap()`, guaranteeing order and completion between items.
2. **Bulk-optimized writes** — for large datasets, `bufferCount(20)` groups records and fires
   `bulkDocs()` per batch, cutting per-write overhead.
3. **Smart buffering with window closure** — `bufferWhen()` combined with `Observable.race()` emits a
   buffered batch after 500 ms **or** on the `'beforeunload'` event, whichever fires first, so
   in-flight data isn't lost when the user leaves the page.
4. **Chained DB operations** — a `withdraw$()` flow queries an account, validates funds, updates the
   balance, then writes a transaction record — all composed through Observables, no nested callbacks.
5. **Lifecycle-aware streams** — `fromEvent(txDb, 'created')` + `switchMap()` waits for DB
   initialization to finish before insertion proceeds.

**PouchDB features leveraged:** schema-less JSON docs (`post`/`put`), bulk writes (`bulkDocs`),
map/reduce queries via design docs, lifecycle events, and its Promise-based interface.

**Takeaways.** Declarative, functional orchestration reduces bugs via immutability; latency is hidden
behind the Observable so DB code reads nearly synchronously; a merged local+remote stream processes
uniformly; and side effects stay unidirectional and contained in the subscriber, keeping business
logic pure.

## Source

- Original article: https://medium.com/@luijar/rxjs-pouchdb-persistent-data-flows-480f503ee41f
- Author: Luis Atencio (`@luijar`)
- Uses RxJS 5 operator syntax (`fromPromise`, `Observable.race`, `do`); map the pre-pipe operators to
  modern pipeable equivalents when applying today.

## Notes

- The write-buffering patterns (2–3) are the reusable core: `bufferCount` for throughput,
  `bufferWhen + race(beforeunload)` for durability. Worth lifting into any offline-first sync layer.
- Companion to the same-day [[couchdb-repo]] offline-first exploration and Atencio's
  [[kleisli-compositions-js]] on functional composition.

## Related

- [[rxjs-heritage]] — where the four flatten/concurrency policies come from
- [[kleisli-compositions-js]] — Luis Atencio on functional composition
- [[couchdb-repo]] — offline-first Angular/Ionic/CouchDB sample
