# Social Media Post Finder

Sammelt aktuelle öffentliche Signale von TikTok, Instagram Reels und YouTube Shorts und übersetzt sie in eigenständige Ideen für Sport, Fitness, Studentenalltag, Sidequestmaxxing und Selbstoptimierung.

## Eigene Accounts

- [@ideas_by_ferdi](https://www.tiktok.com/@ideas_by_ferdi): Kamera, stärker geplantes Konzept und aufwendigere Nachbearbeitung.
- [@ferdifun7](https://www.tiktok.com/@ferdifun7): Talking Head, spontaner und mit geringerem Produktionsaufwand.

## Zweck und Grenzen

Der erste Projektstand konzentriert sich auf Research, Trends, Hooks, Formate und direkt verlinkbare Quellen. 

Die Skill-Datei unter `.agents/skills/social-media-research/SKILL.md` steuert die Befehle `trends`, `topic`, `hooks`, `digest` und `adapt`. Reports werden standardmäßig als minimal gestaltete Typst-Quelldatei erstellt und mit Typst zu einem PDF kompiliert. Das PDF ist das primäre Ergebnis im Chat; die `.typ`-Quelle bleibt unter `research/runs/` zur Nachvollziehbarkeit erhalten.

## Beispielbefehle

research trends
research Sport x Studentenalltag
research Sidequestmaxxing
research hooks für: morgens trainieren trotz Uni
research digest der letzten 7 Tage
adapt item: <ID>
