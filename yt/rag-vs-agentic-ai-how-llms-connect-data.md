---
slug: rag-vs-agentic-ai-how-llms-connect-data
title: RAG vs Agentic AI: How LLMs Connect Data for Smarter AI
channel: IBM Technology
date: 2026-07-05
videoId: fB2JQXEH_94
url: https://www.youtube.com/watch?v=fB2JQXEH_94
type: summary
language: en
---

# RAG vs Agentic AI: How LLMs Connect Data for Smarter AI

## TL;DR

IBM's two-presenter explainer positions agentic AI and RAG as complements, not rivals: agents act autonomously in a perceive–reason–act–observe loop but hallucinate without reliable data access, and RAG is the grounding mechanism — provided you resist dumping everything into context. The practitioner counterpoint to the hype: retrieval quality comes from intentional ingestion (Docling-style curation) plus context engineering (hybrid recall, re-ranking, chunk merging), and the honest answer to "is RAG always best" is "it depends".

## Key Concepts

- **Agentic AI loop** — perceive → consult memory → reason → act → observe, repeating with minimal human intervention; agents operate at the application level, use tools, and talk to each other
- **Coding agents as mini dev team** — architect (plans) / implementer (writes) / reviewer (checks, feeds back); the human becomes an orchestra conductor rather than an instrument player
- **MCP for tool calling** — standardizes how agents reach services and APIs (enterprise routing of support tickets / HR requests)
- **RAG = two phases** — offline: chunk → embed → vector DB; online: embed query → similarity search → top-K chunks → LLM
- **Token/accuracy curve** — retrieving more tokens gives marginal accuracy gains, then *degrades* performance via noise and redundancy, while cost and latency climb
- **Intentional ingestion** — Docling converts PDFs/spreadsheets to LLM-readable Markdown with metadata, preserving tables, graphs, images
- **Context engineering** — hybrid recall (semantic + keyword), re-rank the top-K, merge related chunks into one coherent source of truth → higher accuracy, faster inference, lower cost
- **Local models** — vLLM / llama.cpp keep the same API as proprietary models with data sovereignty and KV-cache tuning

## Summary

The video opens by puncturing two preconceptions: that agentic AI is mainly about coding, and that RAG is always the best way to get fresh, specific information into a model's context. The consultant's answer — "it depends" — frames the rest: explain what each technology actually is, then show what the answer depends on.

**Agentic AI.** Multi-agent workflows perceive their environment, consult memory, reason, act, and observe the result, looping with minimal human intervention. Coding is indeed the flagship use case — an architect agent plans a feature, an implementer writes code straight to the repository, a reviewer checks it and loops feedback, a pattern enabled by LLMs with large context windows and reasoning. The human role shifts to conducting the orchestra. Beyond coding, enterprises route support tickets and HR requests to specialized agents that filter, delegate, and call tools through protocols like MCP — agents responsive in their own environment rather than waiting on a chat window. The catch: without reliable access to external information, agents hallucinate and make misinformed decisions. That is the door RAG walks through.

**RAG.** A two-phase system: offline, documents are chunked, embedded, and stored in a vector database, producing a searchable knowledge index; online, the user's prompt is embedded with the same model, a similarity search returns the top-K (3–5) most relevant chunks, and those land in the LLM's context. Powerful — but scaling breaks the naive version. As more documents and users pile in, more retrieved tokens make recall *harder* for the LLM: the accuracy-vs-tokens curve rises marginally, then bends down as noise and redundancy degrade answers, while the AI bill and wait times grow. The lesson is that not everything should be dumped into context.

**What "it depends" depends on.** Two disciplines rescue RAG at scale. First, intentional ingestion: curate data before it reaches the vector store, using tools like Docling to convert PDFs and spreadsheets into machine- and LLM-readable Markdown with metadata — including tables, graphs, images, and truncated pages, not just body text. Second, context engineering at retrieval time: hybrid recall combines semantic search with keyword search, the returned top-K chunks are re-ranked for relevance, and related chunks are merged so the LLM receives one compressed, prioritized, coherent source of truth. The payoff is higher accuracy, faster inference, and lower cost. A final practical note: open-source local models via vLLM or llama.cpp offer the same API surface as proprietary ones, plus data sovereignty (on-premise) and KV-cache runtime tuning to speed up both RAG and agentic workloads.

Verdict: agents with RAG is a winning combination — usually. It depends.
