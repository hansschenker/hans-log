---
slug: from-option-to-observable
title: From Options to Observables — a monadic journey (Miłosz Piechocki, WarsawJS #43)
date: 2026-08-13
tags: [rxjs, fp, monads, typescript, option, result, promise, observable]
source: rxjs
---

## TL;DR

One code body, four semantics: the same `flatMap → flatMap → map` chain that walks
`employeeId → employee → supervisorId → supervisor → name` works unchanged whether the repository
returns `Option`, `Result`, `Promise`, or `Observable` — only the type signature changes. That is
the whole point of the talk: a monad is not a mathematical curiosity but a *polymorphic interface*
(`return`/`of` to lift a value in, `flatMap`/`bind` to chain) that lets optionality, failure,
asynchrony, and streams-over-time all be composed with identical code. Observables are simply the
last stop on that journey — RxJS is monadic programming most JS developers are already doing
without the vocabulary.

## Key Concepts

- **The formal definition is useless in practice.** "A monad is a monoid in the category of
  endofunctors" is category theory; Piechocki's explicit position is that you learn monads by
  example and intuition, not by studying the definition.
- **The problem being solved is nesting, not math.** `getEmployeeSupervisorName` in imperative
  TypeScript needs three-plus `if (x !== undefined)` checks and two levels of nesting; the checks
  dominate the function and "obfuscate our real intention."
- **`Option<T>` = `Some | None`** — a tagged union making absence explicit in the type. It replaces
  TypeScript's `supervisorId?: number` with `supervisorId: Option<number>` and
  `get(id): Employee | undefined` with `get(id): Option<Employee>`.
- **`map` = apply inside the box.** Same semantics as `Array.prototype.map`: transform the value if
  it's there, do nothing (return a fresh `None`) if it isn't. The "apple in a box" metaphor: `map`
  lifts `apple → orange` into `Box<apple> → Box<orange>`.
- **`flatMap` (a.k.a. `bind`, `chain`, `concatMap`/`mergeMap`) = apply and flatten.** Needed when
  the transforming function *itself* returns a box, which `map` would leave as `Option<Option<T>>`.
  This is the essential operation — the one that makes monads compose.
- **`return`/`unit` = lift a plain value into the context.** `new Some(x)`, `new Success(x)`,
  `Promise.resolve(x)`, `Observable.of(x)` — every monad has one.
- **`Result<T, E>` = `Success | Failure`, i.e. functional exceptions**, and better than exceptions
  because failure is in the *type signature*: the caller cannot forget it, and the error carries
  context ("no employee found" vs "no supervisor").
- **Railway Oriented Programming (Scott Wlaschin).** `Result` is a track switch: green track while
  everything succeeds, and the first failure shunts to the red track, which subsequent steps can
  never leave. `flatMap` is what welds two switches into one line of track.
- **Same body, new behaviour.** Moving the pipeline from `Option` to `Result` changed *only* the
  type signature — the function body was identical. The same trick then carried it to `Promise`
  and `Observable`.
- **Promises are the messy monad.** `.then()` collapses `map` and `flatMap` into one polymorphic
  method — a decision of the Promise authors. RxJS is "even better than promises" here precisely
  because it keeps `map` and `flatMap`/`concatMap` distinct.
- **Monad = programmable semicolon.** Some languages have syntax (Haskell `do`, Scala
  `for`-comprehensions) that makes monadic code look imperative; the monad programs the gap between
  statements — hiding null checks, error propagation, callback waiting — so the source shows only
  business logic.
- **Four benefits claimed:** boilerplate hidden, declarative style (a pipeline of data
  transformations), better type safety, and a single abstraction where imperative languages need
  four separate features (strict null checks, `try/catch`, `async/await`, stream libraries).
- **Monadic laws exist and were deliberately skipped** — associativity and identity rules a type
  must satisfy to behave consistently; intuition first, laws later.

## Content

### 1. The spaghetti that motivates everything

The running example is an employee repository:

```ts
interface Employee {
  id: number;
  name: string;
  supervisorId?: number;   // optional — the source of all the pain
}

class EmployeeRepository {
  get(id: number): Employee | undefined { /* ... */ }
}
```

Asking for an employee's *supervisor's* name means every hop can fail: the id may not exist, the
employee may have no supervisor, the supervisor id may not resolve. Written imperatively it becomes
a pyramid:

```ts
function getSupervisorSupervisorNameImperative(employeeId: number): string | undefined {
  const employee = getImperativeEmployee(employeeId);
  if (employee !== undefined) {
    const supervisorId = employee.supervisorId;
    if (supervisorId !== undefined) {
      const supervisor = getImperativeEmployee(supervisorId);
      if (supervisor !== undefined) {
        // ...and deeper still
      }
    }
  }
  return undefined;
}
```

Piechocki's diagnosis is not "this is ugly" but "this is *about the wrong thing*": the function is
supposed to express `Id → Employee → Supervisor → Name`, and instead almost every line is a check
for emptiness.

### 2. Option — making absence a type

```ts
interface Option<T> {
  map<U>(f: (val: T) => U): Option<U>;
  flatMap<U>(f: (val: T) => Option<U>): Option<U>;
  getOrElse(defaultValue: T): T;
}

class Some<T> implements Option<T> {
  constructor(public readonly value: T) {}
  map<U>(f: (val: T) => U): Option<U> { return new Some(f(this.value)); }
  flatMap<U>(f: (val: T) => Option<U>): Option<U> { return f(this.value); }
  getOrElse(_: T): T { return this.value; }
}

class None<T> implements Option<T> {
  map<U>(_: (val: T) => U): Option<U> { return new None<U>(); }
  flatMap<U>(_: (val: T) => Option<U>): Option<U> { return new None<U>(); }
  getOrElse(defaultValue: T): T { return defaultValue; }
}
```

The domain model changes with it — `supervisorId: Option<number>`, `get(id): Option<Employee>` —
and the pyramid collapses to four lines that read like the sentence they implement:

```ts
function getSupervisorNameOption(employeeId: number, repo: OptionEmployeeRepository): Option<string> {
  return repo.get(employeeId)           // Option<Employee>
    .flatMap(emp => emp.supervisorId)   // Option<number>
    .flatMap(supId => repo.get(supId))  // Option<Employee>
    .map(supervisor => supervisor.name);// Option<string>
}
```

Why `flatMap` twice and `map` once: the first two steps return `Option`s (so without flattening
you'd get `Option<Option<T>>`), while `.name` returns a plain `string`.

### 3. Result — errors with a reason, on rails

`Option` says *nothing happened*; usually you want to know *why*. `Result<T, E>` carries a payload
on success and error metadata on failure:

| Track | Type | Carries |
|---|---|---|
| Green | `Success` | the data (e.g. an `Employee`) |
| Red | `Failure` | error context (`"no employee found"`, `"no supervisor"`) |

The striking part of the talk: the pipeline body is **character-for-character the same** as the
`Option` version — only the signature moved from `Option<string>` to `Result<string, string>`. Same
code, new behaviour, because the branching lives inside the monad's `flatMap`.

```ts
function getSupervisorNameResult(employeeId: number, repo: ResultEmployeeRepository): Result<string, string> {
  return repo.get(employeeId)
    .flatMap(emp => emp.supervisorId)
    .flatMap(supId => repo.get(supId))
    .map(supervisor => supervisor.name);
}
```

Run against the sample hierarchy: a valid employee yields `Success("…")`; an employee with no
supervisor yields `Failure("no supervisor")`; an unknown id yields `Failure("no employee found")`.
This is Wlaschin's Railway Oriented Programming — and it beats exceptions on type safety
(failure is declared), explicitness (the compiler won't let you forget), and predictability (no
non-linear jumps in the call stack).

### 4. Promise — the same shape, now about time

Change `supervisorId: Promise<number>` and `get(id): Promise<Employee>`, and the same chain still
holds — except the operator is spelled `.then`:

```ts
function getSupervisorNamePromise(employeeId: number, repo: PromiseEmployeeRepository): Promise<string> {
  return repo.get(employeeId)
    .then(emp => emp.supervisorId)
    .then(supId => repo.get(supId))
    .then(supervisor => supervisor.name);
}
```

`.then` is `map` and `flatMap` fused into one polymorphic method — convenient, but it blurs the
distinction between transforming a value and flattening a context. The semantics are now
"resolve when every promise on the way resolves"; the *code* is unchanged.

### 5. Observable — the last stop

With `supervisorId: Observable<number>` and `get(id): Observable<Employee>`, the chain returns to
the cleaner two-operator form:

```ts
function getSupervisorNameObservable(employeeId: number, repo: ObservableEmployeeRepository): Observable<string> {
  return repo.get(employeeId)
    .flatMap(emp => emp.supervisorId)
    .flatMap(supId => repo.get(supId))
    .map(supervisor => supervisor.name);
}
```

In RxJS terms `flatMap` is what you now know as `mergeMap`/`concatMap` — `flatMap` is the older
name, `bind` the classical FP one. Piechocki explicitly calls this *better than promises* because
RxJS keeps `map` and `flatMap` separate. The semantics have shifted again — values changing over
time, streams flattened into streams — while the pipeline text stayed put.

### 6. So what is a monad?

Four wildly different concerns — emptiness, failure, latency, change-over-time — implemented with
one interface:

- `return`/`of`/`unit`: wrap a plain value (`new Some(x)`, `new Success(x)`, `Promise.resolve(x)`,
  `Observable.of(x)`)
- `flatMap`/`bind`: chain a function that returns another monad, flattening the result
- (`map` falls out of the two, and the monadic laws keep the behaviour consistent)

An array is a monad too — not quite in plain JavaScript, which lacks some of the operations, but it
becomes one with a library like Lodash.

The framing that ties it together: monads model **effects** polymorphically — optionality
(`Option`), error (`Result`), asynchrony (`Promise`), streaming (`Observable`) — where imperative
languages need a distinct language feature per effect (strict null checking, `try/catch`,
`async/await`). Because the interface is the same, the pipeline looks the same regardless of which
effect is in play.

### 7. Q&A (worth keeping)

- **Can you silence just one kind of error?** Yes — parameterise `Result<T, E>` with an error class
  hierarchy and add a `filter`-style operation that only handles certain error types. (The
  `monad-comparison-v2.ts` export implements exactly this as `filter` on the success value and
  `recover(predicate, recoveryFn)` on the error side, turning a matched `Failure` back into a
  `Success` while letting unmatched errors propagate.)
- **Performance / memory of wrapping every value?** A fair objection to the naive teaching
  implementation — use a real monadic library, which reuses objects and is cleverer about
  allocation, rather than hand-rolling for production.
- **What about exceptions thrown *inside* a monad?** You can write `Result` to catch and convert to
  `Failure`, but in general don't mix the two: exceptions belong to the imperative world, monads to
  the functional one.

## Claude Summary

_(Not separately generated — the Content section above is the synthesis.)_

## NLM

### Report — "Technical Design Specification: Monadic Error Handling & Optionality in TypeScript"

Reframes the talk as an internal architecture decision record: adopt monadic error handling to cut
runtime failures in the domain layer. Its argument:

- **Problem space.** Imperative null-checking fails to scale in three named ways — *boilerplate
  dominance* (most lines verify emptiness rather than do domain work), *context fragmentation*
  (the success path is constantly interrupted by "what if it's missing"), and *mental overhead*
  (developers manually track safety of every variable). The employee-supervisor pyramid inflates
  cyclomatic complexity while masking the trivial intent `Id → Employee → Supervisor → Name`.
- **Framework.** `Option<T>` as a tagged union (`Some`/`None`) for presence; `Result<T, E>` with an
  explicit green/red track table for failure-with-context.
- **Mechanics.** `map` = apply inside the box, preserving the container and auto-propagating the
  unhappy path; `flatMap` = required whenever the transform itself returns a monad, to avoid
  `Option<Option<T>>`. Architect's note: delegating branching to the monad's internals is what
  actually reduces cyclomatic complexity, yielding a linear pipeline.
- **Signature change as the deliverable.** `getEmployee(id): Employee | undefined` becomes
  `getEmployee(id): Option<Employee>` or `Result<Employee, string>` — the compiler now enforces
  acknowledgement of absence/failure.
- **Refactor trace.** `repository.get(id)` → `.flatMap(emp => emp.supervisorID)` →
  `.flatMap(id => repository.get(id))` → `.map(sup => sup.name)`, with the `Result` variant
  preserving `"no employee found"` / `"no supervisor"` context to the end of the pipeline.
- **Universality.** Promises (`.then` = map + flatMap) and Observables (`mergeMap`/`concatMap`)
  are the same abstraction applied to latency and streams; where C#/Java need `async/await` plus
  null-coalescing plus exceptions, the monad is one interface for all four.
- **Directive.** New service development starts with `Option`/`Result` — the payoff being
  eliminated defensive plumbing, declarative pipelines, and compile-time rather than runtime
  certainty.

### Report — "Beyond the Math: 5 Ways Monads Actually Make You a Better JavaScript Developer"

The popular-article rendering of the same material, structured as five practical wins:

1. **The if-statement killer (Option).** The "Tower of Ifs" is a design failure that obfuscates
   intent. `Some`/`None` plus `return` and `flatMap` reduce it to a one-liner; missing values carry
   `None` to the end without a runtime crash. The apple-in-a-box metaphor explains why `map` alone
   gives you a box within a box.
2. **Railway Oriented Programming (Result).** Exceptions are the "side-effect villains" that break
   flow; `flatMap` is the track switch, and a `Failure` shunts everything downstream to the red
   track. Errors become first-class citizens of the data flow rather than control-flow jumps.
3. **You're already using monads.** `Promise.resolve` is `return`/unit and `.then` is monadic
   composition; RxJS `map`/`flatMap` follow the Option pattern exactly. `.then` being polymorphic
   is called out as "messy" next to RxJS's clean split — knowing the difference between mapping a
   value and flattening a context is the junior/senior line.
4. **The programmable semicolon.** The semicolon is dumb glue; a monad lets you *program* the gap —
   null checks, error logging, callback waiting — so you write the "what" instead of the "how".
5. **Type safety.** With TypeScript, `undefined` stops being a ghost: absence enters the function
   signature, the compiler refuses to let you forget it, and code becomes a "stream of data
   transformations" rather than disconnected statements.

Closing line worth keeping: *the next time you're three levels deep in `if` statements, ask whether
a monad turns this into a one-liner.*

### Chat — effects, polymorphically

An "effect" is a computational context wrapping a raw value to handle one runtime concern. The four
from the talk map cleanly: **optionality** (`Option`), **error** (`Result`), **asynchrony**
(`Promise`), **streaming** (`Observable`). The power is polymorphism — imperative code needs strict
null checks *and* `try/catch` *and* `async/await` as separate language features, whereas a
standardised constructor (`return`/`of`) plus a standardised chaining operator (`flatMap`/`bind`)
makes all four pipelines look nearly identical. The monad silently governs how effects interact
(short-circuiting on `None`, propagating a rejection) while the codebase reads as pure business
logic.

### Chat — Haskell's `do` notation in TypeScript

Follow-up on the "programmable semicolon": TypeScript has no native monadic syntax sugar, but there
are three workarounds worth knowing:

1. **Builder pattern (`fp-ts` style)** — a threaded state object starting from an empty environment
   (`O.Do`), with key/value pairs progressively `.bind()`-ed in, keeping earlier variables in scope
   without nesting callbacks.
2. **Generator-based coroutines (Effect-TS style)** — `function*` plus `yield*` suspends on a
   monadic context; a custom runner either feeds the unwrapped value back into scope or
   short-circuits on failure. This is the approach modern frameworks standardised on.
3. **Compiler forks (TS+)** — real experiments generating native `do` syntax, abandoned in favour
   of generators for toolchain/bundler compatibility.

### Mindmap (condensed)

Definition (endofunctor monoid / value wrapper / programmable semicolon) → Problem (nested ifs,
undefined handling, obscured logic, callback hell) → Examples (Option: Some/None; Result:
Success/Failure + ROP; Promise: future results; Observable: reactive streams) → Core operations
(map, flatMap/bind, return, monadic laws) → Benefits (declarative style, boilerplate abstraction,
type safety, composition, readable pipelines).

### Quiz / flashcards

A 26-question multiple-choice set (`Monad-Quiz.md`, plus Quizlet-importable `.txt` and `.pptx`
versions, and a separate flashcard deck) covering the formal definition, `map` on `None`, why
`flatMap` exists, `.then` fusing both operations, the red track, the programmable semicolon,
`return`/`of`, why `Result` beats exceptions, the apple-in-a-box outcomes, the
use-a-library-for-performance answer, `flatMap` on a multi-value stream, and the "you don't need
category theory" claim. Useful as spaced-repetition material — the answers are all recoverable from
the Key Concepts above.

## Recall.ai

_(none)_

## Source

- **Talk:** Miłosz Piechocki, *"From Options to Observables: a monadic journey"* [EN], WarsawJS
  Meetup #43. Speaker's blog: `codewithstyle.info`; he also mentions a YouTube video course on
  functional reactive programming in Angular.
- **Local export dir:** `D:\Learning-Local-Hanss\Rxjs-From-Option-to-Observable-Piechoki`
  (exports dated 2026-08-13; no NotebookLM notebook URL captured — normal workflow is local export
  rather than the login-gated URL)
- **Files used:** `notebooklm-report-technical-design-specification-monadic-error-handl-2026-08-13.md`,
  `notebooklm-report-beyond-the-math-5-ways-monads-actually-make-you-a--2026-08-13.md`,
  `notebooklm-chat-thoughts-expand-morethat-statement-perfectly-captu-2026-08-13.md` (effects
  polymorphism), `notebooklm-chat-thoughts-expand-morehere-s-what-i-found-on-haskell-2026-08-13.md`
  (`do` notation in TS), `from-option-to-observable-mindmap.md`, `Monad-Quiz.md`,
  `monad-comparison-v2.ts` (primary source for the code in Content — includes the `filter`/`recover`
  extensions from the Q&A), and the talk transcript
  `Mi-osz-Piechocki_-From-Options-to-Observables_-a-monadic-journey-EN---WarsawJS-Meetup-43_cockaoo_transcript_basic.txt`
- **Referenced but not extracted:** `Mastering_Monadic_Pipelines.pptx` / `.pdf` and `slides.zip`
  (slide deck of the same material), `Monad-Flashcards.pptx`/`.html`, `Monad-Quiz.pptx`,
  `Deconstructing_the_Monad__From_Spaghetti_Code_to_Declarative_Pi.mp4`, the talk `.mp4`,
  `monad-comparison.ts` (superseded by v2), `from-option-to-observable-freemind.mm`,
  `from-option-to-observable-as-json.json`

## Notes

- **This is the missing bridge in the RxJS-from-FP story.** [[rxjs-from-fp-js-to-rxjs]] promises
  "the same 12 FP concepts rebuilt on streams"; this talk is the single sharpest demonstration of
  *why* that works — the pipeline body literally doesn't change across `Option`, `Result`,
  `Promise`, `Observable`. Worth stealing as the opening lesson: show one function four times.
- **Teaching order matters.** The talk earns `flatMap` by first showing `map` producing
  `Option<Option<T>>`. That's a better motivation for `mergeMap`/`concatMap` than any marble diagram
  — the nesting problem is felt before the operator is named. Ties to
  [[rxjs-operator-renaming]]: `flatMap` → `bind` → `chain` → `concatMap`/`mergeMap` is exactly the
  suffix-grammar problem, one root operation wearing four names across communities.
- **`.then` as an anti-pattern to teach against.** Promises fusing `map` and `flatMap` is why so
  many developers never develop the flattening intuition and then find `switchMap` baffling. RxJS's
  separation is a feature — say so explicitly when teaching.
- **The `recover` operation from the Q&A is the seed of `catchError`.** `recover(predicate, fn)` —
  match certain failures, convert back to success, let the rest propagate — is precisely selective
  `catchError`. Good exercise: implement `catchError` as `recover` on a hand-rolled Observable.
- **Open thread:** the generator-based `do`-notation approach (Effect-TS) is the interesting one for
  the RxJS course — worth a spike on whether a `yield*`-based runner makes multi-step Observable
  pipelines more readable than nested `switchMap`s, or whether it just hides the concurrency
  semantics that RxJS deliberately exposes.
- Piechocki's own framing — intuition first, category theory never — is the right stance for the
  course material; contrast with [[erik-meijer]] duality, which is the deep-theory end of the same
  spectrum.

## Related

- [[rxjs-from-fp-js-to-rxjs]] — the FP-concepts-on-streams course this talk motivates
- [[rxjs-fp]] — from-scratch functional RxJS (curried free operators, cold core)
- [[rxjs-pipe-compose]] — point-free composition; the pipeline-of-transformations idea applied to RxJS
- [[rxjs-operator-renaming]] — `flatMap`/`bind`/`chain`/`mergeMap` as one root under many names
- [[erik-meijer]] — Iterable/Observable duality, the theory end of the same story
- [[js-functional-programming-nlm]] — the 12-module FP-in-JavaScript course
- [[fp-guide]] — Mostly Adequate Guide, the book-length treatment of the same path to monads
- [[universal-algebra]] — operations-and-laws framing behind the monadic laws
