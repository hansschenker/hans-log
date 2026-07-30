---
slug: build-ontology-in-protege-pizzaowl-01-opening-introduction
title: Build Ontology in Protege (pizza.owl) - 01 Opening & Introduction
channel: Xiaoqi (Yasen) Zhao - Enterprise Architecture
date: 2026-07-30
videoId: l0PZhqmTwfM
url: https://www.youtube.com/watch?v=l0PZhqmTwfM
type: summary
language: en
---

# Build Ontology in Protege (pizza.owl) - 01 Opening & Introduction

_First video (of ~49) in the "Ontology Practice — Build pizza.owl in Protégé" playlist. Analyzed as the entry point / representative sample of the series._

## TL;DR

An enterprise architect kicks off a hands-on series that rebuilds the classic **pizza.owl** ontology in Protégé, step by step. The motivation is that his EA tooling now uses Protégé as its ontology backend, so he bridges familiar EA diagram thinking (box–line–box) with ontology triples (subject–relation–object) that feed a knowledge graph. The series is structured around Michael DeBellis's Pizza tutorial (~14 chapters, 36 exercises), with per-video snapshot models tracked in GitHub so you can start from any point.

## Key Concepts

- **Protégé** — open-source ontology editor used to author OWL ontologies and build knowledge graphs / intelligent systems.
- **pizza.owl** — the canonical teaching ontology; this course adopts Michael DeBellis's detailed pizza case study as its exercise material.
- **EA ↔ ontology bridge** — an ArchiMate-style diagram ("application A *realizes* capability") is already a triple: subject–relation–object; ontology just formalizes that as connected knowledge.
- **Triple / knowledge graph** — knowledge captured as subject–predicate–object statements that link into a graph.
- **Snapshot-driven learning** — a GitHub repo stores a saved model file per video/exercise, so learners can verify their work or jump in at any chapter.
- **Course shape** — ~14 chapters, 36 exercises; each video covers one to three exercises.

## Summary

The presenter — an enterprise architect who previously modeled case studies (Arc Assurance, an argument model) in an ArchiMate-style "RT Ultimate" tool — introduces a new practice series built around the **Pizza ontology in Protégé**. His reason for switching tools: his organization has adopted another EA platform that uses **Protégé as its backend modeling engine**, so learning Protégé and ontologies directly is now valuable to his day job.

He frames the conceptual link between enterprise-architecture modeling and ontologies: when you draw a diagram element on the left, one on the right, and a line between them, you are effectively writing a **triple** — one element is the subject, one is the object, and the line is the relation (e.g. "application A realizes a capability"). Ontologies are exactly this: knowledge expressed as triples that connect into a **knowledge graph**. Protégé is the tool for editing that ontology.

The course material is **Michael DeBellis's pizza.owl tutorial** (credited by name), a well-known, detailed case study. The series will work top-to-bottom through roughly **14 chapters and 36 exercises**, recording the modeling on video, with each video covering one to three exercises depending on length. A **GitHub repository** tracks a step-by-step **snapshot model file** for each video, so viewers can start from any point in the pizza ontology and follow along, and the README will drive the walkthrough from the next video onward.

The stated goals: learn Protégé, learn ontology structure and modeling skill through hands-on practice, and feel the difference between **data-package / ArchiMate-style modeling** and **ontology modeling** (which is fundamentally about *connecting data*). Where useful, later videos will abstract reusable modeling patterns. This opener sets up the environment-building and installation work that begins in the following video.

## Source

https://www.youtube.com/watch?v=l0PZhqmTwfM — playlist: [Ontology Practice — Build pizza.owl in Protégé](https://www.youtube.com/playlist?list=PL6DEHvciXKeUx4P32B3hKMK1t6mC8RhsW) (Xiaoqi "Yasen" Zhao). Based on Michael DeBellis's Pizza tutorial; companion repo https://github.com/yasenstar/protege_pizza

## Related

- [[protege-pizza]]
- [[protege-author-matthew-horridge]]
- [[turtle-syntax]]
- [[ytl-modelling-knowledge]]
