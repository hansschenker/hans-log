---
okf_version: "0.2"
---

# Hans Knowledge Base

Flat OKF bundle: every `.md` file is one concept with a frontmatter index card
(`type`, `title`, `description`, `resource`, `tags`, `timestamp`); markdown links
between files form the knowledge graph. Start at a topic hub and follow the links.

## Topics

- [RxJS](./rxjs.md) — reactive programming with RxJS — operators, taxonomy, heritage, FP architecture, and the deep-dive course work
- [Functional Programming](./functional-programming.md) — FP in JavaScript/TypeScript — currying, composition, combinators, monoids, monads, and the road from Option to Observable
- [RAG](./rag.md) — retrieval-augmented generation — patterns, strategies, document ingestion (Docling, LlamaParse), production pipelines
- [Claude Code](./claude-code.md) — working with Claude and Claude Code — courses, workflows, skills, models
- [Knowledge Graphs & Ontologies](./knowledge-graphs.md) — knowledge graphs, semantic web, RDF/OWL, Protege ontology engineering
- [AI Engineering](./ai-engineering.md) — AI engineering concepts, agentic engineering, LLM internals and transformers
- [Fitness & Longevity](./fitness.md) — trail running, training for the older athlete, VO2max and healthy aging

## All concepts by type

### Courses

- [01 Course Introduction - KMST](./01-course-introduction-kmst.md) — Plaban Kumar Bhowmik academic Semantic Web course (RDF, SPARQL, OWL, Linked Data); analyzed first video
- [Build Ontology in Protege (pizza.owl) - 01 Opening & Introduction](./build-ontology-in-protege-pizzaowl-01-opening-introduction.md) — Build pizza.owl in Protégé — 49-video hands-on OWL ontology-engineering course (Yasen Zhao); analyzed first video
- [Claude Mastery Lessons 031–045](./claude-mastery-031-045.md) — Master Claude Code lessons 031-045 — AskUserQuestion, spec developer, CLAUDE.md, MCP servers
- [JavaScript — Functional Programming for JavaScript Developers (Packt code repo)](./js-fp.md) — Packt course code repo
- [Functional Programming in JavaScript — 12-Module NotebookLM Course](./js-functional-programming-nlm.md) — NLM-authored 12-module video course — expression-orientation to Functional FizzBuzz, the source course the RxJS payoff course rebuilds on streams
- [Knowledge Graphs — Lecture 1: Knowledge Representation with Graphs (1.1–1.7)](./kg-lecture-1-knowledge-representation-with-graphs.md) — DIKW → triples/graphs → knowledge graphs → Semantic Web stack & Linked Data (videos 1.1–1.7)
- [Knowledge Graphs — Lecture 2: Basic Knowledge Graph Infrastructure (2.1–2.6)](./kg-lecture-2-basic-knowledge-graph-infrastructure.md) — URIs, RDF, Turtle, RDFS vocabularies, complex structures & RDFS inference (videos 2.1–2.6)
- [Knowledge Graphs - 0.0 Lecture Overview](./knowledge-graphs-00-lecture-overview.md) — first video: course roadmap across all 6 weeks
- [Knowledge Graphs - 1.0 Knowledge Representation with Graphs](./knowledge-graphs-10-knowledge-representation-with-graphs.md) — week-1 intro: DIKW ladder, graphs/triples, ontologies, Semantic Web, Linked Data
- [Master Claude Code Lectures 030–045 — Manage Claude.md](./master-claude-030-045.md) — managing CLAUDE.md — hierarchical files, project vs user rules, best practices
- [Production RAG with LangChain & Vector Databases – Full Course](./production-rag-with-langchain-vector-databases-full-course.md) — end-to-end production RAG build
- [Protégé Pizza Tutorial (yasenstar/protege_pizza)](./protege-pizza.md) — classic hands-on pizza.owl OWL ontology tutorial for Protégé (Yasen/DeBellis)
- [From FP-JS to RxJS — The RxJS Payoff Course](./rxjs-from-fp-js-to-rxjs.md) — the RxJS payoff course — the same 12 FP-in-JavaScript concepts, one per module, rebuilt on streams with runnable strict-TS demos
- [Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 2 - Transformer-Based Models & Tricks](./stanford-cme295-transformers-llms-autumn-2025-lecture-2.md) — RoPE, RMSNorm, MQA/GQA, T5 vs BERT vs decoder-only
- [TypeScript Workshop — TypeScript in the Age of AI (Adam Rackis)](./typescript-workshop.md) — advanced type-system workshop — generics, conditional/mapped/template-literal types, variance — aimed at reading and verifying AI-generated code

