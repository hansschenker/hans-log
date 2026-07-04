---
slug: multimodal-rag-with-docling-from-pdf-to-agentic
title: Multi-modal RAG with Docling: From PDF to Agentic AI Chatbot
channel: Case Done by AI
date: 2026-07-04
videoId: Uky2eJ25oHY
url: https://www.youtube.com/watch?v=Uky2eJ25oHY
type: summary
language: en
---

# Multi-modal RAG with Docling: From PDF to Agentic AI Chatbot

## TL;DR

Hands-on walkthrough (with open-source repo) of building a multimodal RAG chatbot where PDFs containing text *and* images become one enriched knowledge base. Docling (IBM's open-source document processor) converts the PDF, sends detected images to OpenAI for captioning, and inserts the captions into the text — the enriched text is then chunked, embedded, and stored in Milvus, where a LangGraph agent with multiple retrieval tools answers questions and routes to the right knowledge collection by itself.

## Key Concepts

- **Multimodal RAG** — the knowledge base goes beyond text; ~70% of PDF pipelines simply ignore images, losing whatever the figures carry
- **Enriched text** — detect an image → have an LLM describe it → insert the description into the document text; captions get embedded alongside prose
- **Docling** — IBM's open-source document converter: standard PDF pipeline (plus Word/PowerPoint/HTML), export to markdown, and a **hybrid chunker** that outputs LangChain-ready documents with a configurable token size per chunk
- **Picture description API options** — the Docling pipeline hook that sends detected images to a vision model (here GPT-4.1-mini) with a caption prompt during conversion
- **Markdown export with external image references** — keeps the image files alongside the markdown, so you can later embed the images themselves (a second, image-vector pipeline) instead of only their captions
- **Indexing setup** — chunks embedded with OpenAI text-embedding-small into Milvus; one collection per knowledge topic/folder (one demo PDF → 9 chunks; a McKinsey PDF → 51)
- **Agentic RAG in LangGraph** — each collection is a named retrieval tool with a description; the agent routes the question to the right tool, grades whether the retrieved documents suffice, and rewrites the query and loops if not

## Summary

The problem: to RAG over real PDFs you must handle their images, not just the text. The vanilla Docling conversion marks a figure as `image` and moves on — if the surrounding text doesn't describe it, that meaning is lost. The fix is one added step in Docling's PDF pipeline (picture description options): every detected image is sent to OpenAI with a captioning prompt, and the returned description is inserted at the image's position in the markdown. The result is an "enriched document" ready for embedding. Docling can also export markdown with external image references, which the presenter highlights as the door to a second-stage pipeline that embeds the images themselves rather than only their captions.

Indexing: a config file centralizes models, chunk size (512 tokens default), Milvus endpoint and collection names. Docling's hybrid chunker splits the enriched text into LangChain documents, which are embedded (OpenAI text-embedding-small) and stored per-topic — one Milvus collection per document folder, e.g. a Docling-docs collection and an agentic-AI collection.

Serving: a LangGraph agent gets one retrieval tool per collection, each with a meaningful name and description (that's what the LLM uses to pick the right knowledge base). The graph routes an incoming question to a retrieval tool, checks whether the retrieved context is sufficient to answer, and if not rewrites the question and loops until it can terminate. In the chat demo the agent visibly switches tools: a Docling question triggers the Docling retriever, a banking/agentic-AI question triggers the other collection — reasoning over which knowledge source fits the query.

## Source

https://www.youtube.com/watch?v=Uky2eJ25oHY — Case Done by AI (open-source repo accompanies the video)

## Related

- [[rag-explained-in-14-minutes-10-rag-patterns]] — this is patterns 8 (agentic) + 9 (multimodal) implemented concretely
- [[ai-claude-rag-architecture]] — chunking foundations
- [[ai-docling-intro-llm-4]] — Docling as LLM preparation
