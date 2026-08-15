---
type: course
title: TypeScript Workshop — TypeScript in the Age of AI (Adam Rackis)
description: advanced type-system workshop — generics, conditional/mapped/template-literal types, variance — aimed at reading and verifying AI-generated code
resource: https://github.com/arackaf/fm-typescript-workshop
tags: [typescript, course, type-system, generics, ai-engineering]
timestamp: 2026-08-15
---

# TypeScript Workshop — TypeScript in the Age of AI (Adam Rackis)

## TL;DR

Companion repository for Adam Rackis's **"TypeScript in the Age of AI"** workshop: ten numbered modules of advanced type-system material — generics, discriminated unions, `satisfies`, conditional types, function overloading, template literal types, variance, mapped types — with exercises and solutions for hands-on practice. The framing is what makes it current: when an AI writes much of your TypeScript, the human's job shifts to *reading* sophisticated typed code and spotting where it's wrong, so deep type-system fluency becomes a verification skill, not just an authoring one.

## Key Concepts

- **The premise** — master the type system to understand and work with AI-generated code; the course emphasis is identifying errors in complex code, not writing types from scratch.
- **Module ladder** — `module-0-Foundations` → `1-Tips-and-Tricks` → `2-Generics` → `3-Unions` → `4-Satisfies` → `5-Conditional-Types` → `6-Function-Overloading` → `7-Template-Literal-Types` → `8-Variance` → `9-Mapped-Types`; several modules ship paired exercises and solutions.
- **The advanced-TS toolbox covered** — generics, conditional types, discriminated unions, template literal types, mapped types, function overloading, type variance, and the `satisfies` operator.
- **Practical shape** — a `package.json` for dependencies, prettier config, slides hosted on Google Drive; a lean exercises-first repo rather than a book.

## Content

**Why "in the Age of AI".** The workshop's bet is that the type system is the highest-leverage code-review tool available when agents generate code: discriminated unions make illegal states unrepresentable, `satisfies` checks a value against a type *without* widening it, conditional and mapped types encode API contracts the compiler then enforces on whatever the AI produced, and variance explains the assignability surprises that otherwise read as compiler noise. Fluency in these is what lets a reviewer say *precisely* why generated code is wrong.

**Where it sits in this bundle** *(annotation)*: the same skills carry the FP cluster's TypeScript work — discriminated unions are exactly the tagged unions behind `Option`/`Result` in [From Options to Observables](./from-option-to-observable.md), and the strict no-`any` demo discipline of [the RxJS payoff course](./rxjs-from-fp-js-to-rxjs.md) leans on generics and inference throughout. It pairs with [js-fp](./js-fp.md) as the other course-repo log entry of the same week — that one teaches the FP concepts, this one the type machinery to express them safely.

## Source

- GitHub: https://github.com/arackaf/fm-typescript-workshop (README + module layout read 2026-08-15). Logged as a Frontend Masters workshop; the README describes itself as companion to the "TypeScript in the Age of AI" course on Master.dev — same author, the `fm-` prefix reflects the Frontend Masters lineage.

## Notes

- First mostly-TypeScript node in the bundle — if TS notes accumulate (candidate: Gabriel Vergnaud's `type-level-typescript-workshop`, logged 2026 under the old `ts` tag), a `typescript` hub becomes worth creating.
- Course hook: Module 8 (variance) is directly relevant to RxJS teaching — `IObservable<out T>` / `IObserver<in T>` in the [Meijer duality paper](./erik-meijer.md) are variance annotations; a segment connecting the two would land well.

## Related

- [JavaScript — Functional Programming for JavaScript Developers (Packt code repo)](./js-fp.md) — the sibling course-repo entry: FP concepts there, type machinery here
- [From FP-JS to RxJS — The RxJS Payoff Course](./rxjs-from-fp-js-to-rxjs.md) — strict-TS demos that exercise this workshop's toolbox
- [From Options to Observables — a monadic journey](./from-option-to-observable.md) — discriminated unions in anger: `Option`/`Result` as tagged unions
- [Erik Meijer — Subject/Observer is Dual to Iterator (the Rx Duality)](./erik-meijer.md) — `out T`/`in T`: variance doing real work in the Rx interfaces

---

Part of: [AI Engineering](./ai-engineering.md)
