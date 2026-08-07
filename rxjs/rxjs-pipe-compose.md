---
slug: rxjs-pipe-compose
title: Pipe vs Compose — Point-Free Composition in RxJS FP Architecture
date: 2026-08-07
tags: [rxjs, fp, composition, architecture]
source: rxjs
---

## TL;DR

Standalone `pipe`/`compose` are pure higher-order functions, fully decoupled from any Observable —
`compose` builds pure business-rule transformations (`State ⇒ State`, right-to-left, point-free,
aligned with mathematical `f∘g∘h` notation), and RxJS's `pipe` lifts that pure logic into the
reactive layer (`Observable<State> ⇒ Observable<State>`, left-to-right) via `map`. There is no
computational difference between `pipe` and `compose` — only a stylistic signal of intent — but
using both together gives a strict separation between the "what" (business rules, tested without
any Observable) and the "how" (async timing, cancellation, sharing).

## Key Concepts

- **Standalone `pipe(f, g, h)` is a pure higher-order function** that returns a new unary
  function — it doesn't touch an Observable; the source is only supplied when the *returned*
  function is called. Contrast with `Observable.prototype.pipe`, which is bound to an instance.
- **Currying → partial application.** `const addCurried = a => b => a + b` is the structural
  pattern; `addCurried(5)` "freezes" the first argument, producing a reusable, type-safe
  `addFive` function. Currying is the structure; partial application is the act of freezing.
- **`pipe` = left-to-right**, "data flow intuition" (`Input → Output`) — best for sequential data
  processing and reactive pipelines, and it lets `catchError` sit naturally at the end, matching
  the sequence of failure.
- **`compose` = right-to-left**, matches mathematical notation `(f∘g∘h)(x) = f(g(h(x)))`, and is
  the gateway to **point-free programming** — defining functions without naming the argument
  they operate on. Best for pure function factories / small DSLs of business rules.
- **The curry-order myth, debunked.** A common belief is that `compose` is "required" because it
  matches curried call order (`f(g(x))`). False — curried functions are always called right-to-left
  regardless of whether you assemble them with `pipe` or `compose`; both produce identical results
  if the logical sequence is preserved. The choice between them is purely about whether you think
  from the source forward (`pipe`) or the goal backward (`compose`).
- **Hybrid architecture — the payoff pattern.** `compose` assembles curried, pure `State ⇒ State`
  business rules into one pure transformation; that pure function is then lifted with `map` inside
  RxJS's standalone `pipe`, producing `Observable<State> ⇒ Observable<State>`. `compose` answers
  *"what happens to one value?"*, RxJS `pipe` answers *"what happens to values arriving over
  time?"* — a genuine separation of concerns, not just a style choice.
- **The FP style doesn't change RxJS semantics.** `map(pureFn)` introduces no independent clock,
  no inner Observable, and therefore no flattening/cancellation policy of its own — timing comes
  entirely from the source, and unsubscription propagates through the normal subscription chain.
  Sharing (`shareReplay`, etc.) stays an explicit, separate architectural decision layered on top.
- **Point-free is a consequence, not a goal.** Drop the explicit `cart =>` / `cart$ =>` wrapper
  only when the resulting composition is *clearer* — don't force it when naming a value would aid
  debugging, branching, or domain readability.
- **Architectural formula:** `configure → partially apply → compose (pure) → lift via map → pipe
  (reactive) → apply to source$ → subscribe`.
- **Best practices called out across sources:** operator purity (side effects isolated to
  dedicated "Effect" operators), single responsibility (if a function is hard to name, split it),
  immutability (always return new references), descriptive/declarative naming
  (`doubleThenAddFive`, `cartTotalPipeline`).

## Content

### 1. Two kinds of "pipe" and why the distinction matters

The RxJS package exports two things people conflate: `Observable.prototype.pipe`, a method bound
to a stream instance, and a **standalone `pipe` function**, a pure utility that composes plain
functions and has nothing to do with Observables. The standalone version is a genuine
higher-order function: `pipe(f, g, h)` doesn't execute anything — it returns a new unary function,
and the initial value is only supplied when *that* function is called later. This is what makes
standalone `pipe` (and `compose`) usable on **any** data — plain objects, strings, domain state —
not just streams, and it's the foundation for keeping business logic reactive-framework-agnostic.

### 2. Currying is the mechanical enabler

