---
type: video
title: What is JSON-LD?
description: JSON-based format for linked data on the semantic web
resource: https://www.youtube.com/watch?v=vioCbTo3C-4
tags: [json-ld, linked-data, semantic-web, rdf, knowledge-graphs]
timestamp: 2026-07-29
---

# What is JSON-LD?

## TL;DR

**JSON-LD** (JavaScript Object Notation for Linking Data) is an extension of plain JSON that
turns ordinary web data into **linked data** — data that can reference and be reused across
websites. It solves JSON's **ambiguity problem** (does one site's `name` mean the same as
another's?) by adding a **`@context`** that maps short, developer-friendly terms to unambiguous
**URLs**, plus an **`@id`** that gives each thing a global identifier. The three foundations of
linked data it delivers: **context**, **concise terms**, and **identifiers** — and it can be
converted to **RDF**, the underlying model of the Semantic Web.

## Key Concepts

- **Document web vs data web** — today's web links *documents* (HTML + hyperlinks, for humans). Linked data extends the same linking idea to *data* so one site's data can reference another's.
- **Two sides of a site** — front end (HTML/JavaScript, for humans) and a data side that typically serves **JSON** (simple key/value pairs, both human- and machine-readable).
- **The ambiguity problem** — mix JSON from several sites and you can't tell whether each one's `name`/`type` means the same thing (first name? login name?). Sharing data requires removing that ambiguity.
- **URLs as unambiguous identifiers** — replacing a bare term like `name` with a full URL makes its meaning explicit, but writing every property as a URL is far too verbose for developers.
- **`@context`** — JSON-LD's core idea: a mapping (often just a URL to a context document) telling the app how to interpret each term *and* what datatype it carries (string, date, number, URL). Lets you stay concise **and** precise — like shared context in human conversation ("I saw Bob" works because both speakers know which Bob).
- **`@id`** — a URL that globally identifies a thing, so anyone else can make further statements about the same entity (Bob's age, hometown, mood) using his identifier.
- **`@type`** — declares what a node is (Person, Place, Recipe, Event).
- **Language tags** — express the same value in multiple languages (Japanese, Mandarin, Spanish…).
- **RDF** — JSON-LD can be converted to RDF, the fundamental model for linked data.
- **Compaction / expansion / framing** — transformations that reshape a JSON-LD document into whatever form an application finds easiest to consume.
- **RDFa** — the analogous technique for embedding linked data *inside HTML* (tagging page bits for search engines / social networks); JSON-LD is the JSON-side counterpart.

## Summary

**The setup: from a web of documents to a web of data.** Today's web is document-based — HTML
pages served to browsers, linked to each other by hyperlinks, meant for humans. Every site
really has two faces: the front end (HTML + JavaScript that people see) and a data side that
serves **JSON** — simple property/value pairs that are easy for both machines and developers to
read. **Linked data** is the idea of publishing your *data* the way we already publish
documents: with links, so one website's data can reference another's, and your data joins the
rest of the web's data and becomes more useful to everyone.

**The problem JSON-LD fixes: ambiguity.** We already solved this for HTML via **RDFa** (tagging
the meaningful parts of a page for machines while humans just see text and images), but there
was no standard way to do it for JSON. Plain JSON looks self-explanatory — `type: person`,
`name: Bob`, `homepage: <url>` — but the moment you combine JSON from several sites you can't
tell whether everyone uses `name` the same way. One site's `name` is a first name; another's is
a login name, even though the `homepage` matches. To share data across sites, that ambiguity
has to go.

**The fix, and the trade-off.** The web's usual tool for being precise is the **URL**: give a
property a full URL and its meaning is unambiguous. But writing every property as a long URL is
so verbose no developer would tolerate it. You want to be *specific* and *concise* at the same
time.

**JSON-LD's answer: `@context`.** The context tells an application how to interpret the rest of
the document — you point `@context` at a URL, and that document defines exactly what `name` and
`homepage` mean and what datatype each should hold (string, date, number, URL). This mirrors how
humans talk: conversation always carries context, so "I saw Bob the other day" is both concise
and specific because both people share the situation. `@context` gives that shared context to
your JSON data.

**Two more foundations: identifiers and terms.** Beyond concise terms, JSON-LD lets you
**identify** things with **`@id`** — a URL that is the entity's universal identifier on the web.
Once Bob has a URL, anyone else can attach further statements to *that same Bob* (his age, mood,
hometown). So JSON-LD does three foundational things for linked data: **(1)** gives a document
context, **(2)** lets you use short terminology, **(3)** gives your data an identifier.

**Beyond the basics.** JSON-LD also supports **`@type`** (Person, Place, Recipe, Event),
**language tags** for multilingual values, precise value typing (dates, times, units), and
conversion to **RDF** — the fundamental linked-data model. Advanced transformations —
**compaction, expansion, framing** — reshape documents to suit an application. The video points
to **json-ld.org** (tutorials + a live "playground" editor) for JSON, and **rdfa.info** for the
HTML/RDFa equivalent. Presenter: **Manu Sporny** (a co-creator of JSON-LD); released CC-BY-SA.

## Notes

- JSON-LD is the pragmatic, developer-friendly on-ramp to the Semantic Web: you write near-normal JSON, and `@context` quietly upgrades it to RDF-compatible linked data. This is exactly the "explicit meaning a machine can access" idea from the knowledge-graphs course, delivered in JSON.
- The mental model that sticks: **`@context` = the shared situation that lets you be brief but unambiguous**, just like context in human conversation.
- Ties directly to the OWL/ontology thread — JSON-LD/RDF is the *data* layer; ontologies (OWL) are the *schema/meaning* layer that reasoners work over. `@type` and property URLs are where a JSON-LD document meets an ontology's classes and properties.
- Practical next step if I want to try it: the json-ld.org playground.

## Source

- What is JSON-LD? — Manu Sporny — https://www.youtube.com/watch?v=vioCbTo3C-4

## Related

- [OWL (Web Ontology Language) — three-video primer](./owl-web-ontology-language.md) — OWL/ontologies: the schema/reasoning layer above RDF that JSON-LD feeds into
- [Knowledge Graphs - 1.0 Knowledge Representation with Graphs](./knowledge-graphs-10-knowledge-representation-with-graphs.md) — graphs, triples, Linked Data / Web of Data
- [Knowledge Graphs - 0.0 Lecture Overview](./knowledge-graphs-00-lecture-overview.md)

---

Part of: [Knowledge Graphs & Ontologies](./knowledge-graphs.md)
