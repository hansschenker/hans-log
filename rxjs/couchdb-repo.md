---
slug: couchdb-repo
title: Offline-First Apps with Angular, Ionic & CouchDB
date: 2026-07-21
tags: [rxjs, offline-first, couchdb, pouchdb, angular, ionic]
source: rxjs
---

# Offline-First Apps with Angular, Ionic & CouchDB

*GitHub repo — [github.com/deroux/offline-first-apps-angular-ionic-couchdb](https://github.com/deroux/offline-first-apps-angular-ionic-couchdb)*

> Companion source for a Udemy offline-first course. The README is thin; this write-up is from reading
> the actual app under `julies/src/app` (the "Julie's" restaurant/waiters demo).

## TL;DR

The whole offline-first story is ~30 lines in one file: `PouchDBRepository.init()` opens a **local
PouchDB**, calls `db.sync(remoteCouchDB, { live: true, retry: true })` for **continuous bidirectional
replication**, and taps `db.changes({ live: true })` to push every changed doc into an **RxJS
Subject**. Angular services turn that Subject into per-collection `BehaviorSubject`s the UI binds to —
so a write on *any* device flows CouchDB → PouchDB → changes feed → service state → UI with no manual
refresh. A `DBRepository` abstract class + Angular DI makes the storage backend swappable
(`PouchDBRepository` vs `MockDBRepository`).

## Key Concepts

- **Continuous live+retry sync** — one `db.sync(remote, {live, retry})` call *is* the sync engine;
  `retry` is what makes it survive going offline and reconnecting.
- **Changes feed → Subject bridge** — `db.changes(...).on('change', d => subject.next(d.doc))` turns
  DB mutations into an Observable stream (Promise/event → Observable, same move as [[pouchdb-article]]).
- **Reactive change propagation ("4-way binding")** — local + remote writes both re-enter the UI
  through the *same* changes feed, so views stay live without polling.
- **Repository pattern via DI** — `IDBRepository` → abstract `DBRepository` → concrete impls, chosen
  in `app.module.ts` with `{ provide: DBRepository, useClass: PouchDBRepository }`.
- **DB as source of truth** — services write to PouchDB first, then advance local state (e.g. the
  XState table machine only transitions *after* `createOrUpdate` resolves).

## Sync Implementation

**1. Setup & replication** — `julies/src/app/db/PouchDB.repository.ts`, `init()`:

```ts
init(): void {
  PouchDB.plugin(PouchDBFind);                       // Mango-query support (db.find)
  this.db = new PouchDB('julies2');                  // local store
  this.remote = 'http://admin:admin@localhost:5984/julies2';  // remote CouchDB (demo creds!)

  this.db.sync(this.remote, { live: true, retry: true })      // continuous 2-way replication
    .catch(err => console.error(err));

  this.db.changes({ since: 'now', live: true, include_docs: true })
    .on('change', change => this._changesSubject.next(change.doc));  // feed → Subject
}
```

- `sync(..., {live, retry})` replicates in **both directions** forever; `retry` reconnects after
  offline gaps. That single call is the entire offline-first mechanism.
- The `changes` feed (`since: 'now'`) catches every subsequent local mutation — *including ones that
  arrived via replication from CouchDB* — and republishes the doc onto `_changesSubject`
  (`Subject<T>`). Initial data comes separately from `fetchByType`.

**2. Query layer (Promise → Observable):**

```ts
fetchByType(type, fields) {
  const query = { selector: { type }, fields, execution_stats: true };
  return from(this.db.find(query)).pipe(map(obj => obj['docs']));  // Mango find, unwrapped
}
createOrUpdate(doc) { return this.db.put(doc); }     // write
delete(doc)        { return this.db.remove(doc); }   // delete
```

`from(this.db.find(...))` lifts the PouchDB Promise into an Observable — the exact
Promise→Observable adaptation Atencio describes in [[pouchdb-article]].

**3. Reactive propagation into the UI** — each Angular service (`TableService`, `ProductsService`)
holds a `BehaviorSubject<Array<Doc>>` as its UI-facing state and subscribes to the changes stream:

```ts
initChangeHandler() {
  this.dbService.getDocumentChanges$().subscribe((doc: any) => {
    if (doc.type !== 'table') return;                // filter by doc type
    this.dbService.handleDocumentChange(this.tablesSubject, doc,
      () => this.fetchTables());                     // fallback: full refetch for new docs
  });
}
```

`handleDocumentChange` does an in-place merge by `_id`:

```ts
const idx = docs.findIndex(x => x._id === changedDoc._id);
if (idx === -1) { updateManually(); return; }        // unknown doc → refetch
docs[idx] = changedDoc; subject.next(docs);          // known doc → patch + emit
```

The UI binds via `getCurrentTables()` → `tablesSubject.asObservable()`. **Full loop:** UI action →
`createOrUpdate` (`db.put`) → PouchDB → `sync` → CouchDB → (on this and every peer) `changes` feed →
`_changesSubject` → service `BehaviorSubject` → UI. A remote edit on another device lands the same
way — that round trip is the "4-way binding."

**4. Pluggable backend** — `MockDBRepository` implements the same interface with no-op `init()`,
`of([])` queries, and resolved-Promise writes, so tests/offline-dev swap it in via DI without touching
service code.

## Source

- Repo: https://github.com/deroux/offline-first-apps-angular-ionic-couchdb (demo app under `julies/`)
- Sync core: `julies/src/app/db/PouchDB.repository.ts`
- Consumption: `julies/src/app/services/{table,products}/*.service.ts`
- DI wiring: `julies/src/app/app.module.ts` → `{ provide: DBRepository, useClass: PouchDBRepository }`

## Notes

- **The offline-first magic is almost entirely `db.sync(remote, {live, retry})`** — PouchDB's
  replication protocol handles conflict resolution (deterministic `_rev` winner) and reconnection.
  There is *no* custom merge/conflict logic in the app; contrast with the manual `bufferCount` /
  `bufferWhen` write-batching Atencio hand-rolls in [[pouchdb-article]] — this repo delegates all of
  that to `sync`.
- **Concurrency is `_rev`-based (optimistic).** Docs carry `_rev`; `handleDocumentChange` patches by
  `_id` and falls back to a full refetch when it sees a doc it doesn't have yet.
- **Warts worth remembering:** hardcoded `admin:admin@localhost:5984` credentials in source (demo
  only), verbose `console.*` left in, and `since:'now'` means the changes feed only covers post-init
  mutations (initial load is a separate `find`).
- **Takeaway pattern:** *changes-feed → Subject → per-collection BehaviorSubject → UI* is a clean,
  reusable offline-first reactive spine; the Repository abstraction keeps PouchDB swappable for a mock.

## Related

- [[pouchdb-article]] — RxJS + PouchDB persistent data flows (the operator-level view of the same idea)
- [[rxjs-course-modules-drive]] — RxJS Deep Dive course modules (same-day study batch)
