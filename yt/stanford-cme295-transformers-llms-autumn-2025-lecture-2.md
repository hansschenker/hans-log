---
slug: stanford-cme295-transformers-llms-autumn-2025-lecture-2
title: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 2 - Transformer-Based Models & Tricks
channel: Stanford Online
date: 2026-07-04
videoId: yT84Y5zCnaA
url: https://www.youtube.com/watch?v=yT84Y5zCnaA
type: summary
language: en
---

# Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 2 - Transformer-Based Models & Tricks

## TL;DR

Lecture 2 in two halves: how the original 2017 Transformer's components evolved (positional encoding → RoPE, LayerNorm → pre-norm RMSNorm, attention → sliding-window + MQA/GQA), then the taxonomy of transformer models (encoder-decoder / encoder-only / decoder-only) with a BERT deep dive. The load-bearing design choices — RoPE, the GQA-vs-KV-cache tradeoff, and the BERT training recipe — carry directly into modern LLMs and embedding models.

## Key Concepts

- **Self-attention recap** — queries/keys/values, softmax(QKᵀ/√dk)V, multi-head attention as parallel learned projections, interpreted via attention maps
- **Positional encoding evolution** — learned/sinusoidal absolute embeddings → relative-bias methods (T5 learned buckets, ALiBi linear bias) → **RoPE**: rotate Q/K vectors by position-dependent angles so attention depends on relative distance with long-term decay; what most current models use
- **Normalization** — post-norm LayerNorm → pre-norm → **RMSNorm** (fewer learned parameters, comparable convergence)
- **Attention efficiency** — sliding-window/local attention interleaved with global layers avoids O(n²) (Mistral; receptive-field analogy to CNNs); **MQA/GQA** share K/V projections across heads to shrink the KV cache — GQA is the common modern choice
- **Model taxonomy** — encoder-decoder (T5 family, span-corruption with sentinel tokens; mT5, byte-level ByT5), encoder-only (BERT, classification), decoder-only (today's LLMs — next-token prediction scales best)
- **BERT recipe** — bidirectionality vs. causal masking, CLS/SEP tokens, WordPiece, segment embeddings, MLM (~15% masked, 80/10/10) + NSP objectives, fine-tune a small head on CLS
- **BERT successors** — DistilBERT (knowledge distillation via KL divergence on soft targets, half the layers) and RoBERTa (drops NSP, dynamic masking, much more data)

## Summary

The first half (Afshine) walks through the three components of the original Transformer that have changed most since 2017. On positions: the original used learned or sinusoidal absolute embeddings, motivated by wanting nearby tokens to score as more similar via relative-distance dot products. Relative-bias methods came next — T5's learned buckets and ALiBi's deterministic linear bias — before RoPE (rotary position embeddings) won out: rotating query and key vectors by position-dependent angles makes attention scores a function of relative distance and gives long-term decay. On normalization: post-norm LayerNorm gave way to pre-norm placement and then RMSNorm, which drops learned parameters while converging comparably, addressing internal covariate shift. On attention cost: sliding-window/local attention interleaved with global layers (as in Mistral) avoids the O(n²) blow-up, and MQA/GQA share key/value projections across heads to keep the KV cache small at inference — GQA being the standard compromise.

The second half (Shervine) classifies transformer models into three families. Encoder-decoder: the original Transformer and the T5 family (including multilingual mT5 and byte-level ByT5), trained with span corruption using sentinel tokens. Encoder-only: BERT, built for classification — bidirectional attention instead of GPT's causal masking, CLS and SEP tokens, WordPiece tokenization, segment embeddings, and two pre-training objectives: masked language modeling (~15% of tokens masked, with the 80/10/10 mask/random/keep split) and next-sentence prediction; fine-tuning adds a small head on the CLS token (or per-token heads for QA span detection). Decoder-only: today's LLMs — the encoder was dropped because next-token prediction scales best and fits chat use. BERT's successors address its costs: DistilBERT halves the layers via knowledge distillation (KL divergence on soft targets) while retaining most performance; RoBERTa drops NSP with no loss, uses dynamic masking, and trains on far more data.

Worth rewatching: the RoPE intuition, the MQA/GQA-vs-KV-cache tradeoff, and the BERT training recipe — reference points for embeddings and RAG work.

## Source

https://www.youtube.com/watch?v=yT84Y5zCnaA — Stanford Online
