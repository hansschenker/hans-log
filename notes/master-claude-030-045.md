---
slug: master-claude-030-045
title: Master Claude Code Lectures 030–045 — Manage Claude.md
date: 2026-06-25
tags: claude, claude-code, claude-md, rules, hierarchical, context-management
source: ai
---

# Master Claude Code Lectures 030–045 — Manage Claude.md

## TL;DR
Claude.md files can be organized hierarchically across subfolders so only the instructions relevant to the current file are loaded, conserving context window space. A separate rules system (`.claude/rules/`) adds glob-pattern scoping for finer control, and supports both project-level and user-level rules. Together these two mechanisms give full control over what instructions the model sees and when.

## Key Concepts
- **Root claude.md** — loaded as a system reminder at the start of every conversation (always in context)
- **Subfolder claude.md** — loaded reactively only when the model reads a file in that folder; appended to the tool result
- **Inheritance chain** — nested folders stack: reading a deep file appends all claude.md files from its folder up to root
- **`.claude/rules/` directory** — project-level rule files (`.md`) with front matter defining scope via glob patterns
- **Front matter** — metadata at top of a rule file specifying which paths/extensions the rule applies to
- **Glob patterns** — e.g. `**/*.tsx` or `**/*.{tsx,jsx}` to target specific file types
- **User-level rules** — stored in global `~/.claude/rules/`, apply across all projects on the machine
- **Context efficiency** — hierarchical loading leaves more context for actual task content vs. upfront loading everything

## Content

### How Hierarchical Claude.md Works

The top-level `claude.md` (at project root or in `.claude/`) is injected as a system reminder into every message — it's always present. Subfolder `claude.md` files work differently: they're appended to the tool result when the model reads any file in that directory. This means the model only sees subfolder instructions when it's actively working in that part of the codebase.

When a file is deeply nested, Claude Code chains the hierarchy: it appends the immediate folder's `claude.md`, then the parent's, then the grandparent's, all the way up to root. This gives a natural inheritance model — shared conventions at the root, specific patterns closer to the code they govern.

### The Rules System

The `.claude/rules/` folder adds a complementary layer. Each rule is a `.md` file with front matter that declares its scope:

```
---
include: src/components/**/*.{tsx,jsx}
---
Use functional components with explicit prop interfaces.
```

Rules can be organized into subfolders (e.g. `rules/backend/`, `rules/frontend/`). Project rules live in `.claude/rules/` and are codebase-specific. User rules live in a global `~/.claude/rules/` and apply across all projects.

The rules system was introduced primarily to support migration from Cursor, which uses a similar glob-scoped rule format — developers can port their existing rules without rewriting everything as `claude.md` content.

### When to Use Each

| Mechanism | Best for |
|---|---|
| Root `claude.md` | Project identity, always-relevant conventions, startup behaviour |
| Subfolder `claude.md` | Directory-specific patterns (e.g. API routes, UI components) |
| `.claude/rules/` | File-type-specific rules, migrated Cursor rules, fine-grained glob scoping |
| User rules | Personal preferences that apply everywhere (style, language, etc.) |

## Claude Summary

## NotebookLM
[full NotebookLM study guide content | link: url or path]

## Recall.ai
[full Recall.ai summary content | link: url or path]

## Source
- `C:/Users/hanss/Local-Learning/Claude/master-claude-code-course/_lectures/Hierarchical Claude.md and Project Rules Study Guide.md`

## Personal Notes

## Related
- [[claude-mastery-031-045]]
