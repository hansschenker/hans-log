---
type: reference
title: Matthew Horridge (Protégé / OWL author)
description: author of the original Protégé/OWL ontology-building guide (GitHub)
resource: https://github.com/matthewhorridge
tags: [cs, ontology, owl, protege, people, reference]
timestamp: 2026-07-30
---

# Matthew Horridge — Protégé / OWL API author

*GitHub profile analyzed — [github.com/matthewhorridge](https://github.com/matthewhorridge). ORCID 0000-0001-8921-6593.*

## TL;DR

Matthew Horridge is a Stanford-affiliated (Palo Alto) developer and researcher whose work centers on **ontology engineering and the OWL ecosystem**. He is best known in the Protégé community as an author of the foundational tutorial *"A Practical Guide To Building OWL Ontologies Using Protégé"* — the ancestor of the pizza tutorials — and as a contributor to the **OWL API** and OWL tooling. His GitHub hosts explanation, GWT, and document-store libraries around the OWL API.

## Key Concepts

- **Original OWL/Protégé guide** — his pizza-based "Practical Guide to Building OWL Ontologies" is the lineage root behind DeBellis's and Yasen's modern pizza tutorials.
- **OWL API tooling** — libraries for working with OWL ontologies programmatically.
- **Justifications / explanations** — his most-starred repo, `owlexplanation`, generates **justifications for entailments** (why a reasoner inferred something) — key to debugging ontologies.
- **Web/embedding** — `owlapi-gwt` exposes a GWT-compatible subset of the OWL API for browser apps.
- **Academic identity** — maintains an ORCID; research contributions beyond code.

## Content

**Who he is.** A developer based in Palo Alto, affiliated with **Stanford University** (home of Protégé). ~30 public repositories focused on ontology engineering, semantic-web technologies, and the **OWL (Web Ontology Language) API**.

**Notable repositories.**
- **`owlexplanation`** (most popular) — an API and reference implementation for **generating justifications for entailments** in OWL ontologies, so developers can understand a reasoner's inference chains.
- **`owlapi-gwt`** — a GWT-compatible subset of the OWL API, enabling OWL manipulation in web applications.
- **`owl-document-store`** — an experimental library for storing and manipulating OWL ontology documents via the OWL API.
- **`telemetry`** — a utility for recording timings and measurements.

## Source

- GitHub profile: https://github.com/matthewhorridge
- ORCID: https://orcid.org/0000-0001-8921-6593
- Affiliation: Stanford University / Palo Alto

## Notes

- Relevant to the current ontology thread because the **pizza tutorial** being worked through ([Protégé Pizza Tutorial (yasenstar/protege_pizza)](./protege-pizza.md), [Build Ontology in Protege (pizza.owl) - 01 Opening & Introduction](./build-ontology-in-protege-pizzaowl-01-opening-introduction.md)) descends directly from Horridge's original OWL/Protégé guide.
- `owlexplanation` (entailment justifications) is the practical answer to "the reasoner inferred X — *why*?", the debugging counterpart to the HermiT/Pellet reasoning taught in the pizza course.

## Related

- [Protégé Pizza Tutorial (yasenstar/protege_pizza)](./protege-pizza.md) — the pizza tutorial his original guide seeded
- [Build Ontology in Protege (pizza.owl) - 01 Opening & Introduction](./build-ontology-in-protege-pizzaowl-01-opening-introduction.md) — companion video series
- [ontology-tool-protege](./ontology-tool-protege.md) — the Stanford Protégé editor
- [understanding-owl-2](./understanding-owl-2.md) — the OWL 2 language his tooling targets

---

Part of: [Knowledge Graphs & Ontologies](./knowledge-graphs.md)
