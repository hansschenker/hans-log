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

## NLM

# Hierarchical Claude.md and Project Rules Study Guide

This study guide provides a comprehensive overview of managing project instructions and rules within Claude Code. It focuses on optimizing context usage through hierarchical file structures and implementing granular project and user-level rules.

## Short-Answer Quiz

**1\. What is the primary benefit of splitting a single, large** `claude.md` **file into multiple hierarchical files?**Splitting the file reduces the amount of context used at the start of a session. By placing specific instructions in subfolders, Claude Code only loads the information relevant to the files being edited, leaving more room in the context window for actual tasks.

**2\. Where are the two valid locations where a** `claude.md` **file can be placed within a project?**A `claude.md` file can exist at the root directory of the project. Alternatively, it can be placed inside a dedicated `.claude` folder.

**3\. How does the loading mechanism for a top-level** `claude.md` **file differ from subfolder files?**The top-level `claude.md` file is loaded as a "system reminder" at the very beginning of every conversation, meaning it is included in every message. Subfolder files are only loaded reactively when the model decides to read a file within that specific directory.

**4\. Describe how subfolder** `claude.md` **files are passed to the model during a task.**When the model uses a tool to read a file in a subfolder, Claude Code grabs the requested file and appends the contents of the local `claude.md` file to the "tool result." This information is then passed back to the model as part of that specific interaction.

**5\. What occurs when a model reads a file nested within several folders that each contain a** `claude.md` **file?**The loading follows a pattern of inheritance. If a file is deep within a nested structure, Claude Code appends the `claude.md` file from its immediate folder, and then continues to append the `claude.md` files from every parent folder in the hierarchy up to the root.

**6\. Where should project-based rules be stored to be recognized by the system?**Project-based rules are stored within the `.claude/rules` directory. Users can further organize these rules by creating subfolders within the `rules` folder, such as `backend` or `frontend`, and saving instructions as `.md` files.

**7\. What is the function of "front matter" in a rule's Markdown file?**Front matter is a section at the beginning of the Markdown file that provides specific instructions to the system. It defines where the rule should be applied, including directory paths and specific file extensions.

**8\. How are glob patterns utilized within the rules system?**Glob patterns are used in the front matter to define which files a rule applies to. They can specify entire directories (using `**/*`), specific extensions (like `.tsx`), or multiple extensions (using curly braces like `.{tsx,jsx}`).

**9\. What is the distinction between project-level rules and user-level rules?**Project-level rules are stored in the project's `.claude/rules` folder and apply only to that codebase. User-level rules are stored in a global `.claude/rules` folder (typically in the home directory) and can apply to all files or projects on the user's computer.

**10\. Why did Claude Code implement a rules system in addition to the** `claude.md` **file structure?**The rules system was primarily introduced to help users migrating from other platforms, such as Cursor, which use similar rule structures. It allows users to transfer existing instructions into a format Claude Code understands without converting everything into the `claude.md` format.

---

## Essay Questions

1. **Context Management Strategy:** Analyze how the hierarchical organization of instruction files serves as a solution for context window limitations in large-scale software development.
2. **The Role of Tool Interaction:** Explain the technical relationship between tool calls, tool results, and the appending of folder-specific instructions. How does this "reactive" loading improve model focus?
3. **Migration and Compatibility:** Discuss the advantages of supporting glob-based rules for developers transitioning from other AI-integrated editors. Why might a developer choose the rules system over a standard hierarchical `claude.md` approach?
4. **System Reminders vs. Appended Results:** Evaluate the strategic difference between placing information in the root `claude.md` versus a subfolder or rule file. What types of information are best suited for each?
5. **Automation and Tooling:** Based on the use of "Proxy Man" mentioned in the source, describe how intercepting network requests can help a developer understand and optimize the behavior of agentic coding tools.

---

## Comprehensive Glossary

| Term | Definition |
| --- | --- |
| .claude Folder | A hidden directory at the root of a project used to store Claude-specific configuration, including the claude.md file and the rules subfolder. |
| Appended Tool Result | The process by which Claude Code attaches folder-specific instructions or rules to the end of a file's content before sending it back to the model. |
| Claude.md | A Markdown file used to define best practices, coding patterns, and project-specific instructions for the AI model. |
| Context | The limited "memory" or data processing window available to the model during a session; managing this is critical for performance in large projects. |
| Cursor Rules | A legacy rule format from the Cursor editor that influenced the implementation of project-based rules in Claude Code. |
| Front Matter | Metadata located at the top of a rule's Markdown file that defines application scope (e.g., include paths and extension types). |
| Glob Pattern | A string of characters used to match file names or paths, such as **/*.ts to match all TypeScript files in any subfolder. |
| Hierarchical Structure | An organizational method where instructions are nested in subfolders (e.g., Mac OS or Windows folders) to ensure only relevant data is loaded. |
| Proxy Man | A tool used to intercept and inspect network requests between Claude Code and the Anthropic servers to monitor how data is being passed. |
| System Reminder | Information from the top-level claude.md file that is injected at the beginning of every conversation to provide the model with a "big picture" overview. |
| User Rules | Global rules stored in a user-level directory that apply across all projects on a machine rather than being restricted to a single codebase. |

## Recall.ai
[full Recall.ai summary content | link: url or path]

## Source
- `C:/Users/hanss/Local-Learning/Claude/master-claude-code-course/_lectures/Hierarchical Claude.md and Project Rules Study Guide.md`

## Personal Notes

## Related
- [[claude-mastery-031-045]]
