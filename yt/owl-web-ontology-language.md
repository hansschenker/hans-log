---
slug: owl-web-ontology-language
title: OWL (Web Ontology Language) — three-video primer
date: 2026-07-29
type: summary
source: yt
tags: [yt, ontology, owl, knowledge-graphs, semantic-web, description-logic]
videos:
  - title: "Understanding OWL 2: The Semantic Web's Secret Weapon"
    channel: SKG-Team
    url: https://www.youtube.com/watch?v=CWXiNNLuJow
  - title: "OWL Basics"
    channel: "Ontology Explained: Philosophy and AI (Casey Hart)"
    url: https://www.youtube.com/watch?v=cIyBZ15Q65I
  - title: "4.2 Web Ontology Language OWL"
    channel: "OpenHPI Tutorials (ISE Karlsruhe, Semantic Web lecture)"
    url: https://www.youtube.com/watch?v=x7GtYNEWIKE
---

# OWL (Web Ontology Language) — three-video primer

Three videos watched back-to-back, climbing from intuition to formalism:
**(1)** SKG-Team's high-level explainer of *why* OWL exists, **(2)** Casey Hart's practical
tour of OWL's building blocks as triples, and **(3)** the OpenHPI/ISE-Karlsruhe lecture
that grounds OWL in description logic. This note merges all three.

## TL;DR

OWL (Web Ontology Language, a W3C standard) is a **declarative** language for building
**ontologies** — formal, precise descriptions of a domain that a computer can reason over.
Unlike a database it uses the **open-world assumption** (unstated ≠ false, just unknown),
and its whole payoff is **inference**: state a few axioms and a reasoner derives new facts
you never wrote down. Under the hood OWL *is* a **description logic** (OWL 1 ≈ SHOIN(D),
OWL 2 ≈ SROIQ(D)) — a decidable fragment of first-order logic — and it ships in restricted
**profiles/flavors** (OWL 2 EL, QL, RL) that trade expressivity for tractable, fast
reasoning over big data. It's the reasoning layer of the Semantic Web, turning a "web of
documents" into a "web of knowledge."

## Key Concepts

- **Ontology** — a formal, precise description of part of the world: what things exist and how they relate. OWL is *declarative* ("this is how the world is"), **not** a procedural programming language.
- **Open-world assumption (OWA)** — if something isn't stated, it's *unknown*, not false (contrast databases' closed-world assumption). Leaves room for a reasoner to discover facts.
- **No-unique-name assumption** — two names may denote the same individual unless you explicitly say they're different (or the same).
- **Triples** — every statement is `subject – predicate – object`; graphically, subject/object are nodes and the predicate is the edge. Ontologies are graphs of triples.
- **IRIs/URIs** — globally unique identifiers so the same term always picks out the same thing, enabling joins across datasets.
- **Resources** that fill triple slots: **classes** (sets/categories), **individuals** (instances/members), **properties** (edges/verbs), **literals** (typed values: ints, strings, dates).
- **Three kinds of property**: **object property** (individual → individual), **datatype property** (individual → literal), **annotation property** (meta-comments / everything else).
- **Axioms** — the rules that define relationships: subclass hierarchies (`every woman is a person`), `disjoint` classes (nothing is both man and woman), etc.
- **Inference / reasoning** — the payoff: from `Mary is a mother` + `every mother is a woman` + `every woman is a person`, a reasoner concludes `Mary is a person` on its own.
- **Description logic** — OWL's mathematical foundation; a decidable fragment of first-order logic. Each capital letter in a DL name (SHOIN, SROIQ) marks a language feature.
- **Profiles / flavors** — OWL 1: Lite ⊂ DL ⊂ Full (Full is undecidable). OWL 2 profiles: **EL** (huge class hierarchies, e.g. SNOMED CT), **QL** (fast querying over big DBs), **RL** (rule-style reasoning over massive web data).
- **TBox / RBox / ABox** — terminological axioms (class relations), role/property axioms, and assertional facts about individuals.
- **The hard modeling choice** — class vs individual: e.g. is "1500 m freestyle" a class of races (→ annotation property) or a single individual (→ object property)? Prefer object properties, but it's a genuine ontologist's judgment call.

## Summary

### 1. The problem OWL solves (SKG-Team)

The web was built for humans; a computer sees only characters and links, no meaning. "Paris"
the city vs "Paris" the play character is trivial for us and hopeless for software. OWL 2 adds
a layer of *meaning* on top of messy data by letting you build an **ontology** — a formal,
precise description of a slice of the world. Crucially OWL is **declarative** (it describes a
state of affairs, not a sequence of steps) and it adopts the **open-world assumption**: a
database says "not present ⇒ false," but OWL says "not stated ⇒ unknown," leaving room for
discovery.

Building blocks, via a family-tree example: an **individual** is a specific thing (Mary, the
city of Paris); **classes** group individuals (Mary ∈ Person, Mary ∈ Woman); **axioms** are
rules relating classes (`every woman is a person`); **properties** link individuals
(`hasWife(John, Mary)`); and you can assert what *can't* be true (`Man` and `Woman` are
**disjoint**). The magic is **inference**: told `every mother is a woman`, `every woman is a
person`, and the single new fact `Mary is a mother`, the reasoner derives `Mary is a person`
by itself. Because full OWL 2 reasoning is computationally heavy, it comes in **profiles** —
leaner sub-languages trading expressivity for speed: **EL** for very large class hierarchies
(medical vocabularies like SNOMED CT), **QL** for fast querying of big databases, **RL** for
applying rules across massive web data. All of it feeds the **Semantic Web** vision: moving
from a web of documents to a web of knowledge that machines can reason about.