Currying transforms an `n`-argument function into `n` single-argument functions:
`const addCurried = a => b => a + b`. **Currying** is the structural shape; **partial
application** is the runtime act of supplying some arguments early and getting back a specialized
function that "remembers" them:

```ts
const addCurried = a => b => a + b;
const addFive = addCurried(5);   // partial application
const result = addFive(10);       // 15
```

This is what lets an architect build pipelines incrementally — supplying configuration at one
layer of the app and data at another — while keeping each step single-responsibility and
side-effect free.

### 3. Choosing `pipe` vs `compose`

| Operator | Execution order | Mental model | Best use case |
|---|---|---|---|
| `pipe` | Left-to-right | Input → Output | Sequential data pipelines; reactive/async streams; terminal `catchError` |
| `compose` | Right-to-left | Final ← First | Point-free function factories; pure business-rule DSLs |

Both are computationally identical for the same logical sequence — the choice is about whether the
reader should think "start at the source" (`pipe`) or "start at the goal" (`compose`). `pipe` wins
for reactive plumbing because errors flow the same direction as the data, so `catchError` reads
naturally at the tail of the chain; `compose` wins for backend/state-machine logic where
mathematical, point-free symmetry keeps a pipeline of business rules readable as one expression.

### 4. Worked example — a shopping cart, three layers of composition

The case study used throughout (in slightly different variable values across sources, but the
same shape) is a cart made of curried, pure `CartState ⇒ CartState` operations:

```ts
export interface CartItem { id: string; name: string; price: number; quantity: number }
export interface CartState { items: CartItem[]; total: number }
export interface Discount { active: boolean; minAmount: number; rate: number }
export type CartTransform = (cart: CartState) => CartState;

type Endomorphism<A> = (value: A) => A;
export const compose =
  <A>(...functions: Endomorphism<A>[]): Endomorphism<A> =>
  (value) => functions.reduceRight((result, fn) => fn(result), value);

const calculateTotal = (items: CartItem[]): number =>
  items.reduce((sum, item) => sum + item.price * item.quantity, 0);

export const addItem = (item: CartItem): CartTransform => (cart) => {
  const items = [...cart.items, item];
  return { items, total: calculateTotal(items) };
};

export const updateQuantity = (itemId: string, quantity: number): CartTransform => (cart) => ({
  items: cart.items.map(i => i.id === itemId ? { ...i, quantity } : i),
  total: calculateTotal(cart.items.map(i => i.id === itemId ? { ...i, quantity } : i)),
});

export const applyDiscount = (discount: Discount): CartTransform => (cart) => {
  const subtotal = calculateTotal(cart.items);
  if (!discount.active || subtotal < discount.minAmount) return { ...cart, total: subtotal };
  return { ...cart, total: subtotal * (1 - discount.rate) };
};
```

**Layer 1 — partial application.** `addItem(productA)`, `applyDiscount(discount)`,
`updateQuantity('A', 2)` each freeze their configuration now; the `CartState` arrives later. Every
expression becomes a reusable `CartState ⇒ CartState` unary transform.

**Layer 2 — pure composition.** Several `CartState ⇒ CartState` transforms collapse into one via
`compose`, entirely point-free (no `cart =>` appears anywhere):

```ts
const transformCart = compose(
  applyDiscount(discount),
  updateQuantity('A', 2),
  addItem(productB),
  addItem(productA),
);
// runtime order (right-to-left): addItem(A) → addItem(B) → updateQuantity → applyDiscount
```

**Layer 3 — reactive composition.** The pure `transformCart` is lifted into the Observable world
with a single `map`, wrapped in RxJS's *standalone* `pipe` so the whole thing is itself a reusable,
point-free operator:

```ts
const transformCart$: MonoTypeOperatorFunction<CartState> = pipe(
  map(transformCart),
);

const finalCart$ = transformCart$(of(initialCart));
finalCart$.subscribe(cart => console.log(cart));
// productA(20) qty2 + productB(30) qty1 = 70; discount ≥60 @10% → 63
```

Additional RxJS behavior (`distinctUntilChanged`, `tap`, `shareReplay`) composes onto
`transformCart$` without ever touching `transformCart` — the cart *rules* stay pure and
Observable-free, and are testable with plain function calls, no `TestScheduler` required.

### 5. Selection guide

| Requirement | Recommended choice | Rationale |
|---|---|---|
| Reactive UI / events | `pipe` as a method | Async streams; terminal `catchError` placement |
| Backend / state machines | `compose` standalone | Point-free abstraction, mathematical symmetry |
| Data-cleaning utilities | Standalone `pipe` | Left-to-right flow is the most readable for a straight transform chain |

