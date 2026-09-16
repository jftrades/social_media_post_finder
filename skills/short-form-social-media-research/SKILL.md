---
name: short-form-social-media-research
description: Research current public fitness trends, repeatable short-form video formats or challenges, and hooks used by verified viral 30-second-plus videos from Europe, the United States, and Canada. Use for English and German short-form research for Ideas by Ferdi; do not use for storytelling, scripts, content ideas, editing, production planning, favorite-creator analysis, or evaluation of Ferdi's own posts.
metadata:
  short-description: Research viral fitness signals
---

# Short Form Social Media Research

Collect and compare current public evidence for Ideas by Ferdi. Return research findings only. Do not turn findings into original content ideas, scripts, rewritten hooks, shot lists, editing advice, or assessments of Ferdi's own videos.

## Intake gate

Before browsing, ask one compact message containing at most two questions and wait for the answer:

1. Should this be an open fitness scan, or is there a topic, claim, format, or public video to investigate more deeply?
2. Is there a preferred focus or time window, such as gym, running, hybrid athlete, nutrition, a specific sport, or completely open? Default to the last 7 days.

If the request already answers one question, ask only the missing question. Do not begin research before this intake is resolved.

## Research modes

- full scan: 15 trends, 15 formats or challenges, and 15 viral hooks.
- trends [topic]: 15 emerging topics or behaviors.
- formats [topic]: 15 repeatable formats or fitness challenges.
- hooks [topic]: 15 hooks actually used by high-confidence viral videos.
- investigate <public URL or claim>: focused evidence review; do not force the three category counts.

Use full scan when the user asks generally for new fitness research. Follow an explicitly requested narrower mode.

## Workflow

1. Read [config/research_profile.yaml](config/research_profile.yaml).
2. Read [references/research-method.md](references/research-method.md) before collecting candidates.
3. Search public English and German sources from Europe, the United States, and Canada. Treat other regions as out of scope unless the user explicitly requests them. Do not start from a fixed creator list and do not privilege DACH unless the user requests it.
4. Consider only videos with a verified or reasonably supported duration of at least 30 seconds. Inspect enough candidates to meet the requested category counts within the configured retrieval budget.
5. Verify every included item against a direct public post or video URL. Record the metric snapshot and retrieval date. Never infer missing metrics or transcripts.
6. Separate observed facts from interpretation. Use unknown and lower confidence when evidence is incomplete.
7. Rank by outlier evidence, recency, cross-creator recurrence, data completeness, and topical relevance. Do not pad weak items to reach a quota; report a shortfall and explain the access limitation.
8. For a full or category report, read [references/report-contract.md](references/report-contract.md), create the Typst source with [assets/global-fitness-research.typ](assets/global-fitness-research.typ), compile it to PDF, and save both files under `output/research/`. Return a compact chat summary with links to both files.

## Boundaries

- Analyze a source hook only when its first spoken or on-screen line is verifiable from a transcript or frames. Otherwise describe the mechanism and mark the wording unknown.
- A viral claim requires explicit evidence under the research method. Large raw view counts alone are not sufficient when creator size or post age is unknown.
- Do not present one post as a trend. Require recurrence or label it as a single outlier.
- Keep direct sources beside every finding. Do not create a detached source dump.
- Do not compare against Ferdi's posts, use favorite creators as a fixed seed, or force university and student-life angles into the research.
- Never publish, message creators, alter accounts, download private material, or create background jobs.
