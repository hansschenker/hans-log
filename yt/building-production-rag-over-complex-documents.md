---
slug: building-production-rag-over-complex-documents
title: Building Production RAG Over Complex Documents
channel: Databricks
date: 2026-07-15
videoId: dI_TmTW9S4c
url: https://www.youtube.com/watch?v=dI_TmTW9S4c
type: summary
language: en
---

# Building Production RAG Over Complex Documents

## TL;DR

Jerry Liu (co-founder/CEO of LlamaIndex) argues that naive RAG — fixed-size chunks, top-k vector search, stuff-into-prompt — only works for pointed questions over small, simple corpora, and that production RAG fails along two axes: data quality and query complexity. The fix is (1) an LLM-native data pipeline — good parsing (LlamaParse), page-level chunking, and hierarchical indexing where multiple embeddings (summaries, captions, sentences) point to the same underlying chunk — and (2) layering agent ingredients (routing, tool use, query planning, memory, self-reflection) on top of retrieval to turn a lookup system into a knowledge assistant.

## Key Concepts

- **Knowledge assistant** — the real goal beyond RAG: any task in (pointed question, multi-part question, research task) → correct answer out (short answer, structured output, report)
- **Naive RAG** — load → split at fixed chunk size → embed → top-k retrieve → stuff prompt; a "glorified search system" that uses the LLM only once
- **Garbage in, garbage out** — RAG is only as good as its data; bad parsing of tables/layouts causes confident hallucinations even in the best models
- **RAG as a new ETL stack** — parsing, transformation (chunking), and indexing of unstructured data replace classic SQL-based ETL
- **Page-level chunking** — treat each page as a chunk; a surprisingly strong baseline, better than tuning chunk sizes of 512/1024
- **Chunk-boundary failure** — relevant snippets cut in half at chunk boundaries are often never retrieved
- **Hierarchical indexing / decoupled retrieval & synthesis** — embed small references (summaries, captions, individual sentences) that all link to a larger source chunk; retrieve on the small, synthesize on the large
- **Complex documents** — embedded tables, charts, images, irregular layouts, headers/footers; where naive parsers (PyPDF etc.) silently lose or merge table cells
- **LlamaParse** — LLM-native document parser: markdown/JSON output, natural-language parsing instructions (e.g. "output math as LaTeX"), image extraction, multimodal (GPT-4o) mode
- **Agent ingredients vs. full agent systems** — composable pieces (routing, tool use, query decomposition, memory, reflection) vs. cohesive loops (ReAct, DAG-based planning, tree search)
- **Routing** — an LLM prompt as multiple-choice picker; tool use = routing plus parameter inference (function calling)
- **Auto-retrieval / self-query** — LLM infers vector-store metadata filters (e.g. page numbers) from the question; text-to-SQL is the same idea against a SQL database
- **Query planning** — sub-question decomposition, HyDE, step-back prompting, chain of thought; parallelizable sub-queries against different pipelines
- **Reasoning loops** — sequential (ReAct / function-calling while-loop) → DAG-based planning (LLM Compiler; parallelizable but LLMs weaken past ~4–5 steps) → tree search under uncertainty (Tree of Thoughts, LATS; promising but unreliable today)
- **Self-reflection** — lightweight LLM passes for reranking/filtering retrieved nodes and validating final responses (e.g. Prometheus-2 as a small fine-tuned judge)

## Summary

Jerry Liu frames the talk (a 90-minute Databricks workshop with two Colab notebooks using Databricks LLMs — Llama 3 70B — and local Hugging Face embeddings) around building a **knowledge assistant**: an interface that takes any task as input and returns the correct answer, whether that's a short answer, a structured output, or a research report. RAG is just the conceptual framework underneath it.

**Where naive RAG breaks.** The quick-start pipeline — load a PDF, split at a predetermined chunk size, embed into a vector database, top-k retrieval, stuff into a QA prompt — works for simple questions over a few simple documents. It fails on: simple questions over *complex* documents (tables, charts, images, irregular layouts), scaling retrieval quality from 3 PDFs to thousands or millions of documents, and multi-part or vague questions that require iterating over the data. Naive RAG uses the LLM exactly once, as a thin synthesis layer over decades-old retrieval tech — "a glorified lookup system."

