---
type: topic
title: RxJS
description: reactive programming with RxJS — operators, taxonomy, heritage, FP architecture, and the deep-dive course work
tags: [frp, observable, rxjs]
timestamp: 2026-08-15
---

Everything reactive: the RxJS Deep Dive Course feeds on these notes — operator semantics, the Rx heritage from LINQ, observables as a formal taxonomy, and the FP architecture behind pipe/compose.

## Videos

- [Effects as Data | Richard Feldman | Reactive 2015](./effects-as-data-richard-feldman-reactive-2015.md) — modeling side effects as data, the Elm architecture
- [ReactiveConf 2016 - André Staltz: Visualizing the data flow with Cycle.js](./reactiveconf-2016-andr-staltz-visualizing-the-data-flow.md) — André Staltz: Visualizing the data flow with Cycle.js — visualize reactive dataflow in Cycle.js
- [None](./rxjs-74-subjects.md) — Subject as both observer and observable, multicasting
- [I switched a map and you'll never guess what happened next - Pete Darwin, Shai Reznik, Mike Brocchi](./rxjs-switchmap-deep-dive.md) — when to cancel vs merge inner observables, key for HTTP autocomplete

## Concepts

- [What Is a Model](./what-is-a-model.md) — model as static blueprint vs dynamic state machine — from FSM theory to distributed retry architecture
- [From Options to Observables — a monadic journey (Miłosz Piechocki, WarsawJS](./from-option-to-observable.md) — Option monad → Observable, a monadic journey (NotebookLM)
- [RxJS Heritage — from LINQ and Rx.NET](./rxjs-heritage.md) — RxJS heritage from LINQ and Rx.NET (NotebookLM)
- [A Formal Taxonomy of RxJS Observables](./rxjs-observable-taxonomy.md) — invariant semantics vs. variable execution characteristics vs. style; cold/hot ⟂ unicast/multicast (NotebookLM)
- [RxJS Operator Renaming — The Suffix Grammar](./rxjs-operator-renaming.md) — suffix grammar 'keep the root, fix the suffix': curried roots × boundary combinators (NotebookLM)
- [Pipe vs Compose — Point-Free Composition in RxJS FP Architecture](./rxjs-pipe-compose.md) — Point-Free Composition in RxJS FP Architecture — currying, point-free style, hybrid FP-RxJS case study (NotebookLM)

## Articles

- [RxJS & PouchDB — Persistent Data Flows](./pouchdb-article.md) — Luis Atencio on persistent data flows with RxJS + PouchDB

## References

- [Offline-First Apps with Angular, Ionic & CouchDB](./couchdb-repo.md) — offline-first sample app repo
- [rxjs-fp — A Functional-Style RxJS Built From Scratch](./rxjs-fp.md) — from-scratch functional RxJS: cold core, curried free operators, no prototype patching
