---
slug: ontology-expert
title: Harald Sack — Presentations (Knowledge Graphs & Ontologies)
date: 2026-08-01
tags: [cs, ontology, knowledge-graphs, semantic-web, owl, rdf, digital-humanities, neuro-symbolic]
source: cs
---

# Harald Sack — Presentations archive (`lysander07/Presentations`)

*GitHub slide archive analyzed — [github.com/lysander07/Presentations](https://github.com/lysander07/Presentations). ~18 conference talks & keynotes (2021–2023), CC-licensed (CC BY-SA / CC BY-NC). Note synthesized from deck titles + extracted slide text (the DIKW deck) + the symbolic/subsymbolic keynote; most slides are image-based, so this is a thematic summary rather than a slide-by-slide transcript.*

## TL;DR

A public archive of **Prof. Dr. Harald Sack**'s conference presentations. Sack leads **Information Service Engineering** at **FIZ Karlsruhe – Leibniz Institute for Information Infrastructure** (and KIT), and is one of the best-known European lecturers on **knowledge graphs, ontologies, and the Semantic Web** (his open YouTube lecture series are widely used). The decks cluster around three themes: (1) the **Data → Information → Knowledge** progression and why raw data alone is worthless without semantics, (2) **ontologies and knowledge graphs** as the machinery that adds that meaning, and (3) the **symbolic vs. subsymbolic AI "epic dilemma"** — reconciling explicit, logic-based knowledge graphs with statistical neural models and LLMs.

## Key Concepts

- **DIKW pyramid** (Ackoff 1989) — Data → Information → Knowledge → (Wisdom): raw symbols become information when enriched with **semantics**, and knowledge when that information is evaluated and made usable. Sack's recurring thesis: *"warum Daten alleine nicht ausreichen"* — why data alone is not enough.
- **Ontologies** — formal, shared specifications of a conceptualization (classes, properties, axioms in RDF/OWL) that give machines an explicit vocabulary and inference rules. The "Everything you always wanted to know about Ontologies" deck is the primer.
- **Knowledge graphs** — semantically-linked, graph-structured knowledge built on ontologies; the practical, publishable form of the Semantic Web.
- **Symbolic vs. subsymbolic AI** — the "epic dilemma": **symbolic** (KGs, ontologies, logic — explainable, precise, curated) vs. **subsymbolic** (neural nets, embeddings, LLMs like ChatGPT — fluent, scalable, opaque). The 2023 keynote argues toward **neuro-symbolic** integration rather than either extreme.
- **FAIR data** — Findable, Accessible, Interoperable, Reusable research-data management, realized through KGs and ontologies.
- **Digital humanities & research infrastructure** — many talks apply KGs to the humanities: **NFDI4Culture**, **NFDI4DataScience**, the **GND** authority file, **Wikibase**, art history, and historians' tooling.
- **Bias in knowledge graphs** — social and technical biases baked into KGs (Dagstuhl 2022) — a reminder that curated knowledge is not neutral.

## Content

The repository is a flat archive of PDF slide decks from Sack's 2021–2023 talks; there is no code, just the presentations, released for reuse under Creative Commons. Grouped by theme:

**Foundations — from data to knowledge**
- *Data – Information – Knowledge Graph (#vKG2021)* — the DIKW narrative: data is inert symbols; information is data plus semantics; knowledge is evaluated, usable information. The core motivation for the whole knowledge-graph enterprise.
- *Everything you always wanted to know about Ontologies (but were afraid to ask)* (PMD Ontologies Workshop, 2021) — an accessible ontologies primer.
- *Handout — Knowledge Graphen: Publizieren und Forschen mit Wissensgraphen* — a long-form (~190pp) German handout on publishing and doing research with knowledge graphs.

**The AI tension**
- *Symbolic and Subsymbolic AI — an Epic Dilemma?* (EGC 2023, Lyon; and a companion variant) — written in the immediate wake of ChatGPT (the deck cites the OpenAI playground and chat), it frames the field's central question: how to combine the rigor and explainability of symbolic knowledge graphs with the fluency and coverage of large language models. The pitch is **neuro-symbolic AI** — using KGs to ground, constrain, and explain neural models.

**Applications — research data & the humanities**
- *FAIR Research Data Management with Knowledge Graphs and Ontologies* (InnoMatSafety, 2021)
- *Keynote — Graphs & Networks in the Humanities* (2022)
- *Knowledge Graphs — LMU, Future of Art History* (2021)
- *NFDI4Culture — Knowledge Graph and Wikibase*; *KnowledgeGraphs@nfdi4Culture* (2022); *Harald — NFDI4DS Berlin* (2023)
- *Die Welt ist klein… (GNDCon 2.0, 2021)* — small-world networks and the GND authority file
- *Social and Technical Biases in Knowledge Graphs* (Dagstuhl, 2022)
- German digital-humanities talks: *Analytische Visualisierungen (WorkshopDH)*, *Historikertag — Werkzeugkasten*, *Wiedergutmachung Status*, *ReNewRS — Future Democracies*.

The through-line across all of them: **semantics is the missing ingredient that turns data into knowledge**, ontologies and knowledge graphs are how you add it, and the future lies in marrying that symbolic knowledge with subsymbolic (neural / LLM) methods.

## Source

- Repo: https://github.com/lysander07/Presentations
- Author: **Prof. Dr. Harald Sack** — Information Service Engineering, FIZ Karlsruhe – Leibniz Institute for Information Infrastructure & KIT (Karlsruhe Institute of Technology)
- Known for the open YouTube lecture series on Knowledge Graphs and Semantic Web Technologies (ISE / FIZ Karlsruhe)
- Licenses: decks marked CC BY-SA 4.0 / CC BY-NC 4.0
- Logged: `hans-log.md` → 2026-08-01 → `cs | ontology-expert`

## Notes

- This is a **primary-source lecturer** for the ontology/KG track that's been building in `cs` — the theory backdrop to the hands-on Protégé work. Sack answers *why* (semantics, DIKW, KGs); the Protégé notes answer *how*.
- The *Symbolic vs. Subsymbolic* dilemma is the most current thread: it's the KG-vs-LLM debate stated cleanly by a KG insider, and the neuro-symbolic answer is worth tracking as LLMs and knowledge graphs converge (grounding, RAG, GraphRAG).
- For deep dives, his **YouTube lectures** are the better artifact than these slides (which are image-heavy) — a good candidate for a future real `yt note`.

## Related

- [[protege-pizza]] — hands-on OWL ontology building in Protégé (the *how*)
- [[protege-author-matthew-horridge]] — author of the original Protégé/OWL building guide
- [[turtle-syntax]] — RDF serialization for the graphs Sack describes
- [[what-is-a-model]] — conceptual modeling, upstream of ontology engineering
