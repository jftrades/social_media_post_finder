# Research-Reports

Hier werden kompakte Research-Läufe standardmäßig als Typst-Quelldokumente (`.typ`) gespeichert und mit Typst zu PDFs kompiliert. Das PDF ist das primäre Nutzerergebnis; die `.typ`-Quelle bleibt für Nachvollziehbarkeit und spätere Anpassungen erhalten. Ein Lauf sollte den verwendeten Zeitraum, die Quellen und die Confidence-Werte nachvollziehbar machen. Im Chat erscheint zusätzlich eine kurze Zusammenfassung.

Die Vorlage liegt unter `research/templates/social-media-report.typ`. Sie ist bewusst minimal und clean gehalten: A4, zurückhaltende Farben, klare Metadaten und ein kurzer Einstieg statt eines Titelblatts. Die PDF-Datei wird als Build-Artefakt erzeugt; die Typst-Datei ist die editierbare Quelle.

## Inhalt pro Fundstück

```text
id: sm-YYYYMMDD-001
platform: tiktok
public_url: https://...
published_at_if_verified: unknown
title_or_caption: "..."
topic: sport x studentenalltag
format: "..."
hook_or_hook_mechanism: "..."
first_seconds_promise: "..."
pattern_interrupt: "..."
visible_virality_signals:
  - "..."
recency: high
relevance: high
confidence: medium
observed_facts: "..."
interpretation: "..."
independent_adaptation_idea: "..."
```

Wörtliche Hooks, Captions oder Skripte gehören nicht in die Adaption. Beschrieben werden der Mechanismus und eine eigenständige Variante für Ferdis Content-Universum. Wenn sinnvoll, können für denselben Fund jeweils eine spontane Talking-Head-Variante und eine aufwendigere Kamera-/Schnittvariante vorgeschlagen werden.

`runs/.gitkeep` hält den vorgesehenen Speicherort im Repository sichtbar. Große Videodateien und Rohdaten bleiben außerhalb des Git-Repositories.
