---
name: social-media-research
description: Research current public social-media trends, topics, hooks, short-form formats, and independent adaptations for Ferdi's own content accounts. Use for the commands trends, topic, hooks, digest, or adapt; do not use for generic copywriting, publishing, or account actions.
metadata:
  short-description: Research public short-form content signals for Ferdi's accounts
---

# Social-Media-Research-Scout

Use this skill as a bounded research workflow for Ferdi's own content universe. The two TikTok accounts are different production modes, not separate topic niches:

- `@ideas_by_ferdi`: camera-led execution with more planning and post-production.
- `@ferdifun7`: spontaneous talking-head execution with lower production effort.

Read `config/research_profile.yaml` before a research run. The profile is the source of truth for topics, languages, platforms, limits, signals, and the explicit setting that own-video comparison is disabled for now.

## Command routing

Interpret requests after an optional `research` prefix:

- `trends`: scan the configured platforms, named events, and topic space, then return a compact idea menu rather than a feed of explained videos.
- `topic <topic or combination>`: focus the scan on the requested topic, using a configured combination when one matches.
- `hooks für: <idea>`: find useful hook mechanisms and turn them into original, information-led angles; do not copy source wording.
- `digest [zeitraum]`: summarize the strongest recent signals as selectable ideas, defaulting to the configured 14-day lookback.
- `adapt item: <ID>`: turn one idea into an independent concept, optionally giving both production modes.

If a request is ambiguous between `topic` and `hooks`, choose `hooks` when the user supplies a concrete video premise and `topic` when they supply a subject area. Ask only when the distinction would materially change the research.

## Research workflow

1. Define the query, time window, language priority, relevant topic combinations, and event lookahead. Default to DACH/German, use English only as secondary format inspiration, and use the configured 14-day lookback.
2. Search in this order: named/current events and races, German public video sources, direct creator/platform pages, then broader format references. Prefer direct links over listicles or search-result pages. Do not use private, login-gated, or unverifiable material as confirmed evidence.
3. Keep up to `max_candidates` candidates, but produce `min_idea_items` to `max_idea_items` compact idea options. Deduplicate repeated posts and near-identical formats. Do not spend report space explaining individual videos.
4. Separate observed source facts, interpretation, and the original content angle while researching. Mark unavailable dates, metrics, transcripts, or performance comparisons as `unknown`; lower confidence when evidence is incomplete.
5. Convert signals into information-led ideas. Prioritize current events, explainers, rankings, comparisons, experiments, myths/contrarian questions, practical student applications, and combinations with Ferdi's interests. Search broadly across races, championships, livestream events, community formats, and relevant sports news; never let one discovered event dominate the report just because it is a vivid example.
6. Keep the exact creative execution open. Give only a compact production prompt for each account: shot/visual prompts for `@ideas_by_ferdi`, and spontaneous talking-head prompts for `@ferdifun7`. Do not write full scripts, finished captions, or copied source hooks.

Do not claim to have watched a video stream directly. If genuine video analysis is needed, work from verifiable metadata, a transcript, and selected frames when available. Otherwise describe only what can be supported by the public page and clearly label uncertainty.

## Report format

Write the report in German as a minimal, clean Typst document and compile it to PDF by default. Read `config/research_profile.yaml` for the output settings and use `research/templates/idea-dump-report.typ` as the visual and structural template. Save the completed `.typ` source and the compiled `.pdf` under `research/runs/` with matching date-based filenames. Target 2–3 pages. The PDF is the primary user-facing result; keep the `.typ` source for traceability and later edits. Replace all placeholders; do not leave template instructions in the finished report.

The report has exactly three compact sections:

1. `Top 30–40 Hooks / Themenideen`: one-line options with an original angle, the information/value promise, and the useful topic combination. Mix current events, explainers, rankings, comparisons, experiments, and student-relevant applications. This is a menu to choose from, not a list of video reviews.
2. `Produktion minimal`: keep the accounts separate. For `@ideas_by_ferdi`, provide short shot/visual prompts for selected idea clusters; for `@ferdifun7`, provide short spontaneous talking-head prompts. Mention the account mapping exactly as defined above. Leave detailed creative execution to Ferdi.
3. `Quellen-Dump`: list the especially decisive public German/Deutschsprachige videos, event pages, and direct source links used for orientation, preferably from the last 14 days. Give only date/source/platform/link and an occasional `unknown`/confidence note; do not explain each source individually.

Return a short summary in the chat as well, including a link to the generated PDF and, when useful, the Typst source. State the time window, idea count, page count, and the strongest event/topic signals. If the user explicitly asks for chat-only output or another format, follow that request instead.

Each idea line should stay compact and use this internal shape:

```text
01. Originaler Hook-/Themenwinkel — Mehrwert/Info — Kombination
```

Source facts may be used to support the menu, but the final report must not become an item-by-item analysis.

For `adapt`, keep the answer focused on the selected idea and provide, where useful:

```text
Kernbeobachtung
Eigene Idee
Talking-Head-Variante
Kamera-/Postproduktions-Variante
Warum die Adaption eigenständig ist
```

Do not turn the result into an endless feed. End with a short synthesis of repeated patterns and open uncertainties. Never publish, send messages, alter accounts, or create background jobs as part of this skill.
