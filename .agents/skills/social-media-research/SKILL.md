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

- `trends`: scan the configured platforms and topic space for current public signals, then return a small ranked selection.
- `topic <topic or combination>`: focus the scan on the requested topic, using a configured combination when one matches.
- `hooks für: <idea>`: find relevant public hook mechanisms and formats for the idea; do not copy the wording of any source.
- `digest [zeitraum]`: summarize the strongest recent signals, defaulting to the configured 7-day lookback.
- `adapt item: <ID>`: turn one researched item into an independent concept, optionally giving both the spontaneous and higher-production execution variants.

If a request is ambiguous between `topic` and `hooks`, choose `hooks` when the user supplies a concrete video premise and `topic` when they supply a subject area. Ask only when the distinction would materially change the research.

## Research workflow

1. Define the query, time window, language priority, and relevant topic combination. Default to DACH/German, use English as a secondary inspiration source, and use the configured lookback.
2. Search public TikTok, Instagram Reels, and YouTube Shorts sources. Prefer direct post URLs and creator/platform pages over listicles or search-result pages. Do not use private, login-gated, or unverifiable material as confirmed evidence.
3. Keep up to `max_candidates` candidates during research and no more than `max_report_items` items in the final report. Deduplicate repeated posts and near-identical formats.
4. For each selected item, separate observed facts from interpretation and from the proposed adaptation. Mark unavailable dates, metrics, transcripts, or performance comparisons as `unknown`; lower confidence when evidence is incomplete.
5. Analyze the mechanism: what the first seconds promise, how attention is interrupted or maintained, what format and pacing are visible, and which measurable signals are available. Treat virality as a signal, never as a guarantee.
6. Derive an original idea for Ferdi. Preserve the underlying audience problem or format logic, but do not reproduce a hook, caption, script, shot sequence, or creator identity. Mention which production mode is a good fit only when it adds value.

Do not claim to have watched a video stream directly. If genuine video analysis is needed, work from verifiable metadata, a transcript, and selected frames when available. Otherwise describe only what can be supported by the public page and clearly label uncertainty.

## Report format

Write the report in German as a clean Typst document and compile it to PDF by default. Read `config/research_profile.yaml` for the output settings and use `research/templates/social-media-report.typ` as the visual and structural template. Save the completed `.typ` source and the compiled `.pdf` under `research/runs/` with matching date-based filenames. The PDF is the primary user-facing result; keep the `.typ` source for traceability and later edits. Replace all placeholders; do not leave template instructions in the finished report.

Return a short summary in the chat as well, including a link to the generated PDF and, when useful, the Typst source. The chat summary should state the time window, number of selected items, and the strongest repeated patterns. If the user explicitly asks for chat-only output or another format, follow that request instead.

Every research item in the Typst report should contain:

```text
ID
Plattform
Direkter öffentlicher Link
Veröffentlichungsdatum (verifiziert oder unknown)
Titel/Caption
Thema
Format
Hook-Mechanismus
Versprechen in den ersten Sekunden
Pattern Interrupt
Sichtbare Viralitätssignale
Aktualität
Relevanz für Ferdis Themen
Confidence
Beobachtete Fakten
Interpretation
Eigenständige Adaptionsidee
```

For `adapt`, keep the answer focused on the selected item and provide, where useful:

```text
Kernbeobachtung
Eigene Idee
Talking-Head-Variante
Kamera-/Postproduktions-Variante
Warum die Adaption eigenständig ist
```

Do not turn the result into an endless feed. End with a short synthesis of repeated patterns, open uncertainties, and the next useful research command. Never publish, send messages, alter accounts, or create background jobs as part of this skill.
