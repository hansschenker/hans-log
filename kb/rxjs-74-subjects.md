---
type: video
title: #74 Subjects in RxJS  | Understanding Observables & RxJS | A Complete Angular Course
description: Subject as both observer and observable, multicasting
resource: https://www.youtube.com/watch?v=Rh1YHbFg-Tw
tags: [rxjs, subjects, multicasting]
timestamp: 2026-08-02
---

# #74 Subjects in RxJS  | Understanding Observables & RxJS | A Complete Angular Course

## TL;DR

A practical Angular-course lecture on RxJS **Subjects**: a Subject is a special type of Observable that *multicasts* emitted values to many observers, which makes it a clean tool for **cross-component communication** between unrelated (sibling) components. The lecture builds a working sibling-to-sibling example first with a service + `EventEmitter`, then swaps in a `Subject` to show it's a near drop-in replacement — same shared-service pattern, but `.next(value)` instead of `.emit(value)`.

## Key Concepts

- **Subject = special Observable that multicasts**: one Subject can push the same value to many subscribed observers at once (unlike a plain cold Observable, which runs separately per subscriber).
- **Primary use case: cross-component communication** between components with no parent/child relationship (siblings) — mediated by a shared, root-provided Angular service.
- **Subject is both observer and observable in use**: you emit into it with `subject.next(value)` and subscribe out of it with `subject.subscribe(value => ...)`.
- **`Subject` vs `EventEmitter`**: nearly interchangeable for this pattern. EventEmitter uses `.emit(v)`; Subject uses `.next(v)`. Swapping one for the other required changing only the property type and the emit call.
- **The shared-service plumbing**: a `@Injectable({ providedIn: 'root' })` service holds the `Subject<string>`; the sender component injects the service and calls `.next()`; the receiver component injects the same singleton service and `.subscribe()`s in `ngOnInit`, pushing each value into its local array.
- **Modern Angular injection**: uses the `inject(TaskService)` function (not constructor params), and `[(ngModel)]` two-way binding (requires importing `FormsModule`).
- **You rarely create Observables yourself in Angular** — but you constantly *consume* them (e.g. `HttpClient` methods return Observables), so understanding how they work under the hood matters.

## Summary

The lecture answers *what* a Subject is and *when* to reach for one. Definition first: a Subject is a special type of Observable that lets values be **multicasted to many observers** — you emit data through it and any number of subscribers receive that data. Its headline use case is **cross-component communication**, which it makes easy.

The example uses two **sibling** components — `NewTaskComponent` (an input + "Create task" button) and `ShowTaskComponent` (renders a `tasks: string[]` list) — that have no parent/child relationship, so `@Input`/`@Output` won't do. The goal: type a task in one component and have it appear in the other's list.

The presenter first solves it with the **service + EventEmitter** approach from the prior lesson. He creates a root-provided `TaskService` holding a `createTask = new EventEmitter<string>()`, plus an `onCreateTask(value)` method that calls `createTask.emit(value)`. `NewTaskComponent` two-way-binds the input to a `newTask` property via `[(ngModel)]` (importing `FormsModule`), injects the service with `inject(TaskService)`, and on button click calls `taskService.onCreateTask(this.newTask)`. `ShowTaskComponent` injects the same singleton service and, in `ngOnInit`, subscribes to `createTask`, pushing each emitted value into its `tasks` array. Typing "task 4" and clicking the button makes it appear in the sibling's list — data crossed between unrelated components.

Then he shows the same result with a **Subject**. In the service, he replaces the EventEmitter with `createTask = new Subject<string>()` (imported from `rxjs`), and changes the emit call from `.emit(value)` to `.next(value)` — because a Subject is an Observable, so you push values through `next()`, exactly as you'd notify an Observer. Everything else — the subscribe side in `ShowTaskComponent`, the shared service, the flow — stays identical, and the app behaves the same. The takeaway: creating and using a Subject is trivial (`new Subject<T>()`, type its payload, call `.next()`), and it does cross-component communication just as EventEmitters do.

He closes by tying it back to multicasting: in this demo the Subject has a single observer, but if multiple components needed the same data, each would subscribe and the one Subject would fan the value out to all of them — hence "multicast observable." A final caution: in real Angular apps you'll **rarely create Observables yourself**, but you'll constantly consume them (HTTP calls return Observables), so understanding how they work under the hood is worthwhile.

---

Part of: [RxJS](./rxjs.md)
