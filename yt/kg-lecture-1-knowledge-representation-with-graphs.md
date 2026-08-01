---
slug: kg-lecture-1-knowledge-representation-with-graphs
title: "Knowledge Graphs — Lecture 1: Knowledge Representation with Graphs (1.1–1.7)"
channel: ISE FIZ Karlsruhe (Prof. Harald Sack)
date: 2026-08-01
url: https://www.youtube.com/playlist?list=PLNXdQl4kBgzubTOfY5cbtxZCgg9UTe-uF
type: summary
language: en
tags: [yt, cs, knowledge-graphs, semantic-web, ontology, rdf, linked-data, owl, sparql]
source: yt
---

# Knowledge Graphs — Lecture 1: Knowledge Representation with Graphs (1.1–1.7)

*Summary of the 7 opening sub-videos (1.1–1.7, ~10 min each) of Harald Sack's OpenHPI 2023 "Knowledge Graphs — Foundations and Applications" course. Transcripts fetched and synthesized; full transcripts not stored.*

## TL;DR

Week 1 of Harald Sack's **Knowledge Graphs** course builds a single arc: **why data alone is worthless, and how to turn human meaning into machine-understandable knowledge**. It starts at the **DIKW pyramid** (data → information → knowledge → wisdom) and the nature of understanding, then formalizes knowledge as **triples → directed labeled graphs → property graphs → knowledge graphs**. The payoff is **explicit knowledge representation** via **ontologies + mathematical logic** (so a general reasoner can infer, instead of hand-coded software), realized on the web through the **Semantic Web stack** (URI, RDF, RDFS/OWL, SPARQL), the **Web of Data**, and **Linked Data** (4 principles, 5-star open data, FAIR).

## Key Concepts

- **DIKW pyramid** (Ackoff 1989) — Data (raw symbols) → Information (data + relational meaning) → Knowledge (useful info) → Wisdom (judgment about the future); **understanding** is the continuum between them.
- **Knowledge = justified true beliefs** — the classical tripartite analysis (P is true, S believes P, S is justified).
- **Semiotic triangle** (Ogden & Richards) — symbol → concept → referent; communication works only when sender and receiver share the same concept.
- **Ambiguity & paraphrasing** (Saussure) — one expression↔many concepts, and many expressions↔one concept — why natural language is a poor KR for machines.
- **Five ingredients of understanding** — syntax, semantics, context, pragmatics, experience.
- **Triple** (subject–predicate–object) → **directed edge-labeled graph** `G = (V, E, L)`, `E ⊆ V × L × V`.
- **Entities, relations, literals, classes** (defined by extension or intension), and **property graphs**.
- **Implicit vs. explicit knowledge representation** — the hand-coded-meaning trap vs. formal semantics.
- **Ontologies + mathematical logic** → a general **inference engine / semantic reasoner** replaces per-case code.
- **Semantic Web stack** — URI/IRI → RDF → RDFS/OWL/SKOS → SPARQL.
- **Web of Data** — machine-*understandable* (correctly interpretable) vs. merely machine-*readable*.
- **Linked Data** — 4 principles, 5-star Open Data, and FAIR (Findable, Accessible, Interoperable, Reusable).

## Summary

### 1.1 From Data to Knowledge
Opens with a puzzle: **what is "42"?** Asked to ChatGPT it means a dozen things — an integer, *The Hitchhiker's Guide to the Galaxy*, a Tarot card, a spiritual number, unlucky in Chinese (homophone for "death"), a biblical span, a Mayan cycle, the atomic number of molybdenum. As **raw data**, 42 has no significance by itself; you need more to make sense of it. That is the **DIKW pyramid** (Ackoff, 1989): **data** = raw characters/symbols; **information** = data given meaning through relational connections (answers who/what/when/where/how-many); **knowledge** = an appropriate, *useful* collection of information; **wisdom** = accumulated, reflected knowledge that supports judgment and prediction about the **future** (the others only explain the past). **Understanding** is the continuum linking all four. Philosophically, **knowledge = justified true beliefs** (P true ∧ S believes P ∧ S justified). The course's goal is **formal knowledge representation** the machine can access — and sharing knowledge needs a common language: **syntax** (symbols/concepts), **semantics** (agreed meaning), **taxonomy** (classification), **thesaurus** (associations), plus rules/constraints on which relations make sense → **ontologies**.

