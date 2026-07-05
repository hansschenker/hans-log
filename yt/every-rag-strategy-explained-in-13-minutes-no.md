---
slug: every-rag-strategy-explained-in-13-minutes-no
title: Every RAG Strategy Explained in 13 Minutes (No Fluff)
channel: Cole Medin
date: 2026-07-05
videoId: tLMViADvSNE
url: https://www.youtube.com/watch?v=tLMViADvSNE
type: summary
language: en
---

# Every RAG Strategy Explained in 13 Minutes (No Fluff)

## TL;DR

A rapid tour of 11 RAG strategies with the trade-off for each, split between query-time techniques and data-preparation techniques. The central advice: no single strategy wins — the optimal system combines 3–5 of them, and the tactical starter trio is re-ranking + agentic RAG + context-aware chunking (hybrid chunking with Docling). Companion GitHub repo has pseudo code per strategy, built on Postgres + PGVector (Neon).

## Key Concepts

**Query-time strategies:**
- **Re-ranking** — retrieve many chunks, let a cross-encoder pick the truly relevant few for the LLM; his #1, used in almost every implementation
- **Agentic RAG** — agent chooses *how* to search (semantic search vs reading a whole document); flexible but less predictable
- **Knowledge graphs** — vector search + graph DB of entity relationships (Graphiti); great for interconnected data, slow/expensive to build
- **Query expansion** — LLM rewrites the query more specifically before search; one extra LLM call per search
- **Multi-query RAG** — LLM generates several query variants searched in parallel; better coverage, more DB queries
- **Hierarchical RAG** — parent/child chunk metadata: search small (precision), return big (context)
- **Self-reflective RAG** — LLM grades retrieved chunks (e.g. 1–5) and retries with a refined search below threshold

**Data-preparation strategies:**
- **Contextual retrieval** (Anthropic) — LLM prepends per-chunk text explaining how the chunk fits the document, embedded together
- **Context-aware chunking** — split at natural document boundaries found via embeddings (Docling hybrid chunking), not every N characters
- **Late chunking** — embed the whole document first, then chunk the token embeddings; chunks keep full-document context, most complex
- **Fine-tuned embeddings** — train the embedding model on domain data (legal, medical, sentiment); ~5–10% accuracy gain, needs data + infra

## Summary

The video assumes the standard RAG pipeline — data preparation (chunk → embed → vector DB) and query (embed question → similarity search → chunks as LLM context) — and treats every strategy as a variation on one of those two halves. The framing question isn't "which strategy is best" but "which 3–5 combine best for your use case".

**Re-ranking** leads because it's the one he uses almost everywhere: a two-step retrieval that pulls a large candidate set from the vector DB, then a specialized cross-encoder model filters it down to the genuinely relevant chunks. The LLM considers more knowledge without being overwhelmed by 20–50 raw chunks, at the modest cost of a second model call. **Agentic RAG** hands the search decision to the agent itself — his live setup (Neon Postgres) has a chunks table plus a document-metadata table, and the agent picks semantic search or full-document reads per question. Powerful, but only worth it with clear instructions for when to use each search mode, since it trades predictability for flexibility. **Knowledge graphs** add a second store: an LLM extracts entities and relationships from raw text into a graph DB so the agent can traverse relationships rather than just similarity — fantastic for interconnected data, but LLM-driven graph construction is slow and expensive.

**Contextual retrieval** (Anthropic's research) enriches each chunk at indexing time: an LLM writes a short preamble describing how the chunk fits the whole document, and preamble + chunk are embedded together — better retrieval, but an LLM call per chunk. **Query expansion** and **multi-query RAG** are the simple siblings: one LLM call either sharpens a single query or fans it out into parallel variants for broader coverage; both just add latency per search.

On the data-prep side, **context-aware chunking** splits documents at natural boundaries discovered with an embedding model instead of fixed character counts, preserving document structure for free — Docling's hybrid chunking is his implementation of choice and, in his words, "has been killing it". **Late chunking** inverts the usual order — embed the full document with a long-context embedding model, then chunk the token embeddings — so every chunk retains whole-document context; he flags it as the most complex and the only one he hasn't used. **Hierarchical RAG** stores parent/child relationships in chunk metadata to search precisely (paragraph level) and return broadly (whole file) — arguably a subset of agentic RAG. **Self-reflective RAG** wraps search in a self-correcting loop: an LLM grades results against the question and retries with a refined query below a threshold. Finally, **fine-tuned embeddings** retrain the embedding model itself on domain-specific data — for example a sentiment-tuned model puts "my order was late" near "items are always sold out" rather than near "shipping was fast" — worth ~5–10% accuracy and letting small open-source models beat large generic ones, but requiring training data and ongoing infrastructure.

Closing recommendation: start with re-ranking, agentic RAG, and context-aware chunking, then grow toward 3–5 combined strategies as the use case demands.
