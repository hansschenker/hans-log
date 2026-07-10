---
slug: what-is-a-model
title: What Is a Model
date: 2026-07-10
tags: [cs, model, abstraction, state-machine, distributed-systems]
source: cs
---

# What Is a Model

## TL;DR

"Model" is one of the most overloaded words in software — it means different things in ML, simulations, MVC, data layers, and theoretical CS. This deck (NotebookLM: *The Architect's Blueprint to the Living System*) untangles the word by treating a model as a **static blueprint/abstraction** and then showing how a **dynamic state machine** brings that blueprint to life. It walks a two-phase payment finite state machine from abstract theory down to a Spring Statemachine implementation, and finally into the messy reality of a distributed database (CockroachDB serializable isolation), where the abstraction collides with concurrency and needs retry architecture to survive.

## Key Concepts

- **"Model" is overloaded** — the same word covers AI/ML models, simulations, the "M" in MVC, data/domain models, and theoretical models of computation (FSMs). Disambiguating which one you mean is step zero of any design conversation.
- **Model vs State** — the model is the *static* structure (the blueprint, the set of possible configurations); state is the *dynamic* value flowing through it at a moment in time.
- **The 4-layer transformation pipeline** — data flows and is reshaped across **Data Model → Domain Model → DTO → ViewModel**, each layer serving a different concern (persistence, business logic, transport, presentation).
- **Continuous vs discrete behavior** — continuous/streaming behavior is modeled with **RxJS** (observables over time); discrete, well-defined transitions are modeled with **state machines** (XState / Spring Statemachine).
- **FSM anatomy** — a finite state machine is built from four primitives: **State** (node), **Event** (arrow/trigger), **Guard** (padlock/condition), and **Action** (gear/side effect).
- **Two-phase payment FSM** — worked example: `CREATED → AUTHORIZED → CAPTURED → REVERSED`, with branch states `DECLINED` and `ABORTED`. Authorization and capture are the classic two phases of a card payment.
- **Spring Statemachine** — the abstract FSM maps to Java `enum` states/events, with guards and actions wired into the transition configuration.
- **The transaction boundary problem** — when the FSM persists state in a distributed DB, a state-change interceptor can silently *swallow* the serialization exception (CockroachDB `40001`), so the retry must live **outside** the transaction boundary, not inside the interceptor.
- **Two retry architectures** — (1) *Infrastructure*: let the CockroachDB JDBC driver retry (`implicitSelectForUpdate=true`, `retryTransientErrors=true`) → clean app code; (2) *Application*: capture the exception into the FSM's extended state and drive an explicit Spring AOP `@Retryable` loop → explicit control.
- **The living system** — the end state is a static model/blueprint fused with a dynamic state machine, fed by RxJS streams, sitting on CockroachDB — "where the conceptual blueprint and the production code are one and the same."

## Content

### The problem: one word, many meanings

Before you can reason about a "model," you have to say *which* model. The deck opens by listing the overloaded senses of the term:

- **AI / ML models** — trained statistical artifacts.
- **Simulations** — models that imitate a real-world process over time.
- **MVC** — the "Model" that holds application data and rules.
- **Data / domain models** — the shape of persisted and business data.
- **Theoretical models of computation** — finite state machines, automata.

The thesis of the deck is that these are unified by one idea: a model is an **abstraction** — a static blueprint of what is possible — and a **state machine** is what makes that blueprint *live*.

### Model vs State, static vs dynamic

The core distinction: the **model** is static (the structure, the space of legal configurations and transitions), while **state** is the dynamic value moving through that structure right now. Keeping them separate is what lets you reason about a system's *possible* behaviors independently of its *current* one.

Data doesn't stay in one shape either. It moves through a **four-layer pipeline** — **Data Model → Domain Model → DTO → ViewModel** — being reshaped for persistence, business logic, transport, and presentation in turn.

### Two ways to model behavior

- **Continuous / streaming** behavior → **RxJS** observables (values arriving over time).
- **Discrete** behavior with clearly enumerable states → **state machines** (XState in the JS world, Spring Statemachine on the JVM).

### Anatomy of a finite state machine

An FSM is four primitives, given a visual mnemonic in the deck:

| Symbol | Primitive | Meaning |
|---|---|---|
| Node | **State** | a legal configuration the system can be in |
| Arrow | **Event** | a trigger that requests a transition |
| Padlock | **Guard** | a condition that must hold for the transition to fire |
| Gear | **Action** | a side effect run during the transition |

### Worked example: a two-phase payment

The recurring example is a card payment as a two-phase FSM:

```
CREATED ──authorize──▶ AUTHORIZED ──capture──▶ CAPTURED ──reverse──▶ REVERSED
   │                       │
   └──▶ DECLINED           └──▶ ABORTED
```

Authorization (hold funds) and capture (settle) are the two phases; `DECLINED` and `ABORTED` are the failure branches. This maps directly onto **Spring Statemachine**: states and events become Java `enum`s, and guards/actions are wired into the transition configuration.

### Where the abstraction meets reality: distributed concurrency

The clean FSM abstraction cracks when its state is persisted in a **distributed database under serializable isolation**. CockroachDB throws a serialization error (SQL state `40001`) when concurrent transactions contend. The danger: a **state-change interceptor** sitting inside the transaction can *catch and swallow* that exception, hiding the failure — so the machine thinks a transition succeeded when the transaction actually needs to be retried.

This is the **transaction boundary problem**: the retry must happen *outside* the transaction boundary, not inside the interceptor that lives within it.

### Two retry architectures

1. **Infrastructure approach (JDBC driver)** — lean on the CockroachDB JDBC driver's internal retries: `implicitSelectForUpdate=true` (rewrite queries to reduce conflicts) and `retryTransientErrors=true` (driver-level retries for stragglers). Result: clean application code; the driver handles the messy reality.
2. **Application approach (client AOP)** — capture the exception into the FSM's **extended state**, have the outer service read that and intentionally roll back, and trigger a Spring AOP `@Retryable` around-advice on the business method. Result: explicit application control over the retry loop.

### The three angles: Model → State → Stream

The whole deck collapses into one idea seen from three angles. Read left to right they're the layers of the system; read right to left they're the flow of a single event:

```
   MODEL  ──────────────▶  STATE  ──────────────▶  STREAM
   static space of         a disciplined walk       events pushed in
   the possible            through that space        over time
   (FSM / blueprint)       (state machine)           (RxJS observable)

   "what's allowed?"       "where are we now?"       "what just happened?"

        ◀─────────  a Stream event drives the State machine to take
                    one legal step inside the Model  ─────────
```

- **Model** — the static space of possibilities: every legal state and the transitions between them. It never moves.
- **State** — the single node we occupy right now; a state machine is the discipline that walks Model's space one legal step at a time.
- **Stream** — how the outside world reaches in: events arriving over time (RxJS) that trigger those steps.

Same object, three questions: *what's allowed* (Model), *where are we* (State), *what just happened* (Stream).

### The living system, mastered

The closing image stacks three layers: a **static Model / Blueprint** at the base (over CockroachDB), a **dynamic State Machine** overlaid on it, and **RxJS streams** flowing in from outside. The journey: *begin with an abstract mathematical model of computation → translate it into a strict static architecture → let dynamic state flow through it → fortify it against the chaos of distributed concurrency.* The payoff is "a highly cohesive, perfectly synchronized transactional engine where the conceptual blueprint and the production code are one and the same."

## Claude Summary

*(This note was synthesized directly from the slide deck; no separate Claude chat.)*

## NLM

Source deck generated with NotebookLM: **The Architect's Blueprint to the Living System — Unifying Abstract Computer Science Models with Distributed Production Systems** (14 slides). See `cs/what-is-a-model.pdf`.

## Recall.ai

—

## Source

`cs/what-is-a-model.pdf` (NotebookLM slide deck, "Model as Abstraction")

## Notes

- The through-line worth keeping: a *model* is the static space of possibilities; a *state machine* is a disciplined way to walk that space; a *stream* (RxJS) is how the outside world pushes events at it. Same idea seen from three angles.
- The distributed-systems ending is the real lesson: a clean FSM abstraction is necessary but not sufficient — the moment state is persisted under serializable isolation, correctness depends on where the retry boundary sits, not on the diagram.
- Connects to ongoing RxJS work: continuous behavior = RxJS, discrete behavior = state machines — the two abstractions are complementary, not competing.

## Related

- [[staltz-two-fundamental-abstractions]] — Staltz's reactive abstractions, the continuous/streaming side of the same coin
- [[effects-as-data-richard-feldman-reactive-2015]] — the same Model → State → Stream idea from the effects angle; Elm's `update : Action -> Model -> (Model, Effects)` is this note's state machine made concrete
