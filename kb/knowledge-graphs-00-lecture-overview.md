---
type: course
title: Knowledge Graphs - 0.0 Lecture Overview
description: "first video: course roadmap across all 6 weeks"
resource: https://www.youtube.com/watch?v=CiU1sMbL3k4
tags: [knowledge-graphs, semantic-web]
timestamp: 2026-07-28
---

# Knowledge Graphs - 0.0 Lecture Overview

## TL;DR

Opening roadmap for the ISE/FIZ Karlsruhe MOOC *Knowledge Graphs — Foundations and Applications* (OpenHPI 2023), presented by Harald Sack and team (Sasha Bruns, Tabia, Mehwish, Anas). It walks through all six weeks of the course — from data-vs-knowledge and RDF, through SPARQL, ontologies/OWL, ontological engineering, to graph analytics, KG embeddings, and how KGs complement (and fact-check) large language models. Each week ships hands-on Colab/Jupyter notebooks.

## Key Concepts

- **Data → knowledge**: raw data has no meaning; adding context and interpretation turns it into knowledge — the motivation for knowledge representation.
- **Graphs & triples** as an intuitive knowledge-representation form → **knowledge graphs**, whose vision is the **Semantic Web** (its layered architecture / "layer cake").
- **Linked Data principles** and the resulting **Web of Data**.
- **RDF stack**: RDF triples, Turtle serialization, RDFS vocabularies/schema, collections & containers, RDF reification / RDF-star (statements about statements), logical inference with RDFS, RDFa (RDF in HTML).
- **SPARQL**: basic queries, filters, sub-selects, property paths, federation; querying DBpedia and Wikidata; SHACL constraints for quality assurance.
- **Ontologies**: from Aristotle to AI; propositional & first-order logic recap, **Description Logics**, the **Web Ontology Language (OWL)**, authoring in Protégé (online + desktop).
- **Ontological engineering**: SWRL rules (fixing OWL undecidability), design workflow, ontology evaluation, alignment, ontology learning, KG construction from unstructured/structured data (NLP, OpenRefine), best practices.
- **Graph analytics & ML**: formal graph definitions, network analysis, **Knowledge Graph embeddings** (dense vectors, distributional-semantics analogy), **graph representation learning**, **KG completion / link prediction** (TransE), error correction, fact checking.
- **KGs + LLMs**: KGs supply explicit, trustworthy knowledge that complements error-prone/hallucinating LLMs — fact checking, explanations, **semantic & exploratory search**, recommendation.

## Summary

The video is the course-overview episode; each instructor previews one week.

**Week 1 — Knowledge representation with graphs (Sack).** Starts from "what is knowledge and how does it differ from data": data is raw and meaningless, knowledge adds context. Covers the "from data to knowledge" framing, knowledge representation, and understanding/interpretation as more than reading. Introduces graphs + triples as an intuitive representation → knowledge graphs, and the Semantic Web vision and its technology-stack architecture. Then Linked Data principles and the Web of Data. Hands-on: graph creation from text, NLP, and resolving NLP ambiguities.

**Week 2 — Basic knowledge-graph infrastructure (Sasha Bruns).** Identifying, distinguishing and accessing things on the web (URIs — "why apples aren't as simple as they seem"); representing facts with RDF and why we need triples; Turtle serialization; RDFS vocabularies/semantics/meaning; complex structures (lists, containers, collections); Excursion on RDF reification & RDF-star; logical inference with RDFS to derive implicit knowledge; Excursion on RDFa and connecting RDF with HTML. Hands-on: RDF in Jupyter/Colab notebooks — serializing, visualizing and manipulating graphs.

**Week 3 — Querying knowledge graphs with SPARQL (Tabia).** Basic SPARQL syntax and first queries; an excursion into the two largest KGs, DBpedia and Wikidata (how they're built and queried); more complex queries (filters), sub-selects and property paths; "SPARQL is more than a query language"; quality assurance via SHACL constraints. Hands-on: three Colab notebooks — querying Wikidata and DBpedia, plus SPARQL federation (incl. a Performing-Arts dataset).

**Week 4 — Ontologies (Mehwish).** A brief history of ontology "from Aristotle to AI" (philosophy → computer science); a recap of propositional and first-order logic; an excursion into Description Logics (since standard logic isn't strong enough for ontologies); the Web Ontology Language (OWL) and defining classes/relations. Hands-on: build an ontology in the online Protégé, import into the desktop version.

**Week 5 — Ontological engineering for smarter knowledge graphs (Anas).** OWL is expressive but has limits (expressivity → undecidability); Excursion on SWRL (Semantic Web Rule Language = Datalog-style rules + OWL) to address undecidability efficiently for reasoners. A step-by-step workflow for designing your own ontology; better design via ontology evaluation; ontology alignment and ontology learning (from text/other sources); KG construction from unstructured vs structured data; best practices. Hands-on: KG construction from unstructured text with NLP, filling a KG from structured data with OpenRefine, and a SWRL session.

**Week 6 — Intelligent applications with KGs and deep learning (Sack).** Formal definition of a graph and graph analysis; Knowledge Graph embeddings (dense vector representations, analogous to distributional semantics in language models — similar nodes/relations land close in vector space); graph representation learning for ML tasks like classification; KG completion via link prediction (since KGs are always incomplete and the world changes) enabling error correction and fact checking; comparing KGs to large language models — LLMs hallucinate and can't be fully trusted, so KGs' explicit, trustworthy knowledge is a complement (fact checking, explanations); finally semantic search and exploratory search / recommendation. Hands-on: network analysis, and KG completion with the TransE embedding model.

## Related

- [OWL (Web Ontology Language) — three-video primer](./owl-web-ontology-language.md) — OWL primer (week-4 Ontologies material: OWL 2, description logic, profiles)

---

Part of: [Knowledge Graphs & Ontologies](./knowledge-graphs.md)
