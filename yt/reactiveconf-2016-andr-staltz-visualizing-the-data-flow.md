---
slug: reactiveconf-2016-andr-staltz-visualizing-the-data-flow
title: ReactiveConf 2016 - André Staltz: Visualizing the data flow with Cycle.js
channel: ReactiveConf
date: 2026-07-10
videoId: 3a98OPJWFPY
url: https://www.youtube.com/watch?v=3a98OPJWFPY
type: summary
language: en
---

# ReactiveConf 2016 - André Staltz: Visualizing the data flow with Cycle.js

## TL;DR

André Staltz demos a Cycle.js dev tool that *visualizes data flow* so you can understand a program — or spot a bug — at a glance, instead of reconstructing a mental model line-by-line in a debugger. His core argument: to make a program visualizable you must replace ordinary control flow (if/else, call stacks) with reactive streams, because a data-flow graph can be seen in a glance while a stack trace cannot. He explains the whole Cycle.js model with a Lego "stage vs. outside world" metaphor: the stage (pure function) observes the outside world's events and emits descriptions; the outside world (drivers) observes the stage and performs the real effects.

## Key Concepts

- **Debuggers give micro-level info; you need macro-level.** Stepping through a debugger yields tiny puzzle pieces you must assemble into a mental model of the program — slow and stressful. Visualizing data flow gives the *big picture* at a glance (like seeing the whole jigsaw image, not one piece).
- **Visualize the bug, then fix it.** The opening demo: a reproducible framework bug in a recursive component. The dev tool shows events "zapping" through the flow graph (slow-motion available); Staltz *sees* a second DOM node fire that shouldn't, which points straight at the buggy code — no code-diving needed.
- **You must replace control flow to visualize it.** `if`/`else` and call stacks aren't understandable in a glance. Reactive streams (RxJS observables, or anything that looks like data flow) *are* — so the price of visualizability is writing your program as streams.
- **The stage vs. outside world metaphor.** A green "stage" holds people (streams) who only *observe* what's in front of them; the "outside world" is where real events happen (cars passing) and real effects get built. The stage observes the outside world, and the outside world observes the stage — an interplay. That cycle is where "Cycle.js" gets its name.
- **The counter, cast in Lego.** Julia filters blue-car events → `+1`; Raphael filters red-car events → `-1`; Monica observes Julia & Raphael and accumulates a running total (memory over time); Dominic observes Monica and maps her number to a `<div>`; **Mr. Driver** observes Dominic and actually builds it in the real world. Everyone faces one direction — that's separation of concerns.
- **This is just `main(sources)`.** Rename the characters and it's real Cycle.js: `main` takes `sources` (everything from the outside world); Julia→`increment$`, Raphael→`decrement$`, Monica→`count$`, Dominic→`vdom$`, returned as sinks. Effects (DOM, HTTP) are handled by **drivers** — "Earth is DOM, space is HTTP": you observe data from space or hand data to it.
- **Stages nest and collapse.** A stage can be reused inside another stage (stack the green stage on the blue stage); a thousand-node app becomes a pyramid of stages, and the dev tool can collapse/expand a whole stage into one node — the plan for scaling the visualization to real apps.
- **"Everything is a stream" is a foundation.** Like Redux forcing all state transitions through pure reducers (which *buys* time-travel dev tools), Cycle.js forcing everything into streams is the guarantee that makes whole-program data-flow visualization possible. Mix in ad-hoc mutation (or a grab-bag of Redux async middleware) and the foundation — and the tooling — erodes.
- **Async is where Redux's "always the same diagram" breaks.** Redux's mental model looks uniform until you add async: action-creators, thunks/promises, sagas, redux-loop, redux-observable… each yields a *different* big picture. Staltz wanted to allow architectural variation yet still visualize any of it.
- **Other benefits & the ecosystem.** Testability: a stage is a pure function, so you feed inputs and check outputs — no aggressive/global mocking. Performance: with snabbdom + xstream, Cycle.js benchmarks faster than Angular 2 and React. Related visual/data-flow ideas: NoFlow (flow-based), Luna (visual Haskell-like FP), Google Blockly for kids, even circuits / Max MSP / TensorFlow graphs.

## Summary

### The problem: understanding a program at a glance

Staltz (self-described "streams with dollar signs" guy — `foo$`) frames the talk around one question you hit constantly: *why is this behaving like this?* — whether chasing a bug or onboarding to a complex codebase. The standard tool is the **debugger**, which is essential but gives only *micro-level* information: one function calls another, local variables, scope variables, stack frames. To understand the whole program you have to assemble those fragments into a **mental model**, which is slow and mentally draining. His jigsaw analogy: one puzzle piece tells you almost nothing; you want the whole picture in a glance.

What macro-level tools exist? Sublime's minimap (only tells you how much code there is), UML (sequence diagrams are genuinely useful; class-hierarchy diagrams tell you nothing about a bug), react-monocle (component hierarchy + prop propagation — good), and the Redux dev tools (the state tree, with Redux's *predefined* mental model). Redux's picture is uniform… until **async** enters, at which point action-creators vs. thunks vs. sagas vs. redux-loop vs. redux-observable each produce a different big picture. "The devil is in the details" — async is exactly where buggy behavior hides, so that's what deserves visualizing.

