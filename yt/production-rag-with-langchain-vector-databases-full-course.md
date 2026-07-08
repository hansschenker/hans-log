---
slug: production-rag-with-langchain-vector-databases-full-course
title: Production RAG with LangChain & Vector Databases – Full Course
channel: freeCodeCamp.org
date: 2026-07-08
videoId: mHxLXzYjQRE
url: https://www.youtube.com/watch?v=mHxLXzYjQRE
type: summary
language: en
---

# Production RAG with LangChain & Vector Databases – Full Course

## TL;DR

This freeCodeCamp course walks through building **production-grade Retrieval-Augmented Generation (RAG)** systems in Python with LangChain and LangGraph, starting from the premise that most RAG tutorials work on 10 documents but collapse at 10,000. Rather than just building a naive `retrieve → stuff → generate` chain, it diagnoses the five failure modes that kill RAG in production (bad chunking, embedding mismatch, retrieval noise, context overflow, hallucination) and fixes each, then layers on quality upgrades (semantic/late chunking, hybrid search, reranking, parent-document and compression retrievers), scaling and cost engineering (vector-DB index tuning, caching, token budgets), observability (LangSmith), a full FastAPI service deployed to the cloud, and the 2025/2026 cutting edge (agentic RAG, GraphRAG, contextual retrieval, multimodal RAG). "Production" here means secure, observable, cost-aware, self-correcting, and deployable — not a notebook demo.

## Key Concepts

- **RAG chain with LCEL** — LangChain Expression Language pipes (`{context, question} | prompt | llm | StrOutputParser`) compose retriever, prompt, model and parser; `RunnablePassthrough` forwards the raw question, `RunnableParallel` feeds context and question in parallel.
- **Grounding prompt pattern** — "Answer based only on the following context; if you don't know, say I don't know," plus source tags, reduces hallucination and enables citations users can verify.
- **Document loaders** — LangChain wrappers (`PyPDFLoader` fast/basic, `PyMuPDFLoader` fast+rich metadata, `UnstructuredPDFLoader` for tables/complex layouts, `TextLoader`, `DirectoryLoader` with glob filters, `WebBaseLoader`) turn raw files into `Document` objects with `page_content` + `metadata`.
- **Chunking is architecture, not preprocessing** — the single biggest lever on retrieval quality; four variables: chunk size (~200–1000 tokens sweet spot), overlap (cheap insurance against orphaned context at boundaries), split boundaries, and content type.
- **Chunking strategies** — fixed (never in production), recursive (`RecursiveCharacterTextSplitter`, the reliable default that splits on a separator hierarchy: paragraphs → sentences → words → chars), semantic (`SemanticChunker` from langchain-experimental, splits at embedding-similarity drops), and late chunking (embed whole doc first, then split embeddings — preserves cross-chunk context, ~10–12% accuracy gain, needs models like Jina embeddings v2).
- **Embeddings vs chat models** — embedding models (`text-embedding-3-small`=1536 dims, `-3-large`=3072, Gemini=768, BGE-small=384) output vectors, not text; more dimensions = more nuance but more storage and slower search. Rule: use the *same* embedding model for indexing and querying.
- **Two-phase pipeline** — indexing (load → split → embed → store) is one-time; querying (embed query → search → retrieve → augment → generate) runs per question. ~90% of RAG failures are retrieval failures, not generation failures.
- **Vector databases** — Chroma (local, `get_or_create_collection`, `upsert`, distance scores where lower = more similar), PGVector (Postgres extension, self-host or managed), Pinecone (managed, auto-tuned); metadata filtering narrows retrieval.
- **Hybrid search (BM25 + vector + RRF)** — vector search fails on product codes, acronyms (WCAG), exact names, and error codes; BM25 catches exact/keyword matches; `EnsembleRetriever` (or manual reciprocal rank fusion) fuses them with tunable weights (start 50/50, K≈4). Note: BM25 needs a full rebuild on document adds and adds ~20–50ms latency.
- **Advanced retrievers** — `ParentDocumentRetriever` (search small chunks, return their large parent for full context), `ContextualCompressionRetriever` + `LLMChainExtractor` (extract only relevant sentences, ~82–87% token reduction), `MultiQueryRetriever` (LLM generates query variants for broader recall).
- **HNSW index tuning** — hierarchical navigable small world graphs; `M` (max connections per node) and `ef` (search-effort candidate-list size) create a three-way tradeoff among accuracy, speed, and index size — pick two.
- **Cost & scaling engineering** — reduce embedding dimensions (1536→512 saves 30–60%), quantization (float32→int8, 50–75%), batch queries, caching (embedding cache via `CacheBackedEmbeddings`, exact-match and semantic response caching), right-sizing; vertical scaling first, shard only past ~10M vectors.
- **Token budgeting & guardrails** — estimate tokens before the call and reject over-budget requests (no API call, no cost); track input/output tokens and request counts per user/endpoint for chargeback and abuse prevention.
- **Observability with LangSmith** — three pillars (structured JSON logging, metrics collection, instrumented LLM calls); traces/metrics/evals expose the whole journey via `@traceable` decorator and two env vars, so you debug non-deterministic, silently-failing, cascading LLM systems instead of guessing.
- **Agentic RAG (LangGraph)** — a `StateGraph` with retrieve → grade → (rewrite/retry loop) → generate/fallback nodes; the agent self-corrects on low-relevance results, capped by `max_retries` to bound cost. This is the recommended 2026 production pattern.
- **GraphRAG, contextual retrieval, multimodal RAG** — knowledge graphs (entities as nodes, relationships as edges) for multi-hop reasoning; Anthropic's contextual retrieval (LLM prepends context to each chunk before embedding, ~49% fewer failures alone, 67% with reranking); ColPali + vision LMs embed document *images* to preserve tables/charts/layout (~10× the cost).

