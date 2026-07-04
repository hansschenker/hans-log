---
slug: import-everything-into-your-rag-agent-docling-llamaparse
title: Import EVERYTHING Into Your RAG Agent (Docling & LlamaParse)
channel: The AI Automators
date: 2026-07-04
videoId: eHw_6jhK8AM
url: https://www.youtube.com/watch?v=eHw_6jhK8AM
type: summary
language: en
---

# Import EVERYTHING Into Your RAG Agent (Docling & LlamaParse)

## TL;DR

How to ingest 95+ file formats (documents, presentations, spreadsheets, images) into a RAG agent by routing everything through a document parser that outputs **consistent markdown** — the key that makes the rest of the pipeline (chunk → embed → vector DB → agent) uniform. Three parsers compared in n8n workflows: LlamaParse (hosted, easy, generous free tier), Docling (open source, self-hosted, no external APIs — best for cost at scale and data privacy), and Mistral OCR (PDF-only, fast, cheapest at scale). 80–90% of organizational data is unstructured — this is the door to it.

## Key Concepts

- **Consistent markdown as the pivot format** — whatever the input (PDF, DOCX, PPTX, XLSX, HTML…), parse it to markdown first; naive text extraction (e.g. n8n's extract-from-PDF node) loses images, layout, formatting, and tables
- **LlamaParse (LlamaCloud)** — hosted parsing; free tier 10k credits/month, agentic mode 10 credits/page ≈ 1,000 free pages; options: vision model (GPT-4.1-mini), high-res OCR, adaptive long tables, tables as HTML. Async API: upload → poll job status (pending/success/error/partial) or webhook → fetch markdown result
- **Docling (IBM, open source)** — parses natively with OCR where needed, **no external APIs**: you pay server costs only — best for bulk ingestion, data security, strict privacy. Deploy via the `docling-serve` image (API + optional UI, `DOCLING_SERVE_ENABLE_UI=1`) e.g. on render.com; production needs a gateway app for API key + password protection
- **Docling tradeoffs** — slower (~45s per test PDF vs LlamaParse), resource-hungry (easyOCR crashed a $25/month instance; scale RAM/CPU accordingly)
- **Mistral OCR** — PDFs only, very fast, $1/1k pages (annotations $3/1k), typically cheaper than LlamaParse at scale without self-hosting
- **Structured data goes elsewhere** — spreadsheets with transactions/financials belong in a relational DB queried via natural language (NLQ), not the vector store
- **Full pipeline extras** — mime-type routing per format, create/update/delete handling to avoid stale or duplicated vectors, metadata enrichment, contextual embeddings

## Summary

The premise: most RAG demos only ingest clean text, but 80–90% of an organization's data is unstructured and spread across dozens of formats. The solution is an ingestion layer that converts *anything* into markdown before it touches the vector store. The demo pipeline (n8n) watches a Google Drive folder, downloads new files, routes them by mime type, and sends them to a parser; the returned markdown is chunked (recursive character splitter in markdown mode), embedded with text-embedding-3-small, and stored in Supabase, where a chat agent retrieves it.

**LlamaParse** is the quick start: sign up at llamaindex.ai, test in the playground, then reproduce via API (n8n HTTP nodes — upload the file with parsing options, poll the async job until success, fetch the raw markdown). Its agentic mode handles complex PDFs well, annotates images with inline descriptions (a lightweight alternative to full multimodal RAG), and extracts tables — even from DOCX.

**Docling** is the sovereignty option: IBM's open-source parser runs entirely on your own server, so heavy ingestion volumes cost server time, not API credits — and documents never leave your infrastructure. The practical route is the `docling-serve` container (API + test UI) deployed on render.com; results were slightly below LlamaParse in this test but "very usable". Caveats: it's compute-hungry (upgrade the instance; watch easyOCR memory), and for production you front the private instance with a small gateway app enforcing an API key and login.

**Mistral OCR** remains the recommendation for PDF-only workloads at scale: fast, good quality, $1 per thousand pages, and its annotations feature can extract image/diagram descriptions as JSON.

Rule of thumb: LlamaParse for easy start and breadth of formats, Docling for cost-at-scale and privacy requirements, Mistral OCR for cheap fast PDF volume — and keep genuinely structured data (CSV/Excel) in a relational database with NLQ instead of embedding it.

## Source

https://www.youtube.com/watch?v=eHw_6jhK8AM — The AI Automators

## Related

- [[multimodal-rag-with-docling-from-pdf-to-agentic]] — Docling's image-captioning pipeline in depth
- [[rag-explained-in-14-minutes-10-rag-patterns]] — where ingestion sits among the 10 RAG patterns
- [[ai-claude-rag-architecture]] — chunking strategies for the markdown output
- [[ai-docling-intro-llm-4]] — Docling as LLM preparation