## NLM

Condensed from the individual NotebookLM exports (each is a different framing of the same
material — kept separately here so the original angle isn't lost in the merged Content above):

**"Architectural Design Specification: Functional Composition in Reactive Systems"** — the most
formal write-up; frames the shift from `.pipe()` method-chaining to standalone composition as a
prerequisite for modularity ("logic is trapped within the reactive framework" under method
chaining). Introduces the Method-Based vs. Standalone comparison table and the "Discount Rule"
cart case study almost verbatim to what's above. Closing line: "The ultimate goal ... is to move
beyond the limitations of method chaining, achieving a level of clarity and structural integrity
required for sophisticated, high-scale business applications."

**"Beyond the Stream: 4 Surprising Truths About RxJS Pipe and Compose"** — lighter, listicle-style
piece built around quotable one-liners: *"The key insight is that pipe is just a function that
composes other functions — you don't need an Observable to use it!"* and *"Business logic remains
in pure functional pipelines (compose), while the reactive plumbing (asynchrony, side effects) is
handled by RxJS (pipe)."* Frames the hybrid pattern as "the Power Couple" and ends on: "is it
organized by *how it works* or *what it does*?"

**"Function-Composition-with-Pipe-and-Compose" (mindmap)** — bare outline confirming the same
top-level structure: Pipe Operator (left-to-right, standalone pure function, key benefits:
reusability, isolated testability, readability, flexible data compatibility) / Compose Function
(right-to-left, mathematical alignment, point-free, abstract function factories) / Currying and
Partial Application / Selecting Composition Operators / Shopping Cart Use Case / Best Practices.

## Source

- **Local export dir:** `D:\Learning-Local-Hanss\Rxjs-Fp` (exports dated 2026-08-07; no NotebookLM
  notebook URL captured — Hans's normal workflow is to download NotebookLM exports locally rather
  than share the login-gated URL)
- **Files used:** `Architectural Design Specification_ Functional Composition in Reactive
  Systems.md`, `Beyond the Stream_ 4 Surprising Truths About RxJS Pipe and Compose.md`,
  `Function-Composition-with-Pipe-and-Compose.md`, `Rxjs-FP-Style-Architecture.md` (most complete —
  primary source for the Content section's code and the "three composition layers" / RxJS-semantics
  framing)
- **Referenced but not extracted:** `Architecting_Business_Readable_Pipelines.pptx` (slide deck,
  same material), `Transforming_Reactive_Code.mp4`, `Pipe,_Compose___RxJS.mp4`, `meijer.duality.pdf`
  (Erik Meijer duality material — deeper category-theory source, not yet mined)
- **Not used here:** `rxjs-fp-mindmap-markdown.md` and `rxjs-fp-style.txt`/`rxjs-fp.txt` in the same
  dir are about the [[rxjs-fp]] project itself, not this pipe/compose topic — see Notes below

## Notes

- The same directory (`Rxjs-Fp`) now holds two distinct bodies of material: the original
  [[rxjs-fp]] project session log (2026-08-05) and this newer, general-purpose pipe/compose
  NotebookLM export (2026-08-07). `rxjs-fp-mindmap-markdown.md` in this dir is a NotebookLM
  mindmap of the **rxjs-fp project itself** (Tier 1–3 effect boundaries, two-layer naming) —
  that belongs as a supplement to [[rxjs-fp]], not to this note.
- [[rxjs-fp]]'s Key Concepts already states the terse version of the pipe/compose distinction
  (`pipe(source$, op1, op2)` runs a pipeline; `compose(op1, op2)` builds a reusable operator) — this
  note is the deep-dive behind that one-liner: why compose is right-to-left/point-free, why pipe is
  better for terminal error handling, and the explicit "compose = what, RxJS pipe = how" hybrid
  architecture.
- Genuinely new information for me: the debunking of the "compose matches curried call order"
  myth. All four sources independently insist there's no technical requirement — it's purely
  stylistic — which is worth remembering next time a design review claims otherwise.

## Related

- [[rxjs-fp]] — the project this composition pattern applies to; shares the curried/`pipe`/
  `compose` vocabulary but at project-architecture scale rather than a single pattern
- [[rxjs-operator-renaming]] — the sibling composition thesis (curried roots × boundary
  combinators) from the same NotebookLM-export workflow
