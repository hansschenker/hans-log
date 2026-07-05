---
slug: ai-engineering-was-hard-until-i-learned-these
title: AI Engineering was HARD until I Learned these 10 Concepts
channel: Andrew Codesmith
date: 2026-07-05
videoId: -qC_1A_WZbs
url: https://www.youtube.com/watch?v=-qC_1A_WZbs
type: summary
language: en
---

# AI Engineering was HARD until I Learned these 10 Concepts

## TL;DR

A beginner-friendly map of the 10 concepts that define modern AI engineering, ordered from basic to complex: LLMs, prompt engineering, context engineering, RAG, embeddings/vector search, tokens/context windows, agents, fine-tuning, MCP, and multimodal AI. The core message: an AI engineer doesn't train models — they pick the right base model and build products on top of it, and the recurring job is deciding which technique (prompting vs context vs RAG vs fine-tuning) solves which problem.

## Key Concepts

- **LLM** — general-purpose text model, "super advanced autocomplete"; you pick one and build on it, never train your own
- **Prompt engineering** — *how* you ask: define format, audience, length, and goal to get consistent output in products
- **Context engineering** — *what* you give it: memory, instructions, documents, chat history, user data around the prompt
- **RAG** — retrieve your private data first, then let the model answer grounded in it; fixes "LLM doesn't know your data"
- **Embeddings & vector search** — text as coordinates on a meaning map; search by meaning, not keywords, at scale via a vector DB
- **Tokens & context window** — models see tokens (~750 words per 1,000 tokens), pricing is per token; context window = whiteboard that wipes the oldest content when full
- **Agents** — set a goal, plan steps, call tools, check results, loop until done; the planning + looping is what makes it an agent
- **Fine-tuning** — change model *behavior* (tone, style, output format); RAG adds *knowledge* — they combine
- **MCP** — "USB port for your AI": one open protocol instead of a custom integration per tool/data source
- **Multimodal AI** — images, audio, video in (and sometimes out); multimodal + agentic is where it gets interesting

## Summary

The video argues that a working vocabulary of AI engineering is now baseline knowledge for anyone in tech — PM, developer, or student — and walks through ten concepts in increasing complexity.

**Foundation layer.** LLMs are big general-purpose models trained on massive text/code corpora — best understood as very good autocomplete. The AI engineer's role is explicitly *not* training them (too complex, too expensive) but picking the right one, knowing its strengths and weaknesses, and building products on top. Prompt engineering is the first lever on quality: "summarize this article" vs "summarize in 3 bullets for a beginner, under 100 words, practical takeaways" — the second defines format, audience, length, and goal, which matters doubly in products where the model must behave consistently for every user. Context engineering extends this from *how you ask* to *what you provide*: memory, instructions, documents, history, user data — like a boss who hands over a project with audience, client, constraints, and success criteria rather than just "do it". Most model failures trace to missing context, not bad models.

**Making models know your data.** RAG solves the problem that LLMs are trained on old, public data. Instead of relying on model memory, the system retrieves relevant chunks from your own documents and grounds the answer in them — the example is an internal support bot that pulls the actual password-reset doc rather than guessing generically. In practice: documents → embeddings → vector database → nearest-match retrieval → chunks fed to the LLM. RAG appears on most AI-engineering job descriptions because it turns a general model into one that knows your stuff. Embeddings are the mechanism underneath: text becomes coordinates on a meaning map where "cat" sits near "kitten", so a search for "best laptop for coding" matches "ideal machine for software development" despite zero keyword overlap; vector search makes that lookup fast at scale.

**Operating constraints.** Models read tokens, not words (a word may split into several tokens; ~750 English words ≈ 1,000 tokens). Tokens drive both limits and cost — APIs charge per token. The context window is a whiteboard of fixed size: fill it and the oldest content gets wiped, which is why long chats "forget" early messages — the model isn't dumb, it ran out of space. Newer million-token windows fit whole books and codebases but cost more and can be slower; balancing window size against cost and latency is a core part of the job.

**The frontier.** Agents move from responding to acting: set a goal, plan steps, call tools/APIs, check results, loop until done — a chatbot answers, an agent works the problem (trip example: research, book hotel and flights, check in). Fine-tuning customizes the model itself when prompting alone is unstable or expensive — brand voice, consistent JSON output; the rule of thumb is RAG for facts the model wasn't trained on, fine-tuning for behavior, and the two combine. MCP standardizes how models reach the outside world — one open protocol as the "USB port" replacing a custom integration per database/email/CRM — and is rapidly becoming the norm for how agents connect to tools. Finally, multimodal AI handles images, audio, and video (whiteboard photos, voice memos, video Q&A); the closing claim is that multimodal input combined with agentic loops is where the future of the field gets genuinely interesting.
