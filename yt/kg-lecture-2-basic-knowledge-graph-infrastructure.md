---
slug: kg-lecture-2-basic-knowledge-graph-infrastructure
title: "Knowledge Graphs — Lecture 2: Basic Knowledge Graph Infrastructure (2.1–2.6)"
channel: ISE FIZ Karlsruhe (Prof. Harald Sack)
date: 2026-08-01
url: https://www.youtube.com/playlist?list=PLNXdQl4kBgzubTOfY5cbtxZCgg9UTe-uF
type: summary
language: en
tags: [yt, cs, knowledge-graphs, semantic-web, rdf, rdfs, turtle, uri, reasoning]
source: yt
---

# Knowledge Graphs — Lecture 2: Basic Knowledge Graph Infrastructure (2.1–2.6)

*Summary of the 6 lecture sub-videos (2.1–2.6) of Week 2 of Harald Sack's OpenHPI 2023 "Knowledge Graphs" course. Transcripts fetched and synthesized; full transcripts not stored. Hands-On 2.1/2.2 (RDFLib) not covered here.*

## TL;DR

Week 2 builds the **concrete machinery of the Semantic Web stack, bottom-up**: how to **identify** things (URIs/IRIs, designator vs. designatum, HTTP content negotiation), how to **state facts** about them (**RDF** triples with literals, datatypes, language tags, blank nodes), how to **write them readably** (**Turtle** — prefixes, `;`/`,` shortcuts, blank-node syntax for n-ary relations), how to **model vocabularies** (**RDFS** — classes, `rdf:type`, `domain`/`range`, `subClassOf`/`subPropertyOf`), how to **structure data** (containers, collections, named graphs/datasets), and finally how to **reason** over it (RDFS **entailment** rules that make implicit knowledge explicit). The recurring Spock/Star Trek example threads through all six.

## Key Concepts

- **URI vs. IRI** — worldwide-unique identifiers (IRI = Unicode-extended); 4 parts: scheme, host, path, fragment. **URL** locates documents *on* the web; **URI** identifies *anything* via the web.
- **Designator vs. designatum** — the resource that *describes* a thing vs. the thing itself; separate URIs, resolved via **HTTP content negotiation** (ask for HTML vs. Turtle).
- **Language-independent identifiers** — Wikidata Q-numbers (apple = Q89, Apple Inc. = Q312) plus `rdfs:label` for multilingual names.
- **RDF triple** — subject–**property**–object; subject ∈ (IRI ∪ blank), property ∈ IRI, object ∈ (IRI ∪ blank ∪ literal); an **RDF graph** is a set of triples.
- **Literals, datatypes, language tags** — `"2"^^xsd:integer`, `"2023-08-02"^^xsd:date`, `"semantics"@en`; datatypes borrowed from **XML Schema**.
- **Blank nodes** — existential "there exists something with these properties"; also the mechanism for **n-ary relations**; not referenceable from outside.
- **Turtle** — the readable serialization: `@prefix`/`@base`, `;` (same subject), `,` (same subject+property), `[ ]` blank nodes, `_:id` labeled blank nodes, `a` = `rdf:type`, `( )` collections.
- **RDFS** — classes (`rdfs:Class`), `rdf:type`, properties (`rdf:Property`), `rdfs:domain`/`rdfs:range`, `rdfs:subClassOf`/`rdfs:subPropertyOf`; annotation props (`label`, `comment`, `seeAlso`, `isDefinedBy`) carry **no formal semantics**.
- **TBox vs. ABox** — terminological (schema) vs. assertional (instance) knowledge.
- **Complex structures** — containers (`rdf:Bag`/`Seq`/`Alt`, open), collections (`rdf:first`/`rest`/`nil`, closed linked list), and **named graphs / datasets** → quads.
- **Inference vs. entailment** — entailment = what follows; inference = computing it. **Deductive** (logic, this course) vs. inductive (ML) vs. abductive reasoning. RDFS inference is **monotonic/additive**.

## Summary

### 2.1 How to identify and access Things
Humans identify a thing from a mere symbol; we want machines to do the same. On the web, that requires a **URI** (Uniform Resource Identifier — "a street number for a resource"), or its Unicode-extended form the **IRI**. Both have four parts: **scheme** (protocol), **host/domain**, **path** (the resource), and optional **fragment** (a section). A **resource** is anything with a clear identity — apple, web page, book, person, even a relation. Note **URL vs. URI**: a URL locates what exists *on* the web (documents); a URI identifies *anything* via the web. Established schemes include URLs, ISBN/ISSN, and DOIs. To avoid language- and synonym-dependence, use **language-independent identifiers** like **Wikidata Q-numbers** (apple = Q89 vs. Apple the company = Q312), attaching human names through `rdfs:label` in many languages. Crucial distinction: the apple itself can't be on the web, so a **designator** (a resource that *describes* the apple) stands in for the **designatum** (the thing). They get **separate URIs**, resolved through **HTTP content negotiation** — request Q89 as `text/html` (human-readable) or as Turtle (machine-readable) and the server returns the right representation. Demoed live with `curl`.