### 1.2 Knowledge and how to represent it
**Context** is the extra information that fixes a specific meaning (42 *in chemistry* = molybdenum's atomic number). Language itself is a knowledge representation, and its core job is **communication**: a sender encodes a message, sends it over a channel, the receiver decodes it — with failure modes of **noise/information loss** and **insufficient encoding/decoding**. The **semiotic triangle** (Ogden & Richards, 1920s; roots in Aristotle) links **symbol → concept → referent**: "Jaguar" is ambiguous (car / cat / OS), and communication only succeeds if both parties share the same **concept**. Saussure's two hard problems — **ambiguity** (one expression, many concepts) and **paraphrasing** (many expressions, one concept) — make natural language ill-suited for machines. Hence **formal knowledge representation** (a field of AI): it unambiguously captures the semantics of concepts, properties, relationships, and entities as **structured data** the machine can **interpret correctly** — which is what "understanding" means here.

### 1.3 The Art of Understanding
**Meaning** is a relationship between signs and what they signify; words are necessarily meaningful. Correct interpretation depends on **five factors**: **syntax** (rules for well-formed expressions — "this sentence no verb" is broken), **semantics** (meaning built from simple concepts via syntactic rules — "this sentence has no verb" is syntactically fine but semantically false), **context** (surroundings that fix interpretation — a "Jaguar" in the jungle is the animal), **pragmatics** (the speaker's *intention* — earnest vs. sarcastic; "is there any beer left in the fridge?" is really a request), and **experience** (world / common-sense knowledge — VW's "Think Small" ad only lands if you're old enough to remember it). Successful communication needs all of them together.

### 1.4 Graphs and Triples
A natural-language sentence — *Leonard Nimoy played Spock* — is **subject–predicate–object**, i.e. a **triple**, which maps intuitively onto a **graph**: subject and object are **nodes/vertices**, the predicate is a **directed, labeled edge**. Formally, a **directed edge-labeled graph** `G = (V, E, L)`: `V` nodes, `L` edge labels, `E ⊆ V × L × V` (each edge an ordered triple of start node, label, end node). Nodes are **entities** (things of distinct, independent existence); edges are **relations** (`R ⊆ N × N`). **Literals** are data values with no separate existence (dates, numbers), drawn as boxes. **Classes** are collections of individuals (person, fictional character), defined by **extension** (listing members) or **intension** (constraints). **Property graphs** attach properties to nodes and relations (birth/death dates), embed class info in the node (`Leonard Nimoy : person`), and stamp relations with validity (`played`, 1965–2013). But a property graph only gives the semantics of entities/relations/classes — nothing formal about what "person" or "start date" actually *means*.

### 1.5 Knowledge Graphs
Extending the graph (Alec Guinness → Obi-Wan → Star Wars), the key insight: the **machine only sees character strings and structure**, no meaning. The **traditional solution** — a programmer reads the labels and **hard-codes** the meaning — is brittle: it breaks when new nodes appear (Spock's home planet Vulcan) or a label is renamed (`played` → `character-played`), demanding endless adaptation. This is **implicit** knowledge representation (meaning carried in natural-language labels, needing shared glossaries and metadata standards) versus **explicit** representation. A **knowledge graph** describes real-world entities and their interrelations in a graph, defines possible **classes and relations in a schema**, interrelates arbitrary entities, and spans domains. **Semantic networks** did the graph part back in the 1980s — what's new is **explicit KR via ontologies grounded in mathematical logic**, letting a **general inference engine / semantic reasoner** do the work. With set theory — `fictional character ⊆ agent`, `person ⊆ creature`, `film series ∩ creature = ∅` (disjoint) — the reasoner *deduces* that Alec Guinness is a creature and that he differs from Star Wars, generically. Three advantages of formal KR over traditional data structures: (1) math logic **expresses semantics** formally, (2) semantics is **explicit**, (3) it enables **general logical inference** rather than per-case code.

### 1.6 The Semantic Web
The **Semantic Web** is "a web of data" — an **extension** of the existing web where information is given **well-defined meaning** so computers and people can cooperate (Scientific American, ~2001; **Tim Berners-Lee**). Walking the **technology stack** bottom-up: **URIs/IRIs** identify everything (Obi-Wan → a dbpedia resource); **RDF** (Resource Description Framework) encodes **triples** (`Obi-Wan hasOccupation Jedi`); **RDFS / OWL / SKOS** model **classes and relations** (schema) — e.g. `fictional character subClassOf agent`, property `portrayer` with domain *fictional character* and range *person* — themselves written as RDF triples; **OWL + rules/logic** define complex classes and constraints (living vs. dead people are **disjoint**; a first-order rule "if X has a death date then X is dead"); **SPARQL** queries the graph (SQL-like **pattern matching**) across dbpedia and Wikidata — e.g. which actors who portrayed Obi-Wan acted elsewhere → Alec Guinness, Ewan McGregor — and can even map their filming locations. The result is a **global database / universal network of semantic propositions**.

### 1.7 Linked Data and the Web of Data
The **traditional web** = **URL** (address) + **HTTP** (communication) + **HTML** (representation). The **Web of Data** swaps in **URI** (identify *everything*, including statements) + **HTTP** + **RDF** (exchange & representation). It's an **upgrade of the web of documents** — a huge decentralized **knowledge base** that is **machine-understandable** (correctly interpretable), not merely **machine-readable** (parseable HTML). Access runs through **intelligent infrastructure services** and a **personal assistant** that aggregates data and builds virtual pages on the fly. Scale (LOD cloud, Jan 2023): ~1,588 linked datasets; Common Crawl 2021 reported >8M sites, >700M URLs, >7B entities, >37B triples. Traditional data access fails because web **APIs** create **data islands** and **mashups break** whenever an API or schema changes. **Linked Data** fixes this by publishing structured RDF and linking across sources over HTTP, following **four principles** (Berners-Lee): (1) use **URIs as names**; (2) use **HTTP URIs** so they can be looked up; (3) on lookup, **provide useful info** (RDF/SPARQL); (4) **include links to other URIs**. The **5-star Open Data** scale: ★ on the web (any format, e.g. PDF) → ★★ machine-readable structured (Excel) → ★★★ non-proprietary (CSV) → ★★★★ W3C standards (RDF/SPARQL, URIs) → ★★★★★ linked to other data. Finally, **FAIR** (Findable, Accessible, Interoperable, Reusable): linked-data / semantic-web tech already complies. This concludes week 1.

## Source

- Playlist: **Knowledge Graphs — Foundations and Applications (OpenHPI 2023)** — https://www.youtube.com/playlist?list=PLNXdQl4kBgzubTOfY5cbtxZCgg9UTe-uF
- Lecturer: **Prof. Dr. Harald Sack** — ISE, FIZ Karlsruhe / KIT
- The 7 sub-videos summarized here:
  - 1.1 From Data to Knowledge — https://www.youtube.com/watch?v=8ps5RrVHGxE
  - 1.2 Knowledge and how to represent it — https://www.youtube.com/watch?v=uxs6CFQ52DU
  - 1.3 The Art of Understanding — https://www.youtube.com/watch?v=lVVxSL6-J1c
  - 1.4 Graphs and Triples — https://www.youtube.com/watch?v=59w3SHtk2vI
  - 1.5 Knowledge Graphs — https://www.youtube.com/watch?v=g0VE611HkIU
  - 1.6 The Semantic Web — https://www.youtube.com/watch?v=eJ2SPniB0VY
  - 1.7 Linked Data and the Web of Data — https://www.youtube.com/watch?v=fNcxAD5Lg5A

## Notes

- This is the **theory backbone** for the ontology/KG track in the log — Sack explains *why* the Semantic Web needs formal representation; the Protégé notes are the *how*.
- The 1.5 disjointness example (`film series ∩ creature = ∅`) is the cleanest one-slide argument for *why ontologies beat hand-coded rules*: one reasoner, arbitrary deductions.
- Next up in the course: **Week 2 — Basic Knowledge Graph Infrastructure** (a natural follow-on note).

## Related

- [[ontology-expert]] — Harald Sack's presentation archive (same author, broader talks)
- [[protege-pizza]] — building an OWL ontology hands-on (the *how*)
- [[what-is-json-ld]] — JSON serialization for linked data / RDF
- [[turtle-syntax]] — Turtle serialization of the RDF triples described here
- [[01-course-introduction-kmst]] — parallel academic Semantic Web course intro