### Videos

- [12 Important Concepts In the Age of AI Software Development](./12-important-concepts-in-the-age-of-ai.md) — mental models for AI-era dev
- [160,000+ Cloned These 3 FREE AI Employees: Here's How (GitHub Claude Skills)](./160000-cloned-these-3-free-ai-employees-heres.md) — LLM council, last-30-days sentiment scan, virtual dev team
- [Docling an intro to LLM 4](./ai-docling-intro-llm-4.md) — Docling is the preparation for LLM
- [AI Engineering Explained in 17 mins | The Ultimate Beginner’s Guide](./ai-engineering-explained-in-17-mins-the-ultimate.md) — LLM + Tools/Knowledge/Memory = agent; evals, multi-agent, AI Ops
- [AI Engineering was HARD until I Learned these 10 Concepts](./ai-engineering-was-hard-until-i-learned-these.md) — core AI engineering mental models
- [Build Agentic RAG With Claude Code](./build-agentic-rag-with-claude-code.md) — four-layer codebase RAG pipeline in Claude Code; ~10x less token burn
- [Building Production RAG Over Complex Documents](./building-production-rag-over-complex-documents.md) — Databricks talk on production RAG over complex docs
- [Claude Cowork Private Lesson](./claude-cowork-private-lesson.md) — different ways to use Claude Cowork
- [Claude Fable 5 Is BACK! Should You Still Use Opus? (Real Test)](./claude-fable-5-is-back-should-you-still.md) — when to pick Fable 5 vs Opus for coding
- [Docling — prepare pdf and other doc formats for working with AI and RAG](./docling-pdf-for-ai-rag.md) — prepare pdf and other doc formats for working with AI and RAG
- [Effects as Data | Richard Feldman | Reactive 2015](./effects-as-data-richard-feldman-reactive-2015.md) — modeling side effects as data, the Elm architecture
- [Every RAG Strategy Explained in 13 Minutes (No Fluff)](./every-rag-strategy-explained-in-13-minutes-no.md) — compact no-fluff tour of RAG strategy options
- [Google Just Dropped a Masterclass on Agentic Engineering (It's SO Good)](./google-just-dropped-a-masterclass-on-agentic-engineering.md) — walkthrough of Google's agentic engineering guide
- [Google OKF + Claude : Why We Stopped Using RAG](./google-okf-agent-memory.md) — agent memory as a folder of linked markdown files — OKF standardizes it; files + grep beat vector DBs
- [I Spent a Day With Anthropic Engineers. Here's Their REAL Workflow.](./i-spent-a-day-with-anthropic-engineers-heres.md) — no secret workflow: plan light, verify where users meet the change, review loops
- [Import EVERYTHING Into Your RAG Agent (Docling & LlamaParse)](./import-everything-into-your-rag-agent-docling-llamaparse.md) — 95+ formats to markdown: LlamaParse vs Docling vs Mistral OCR
- [Intent-driven development with Claude Code & Fable 5](./intentdriven-development-with-claude-code-fable-5.md) — spec/intent-first workflow driving Claude Code
- [Multi-modal RAG with Docling: From PDF to Agentic AI Chatbot](./multimodal-rag-with-docling-from-pdf-to-agentic.md) — PDF images captioned via LLM into enriched text, Milvus + LangGraph agent
- [OWL (Web Ontology Language) — three-video primer](./owl-web-ontology-language.md) — OWL 2 ontology language for the semantic web
- [RAG Explained in 14 Minutes | 10 RAG Patterns Every AI Engineer Must Know (2026)](./rag-explained-in-14-minutes-10-rag-patterns.md) — 10 RAG patterns every AI engineer must know, in 14 minutes
- [RAG vs Agentic AI: How LLMs Connect Data for Smarter AI](./rag-vs-agentic-ai-how-llms-connect-data.md) — when retrieval beats agents and vice versa
- [ReactiveConf 2016 - André Staltz: Visualizing the data flow with Cycle.js](./reactiveconf-2016-andr-staltz-visualizing-the-data-flow.md) — André Staltz: Visualizing the data flow with Cycle.js — visualize reactive dataflow in Cycle.js
- [None](./rxjs-74-subjects.md) — Subject as both observer and observable, multicasting
- [I switched a map and you'll never guess what happened next - Pete Darwin, Shai Reznik, Mike Brocchi](./rxjs-switchmap-deep-dive.md) — when to cancel vs merge inner observables, key for HTTP autocomplete
- [Training for the Older Athlete](./training-older-athlete.md) — training adaptations for masters athletes — recovery, intensity, and strength for aging runners
- [What is JSON-LD?](./what-is-json-ld.md) — JSON-based format for linked data on the semantic web

### Concepts

- [Learn RAG Architecture](./ai-claude-rag-architecture.md) — chunking strategies: fixed-size, semantic, hierarchical small-to-big
- [From Options to Observables — a monadic journey (Miłosz Piechocki, WarsawJS](./from-option-to-observable.md) — Option monad → Observable, a monadic journey (NotebookLM)
- [JavaScript Combinators — Deriving leftApply, rightApply, and Friends](./javascript-combinators.md) — Braithwaite's derivation — partial application decomposes a function's interface outside-in, and repeated extraction ends at named combinators like C
- [RxJS Heritage — from LINQ and Rx.NET](./rxjs-heritage.md) — RxJS heritage from LINQ and Rx.NET (NotebookLM)
- [A Formal Taxonomy of RxJS Observables](./rxjs-observable-taxonomy.md) — invariant semantics vs. variable execution characteristics vs. style; cold/hot ⟂ unicast/multicast (NotebookLM)
- [RxJS Operator Renaming — The Suffix Grammar](./rxjs-operator-renaming.md) — suffix grammar 'keep the root, fix the suffix': curried roots × boundary combinators (NotebookLM)
- [Pipe vs Compose — Point-Free Composition in RxJS FP Architecture](./rxjs-pipe-compose.md) — Point-Free Composition in RxJS FP Architecture — currying, point-free style, hybrid FP-RxJS case study (NotebookLM)
- [RxJS Operator Taxonomy — The 22-Axis Fingerprint Model](./rxjs-taxonomy.md) — every operator is a point in a 22-axis behavior space — lossy/lossless is one axis, and confused operators are neighbors differing on a single axis
- [Turtle (Terse RDF Triple Language)](./turtle-syntax.md) — Terse RDF Triple Language, compact text serialization for RDF graphs
- [Universal Algebra — Operations + Laws as a General Theory](./universal-algebra.md) — an algebra is just a set with operations satisfying equational laws — the single lens behind monoids, functor laws, and lawful APIs
- [Vo2max — Fifth Vital Sign](./vo2max.md) — vo2max is the result of all 5 vital signs working together
- [What Is a Model](./what-is-a-model.md) — model as static blueprint vs dynamic state machine — from FSM theory to distributed retry architecture

### Articles

- [Erik Meijer — Subject/Observer is Dual to Iterator (the Rx Duality)](./erik-meijer.md) — the two-page paper where Rx is derived, not designed — dualize IEnumerable/IEnumerator mechanically and IObservable/IObserver falls out
- [Kleisli Compositions in JavaScript](./kleisli-compositions-js.md) — Luis Atencio on Kleisli composition in JS
- [RxJS & PouchDB — Persistent Data Flows](./pouchdb-article.md) — Luis Atencio on persistent data flows with RxJS + PouchDB

### References

- [Offline-First Apps with Angular, Ionic & CouchDB](./couchdb-repo.md) — offline-first sample app repo
- [crocks Combinators — applyTo, composeB, converge, psi, substitution & friends](./fp-combinators.md) — combinator helpers (composeB, substitution, applyTo) in the crocks FP library
- [crocks Functions — the whole library index, by category](./fp-functions.md) — index of crocks' point-free helper functions
- [Professor Frisby's Mostly Adequate Guide to Functional Programming](./fp-guide.md) — the classic FP-in-JavaScript book, currying → monads
- [crocks Monoids — Prod, and the shared empty/concat interface](./fp-monoids.md) — multiplicative monoid, concat/empty laws in the crocks library
- [IxJS — Interactive Extensions for JavaScript](./interactive-rx.md) — the pull-based dual of RxJS — LINQ-style operators over Iterable/AsyncIterable, where the consumer controls the pace
- [Harald Sack — Presentations (Knowledge Graphs & Ontologies)](./ontology-expert.md) — Harald Sack's presentation slides on knowledge graphs & semantic web
- [Matthew Horridge (Protégé / OWL author)](./protege-author-matthew-horridge.md) — author of the original Protégé/OWL ontology-building guide (GitHub)
- [rxjs-fp — A Functional-Style RxJS Built From Scratch](./rxjs-fp.md) — from-scratch functional RxJS: cold core, curried free operators, no prototype patching
