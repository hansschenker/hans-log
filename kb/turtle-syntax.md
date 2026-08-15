---
type: concept
title: Turtle (Terse RDF Triple Language)
description: Terse RDF Triple Language, compact text serialization for RDF graphs
resource: https://en.wikipedia.org/wiki/Turtle_(syntax)
tags: [cs, rdf, turtle, semantic-web, serialization, linked-data]
timestamp: 2026-07-30
---

# Turtle (Terse RDF Triple Language)

*Wikipedia analyzed — [en.wikipedia.org/wiki/Turtle_(syntax)](https://en.wikipedia.org/wiki/Turtle_(syntax))*

## TL;DR

**Turtle** is a compact, human-readable text syntax for serializing **RDF** graphs — a friendlier alternative to RDF/XML. It writes knowledge as **subject–predicate–object** triples using `@prefix` shorthands for URIs, with abbreviations (`;` to share a subject, `,` to share a predicate, `[ ]` for blank nodes) that keep files terse. A W3C Recommendation since **February 2014**, MIME type `text/turtle`, file extension `.ttl`, and the serialization most people actually read and hand-edit.

## Key Concepts

- **RDF triple** — the atomic unit: `subject predicate object .`, each typically a URI (objects may also be literals).
- **`@prefix`** — declares a namespace shorthand (e.g. `@prefix foaf: <http://xmlns.com/foaf/0.1/> .`) to avoid repeating long URIs.
- **Abbreviations** — `;` chains multiple predicates for the same subject; `,` chains multiple objects for the same predicate; `[ ]` denotes blank nodes; `a` is shorthand for `rdf:type`.
- **UTF-8**, MIME `text/turtle`, extension `.ttl`, W3C Recommendation (Feb 2014).
- **Superset of N-Triples** — every N-Triples doc is valid Turtle; Turtle adds prefixes and abbreviations.
- **Subset of Notation3 (N3)** — Turtle drops N3's rule/logic features.
- **SPARQL kinship** — SPARQL's triple-pattern syntax deliberately mirrors Turtle.
- **TriG** — extends Turtle with named graphs (multiple graphs per file).

## Content

**What it is.** A standardized syntax and file format (`.ttl`) for representing data in the **RDF** model — listed by the W3C alongside N-Triples, JSON-LD, and RDF/XML as a common RDF serialization.

**Problem it solves.** RDF/XML is verbose and awkward to read or hand-edit. Turtle is **human-friendly and editable** while remaining a fully standard, interoperable RDF format.

**Syntax essentials.**
- **Prefixes** — `@prefix` declarations factor out namespace URIs, cutting verbosity.
- **Triples** — `subject predicate object .`; each component usually a URI, objects can be typed/plain literals.
- **Abbreviations** — semicolons chain predicates on one subject; commas chain objects on one predicate; square brackets create blank nodes; `a` abbreviates `rdf:type`.

**Relationships.**

| Technology | Relationship to Turtle |
|---|---|
| **RDF** | Turtle is a serialization of the RDF graph model |
| **N-Triples** | Turtle is a superset (adds prefixes/abbreviations) |
| **Notation3 (N3)** | Turtle is a subset (no rules/logic) |
| **SPARQL** | Uses Turtle-like triple-pattern syntax |
| **JSON-LD / RDF/XML** | Alternative RDF serializations |
| **TriG** | Extends Turtle with named-graph support |

**Tooling.** Widely supported: Redland, RDF4J, Apache Jena, RDFLib (Python), N3.js.

## Source

- https://en.wikipedia.org/wiki/Turtle_(syntax)
- W3C Recommendation (RDF 1.1 Turtle), February 2014; MIME `text/turtle`, extension `.ttl`

## Notes

- Turtle is the format you'll read when Protégé exports an ontology, and the natural companion to the OWL/pizza work ([Protégé Pizza Tutorial (yasenstar/protege_pizza)](./protege-pizza.md)) — OWL ontologies are RDF graphs, and Turtle is the readable way to see the triples.
- Contrast with [What is JSON-LD?](./what-is-json-ld.md): JSON-LD serves RDF as JSON for web APIs, Turtle serves the same graph as terse text for humans — same model, different skin.
- The KMST intro ([01 Course Introduction - KMST](./01-course-introduction-kmst.md)) names RDF as the standard representation for the web of data; Turtle is how you write it by hand.

## Related

- [What is JSON-LD?](./what-is-json-ld.md) — JSON serialization of the same RDF model
- [Protégé Pizza Tutorial (yasenstar/protege_pizza)](./protege-pizza.md) — OWL ontologies serialized as RDF/Turtle
- [01 Course Introduction - KMST](./01-course-introduction-kmst.md) — why RDF is the web-of-data standard
- [understanding-owl-2](./understanding-owl-2.md) — OWL builds on the RDF triple model

---

Part of: [Knowledge Graphs & Ontologies](./knowledge-graphs.md)