### 2.2 How to Represent Simple Facts with RDF
**RDF** (Resource Description Framework) sits at the information-exchange layer. A fact like *Spock homePlanet Vulcan* is a subject–predicate–object triple — in RDF the predicate is called a **property**. Everything addressable becomes a URI (shown in angle brackets in N-Triples); the object may instead be a **literal**. Building blocks: **IRIs**, **literals** (data values with no independent existence), **datatypes** (borrowed from **XML Schema** — `xsd:string`, `xsd:float`, `xsd:date`, written `"value"^^<datatype>`), **language tags** (`"semantics"@en`, `"Semantik"@de`), and **blank nodes** (existential statements — "there exists something with these properties" — not referenceable from outside). Formal definitions: `I` = IRIs, `L` = literals, `B` = blank nodes; **RDF term** = `I ∪ L ∪ B`; a **triple** `SPO` has subject ∈ `I ∪ B`, property ∈ `I`, object ∈ `I ∪ B ∪ L`; an **RDF graph** is a set of triples. RDF has many **serializations**: **N-Triples** (simplest, verbose), **Turtle** (abbreviated, readable — the course default), RDF/XML, Notation3, **HDT** (compressed), **N-Quads** (multiple graphs), **RDFa** (RDF inside HTML), and **JSON-LD** (RDF in JSON — important for programming).

### 2.3 RDF Turtle Serialization
N-Triples spells out every triple as `<uri> <uri> "literal"@en .` — URIs in angle brackets, literals in quotes, a period ending each triple — which becomes unreadable at scale. **Turtle** adds pure syntactic sugar (no new semantics): the **`@prefix`** directive binds a short label to a namespace (write `dbp:origin` instead of the full URI); the **`@base`** directive sets a default URI for the file; a **semicolon `;`** continues with the same subject; a **comma `,`** continues with the same subject *and* property (a property list); literals can be typed (`"1951"^^xsd:gYear`, `"2"^^xsd:integer`). For **n-ary relations** — e.g. which starship Spock served on (Enterprise NCC-1701 from 2265, NCC-1701-A from 2287) with which position — plain edges are ambiguous, so **blank nodes** aggregate the correct grouping. Turtle's blank-node forms: **`[ ]`** for an anonymous blank node as subject; **nested** `[ ... ]` when the blank node sits at the object position (its content written inside the brackets); and **labeled/dereferenceable blank nodes** `_:id1` (underscore prefix, referenceable only *within* the document) for cleaner writing of complex graphs.

