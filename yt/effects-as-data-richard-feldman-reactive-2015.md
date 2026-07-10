---
slug: effects-as-data-richard-feldman-reactive-2015
title: Effects as Data | Richard Feldman | Reactive 2015
channel: ReactiveConf
date: 2026-07-10
videoId: 6EdXaWfoslc
url: https://www.youtube.com/watch?v=6EdXaWfoslc
type: summary
language: en
---

# Effects as Data | Richard Feldman | Reactive 2015

## TL;DR

Richard Feldman argues that the reason effectful code (file IO, HTTP, process management) is painful to test — and therefore usually goes untested — is that effects are *performed* inline instead of *described*. The fix is to represent effects as plain data ("actions"/"tasks") returned from stateless business-logic functions, and confine the actual execution to one tiny `run action` wiring function. Elm takes this to its conclusion: effects can *only* exist as returned `Task` values, so the compiler guarantees which functions are pure, error handling can't be forgotten, and you can test an entire app with zero mocks.

## Key Concepts

- **Effects = interactions with external state.** Effectful (stateful) functions read/write external state; stateless (pure) functions only look at their arguments and return a value. Stateless tests are trivial (set up args → call → check return); stateful tests need you to set up *and* inspect external state, which is why they get skipped under deadline pressure.
- **The origin story.** A résumé-parsing system had a `convert` pipeline (file IO, S3 HTTP, headless LibreOffice process management) and a `parse` pipeline (string→string). Under an unrealistic deadline they cut *all* testing on `convert` — and that's exactly where every production fire happened. The effectful code was hard to test precisely because it *ran* effects instead of returning data.
- **Representing effects as data.** Instead of a function calling `postToS3(...)` with a callback, it returns an *action* — a plain object/value like `{ actionType: 'PostToS3', name, path, data }` — describing what should happen. Business logic becomes stateless: it just decides *which action comes next* (e.g. `handleResponse` returns a `SavedSuccess` or `LogError` action depending on status code).
- **Isolate execution in `run action`.** One function switches on `action.actionType` and performs the real effect, then feeds the resulting action back into itself. All the impure wiring lives in this one place, so it's the only thing that ever needs a mock.
- **Three testing tactics (in JS).** (1) Split chained callbacks into separate functions so you can pass args in; (2) isolate all effects into one `run action`; (3) what you mock is now just *wiring*, never business logic.
- **State can still sneak back in.** Feldman's "one drop of urine in a barrel of water" metaphor: a single hidden dependency on `localStorage`, a mutated argument, a closed-over mutable `extras`, or a pure-looking function with a side effect can silently make a "stateless" function stateful — and tests often won't catch it (`const` over `var` helps but doesn't fix it).
- **Elm enforces it.** Elm has only immutable values and stateless functions. The *only* way to produce an effect is to return a `Task` (a first-class value describing an effect, with built-in success/error types), handed to the runtime via a one-line `port`. You can't sneak a side effect into a function that returns `ContactInfo` — the compiler forbids it.
- **Compiler-verified purity → cheap debugging.** "Who mutated this?" becomes trivial: only functions that return a `Task` can have effects, and the compiler guarantees a function's return type is consistent every time. You narrow culprits by *reading signatures*, not tracing execution.
- **Error handling you can't forget.** JS has three ways to run effects (sync, callback, promise) and three ways to surface errors (exceptions, callback error-args, promise failures) that interact badly (promises swallowing exceptions). Elm has exactly one of each: `Task`. `Task.map` translates success, `Task.onError` + `Task.succeed` turn a failing task into one that always yields an action — so forgetting to handle an error is a *compile error*. Swallowing an error must be a deliberate no-op action.
- **This is the Elm Architecture.** `run action` generalizes into `update : Action -> Model -> (Model, Effects)`; `model` is data, `view : Dispatcher -> Model -> Html` returns a description of the UI (stateless, virtual-DOM diffed), and user interactions are just more actions. Model-View-Update — the pattern that inspired Redux.
- **Payoff:** mock-free testing, faster debugging, unforgettable error handling. Trade-off: a learning curve and JS interop via a client-server `port` boundary. Feldman's rule of thumb: throwaway prototypes → JavaScript; anything maintained long-term → Elm wins clearly over a 3-month horizon.

## Summary

### The problem: effectful code doesn't get tested

Feldman opens with a real project: a job-application system where users upload résumés, which are stored raw on S3 and parsed for contact info. It had two halves. **`convert`** dealt with messy file formats (PDF, doc/docx, HTML) by shelling out to `pdftohtml`, jsdom, and a headless LibreOffice process, then storing to S3 — i.e. file IO, HTTP, and process management. **`parse`** turned the resulting strings into contact info via tokenizing, fuzzy matching, and regexes — pure string→string work.

Under an unrealistic deadline, the team cut corners on testing. Specifically they cut the *entire* corner off `convert` and shipped it completely untested. Every production fire landed there. The lesson isn't "they were lazy" — it's *why* that code resisted testing. `convert` **ran effects**; `parse` **transformed data**. Stateless tests are just "set up arguments → call → check the return value." Stateful tests demand you also construct and inspect external state, and the only tool for the effectful API was **mocks** — a hostile, tedious API that made skipping the tests feel reasonable.

### The fix: describe effects instead of performing them

The insight (shared by Flux, Redux, and the Elm Architecture): an **action is a value that describes an effect, not the effect itself**. Rather than `storeResume(file, callback)` calling `postToS3` directly, it *returns* an action like `{ actionType: 'PostToS3', name, path, data }`. `handleResponse(name, response)` likewise returns a *next* action — `SavedSuccess` on 200, otherwise `LogError` with a message. All the business logic is now stateless functions that decide which action comes next.

You still have to actually *do* it, so a single **`runAction`** function switches on `action.actionType` and performs the real effect for each of the four types, recursively feeding the resulting action back in. Crucially, `runAction` contains **no business logic** — just translation from action-data to real effects. Now the only thing that needs a mock is this one wiring function, and the mock only verifies plumbing (e.g. that a newly added `fileSize` field is threaded through correctly), never business rules.

### How state sneaks back in

Making functions *look* stateless isn't enough. Feldman's metaphor: one drop of urine turns a whole barrel of water into a barrel of urine-water. Examples of a "stateless" `countUsable`/`countResumes` quietly becoming stateful:

- reading `localStorage` at call time (a test that sets up args but not storage will at least fail — you get lucky);
- **mutating** an argument (`rs.pop()`) then compensating — only breaks for specific inputs like an empty array, so tests often pass;
- closing over a mutable outer `extras` — every call with the same args returns the same value *unless* something else mutates `extras`, so it looks pure and fails only in production;
- a pure return value with a hidden **side effect** mutating external state — impossible to catch by inspecting return values.

`const` instead of `var` helps but doesn't close these holes. The takeaway: in a language with side effects, "stateless" is a convention you can't enforce.

### Elm: purity the compiler guarantees

Elm has only immutable values and stateless functions, so the `extras` trick literally can't compile — `List.length extras` is always 0. But then how do you *do* anything? Instead of `runAction` returning `undefined` and performing effects, in Elm it returns a **`Task`** — a first-class value describing an effect, with two type parameters (an error type and a success type), similar to a promise but inert until handed to the runtime. Actions are modeled with **union types** (parameterized enums) and destructured with `case` expressions.

Because effects are data verified at build time, several things fall out:

- **Compiler-checked purity.** `parseResume` returns `ContactInfo`, not a `Task`, so it *cannot* have effects — the compiler proves it, every time. Debugging "who caused this effect?" becomes reading signatures, not stepping through code.
- **Mock-free testing.** The wiring that needed a mock in JS is now compiler-verified: change `handleResponse`'s signature and any stale caller is a build error. With the compiler covering the wiring, *nothing* needs mocking — the whole app tests as stateless functions.
- **Unforgettable error handling.** Elm has one way to run effects (`Task`) and one way to fail (task failure) — nothing to swallow, no `try/catch`. `Task.map` maps the success case into a `handleResponse` action; `Task.onError` + `Task.succeed` convert a failure into a guaranteed-succeeding task carrying a `LogError` action. Forget to handle the error and you get a compile error. Swallowing must be an explicit no-op action — a deliberate choice, never an accident. At NoRedInk this measurably improved UX: previously-forgotten error branches now surface to users or recover gracefully.

### The Elm Architecture

Combine the pieces and `runAction` becomes **`update : Action -> Model -> (Model, Effects)`** — returning a tuple of the new model plus effects to run. `model` is plain data; `view : Dispatcher -> Model -> Html` is a stateless function returning a description of the UI (virtual-DOM diffed like React); user interactions are just actions dispatched back into `update`. That's Model-View-Update — everything stateless, everything easy to test, and the direct inspiration for Redux.

### Trade-offs (from the Q&A)

- **Learning curve.** The biggest cost is relearning your toolbox — reaching for side effects that aren't there. Doable fast (a bootcamp grad shipped production Elm in week one) but real.
- **JS interop via ports.** Elm talks to JS through a client-server-style `port` boundary (send data, get data back) rather than sharing code, which keeps guarantees intact but makes every JS-library call feel like talking to a server. The team's recurring pain was a jQuery date picker behind a port.
- **Young ecosystem.** Small library ecosystem (mitigated by ports); no SSR or React Native bindings yet at the time — feasible, just unbuilt.
- **Speed.** For the first 2–3 weeks a feature is *slower* in Elm (it forces you to handle error cases JS lets you skip). Over a 3-month maintained feature Elm wins clearly. Rule of thumb: throwaway prototypes → JS/jQuery; long-lived code → Elm.

### Logging

Since logging is itself a side effect, it's just another action: a `recordError` action wired to Rollbar via a port. Ajax flows read naturally — `onSuccess` runs a success action, `onError` runs a `recordError` action — so failures reliably reach the logger.

## Related

- [[what-is-a-model]] — same Model → State → Stream idea from the effects angle. Elm's `update : Action -> Model -> (Model, Effects)` *is* a state machine walking the model; actions are the discrete events driving it, and `Task`s are the managed effects — the disciplined counterpart to "effects as side effects."
