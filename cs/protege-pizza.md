---
slug: protege-pizza
title: Protégé Pizza Tutorial (yasenstar/protege_pizza)
date: 2026-07-30
tags: [cs, ontology, owl, protege, semantic-web, knowledge-graphs]
source: cs
---

# Protégé Pizza Tutorial — `yasenstar/protege_pizza`

*GitHub repo README analyzed — [github.com/yasenstar/protege_pizza](https://github.com/yasenstar/protege_pizza). Published site: [yasenstar.github.io/protege_pizza](https://yasenstar.github.io/protege_pizza/). Local clone: `C:\Users\hanss\Web\Hans\protege\protege_pizza`.*

## TL;DR

A complete, open-source learning hub for **ontology engineering**, centered on building the classic **pizza.owl** ontology in **Protégé** step by step. Xiaoqi "Yasen" Zhao packages a 49-video YouTube course, two Leanpub/Kindle eBook volumes, and progressive **snapshot model files** so learners can verify their work at each stage. It teaches OWL from simple class hierarchies through reasoning, restrictions, SWRL rules, and SPARQL — built on Michael DeBellis's pizza tutorial (itself descended from the original Horridge guide).

## Key Concepts

- **Pizza ontology as pedagogy** — the pizza domain is the canonical vehicle for teaching OWL: classes, properties, individuals, and restrictions in a familiar domain.
- **Class hierarchies & disjointness** — taxonomies with subclass relations and disjoint constraints.
- **Object properties** — domains, ranges, inverse relations, property characteristics.
- **Logical restrictions** — existential (`some`) and universal (`only`) quantifiers, cardinality, defined vs primitive classes.
- **Reasoning** — HermiT / Pellet reasoners validate and enrich the model; the **Open World Assumption** and Description Logic underpin inference.
- **SWRL & SPARQL** — rules for enhanced inferencing; SPARQL for querying the knowledge base; plus SHACL, WebProtégé, WebVOWL.
- **Snapshot-driven repo** — `/snapshot_models` holds a model file per video so you can jump in at any chapter.

## Content

The repository is the free companion to the eBook **"Mastering Ontology Engineering with Protégé and Pizza.owl"** (Volume 1: Foundations to Reasoning; Volume 2: Class Hierarchy to Semantic Restrictions; Volume 3, on the Semantic Knowledge Development Lifecycle, forthcoming). All chapters, code snapshots, and reference models are released under **CC BY-SA**.

The curriculum runs from the Protégé interface basics to advanced reasoning and querying:
- **Foundations** — classes, properties, individuals in the pizza domain; creating a first OWL ontology.
- **Structure** — RDF file structure, class-hierarchy tools, object properties, inverse properties, domains/ranges.
- **Restrictions** — existential and universal quantifiers, subclasses, primitive vs defined classes, enumerated classes, cardinality, data properties.
- **Reasoning & querying** — HermiT/Pellet, Description Logic queries, SPARQL, SWRL/SQWRL rules, SHACL.
- **Tooling** — Protégé UI customization, namespaces, ontology merging, WebProtégé, WebVOWL visualization.

The project is explicitly built on **Michael DeBellis's** pizza tutorial and reviewed with him for accuracy; it positions ontologies as foundational infrastructure for **AI and knowledge graphs** in the LLM era.

## Source

- Repo: https://github.com/yasenstar/protege_pizza
- Published site: https://yasenstar.github.io/protege_pizza/
- Local clone: `C:\Users\hanss\Web\Hans\protege\protege_pizza`
- Author: Xiaoqi (Yasen) Zhao — Global Enterprise Architect; founder of the Executable Knowledge Architecture (EKA) framework
- Based on Michael DeBellis's pizza tutorial: https://www.michaeldebellis.com/post/new-protege-pizza-tutorial

## Notes

- The pizza tutorial lineage: original **Horridge** "Practical Guide to Building OWL Ontologies Using Protégé" → **DeBellis** modernization → this **Yasen** hands-on course. See [[protege-author-matthew-horridge]].
- Complements the theory in the KMST course intro ([[01-course-introduction-kmst]]) — that course explains *why* the Semantic Web needs ontologies; this repo is the *how* in Protégé.

## Related

- [[protege-author-matthew-horridge]] — author of the original Protégé/OWL building guide
- [[build-ontology-in-protege-pizzaowl-01-opening-introduction]] — first video of the companion playlist
- [[turtle-syntax]] — RDF serialization you'll meet when saving/loading OWL
- [[ontology-tool-protege]] — the Protégé editor itself
- [[01-course-introduction-kmst]] — theory backdrop for ontology engineering