### 2.4 Vocabularies and Model Building with RDFS
Bare URIs carry no meaning, so we climb to the next stack level — **RDF Schema (RDFS)** — for semantic expressivity. Definitions: a **term** (a word given specific meaning in context), a **vocabulary/terminology** (a set of terms for a domain), a **schema** (formal description of a dataset's high-level structure, usable for reasoning/validation/querying), and a **semantic schema** (one that defines the *meaning* of its terms). **Classes** (`rdfs:Class`, the class of all classes) are abstract sets of resources sharing properties; **instances** are members, declared with **`rdf:type`** (`Leonard_Nimoy rdf:type Person`). **Properties** are instances of **`rdf:Property`**, and `rdfs:domain`/`rdfs:range` constrain (and entail) the classes of a property's subject and object. Everything is an **`rdfs:Resource`**. **`rdfs:subClassOf`** builds class hierarchies with real semantics: if `A subClassOf B` and `a ∈ A`, then `a ∈ B` (a derivable triple); **`rdfs:subPropertyOf`** does the same for properties (`firstName subPropertyOf name`). **Annotation properties** — `rdfs:label`, `rdfs:comment`, `rdfs:seeAlso`, `rdfs:isDefinedBy` — are for humans and carry **no formal semantics**. Class/property definitions are **terminological knowledge (TBox)**; concrete instances are **assertional knowledge (ABox)**. Shared vocabularies enable **reuse and data integration**; naming convention: classes **UpperCamelCase** singular, properties **lowerCamelCase** singular.

### 2.5 RDF Complex Data Structures
An RDF graph is an *unordered* set of triples, so RDF adds **list** structures. Two families: **containers** (open — extensible) and **collections** (closed — fixed). A **container** is a blank node linked via `rdf:_1, rdf:_2, …` to its members, typed as **`rdf:Bag`** (unordered), **`rdf:Seq`** (ordered), or **`rdf:Alt`** (alternatives) — its drawback being the potentially unbounded `rdf:_n` properties. A **collection** is a **linked list** using `rdf:first` (head) and `rdf:rest` (tail), terminated by **`rdf:nil`** — exactly the Lisp cons-list idea — and is closed once built; Turtle abbreviates it with **parentheses** `( item1 item2 … )`. (`a` also abbreviates `rdf:type`.) Finally, **RDF datasets** are dictionaries of graphs: one **default graph** plus zero or more **named graphs** (name = URI/blank node + graph), useful for tracking provenance, trust, or time — which extends triples into **quads** (triple + graph name). Reification / RDF-star follows as an excursion.

### 2.6 Logical Inference with RDF(S)
RDFS's special properties (`subClassOf`, `rdf:type`, `domain`, `range`, `subPropertyOf`) have **formal, model-theoretic semantics** grounded in logic, so a reasoner can draw **valid, sound inferences** — making implicit knowledge explicit. **Entailment** is what follows as a consequence; **inference** is the *process* of computing entailments (≈ reasoning). Three reasoning kinds: **deductive** (apply rules to premises → conclusions; the subject of logic, and of this course), **inductive** (learn patterns from many examples; machine learning), and **abductive** (infer a likely explanation for an observation). The core **RDFS inference rules**: (1) `I rdf:type C1 ∧ C1 subClassOf C2 ⊢ I rdf:type C2`; (2) `(i1 P i2) ∧ P domain C1 ⊢ i1 rdf:type C1`; (3) `(i1 P i2) ∧ P range C2 ⊢ i2 rdf:type C2`; (4) `(i1 P1 i2) ∧ P1 subPropertyOf P2 ⊢ (i1 P2 i2)`. These inferences are **additive/monotonic**: an instance may belong to several classes, and new derived facts don't contradict existing ones — a contradiction only arises if classes are explicitly declared **disjoint**. This concludes Week 2.

## Source

- Playlist: **Knowledge Graphs — Foundations and Applications (OpenHPI 2023)** — https://www.youtube.com/playlist?list=PLNXdQl4kBgzubTOfY5cbtxZCgg9UTe-uF
- Lecturer: **Prof. Dr. Harald Sack** (with Sascha Bruns) — ISE, FIZ Karlsruhe / KIT
- The 6 sub-videos summarized here:
  - 2.1 How to identify and access Things — https://www.youtube.com/watch?v=HW5dNSuwGyY
  - 2.2 How to Represent Simple Facts with RDF — https://www.youtube.com/watch?v=xsw9cCbZqM8
  - 2.3 RDF Turtle Serialization — https://www.youtube.com/watch?v=8FbYZDOCBeM
  - 2.4 Vocabularies and Model Building with RDFS — https://www.youtube.com/watch?v=GXYgASC87NI
  - 2.5 RDF Complex Data Structures — https://www.youtube.com/watch?v=edZmB4P75ik
  - 2.6 Logical Inference with RDF(S) — https://www.youtube.com/watch?v=Fc_SBVKvGVs

## Notes

- This is the **hands-keyboard** week: [[kg-lecture-1-knowledge-representation-with-graphs]] motivates *why* explicit representation matters; Week 2 is the actual RDF/RDFS/Turtle you'd type.
- The `[[turtle-syntax]]` note now has a full worked context — prefixes, `;`/`,`, blank nodes, and collections all appear here in Sack's Spock examples.
- `rdfs:domain`/`range` are **not constraints that reject data** — they are *inference rules* that add `rdf:type` triples. A common beginner misconception worth remembering.
- Next in the course: **Excursion 2 — RDF-star / RDFa & the Web**, then Week 3 (OWL). Natural follow-on notes.

## Related

- [[kg-lecture-1-knowledge-representation-with-graphs]] — Week 1 (the theory behind this infrastructure)
- [[turtle-syntax]] — the Turtle serialization detailed here
- [[what-is-json-ld]] — JSON-LD, one of the RDF serializations mentioned in 2.2
- [[ontology-expert]] — Harald Sack's broader presentation archive
- [[protege-pizza]] — building an OWL ontology (the OWL layer that comes after RDFS)