## Summary

**Foundations.** The course opens with a RAG overview — a query hits a retriever, retrieved context plus the question feeds a prompt template, and an LLM generates a grounded answer — then sets up the toolchain with `uv` for packaging and `langchain`, `langchain-core`, `langgraph`, `langchain-openai`, and `langchain-anthropic`, keying OpenAI and Anthropic. It covers document loaders (PyPDF, PyMuPDF, Unstructured, Text, Directory, WebBase), then makes chunking the centerpiece: fixed vs recursive vs semantic vs late chunking, with the four quality variables (size, overlap, boundaries, content type). Embeddings are contrasted with chat models (vectors vs text), dimensions explained (`text-embedding-3-small`=1536), and the two-phase indexing/querying pipeline established with the rule that the same embedding model must be used in both phases.

**Vector stores and the basic chain.** Chroma is used hands-on for `add`/`upsert`, similarity search with distance scores, and metadata filtering. A basic RAG chain is assembled in LCEL with `RunnablePassthrough`, `format_docs`, prompt, LLM, and `StrOutputParser`, later extended to return sources for citations.

**The five failure modes.** The spine of the course: (1) bad chunking → recursive splitters and overlap; (2) embedding mismatch → deeper embedding work, batching, cosine similarity ranking; (3) retrieval noise → hybrid search combining BM25 and vector via reciprocal rank fusion (`EnsembleRetriever`, with a manual RRF fallback since it was removed from the SDK); (4) context overflow → token budgeting that rejects oversized requests pre-call; (5) hallucination → grounding prompts and output validation.

**Quality optimization.** Semantic vs recursive chunking is benchmarked on the same documents — and, instructively, recursive *wins* on well-structured docs with headers while semantic shines on flowing unstructured text (with a "smart chunker" using semantic-primary/recursive-fallback). Advanced retrievers are demonstrated: `ParentDocumentRetriever` (small chunks for precision, parent chunks for context), `ContextualCompressionRetriever` with `LLMChainExtractor` (dramatic token reduction), and `MultiQueryRetriever`.

**Scaling and cost.** HNSW `M`/`ef` tuning and the accuracy/speed/size tradeoff are explained across Chroma, PGVector, and Pinecone, with vertical vs horizontal (sharding) scaling guidance and real cost curves at 500K/5M/50M vectors. Deployment paths (Supabase — recommended, Neon, AWS RDS) are shown, with a full Supabase PGVector connection walkthrough including RLS. Cost-optimization levers: dimension reduction, quantization, batching, embedding caching (`CacheBackedEmbeddings`), and exact-match plus semantic response caching.

**Observability and a production API.** LangSmith is wired in via `@traceable` and env vars, covering structured JSON logging, metrics, and traces. The course then builds a complete FastAPI + LangGraph chat API module by module: Pydantic config/models, a security layer (prompt-injection sanitizer, PII detection/masking, output validation), a TTL response cache, monitoring (JSON logger + metrics collector), and a LangGraph agent with retry/fallback nodes. Everything is wired into FastAPI with SlowAPI rate limiting, health/metrics/cache endpoints, tested with pytest, Dockerized (non-root user, health checks, docker-compose), and deployed to Render with `render.yaml` infrastructure-as-code and auto-deploy on git push.

**Cutting edge.** The finale covers RAG vs long-context (RAG ~1200× cheaper at scale, so combine both), Anthropic's contextual retrieval (LLM-prepended context before embedding), late chunking (embed-then-split preserves pronoun/reference context), agentic RAG (a self-correcting LangGraph `StateGraph` that grades retrievals and rewrites queries within a `max_retries` bound), Microsoft-style GraphRAG (entity/relationship knowledge graphs, multi-hop traversal, local vs global search, using NetworkX and optionally Neo4j), and multimodal RAG with ColPali + vision LMs for tables/charts/images. The closing arc frames RAG's evolution — naive (2023) → optimized hybrid+rerank (2024) → intelligent/self-correcting (2025) → agentic/multimodal/graph-enhanced (2026) — declaring the naive "chunk and pray" approach dead.

## Related

**Agentic & Claude-centric RAG** — the self-correcting / orchestrated end of the spectrum this course builds toward:
- [Build Agentic RAG With Claude Code](./build-agentic-rag-with-claude-code.md)
- [RAG vs Agentic AI: when retrieval beats agents and vice versa](./rag-vs-agentic-ai-how-llms-connect-data.md)

**RAG strategy & patterns** — the conceptual map this course is one implementation of:
- [Every RAG Strategy Explained in 13 Minutes](./every-rag-strategy-explained-in-13-minutes-no.md)
- [RAG Explained in 14 Minutes: 10 RAG Patterns](./rag-explained-in-14-minutes-10-rag-patterns.md)

**Ingestion (Docling)** — the parsing/loading layer that feeds chunking:
- [Docling: prepare PDF and other doc formats for AI and RAG](./docling-pdf-for-ai-rag.md)
- [Import EVERYTHING Into Your RAG Agent (Docling & LlamaParse)](./import-everything-into-your-rag-agent-docling-llamaparse.md)
- [Multi-modal RAG with Docling: From PDF to Agentic AI Chatbot](./multimodal-rag-with-docling-from-pdf-to-agentic.md)
