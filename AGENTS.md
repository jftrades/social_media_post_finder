# Arbeitsregeln für dieses Projekt

## Scope

- Bei „Video schneiden“ zuerst `skills/video_editing/ideas-by-ferdi-video-editor/SKILL.md` verwenden. Vor Transkription oder Schnitt die sieben Pflichtfragen beantworten lassen. General-, Multi-Video- und Voice-over-Skill teilen sich dessen lokales Tooling.

- Für aktuelle öffentliche Fitness-Trends, Formate, Challenges und nachweislich verwendete virale Hooks den Workflow aus `skills/social-media-research/SKILL.md` verwenden.
- Für Hooks, Skripte, Story-Arcs und Drehstrukturen den Workflow aus `skills/ideas-by-ferdi-storytelling/SKILL.md` verwenden.
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