**Axis 1: data quality.** RAG is only as good as its data — garbage in, garbage out holds even for GPT-4-class models: if the ground truth is missing or mangled in the prompt, no model recovers it. The data-processing layer is effectively a new ETL stack with three steps: parsing, chunking, indexing.

- *Parsing:* legacy parsers (PyPDF etc.) were never designed to minimize LLM hallucinations — they collapse missing table cells, merge columns, and the resulting "information chaos" measurably raises hallucination rates. LlamaParse parses documents into semi-structured markdown or JSON, supports natural-language parsing instructions (the manga example: "output any math equation in LaTeX markdown"; an insurance example: annotate each claim as covered/not covered during parsing), extracts images and whole pages as images, and handles PDF/PPTX/DOCX/XML/Excel. In an Apple 10-K cell-by-cell benchmark, a LlamaParse-based pipeline answered nearly every table cell correctly where PyPDF/PyMuPDF/Textract/PDFMiner pipelines mostly failed.
- *Chunking:* preserve semantically similar content; watch for relevant text cut at chunk boundaries — the second half often can't be retrieved at all. Page-level chunking is a strong, underrated baseline: documents are written to pack coherent bite-size content into pages, and with falling model costs you can just feed whole pages. Open question for the future: will chunks natively become images (multimodal models), with cost/latency as the current tradeoff?
- *Indexing:* don't just embed raw text — embedding a raw table means embedding a wall of numbers. Instead embed multiple references (extracted summary, caption, individual sentences) that all point to the same underlying node, and store raw data (e.g. images) wherever appropriate with a reference back. This decouples retrieval optimization from synthesis: retrieve on small precise representations, then feed the LLM the full page/table. Demo result: "repayments of debt for Netflix" — naive pipeline says the information isn't provided; the parsed + hierarchically indexed pipeline returns the correct figure.

**Axis 2: query complexity.** Question classes that break naive RAG: summarization over whole documents, comparisons across documents, questions blending unstructured and structured data, and multi-part or vague tasks. The answer is adding agent layers to retrieval. A traditional RAG pipeline is single-shot, has no query understanding/planning, no tool use (the vector DB interface is fixed), no self-correction, and no memory.

He distinguishes **agent ingredients** — simple, testable, composable: routing (LLM as multiple-choice picker, e.g. route summarization questions to a whole-document pipeline and pointed questions to vector search), tool use (routing + parameter inference via function calling; auto-retrieval infers metadata filters, text-to-SQL infers SQL — both are tool use), query planning (sub-question decomposition, HyDE, step-back prompting, CoT), and conversation memory (mostly still a rolling chat buffer; indexing dynamic conversations is unsolved) — from **full agent systems**, which combine them into reasoning loops. Three loop families, in increasing sophistication and cost: sequential (ReAct, or simply a while-loop over native function calling), DAG-based planning (LLM Compiler — plan the whole dependency graph upfront, parallelize independent branches like "Uber revenue" + "Lyft revenue"; LLMs degrade beyond ~4–5 planned steps), and tree search under uncertainty (Tree of Thoughts, reasoning-via-planning, LATS — AlphaGo-style explore/exploit; promising but unreliable at current model capability). Self-reflection belongs throughout: lightweight rerank/filter passes on retrieved nodes and whole-loop response validation, potentially with small fine-tuned judges like Prometheus-2. His read on multi-agent frameworks (AutoGen, CrewAI, LangGraph): most teams today prefer explicitly defined, observable flows composed from ingredients over free-form autonomous agent swarms, though the balance shifts as models improve.

**Workshop 2** builds a research agent over three ICLR 2024 papers (MetaGPT, LongLoRA, Self-RAG): each paper becomes two tools (a vector-search tool whose function signature includes optional page numbers — the docstring *is* the prompt — plus a summary tool), fed to a ReAct agent since Llama 3 lacks native function calling. Asking "MetaGPT comparisons with ChatDev on page 8" shows auto-retrieval inferring the page-number metadata filter; a Self-RAG vs. MetaGPT complexity comparison shows multi-part decomposition across tools. Caveat he flags: one-tool-per-document doesn't scale to hundreds of papers — instead retrieve tools dynamically from a vector store, or use a single tool parameterized by document name.

## Source

https://www.youtube.com/watch?v=dI_TmTW9S4c

## Related

- [[build-agentic-rag-with-claude-code]]
- [[production-rag-with-langchain-vector-databases-full-course]]
- [[rag-fundamentals-and-advanced-techniques]]
