# Research-Reports

Hier werden kompakte Research-Läufe standardmäßig als Typst-Quelldokumente (`.typ`) gespeichert und mit Typst zu PDFs kompiliert. Das PDF ist das primäre Nutzerergebnis; die `.typ`-Quelle bleibt für Nachvollziehbarkeit und spätere Anpassungen erhalten. Ein Lauf sollte den verwendeten Zeitraum, die Quellen und die Confidence-Werte nachvollziehbar machen. Im Chat erscheint zusätzlich eine kurze Zusammenfassung.

Die Vorlage liegt unter `research/templates/idea-dump-report.typ`. Sie ist bewusst minimal und clean gehalten: A4, zurückhaltende Farben, kompakte Ideenzeilen und kein langes Titelblatt. Ziel sind 2–3 Seiten. Die PDF-Datei wird als Build-Artefakt erzeugt; die Typst-Datei ist die editierbare Quelle.

## Report-Struktur

1. **Top 30–40 Hooks / Themenideen** – jeweils ein eigenständiger Winkel, der Mehrwert/Info und Themenkombination sichtbar macht.
2. **Produktion minimal** – getrennt nach `@ideas_by_ferdi` (Kamera-/Shot-Impulse) und `@ferdifun7` (spontane Talking-Head-Impulse).
3. **Quellen-Dump** – besonders ausschlaggebende, direkt verlinkte deutschsprachige Quellen, bevorzugt aus den letzten 14 Tagen.
```

Wörtliche Hooks, Captions oder Skripte gehören nicht in den Report. Quellen dienen als Orientierung für Themen, Events und Mechaniken; der Report erklärt nicht jedes einzelne Video. Die genaue kreative Umsetzung bleibt bei Ferdi.

`runs/.gitkeep` hält den vorgesehenen Speicherort im Repository sichtbar. Große Videodateien und Rohdaten bleiben außerhalb des Git-Repositories.
