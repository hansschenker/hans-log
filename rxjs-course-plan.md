# RxJS Course Plan

**Goal:** Build and publish a complete RxJS course
**Daily budget:** 2 hours/day
**Start:** 2026-06-24
**Target:** 2026-09-30 (~14 weeks, ~196 hours)
**Content base:** `C:/Users/hanss/Local-Learning/Rxjs/`

---

## Course Structure

8 modules derived from existing content, plus operator reference and capstone.

| # | Module | Source file |
|---|---|---|
| 1 | History, Origins & Evolution | Rxjs-Course-Modules/Module-1 |
| 2 | Functional Programming Foundations | Rxjs-Course-Modules/Module-2 |
| 3 | RxJS as FRP | Rxjs-Course-Modules/Module-3 |
| 4 | Core Concepts: Observable, Observer, Subscription | Rxjs-Course-Modules/Module-4 |
| 5 | Operators Deep Dive (7 families) | Rxjs-Course-Modules/Module-5 |
| 6 | Pipelines as a DSL | Rxjs-Course-Modules/Module-6 |
| 7 | Custom Operators | Rxjs-Course-Modules/Module-7 |
| 8 | Testing with Marble Diagrams | Rxjs-Course-Modules/Module-8 |
| R | Operator Reference (8-policy framework) | Rxjs-Artifacts-Claude-Desktop/rxjs-operator-policies.md |
| C | Capstone: Reactive SPA Framework | Rxjs-Course-Modules/Rxjs-spa-extended.md |

---

## Phases & Weekly Plan

### Phase 1 — Foundation & Setup (Week 1–2, ~28 hrs)
*What:* Course scaffolding, tooling, intro module draft, study path alignment
*Daily rhythm:* 1hr content writing + 1hr code examples

| Week | Days | Work |
|---|---|---|
| 1 | Mon–Fri | Set up course repo structure, README, code sandbox template |
| 1 | Sat–Sun | Draft Module 1: History — Haskell → LINQ/Rx.NET → RxJS lineage |
| 2 | Mon–Fri | Draft Module 2: FP Foundations — functors, applicatives, monads |
| 2 | Sat–Sun | Review + code examples for Modules 1–2, add marble diagrams |

**Deliverable:** Course repo live, Modules 1–2 complete with code examples.

---

### Phase 2 — Core Concepts (Week 3–5, ~42 hrs)
*What:* The foundational RxJS building blocks — the heart of the course

| Week | Days | Work |
|---|---|---|
| 3 | Mon–Fri | Draft Module 3: FRP — declarative vs imperative, space/time abstraction |
| 3 | Sat–Sun | Draft Module 4 Part A: Observable, Observer, Subscription, lifecycle |
| 4 | Mon–Fri | Draft Module 4 Part B: Schedulers, Subject, hot vs cold observables |
| 4 | Sat–Sun | Code examples for Modules 3–4, hot/cold matrix, Subject patterns |
| 5 | Mon–Sun | Review Modules 1–4 end-to-end, polish, add quizzes/checkpoints |

**Deliverable:** Modules 1–4 production-ready. Core RxJS concepts fully covered.

---

### Phase 3 — Operators & DSL (Week 6–8, ~42 hrs)
*What:* The practical heart — operators, pipelines, the DSL philosophy

| Week | Days | Work |
|---|---|---|
| 6 | Mon–Fri | Draft Module 5 Part A: Transform & Filter families with marble diagrams |
| 6 | Sat–Sun | Draft Module 5 Part B: Flatten strategies (mergeMap/switchMap/concatMap/exhaustMap) |
| 7 | Mon–Fri | Draft Module 5 Part C: Combine, Window/Buffer, Error Handling, Utility |
| 7 | Sat–Sun | Draft Module 6: Pipelines as DSL — pipe(), outcome-trigger naming, clean pipelines |
| 8 | Mon–Sun | Code examples for Modules 5–6, form validation case study, review |

**Deliverable:** Modules 5–6 complete. All 7 operator families with marble diagrams and code.

---

### Phase 4 — Advanced Topics (Week 9–11, ~42 hrs)
*What:* Custom operators, testing, operator reference

| Week | Days | Work |
|---|---|---|
| 9 | Mon–Fri | Draft Module 7: Custom Operators — composition-first, business logic operators |
| 9 | Sat–Sun | Custom operator code examples: typeahead, authorization guard |
| 10 | Mon–Fri | Draft Module 8: Testing — TestScheduler, marble syntax, virtual time |
| 10 | Sat–Sun | Testing code examples, cold/hot observable test patterns |
| 11 | Mon–Sun | Build Operator Reference section from 8-policy framework + 100+ operators |

**Deliverable:** Modules 7–8 + Operator Reference complete.

---

### Phase 5 — Capstone & Polish (Week 12–14, ~42 hrs)
*What:* Reactive SPA capstone, full review, course publishing

| Week | Days | Work |
|---|---|---|
| 12 | Mon–Sun | Draft Capstone: Reactive SPA — MVU state engine, reactive router, custom domain operators |
| 13 | Mon–Sun | Full course review: consistency, progression, gaps. Add intro/outro per module |
| 14 | Mon–Sun | Final polish, publish-ready formatting, course landing page copy |

**Deliverable:** Complete course published. All 8 modules + reference + capstone.

---

## Daily 2hr Work Block

```
Hour 1 — Content (writing, structuring, explaining)
  - Draft or refine a section
  - Write explanations in plain language
  - Add diagrams / marble diagrams

Hour 2 — Code (examples, exercises, solutions)
  - Build runnable TypeScript examples
  - Write exercises for students
  - Verify marble diagram code with TestScheduler
```

---

## Key Content Assets (already built)

| Asset | Location | Use in course |
|---|---|---|
| RxJS_Study_Path.md | Rxjs/ | Course navigation map, stage checkpoints |
| RxJS_Gesamtuebersicht.md | Rxjs/ | Module overviews, through-line narrative |
| rxjs-operator-policies.md | Rxjs-Artifacts-Claude-Desktop/ | Operator Reference section |
| Rxjs-operator-policy-renaming-operators-chatgpt.md | Rxjs-8-Policies/ | Operator story framework, 100+ operator docs |
| Rxjs-spa-extended.md | Rxjs-Course-Modules/ | Capstone module |
| Module-1 through Module-8 | Rxjs-Course-Modules/ | Direct module drafts |
| rxjs-operator-policies.md | Rxjs-Artifacts-Claude-Desktop/ | Policy framework, testing templates |

---

## Progress Tracker

| Module | Status | Hours spent | Done by |
|---|---|---|---|
| Setup & scaffolding | todo | 0 | 2026-07-04 |
| Module 1: History | todo | 0 | 2026-07-06 |
| Module 2: FP Foundations | todo | 0 | 2026-07-11 |
| Module 3: FRP | todo | 0 | 2026-07-18 |
| Module 4: Core Concepts | todo | 0 | 2026-07-25 |
| Module 5: Operators | todo | 0 | 2026-08-08 |
| Module 6: DSL Pipelines | todo | 0 | 2026-08-15 |
| Module 7: Custom Operators | todo | 0 | 2026-08-22 |
| Module 8: Testing | todo | 0 | 2026-08-29 |
| Operator Reference | todo | 0 | 2026-09-05 |
| Capstone: Reactive SPA | todo | 0 | 2026-09-12 |
| Full review & polish | todo | 0 | 2026-09-26 |
| Published | todo | 0 | 2026-09-30 |
