# Arbeitsregeln für dieses Projekt

## Scope

- Bei einem Short-Form-Auftrag mit `bitte editiere` oder „Video schneiden“ zuerst `skills/short-form-video-editing/ideas-by-ferdi-video-editor/SKILL.md` verwenden: strikt Level 1 Format → User-Antwort → Level 2 formatspezifischer Projektstandard → User-Antwort → Level 3 konkrete Dateien/Ausnahmen → User-Antwort. Keine Transkription oder Bearbeitung vor Abschluss aller Levels. Voiceover hat genau eine Sprachdatei plus viele Bildclips; keine Auto-Cutout-Abfrage. Alle drei Short-Form-Video-Skills teilen sich das lokale Tooling.
- Für YouTube- oder andere Long-Form-Schnittaufträge `skills/long-form-video-editing/SKILL.md` verwenden. Short-Form-Renderer, Hochkant-Defaults und Short-Form-Projektordner nicht automatisch übernehmen.

- Für aktuelle öffentliche Short-Form-Fitness-Trends, Formate, Challenges und nachweislich verwendete virale Hooks den Workflow aus `skills/short-form-social-media-research/SKILL.md` verwenden.
- Für Short-Form-Hooks, Skripte, Story-Arcs und Drehstrukturen den Workflow aus `skills/short-form-ideas-by-ferdi-storytelling/SKILL.md` verwenden.
- Der Standardscope umfasst Europa, die USA und Kanada. Andere Regionen nur nach ausdrücklicher Nutzeranfrage einbeziehen.
- Research bleibt externe Evidenz für Ideas by Ferdi. Storytelling, eigene Ideen, Skripte, Editing, Produktionsplanung, Lieblingscreator-Analysen und die Auswertung eigener Posts gehören in getrennte Skills.
- Vor einem Research-Lauf die kurze Intake-Frage des Skills abwarten.

## Research-Qualität

- Nur öffentliche und direkt verlinkbare Quellen verwenden.
- Beobachtete Fakten und Interpretation sichtbar trennen.
- Veröffentlichungsdatum, Dauer, Performancewerte und Transkripte nur als verifiziert ausgeben, wenn sie tatsächlich überprüfbar sind; sonst unknown oder niedrigere Confidence verwenden.
- Keine einzelnen Posts ohne Wiederholung als Trend darstellen.
- Keine Veröffentlichung, keine Nachrichten und keine Änderungen an Social-Media-Accounts durchführen.

## Repository-Hygiene

- Keine Secrets, API-Keys, großen Videodateien oder Rohdaten committen.
- Generierte Reports gehören nach `output/research/` und werden nicht committed; jeder Befund verlinkt seine Quelle direkt.
- Typst-Quellen bleiben nachvollziehbar erhalten; PDFs sind Build-Artefakte.
- Vor Änderungen an einer Skill-Datei die lokale Skill-Creator-Anleitung berücksichtigen und danach den Skill-Validator ausführen.
