---
slug: build-agentic-rag-with-claude-code
title: Build Agentic RAG With Claude Code
channel: The Explainer 
date: 2026-07-08
videoId: j0D-i_O_cPw
url: https://www.youtube.com/watch?v=j0D-i_O_cPw
type: summary
language: en
---

# Build Agentic RAG With Claude Code

## TL;DR

Dumping raw code chunks into a plain vector database is an operational trap: vector search matches on fuzzy conceptual proximity, but code is deterministic, so the agent floods its context window, hallucinates file paths, and burns tokens chasing dead-end references. The fix is *agentic RAG* — a four-layer pipeline (CLAUDE.md constraints → structured multi-format ingestion → hybrid BM25 + vector search fused with Reciprocal Rank Fusion → Docker-sandboxed execution) with Claude Code as the orchestrator. On a benchmark that traced and patched a deprecated API endpoint across legacy modules, the agentic stack cut token burn ~10× versus naive vector search.

## Key Concepts

- **The semantic gap** — vector search ranks by fuzzy mathematical proximity, but resolving a variable, route, or dependency in code needs *precise structural routing*, not conceptual closeness. Naive semantic search over a codebase is an architectural mismatch that floods context and escalates API cost.
- **Codebase-as-a-grid analogy** — naive search is a single light scanning randomly in the dark (blind text matching); an agentic system reads the metadata layer and maps exact coordinates, following structural relationships between modules.
- **Layer 1 — deterministic onboarding constraints** — a `CLAUDE.md` file in the project root acts as a repository-level system prompt: restricted file paths, mandatory linting standards, architectural boundaries. These guardrails stop context drift and "token bleed" before a query even runs.
- **Layer 2 — multi-format ingestion** — a document parser (e.g. Docling) normalizes markdown, PDF docs, and raw code into a consistent format, isolating core logic and structural hierarchy. Each file exits as a standardized block tagged with a **unique content hash + metadata**, assigned *at the source before chunking*, which prevents context hallucination downstream.
- **Layer 3 — hybrid search + Reciprocal Rank Fusion (RRF)** — **BM25 keyword matching** retrieves exact syntax, variable names, and function definitions; **vector search** is restricted to conceptual routing / semantic intent. RRF reconciles the two ranked lists into one unified priority score (from the reciprocal of each rank), and only the top fused results consume context tokens.
- **Layer 4 — Docker sandboxing** — Claude Code uses a tool-calling architecture to run terminal commands in the repo; a Docker container contains all agent operations. Inside it, Claude writes scripts/queries, tests them against the retrieved context, and validates output — enabling self-correction and independent verification.
- **Benchmark result** — tracing and patching a deprecated API endpoint across multiple legacy modules: naive vector search failed (hallucinated paths, exhausted context); the agentic stack found the logic via the hybrid index, verified the patch in the sandbox, and generated the fix — **~10× reduction in token burn**.

## Summary

**The problem: naive RAG breaks on code.** Building a retrieval pipeline for a codebase by dumping raw code chunks into a standard vector database wastes tokens systematically. Without structural awareness, an agent hunting a dependency loops endlessly through terminal output chasing references it cannot resolve. This is the *semantic gap*: vector search relies on fuzzy mathematical proximity, but code is deterministic — resolving a variable, route, or syntax dependency requires precise structural routing, not conceptual closeness. The symptoms are tangible: the context window floods with irrelevant files and API costs climb with every query. The strict logic of a codebase needs a different retrieval architecture than plain text.

**The shift: agentic RAG.** The answer is a multi-layered retrieval pipeline built for precision rather than broad matching, with Claude Code acting as an autonomous terminal orchestrator that manages specialized sub-agents. If the codebase is a grid, traditional search is one light scanning randomly in the dark; an agentic system reads the metadata layer and maps exact coordinates between modules. The pipeline has four layers: deterministic onboarding constraints, multi-format ingestion, hybrid search ranking, and secure Docker sandboxing — turning the model from a passive completion tool into an active, sandboxed orchestrator.

**Layer 1 — constraints first.** Before any data is processed, a `CLAUDE.md` config file goes in the project root as a deterministic, repository-level system prompt. It defines the environment's rules — restricted file paths, mandatory linting standards, architectural boundaries — so the model can't drift into irrelevant directories and lose the query. These file-level guardrails prevent token bleed by stopping the agent from exploring dead-end paths before a query executes.

**Layer 2 — structured ingestion.** Extracting raw text from enterprise repos usually strips the hierarchy and structural context needed for reasoning. A parser such as Docling normalizes disparate file types (markdown, PDF documentation, raw code) into a consistent format, isolating the core logic and structural hierarchy. Each file leaves the parser as a standardized block tagged with a unique content hash; those hashes and metadata tags are assigned at the source *before* the data is chunked, so the model always knows the origin and file type of every snippet — which prevents context hallucination as data moves through the pipeline.

**Layer 3 — hybrid retrieval with RRF.** Pure vector embeddings are insufficient for code search. BM25 keyword matching retrieves exact syntax, specific variable names, and function definitions, while vector search is restricted to conceptual routing and semantic intent. Reconciling the two scoring systems — one ranked by keyword frequency, the other by semantic similarity — is done with Reciprocal Rank Fusion (RRF), which computes a unified priority score from the reciprocal of both lists. Only the top results of this fused list enter the context window, so the most relevant chunks are the ones that spend tokens.

**Layer 4 — sandboxed execution.** Claude Code uses a tool-calling architecture to run terminal commands directly in the repository, so the system needs absolute containment. Docker containers provide a secure sandbox for all agent operations: inside the container Claude writes scripts or queries, tests them against the retrieved context, and validates the output — becoming a development partner capable of independent verification and self-correction.

**The benchmark.** The task: trace and patch a deprecated API endpoint across multiple legacy modules. A naive system relying only on vector search failed — it hallucinated file paths and exhausted its context window with terminal searches before finding the deprecated code. The same task through the optimized agentic RAG stack used the hybrid index to locate the logic, verified the patch inside the Docker sandbox, and generated the fix — a **10-fold reduction in token burn** versus the naive baseline. The takeaway: naive semantic search can't meet the deterministic requirements of software development; structural agentic orchestration makes retrieval of logic in complex repositories reliable.

## Related

**Docling ingestion (Layer 2)** — this video's parser, covered in depth:
- [[docling-pdf-for-ai-rag]] — Docling: prepare PDF and other doc formats for AI and RAG
- [[import-everything-into-your-rag-agent-docling-llamaparse]] — Import EVERYTHING Into Your RAG Agent (Docling & LlamaParse)
- [[multimodal-rag-with-docling-from-pdf-to-agentic]] — Multi-modal RAG with Docling: From PDF to Agentic AI Chatbot

**RAG strategy & patterns** — where naive vs. hybrid/agentic retrieval fits:
- [[rag-vs-agentic-ai-how-llms-connect-data]] — RAG vs Agentic AI: when retrieval beats agents and vice versa
- [[every-rag-strategy-explained-in-13-minutes-no]] — Every RAG Strategy Explained in 13 Minutes
- [[rag-explained-in-14-minutes-10-rag-patterns]] — RAG Explained in 14 Minutes: 10 RAG Patterns
