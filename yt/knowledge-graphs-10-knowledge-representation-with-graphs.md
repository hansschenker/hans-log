---
slug: knowledge-graphs-10-knowledge-representation-with-graphs
title: Knowledge Graphs - 1.0 Knowledge Representation with Graphs
channel: ISE FIZ Karlsruhe
date: 2026-07-28
videoId: NTyzkmDyRFs
url: https://www.youtube.com/watch?v=NTyzkmDyRFs
type: summary
language: en
---

# Knowledge Graphs - 1.0 Knowledge Representation with Graphs

## TL;DR

Week-1 intro of the ISE/FIZ Karlsruhe *Knowledge Graphs* course (Harald Sack with Tabia, Anas, Mehwish). It sets up the week's arc: climb the **data → information → knowledge → wisdom** ladder, see why natural language is too ambiguous to represent knowledge formally, then move through graphs & triples to formal knowledge representation, ontologies, the Semantic Web, and Linked Data / the Web of Data. Closes by previewing three hands-on notebooks.

## Key Concepts

- **DIKW ladder**: data is raw and meaningless on its own; adding context lifts it to information, then knowledge, potentially wisdom — knowledge is the course's central focus.
- **Language is ambiguous** and therefore a poor medium for representing knowledge to a machine; we need something more **formal**.
- **Graphs & triples** as an intuitive first form of representing information/knowledge, en route to **formal knowledge representation** that machines can process.
- **Knowledge graphs** rest on explicit semantics via **ontologies**; ontologies + graphs constitute the **Semantic Web** — not a new web but an extension giving each piece of information explicit, machine-accessible meaning.
- **Linked Data & the Web of Data**: what they are, how large the web of data has grown, and why it's needed.
- **NLP pipeline for graph construction**: tokenization, syntactic analysis (part-of-speech tagging, dependency parsing), named-entity recognition.
- **Semantic ambiguity / word-sense disambiguation**: the Lesk algorithm, WordNet, and synsets.

## Summary

This is the opening lecture of week 1, presented by Harald Sack with the team introducing each part.

**The week's lecture arc.** It begins with data: data alone is useless — raw and impossible to make sense of without further information. Part 1 ("From Data to Knowledge") climbs the ladder from **data → information → knowledge → (potentially) wisdom**, with knowledge as the series' central focus and the question of how to represent it. The next lecture, "the art of understanding," asks what makes language ambiguous and what it means to *understand* — concluding that natural language, being highly ambiguous, isn't the best means for representing knowledge, so something **more formal** is needed. Before that formalism, the course introduces **graphs and triples** as an intuitive way to represent information and knowledge. To let a machine actually understand it, this is lifted into **formal knowledge representation**, which leads to **knowledge graphs**. Their explicit semantics rests on **ontologies**; ontologies together with graphs form the **Semantic Web** — described as not a new web but an extension of the current one, where each piece of information carries explicit meaning a machine can access and understand. The week's final lecture covers **Linked Data and the Web of Data** — what they are, how large the web of data has become, and why it's needed.

**Hands-on sessions (3).** (1) *Graph creation from text* done intuitively by hand — turning a short paragraph into a simple knowledge graph as a human would. (2) The first **Python notebook**, showing manual graph creation from raw text via an NLP pipeline: tokenization, syntactic analysis (part-of-speech tagging, dependency parsing) and named-entity recognition. (3) A notebook on **semantic ambiguities** and word-sense disambiguation using the **Lesk algorithm**, **WordNet**, and synsets. The video ends by handing off to the first content lecture, "From Data to Knowledge."
