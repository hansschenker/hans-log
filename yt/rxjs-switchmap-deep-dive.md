---
slug: rxjs-switchmap-deep-dive
title: I switched a map and you'll never guess what happened next - Pete Darwin, Shai Reznik, Mike Brocchi
channel: ng-conf
date: 2026-08-02
videoId: rUZ9CjcaCEw
url: https://www.youtube.com/watch?v=rUZ9CjcaCEw
type: summary
language: en
---

# I switched a map and you'll never guess what happened next - Pete Darwin, Shai Reznik, Mike Brocchi

## TL;DR

An ng-conf comedy sketch that teaches RxJS `switchMap` through an extended metaphor: a startup CEO who hires developers from a recruitment agency for whatever JavaScript framework is trending on Twitter, and fires the old agency the moment a new framework arrives. The talk builds `switchMap` up from first principles — mapping to inner observables, subscribing inside a subscribe (flattening), needing a *flattening strategy*, and finally the *switch strategy* (unsubscribe from the previous inner observable before subscribing to the new one) — then collapses all that hand-written logic into a single `switchMap` call.

## Key Concepts

- **The metaphor**: framework tweets = source (outer) observable; each tweet → a recruitment *agency* (a mapped value); each agency → a stream of *recruits* = inner observable. The CEO switching agencies when a new framework trends = `switchMap`.
- **Mapping to an observable of observables**: `tweets.pipe(map(getAgency), map(a => a.getRecruits()))` yields an observable whose values are themselves observables — you see the inner observable logged, not the recruits.
- **Flattening**: subscribing to the inner observable *inside* the outer `subscribe` to get at the individual inner values. Analogy: an array of arrays flattened into one array.
- **Flattening strategy**: once you flatten, you must decide what to do with overlapping inner subscriptions. Doing nothing = both agencies keep sending recruits (this is `mergeMap` behavior — the bug in the sketch where old backbone devs keep arriving).
- **Switch strategy**: store the current inner subscription; when a new inner observable arrives, *unsubscribe from the previous one before subscribing to the new one*. Only the most recent inner observable stays alive.
- **`switchMap` = map to inner observable + subscribe/flatten + switch strategy**, all in one operator. Not magic — "it's just code."
- **Modern usage**: put operators in `.pipe(...)` rather than chaining methods, so the code stays tree-shakable.
- **Practical payoff**: this is exactly what makes an autocomplete component correct — each new keystroke cancels the in-flight request for the previous one.

## Summary

The sketch frames `switchMap` as a story rather than a definition. A junior dev has copy-pasted a `switchMap`-based autocomplete off Stack Overflow without understanding it; the "Reactive Teacher Man" explains it via a fable set in 2018, when "every five minutes a new JavaScript framework is born."

CEO Kevin Belson obsessively chases whatever framework is trending on Twitter. When "Backbone is the new hot framework" trends, he calls the Backbone recruitment agency and developers start streaming in. The stream of **framework tweets** is the source observable; each tweet maps to an **agency**, and each agency emits a **stream of recruits** — an inner observable. So one outer observable produces inner observables, and both run at the same time.

The trouble starts when "Angular is the new hot framework" arrives. Kevin hires the Angular agency — but in the naïve code, he *never fired Backbone*, so Backbone recruits keep pouring in alongside the Angular ones. In RxJS terms: mapping tweets to `agency.getRecruits()` gives an observable of observables; to see individual recruits you must subscribe to the inner observable inside the outer subscribe — **flattening**. But flattening forces a decision — a **flattening strategy** — about what to do with the still-live previous inner subscription.

They first solve it by hand: store the current recruits subscription in a variable, and when a new recruits observable arrives, unsubscribe from the previous one before subscribing to the new one. That "unsubscribe-before-subscribe" is the **switch strategy** — it kills the Backbone stream the instant Angular arrives, so only the most recent inner observable survives. Then they delete all that scary manual bookkeeping and replace it with a single `switchMap`, which does exactly three things under the hood: (1) map each source value to an inner observable, (2) subscribe to and flatten it, and (3) apply the switch strategy — unsubscribe from the previous inner observable before subscribing to the new one.

The dev finally gets it, realizing this cancellation behavior is precisely why his autocomplete works: every new keystroke switches to a fresh request and abandons the previous in-flight one. The talk closes with a nod toward `concatMap` (a different flattening strategy) and an Angular change-detection gag. Along the way it drops a practical note — modern RxJS puts operators inside `.pipe(...)` to keep code tree-shakable.