### The insight: replace control flow with data flow

Staltz didn't want to impose one fixed architecture. He wanted: *given any program, make it possible to see the data flowing through it at a glance.* The realization: you **cannot** visualize normal control flow — `if`/`else` and stack traces aren't glanceable. You have to *replace* control flow with something that is: **reactive streams** (RxJS observables, or anything shaped like data flow). Streams aren't scary, he insists — just different, and simple enough that a stripped-down RxJS is ~30 lines.

### The Lego metaphor: stage vs. outside world

Rather than code, Staltz uses Lego. There's a green **stage** and, around it, the **outside world**. In the outside world, real events happen — a blue car passes, a red car passes — and there's **Mr. Driver**, who knows how to build real things.

On the stage stand people who each only **observe** what's directly in front of them:

- **Julia** watches the outside world; on a *blue* car she raises a **+1** sign.
- **Raphael** watches the outside world; on a *red* car he raises a **−1** sign.
- **Monica** doesn't watch the cars — she watches **Julia and Raphael**, and raises a sign with the *running sum* of everything they've shown (she has memory).
- **Dominic** watches **Monica** and turns her number into a `<div>` description.
- **Mr. Driver** watches **Dominic** and actually **builds it in the real world**.

Everyone faces one direction on purpose. If Julia had to *chase down* a red car, or Monica had to be *told* by Julia when to react, you'd lose separation of concerns. Because each only observes the one thing in front, each stays cleanly focused. The stage is pure play (signs going up and down); real things only happen out in the world. The stage observes the outside world; the outside world observes the stage — an endless interplay. **That cycle is the name Cycle.js.**

### From metaphor to code

In code it's the same shape: import a stream library and a driver, define the stage as a function that receives *events from the outside world*. Julia = `events.filter(blueCar).map(() => +1)`, Raphael = `events.filter(redCar).map(() => -1)`, Monica folds them over time with memory, Dominic maps the count to virtual-DOM, and the stage returns that to the outside world. Rename the cast and it's canonical Cycle.js: `main(sources)` returning sinks — `increment$`, `decrement$`, `count$`, `vdom$`. Effects live in **drivers**: "Earth is DOM, space is HTTP" — you observe data from space or hand data to it. The same structure visualizes an HTTP random-user fetcher, a BMI calculator, etc. — open the dev tool and watch which part of the program reacts to which input, in slow motion if needed.

### Scaling the visualization

Won't a real app be thousands of nodes? Staltz's answer is compositional: a stage can be **nested** inside another stage (stack the green stage on top of the blue stage; the whole thing is still a stage the outside world can observe). A big app becomes a pyramid of stages — and the dev tool will **collapse/expand** an entire stage into a single node, so you never have to stare at a thousand nodes at once. (Expand/collapse and higher-order-stream support were still on the roadmap at the time, but the tool already worked well enough to diagnose real bug reports without reading code.)

### "Everywhere as a foundation"

The deeper principle (from his blog post): when the *same pattern is used everywhere*, it becomes a foundation you can build tooling on. Redux forces every state transition through pure reducers → that guarantee *buys* time-travel debugging. The moment something mutates state outside a reducer, the dev tools stop being accurate. Cycle.js's equivalent guarantee is "everything is a stream," which is what makes whole-program data-flow visualization possible. He's skeptical a redux-observable-plus-assorted-middleware stack has a solid enough foundation to be visualized the same way.

### Q&A highlights

- **xstream vs. RxJS:** he mostly uses **xstream** (built for Cycle.js — fewer operators, smart defaults); RxJS is the general-purpose choice for anything else.
- **Testability:** because a stage is a pure function, testing is feed-input/check-output — no global mocking. He calls this one of Cycle's bigger advantages, alongside visualization.
- **Performance:** thanks to snabbdom (vdom) and xstream, Cycle.js benchmarks faster than Angular 2 and React — "in the league of the fastest."
- **cycle-onionify:** a state-management approach where each stage emits reducers that compose (reducer wrapping reducer), created because handling lists in Cycle.js had been painful; he's candid about that rough edge.
- **Production use:** used by Staltz and by **Danske Bank** in Copenhagen (a 14-developer team that chose Cycle.js after a thorough framework evaluation). Best-fit use case: **dashboards** — lots of data from many sources (web sockets, REST, sensors).
- **Redux + RxJS:** worth it for the async benefits — reach for redux-observable.
- **Cancel tokens:** "if you think promises are complicated, a tsunami is arriving" — he's strongly against them. **MobX:** "a good idea" — spreadsheet-like reactive cells. **Elm/PureScript:** "double awesome," and Elm is easier than it first looks.
- **Related paradigms:** the same data-flow ideas appear in NoFlow, Luna (visual FP), Blockly (teaching kids), electronic circuits, Max MSP, and TensorFlow graphs.

## Related

- [[what-is-a-model]] — Cycle.js is the *continuous / streaming* corner of that note's Model → State → Stream triad; the stage-observing-world cycle is data flow made visible.
- [[effects-as-data-richard-feldman-reactive-2015]] — same ReactiveConf lineage and the same move: keep business logic pure (the stage / stateless functions) and push effects to the edge (drivers / `runAction`). Cycle's "drivers observe the stage" is Feldman's "represent effects as data" in another shape.
