---
slug: 160000-cloned-these-3-free-ai-employees-heres
title: 160,000+ Cloned These 3 FREE AI Employees: Here's How (GitHub Claude Skills)
channel: Helena Liu
date: 2026-07-05
videoId: cBgT0PG4JkM
url: https://www.youtube.com/watch?v=cBgT0PG4JkM
type: summary
language: en
---

# 160,000+ Cloned These 3 FREE AI Employees: Here's How (GitHub Claude Skills)

## TL;DR

A beginner-oriented tour of three popular open-source Claude skill repos on GitHub — an LLM-council advisor panel (Karpathy-inspired), a "last 30 days" multi-platform sentiment scanner, and a full virtual dev team attributed to Garry Tan — installed by cloning the repos into Claude's desktop app (Cowork). Framed by two Stanford AI Index findings: frontier models have converged (<5% gap, AI is commoditized) and most businesses still use AI as a chatbot while the technology has moved on to agents.

## Key Concepts

- **Model convergence** — Stanford's annual AI report: best-to-worst model gap is now under 5%, so paid/free/open-source barely matters; the edge shifts from *which model* to *how you use it*
- **Chatbot → agent gap** — most businesses still prompt-and-respond; agents take actions, and pre-built open-source agents shortcut the adoption curve
- **LLM Council skill** — five Claude advisors debate in parallel (contrarian, first-principles thinker, expansionist, outsider, executor), then cross-review → verdict + blind spots + recommendation; trigger: "council this …"
- **Last 30 Days skill** — scans Reddit, X, YouTube, TikTok, Instagram, Hacker News for recent sentiment on any topic; returns a report with exact quotes and source URLs — visibly richer than vanilla Claude on the same prompt
- **Virtual dev team repo** — CEO/founder, engineering manager, senior designer, staff engineer, QA lead etc. as slash commands (office hour, plan CEO review, design review); demo builds a 3D landing page in minutes
- **Vetting open-source skills** — read the repo README, judge by stars and forks before installing
- **Installation** — requires the Claude desktop app (not web); clone the GitHub repo into the local Claude folder; skills appear as slash commands when loaded

## Summary

The video opens with two findings from Stanford's 400-page annual AI report. First, the large language models have converged: a gap that was dramatic a couple of years ago is now under 5%, meaning paid, free, and open-source models all work well — AI has been commoditized, so the differentiator is no longer model choice. Second, businesses haven't caught up: most owners still use AI as a chatbot (type a prompt, get a response) while the technology has moved to agents that take actions. Her proposed shortcut for closing that gap is adopting pre-built, open-sourced agent skills from GitHub — vetted by stars and forks — rather than building from scratch.

**Skill 1: LLM Council.** A variation on Andrej Karpathy's method of having several LLMs (ChatGPT, Gemini, Claude, Perplexity) debate the same question — except here all five debaters are Claude personas running in parallel: a contrarian, a first-principles thinker, an expansionist, an outsider, and an executor. Her worked example is a bakery strategy question (grow subscribers vs monetize the loyal base; referral program vs second location): each advisor argues, they review each other, and the output ends with a verdict (monetize the loyal base first), the blind spots the council caught, and a recommendation. She describes it as a free board of advisors and uses it nearly daily for strategic questions.

**Skill 2: Last 30 Days.** A trending repo (46k+ stars, #1 repository of the day) that scans Reddit, X, YouTube, TikTok, Instagram, and Hacker News for what people said about any product, topic, or industry in the last month. Her Zapier demo surfaces ranked pain points with exact quotes and clickable source URLs — people wanting a human-approval layer in workflows, complaints about pricing, PDF-generation frustrations — and she contrasts it with the same prompt to vanilla Claude, which returns a generic G2/Capterra-flavored summary. Use cases: product research, competitor differentiation, mining pain points before starting a business, and content research for videos.

**Skill 3: The virtual dev team.** A repo she attributes to Garry Tan of Y Combinator (115k+ stars) containing an entire software team as agents — CEO/founder, engineering manager, senior designer, design partner, staff engineer, tester, design engineer, QA lead. Once cloned, they surface as slash commands: an office-hour skill, a "plan CEO review" that rethinks a request to find "the 10-star product hiding inside it," plus design review, development, debugging, and testing commands. Her demo prompt — a landing page for a fictional AI startup — produces a site with an interactive 3D header in a few minutes, work she frames as previously costing thousands of dollars and months of designer/developer time.

All three install the same way: download the Claude desktop app (the skills don't work in the web version), paste a clone command pointing the GitHub repo into the local Claude folder, approve the permission prompts, and confirm the skill appears when typing `/`. The closing pitch: these repos move you from typing prompts like everyone else to differentiated, agentic output. Worth noting the video is light on exact repo names/URLs (they live in her description links), and claims like the Garry Tan attribution and an "upcoming Claude IPO" example are the creator's framing, not verified facts.
