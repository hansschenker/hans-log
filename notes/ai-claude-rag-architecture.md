---
slug: ai-claude-rag-architecture
title: Learn RAG Architecture
date: 2026-07-04
tags: [ai, rag, chunking, retrieval, architecture]
source: ai
---

# Learn RAG Architecture

## TL;DR

Chunking — splitting raw documents into smaller pieces during ingestion — is the make-or-break step when moving a RAG system from prototype to production. The chunking strategy directly determines the quality of semantic search and the accuracy of generated answers: too-large or arbitrarily split chunks either drown the LLM in irrelevant context or destroy the meaning of the information.

## Key Concepts

- **Chunking** — breaking raw documents into manageable pieces in the RAG ingestion phase
- **Fixed-size chunking** — simplest: split by token or character count
- **Semantic chunking** — split at logical topic shifts, so each chunk holds one coherent thought
- **Hierarchical (small-to-big) chunking** — store precise small chunks linked to larger parent contexts; retrieve small, expand to parent for better LLM understanding
- Chunking quality → semantic search quality → answer accuracy (the chain that matters in production)

## Content

In RAG (Retrieval-Augmented Generation) systems, chunking happens during the ingestion phase. Choosing the right strategy is critical for moving from simple prototypes to production-ready systems.

**Three common strategies, in increasing sophistication:**

1. **Fixed-size chunking** — split text by a specific token or character count. Trivial to implement, but splits are arbitrary and can cut through the middle of a thought.
2. **Semantic chunking** — split on logical topic shifts rather than length, ensuring each chunk contains a coherent topic. Better retrieval precision at the cost of more ingestion work.
3. **Hierarchical (small-to-big) chunking** — store granular chunks linked to larger "parent" contexts. Retrieval matches on the precise small chunk, then pulls in the broader parent context so the LLM understands the surroundings. Best of both: precise matching + full context.

**Why it matters:** engineers must deliberately design the content flow, because chunking directly impacts semantic search quality and final answer accuracy. Poor chunking causes the two classic failure modes — the model struggling with too much irrelevant context, or losing meaning through arbitrary splits.

## Claude Summary

—

## NLM

—

## Recall.ai

—

## Source

Original file: `D:/Learning-Local-Hanss/AI-RAG/RAG-Architecture.md.txt` (copy: [ai-claude-rag-architecture.txt](ai-claude-rag-architecture.txt))

## Notes

—

## Related

- [[ai-docling-intro-llm-4]] — Docling prepares documents for exactly this ingestion/chunking step