### 2. The building blocks as triples (Casey Hart, "OWL Basics")

OWL = **Web Ontology Language** (the acronym deliberately scrambles the letters). It sits atop
a stack: **XML** → **XML Schema** (constraints) → **RDF** (data modeling) → **OWL** (inference),
all part of the Semantic Web tower that culminates in *trust*. Terms are named by **URIs/IRIs**
(internationalized identifiers) so every mention of "Casey Hart" resolves to the same node,
which is what lets separate datasets join.

Sentences in an ontology are **triples** — three slots, `subject – predicate – object`
(e.g. "2001 Masters — was won by — Tiger Woods"). Each slot is filled by a **resource**:

- **Classes** — collections of things, like mathematical sets (the class of all foxes); taxonomies are hierarchies of classes.
- **Individuals** — instances/members of classes (Jenny the fox); most real data are individuals.
- **Properties** — the edges/verbs, in three kinds:
  - **Object property** relates two individuals (`Jenny eats strawberry01`),
  - **Datatype property** relates an individual to a **literal** (`goldMedalCount = 9`),
  - **Annotation property** is the catch-all for meta-comments (term history, notes) and for cases where you relate an individual to a whole class.
- **Literals** — the quoted, typed values: integers, strings, dates (`2001-04-05`).

Worked example (Katie Ledecky): `rdf:type` links an individual to a class (`Katie Ledecky is a Person`); `goldMedalCount` is a datatype property (→ integer literal); `bornIn` is an object property (`Katie → Washington DC`). The tricky one — "specializes event type 1500 m freestyle" — exposes the core modeling decision: if 1500 m freestyle is a **class**, you must reach for an **annotation property**; if you define it as an **individual**, you can use an **object property**. Ontologists prefer object properties but the choice recurs constantly and has downstream consequences.

### 3. OWL as description logic (OpenHPI / ISE Karlsruhe, lecture 4.2)

Formally, OWL **is** a **description logic (DL)** — a fragment of first-order logic that is (in
the important cases) **computable and decidable**. Two variants:

- **OWL 1** (W3C 2004) is based on the DL **SHOIN(D)**.
- **OWL 2** (W3C recommendation since 2009) is based on the richer **SROIQ(D)** — the version to use going forward.

