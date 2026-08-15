---
type: course
title: 01 Course Introduction - KMST
description: Plaban Kumar Bhowmik academic Semantic Web course (RDF, SPARQL, OWL, Linked Data); analyzed first video
resource: https://www.youtube.com/playlist?list=PLvr5jbmh57-JMThwJ-d6NEnt_X3xRVL2p
tags: [knowledge-graphs, semantic-web, ontology]
timestamp: 2026-07-30
---

# 01 Course Introduction — KMST (Knowledge Modelling and Semantic Technologies)

_First video (of 45) in the "Knowledge Modelling and Semantic Technologies" course playlist. Analyzed as the entry point / representative sample of the series._

## TL;DR

The opening lecture of an academic course (ET 60019, by Plaban Kumar Bhowmik) that motivates the **Semantic Web** as "a different kind of internet." It traces the web from a web of *documents* (human-readable but machine-opaque, fragmented across sites) to a web of *data* (entities linked by URIs, machine-processable) topped by a *semantic layer* (ontologies + reasoning). A COVID-19 example shows why fragmented, multi-schema, multi-language data forces humans into tedious "mental integration" — the task the Semantic Web aims to delegate to machines. Closes with the course roadmap: RDF, SPARQL, OWL/ontology engineering, and Linked Data.

## Key Concepts

- **Two drivers of the knowledge society** — storing/processing knowledge and collaborating; the internet massively amplifies both.
- **Web of documents** — hyperlinked pages, human-processable, unstructured and noisy → not machine-understandable.
- **Web of data** — concrete entities identified and linked by **URIs**, so *data* (not just documents) can be hyperlinked and processed by generic programs.
- **Semantic / sense-making layer** — abstract concepts and ontologies enabling **inference** (e.g. bat ⊑ mammal ⊑ animal).
- **Mental integration** — the manual effort of gathering and reconciling facts across many sites; the Semantic Web delegates it to machines.
- **Three stages of delegation** — (1) web of documents, (2) standardized web of data via URIs + a common representation (RDF), (3) semantic layer + reasoning engine.
- **Why mashups fall short** — API/scraping integration needs per-source schema mapping, is brittle to change, and keeps presentation control in the app, not the user.
- **Network effect** — links make documents important (PageRank); the same effect should power the web of data.
- **AI at web scale** — deep inference needs knowledge representation + structured semantics + an inference engine; Tim Berners-Lee's Scientific American proposal ("it's interesting" = the boss wasn't).

## Summary

Bhowmik opens by arguing that humanity's edge comes from two capacities — **storing/processing knowledge** and **collaborating** — and that the internet supercharges both. He then re-frames the course as "the story of a different kind of internet."

**A brief history.** ARPANET, 1969: four nodes (SRI, UCLA, UCSB, Utah); the first message "LOGIN" got as far as "LO" before the system crashed. The **WWW** followed at CERN (Tim Berners-Lee and Robert Cailliao), built on **hypertext**, HTTP, and HTML, turning the internet into a vast graph of interlinked documents. Discovery evolved from typing URLs, to curated directories (Yahoo), to **search engines** (AltaVista, Google) — Google's **PageRank** exploiting the link structure.

**The problem.** Today's web is a **web of documents**: human-readable but **unstructured and noisy**, so machines can't interpret it. Worse, useful data is **fragmented** across sites with different styles, schemas, and languages. His running example is **COVID-19**: transport networks, genome sequences, protein data, national statistics, news, and research papers each live on separate sites in incompatible forms. A virologist must visit each source and **mentally integrate** the pieces — long and tedious. Availability of data isn't the bottleneck; **integration** is.

**The goal: delegate mental integration to machines**, in three stages.
1. **Web of documents** — human-processable pages.
2. **Web of data** — attach **URIs** to *entities* (reusing the web's URI infrastructure) so data items can be **linked** to one another the way documents are, and adopt a **standard representation** so a single generic program works across organizations. Just as HTML standardized publishing documents, the web of data needs a standard for publishing data — this is **RDF**. Ad-hoc XML with private tags doesn't count as standard.
3. **Semantic (sense-making) layer** — add abstract concepts/ontologies plus a **reasoner**. The query "animals that use sonar but neither bats nor dolphins" needs classification and **inference** over an ontology (bats and dolphins are mammals are animals), not just stored facts.

**Why not mashups?** They *do* integrate (World-o-meter, WHO dashboards, travel booking), but via APIs or scraping plus bespoke **schema-mapping** per source — brittle when any API or page changes, and the **presentation is controlled by the app, not the user**. A standard, generic data representation avoids this. And the **network effect** that made documents discoverable (PageRank) should likewise reward well-linked data.

**AI at web scale.** Deep inference needs three ingredients: a way to **represent knowledge**, a way to encode the **semantics** of content in structured form, and an **inference engine** to derive new knowledge — the long-standing agenda of AI, now applied at web scale. He recalls Berners-Lee's Semantic Web proposal in *Scientific American*, and the anecdote that his boss called it merely "interesting."

**Course plan.** Modules: Introduction (architecture, vision, requirements), a light treatment of Knowledge Representation & Logic, **RDF**, **SPARQL**, **OWL / ontology engineering** (the sense-making layer and reasoning), and **Linked Data**, with a possible module on processing information networks / **knowledge graphs**. Grading: four quizzes (80%) plus a term-paper video presentation (20%). Primary texts: Hitzler, Krötzsch & Rudolph, *Foundations of Semantic Web Technologies*, and *The Semantic Web Explained*.

## Source

https://www.youtube.com/watch?v=-LAyRLK0QjQ — playlist: [Knowledge Modelling and Semantic Technologies](https://www.youtube.com/playlist?list=PLvr5jbmh57-JMThwJ-d6NEnt_X3xRVL2p) (Plaban Kumar Bhowmik, ET 60019)

## Related

- [Turtle (Terse RDF Triple Language)](./turtle-syntax.md)
- [Protégé Pizza Tutorial (yasenstar/protege_pizza)](./protege-pizza.md)
- [Build Ontology in Protege (pizza.owl) - 01 Opening & Introduction](./build-ontology-in-protege-pizzaowl-01-opening-introduction.md)
- [Knowledge Graphs - 0.0 Lecture Overview](./knowledge-graphs-00-lecture-overview.md)
- [OWL (Web Ontology Language) — three-video primer](./owl-web-ontology-language.md)

---

Part of: [Knowledge Graphs & Ontologies](./knowledge-graphs.md)
