# Arbeitsregeln für dieses Projekt

## Scope

- Den Research-Workflow aus `.agents/skills/social-media-research/SKILL.md` verwenden, wenn der Nutzer Trends, Themen, Hooks, Digests oder Adaptionen anfordert.
- Nicht in generisches Social-Media-Copywriting, Veröffentlichung, Outreach oder Account-Management abdriften.
- Beide eigenen Accounts als ein gemeinsames Content-Universum behandeln. Unterschiede im Produktionsaufwand nur bei der Adaption berücksichtigen.

## Research-Qualität    

- Nur öffentliche und direkt verlinkbare Quellen verwenden.
- Beobachtete Fakten, Interpretation und eigene Content-Idee sichtbar trennen.
- Veröffentlichungsdatum, Performancewerte und Transkripte nur als verifiziert ausgeben, wenn sie tatsächlich überprüfbar sind; sonst `unknown` oder niedrige Confidence verwenden.
- Keine wortwörtliche Übernahme von Hooks, Captions oder Skriptpassagen.
- Reports begrenzen: standardmäßig maximal 50 Kandidaten prüfen und maximal 10 Fundstücke ausgeben.
- Keine Veröffentlichung, keine Nachrichten und keine Änderungen an Social-Media-Accounts durchführen.

## Repository-Hygiene

- Keine Secrets, API-Keys, großen Videodateien oder Rohdaten committen.
- Reports gehören nach `research/runs/` und sollen kompakt sowie reproduzierbar sein.
- Reports werden standardmäßig als Typst-Quelle (`.typ`) erstellt und mit Typst zu einem PDF kompiliert; die Quelle bleibt nachvollziehbar erhalten.
- Vor Änderungen an der Skill-Datei die lokale Skill-Creator-Anleitung berücksichtigen; danach den Skill-Validator ausführen.