Every capital letter names a language feature. In **SHOIN(D)**: **H** = property/subclass
**h**ierarchies; **I** = **i**nverse properties; **S** = transitive roles (+ ALC base);
**O** = nominals / **o**ne-of enumerated (closed) classes; **N** = unqualified **n**umber
restrictions; **(D)** = datatypes. OWL 2's **SROIQ(D)** adds more (e.g. **R** = complex role
inclusion / property chains, **Q** = *qualified* number restrictions). Both keep the
**open-world** *and* **no-unique-name** assumptions.

Language layering repeats at both versions:

- **OWL 1**: `OWL Lite ⊂ OWL DL ⊂ OWL Full`. Lite and DL are decidable; **OWL Full** is **undecidable** because it inherits the full semantics of RDFS (reification breaks decidability). Between first-order logic and OWL DL sit **SWRL/RIF** rule languages.
- **OWL 2**: three tractable profiles **EL, RL, QL** (sub-polynomial/polynomial reasoning), then **OWL 2 DL** (decidable), then **OWL 2 Full** (undecidable, again via RDFS legacy).

Knowledge is organized as **TBox** (terminological: class inclusions/equivalences), **RBox**
(role/property axioms: sub-properties, inverses, transitive/symmetric/reflexive/disjoint roles,
and **general class inclusion** i.e. property chains — e.g. define *uncle* as "brother of a
parent"), and **ABox** (assertions about individuals: class membership, property relations,
(in)equality). Class constructors include conjunction, disjunction, negation; property
restrictions are **universal** (∀, "strict binding") and **existential** (∃, "loose binding");
plus **number restrictions**, **self** restrictions, and **closed/enumerated** classes. OWL 2
also lets number restrictions be qualified by a class range.

**Syntaxes** — OWL can be serialized several ways: **functional** (compact, replaces OWL 1's
abstract syntax), **RDF/XML** (verbose, legacy), **OWL/XML** (independent XML serialization),
**Manchester** (concise, human-readable, used in ontology **editors** like Protégé), and
**Turtle** (the one the lecture course adopts going forward). The recurring worked example is
the **"happy person"**: *a happy person is someone all of whose children are happy persons
**and** who has at least one happy child* — the existential clause is needed so childless
people don't vacuously satisfy the universal clause. Seeing the same axiom in functional vs
Manchester vs Turtle makes the compactness differences obvious.

## Notes

- The three videos are a nice ladder: **why** (SKG) → **what/how, informally** (Hart) → **formal DL** (OpenHPI). Watch in that order.
- The single most load-bearing idea across all three: **OWA + inference**. Everything OWL does that a plain database can't traces back to "unstated = unknown, and a reasoner fills gaps."
- Practical throughline for modeling: **prefer object properties**, be deliberate about **class-vs-individual**, and remember **disjointness/number restrictions** are what let the reasoner catch contradictions.
- The DL-letter decoder (S H O I N / S R O I Q + D) is worth memorizing — it tells you a profile's expressivity and its decidability at a glance.
- Protégé (already logged this week) is where the **Manchester syntax** shows up in practice; **Turtle** is the serialization the KG course will use.

## Sources

- Understanding OWL 2: The Semantic Web's Secret Weapon — SKG-Team — https://www.youtube.com/watch?v=CWXiNNLuJow
- OWL Basics — Ontology Explained: Philosophy and AI (Casey Hart) — https://www.youtube.com/watch?v=cIyBZ15Q65I
- 4.2 Web Ontology Language OWL — OpenHPI Tutorials (ISE Karlsruhe, Semantic Web lecture) — https://www.youtube.com/watch?v=x7GtYNEWIKE

## Related

- [[knowledge-graphs-10-knowledge-representation-with-graphs]]
- [[knowledge-graphs-00-lecture-overview]]
- [[ytl-knowledge-graphs]]
