# Ideas by Ferdi Skills

Lokales Skill-Repository für Research, Storytelling und künftig automatisiertes Video-Editing rund um Ideas by Ferdi.

## Skills

| Skill | Aufgabe |
|---|---|
| [`ideas-by-ferdi-storytelling`](skills/ideas-by-ferdi-storytelling/SKILL.md) | Entwickelt aus echten Notizen genau zwei ehrliche deutsche Storytelling-Varianten inklusive Hook, Script und realistischer Drehstruktur. |
| [`social-media-research`](skills/social-media-research/SKILL.md) | Untersucht aktuelle öffentliche Fitness-Trends, wiederkehrende Formate und belegbare virale Hooks aus Europa, den USA und Kanada. |
| [Video-Editor](skills/video_editing/ideas-by-ferdi-video-editor/SKILL.md) | „bitte editiere“: dreistufiger Intake, Routing und einzelnes Sprechvideo. |
| [Multi-Video](skills/video_editing/ideas-by-ferdi-multi-video/SKILL.md) | Mehrere Sprechclips. |
| [Voice-over](skills/video_editing/ideas-by-ferdi-voiceover/SKILL.md) | Vorhandenes Voice-over mit B-Roll. |

## VideoEditor-PoC

Der minimale lokale Workflow deckt drei Fälle ab:

1. Ein durchgehender Talking-Head-Shot.
2. Mehrere Kamera- oder Positionswechsel entlang eines Skripts.
3. Talking Head plus gezielt ausgewählte B-Roll aus einer großen lokalen Bibliothek.

Trigger `bitte editiere` (auch „Video schneiden“): **Level 1 Format → Antwort abwarten → Level 2 formatspezifischer Projektstandard → Antwort abwarten → Level 3 konkrete Dateien und Ausnahmen → Antwort abwarten.** Erst danach bearbeiten. Die exakten Auswahlfragen stehen zentral im [Video-Editor-Skill](skills/video_editing/ideas-by-ferdi-video-editor/SKILL.md). Voiceover bedeutet immer genau eine Sprachdatei plus viele Bildclips; Level 2 fragt dort statt der Talking-Head-Schnittbereinigung nach Originalton-Unterbrechungen. Auto-Cutout wird bei Voiceover nie abgefragt.

Defaults: Purfview Faster Whisper **Medium**, Deutsch, ohne API-Key. Alte Haas Grotesk Bold, weiß mit dezentem, weichgezeichnetem Schatten; fett und Buchstabenabstand −1, kurze Caption-Blöcke, y=1200 bei 1080×1920. Talking Head: **Phrygian Drift ab 0:30 mit −20 dB**. Voiceover: **Warm Relaxed Groove ab 0:00 mit −20 dB**. Bei bestätigter Audio-Normalisierung Sprache auf −16 LUFS mit −2 dBTP Ziel anpassen; Voiceover und Originalton-Einschübe vor dem Verbinden separat angleichen. Master-Limiter schützt gegen Übersteuerung.

Voiceover-Bildregel: Jeder verwendete Originalclip über 5 Sekunden wird als mehrere unterschiedliche 1-Sekunden-Schnipsel geschnitten. Zusätzliche B-Roll aus der Bibliothek ist nur erlaubt, wenn sie ausdrücklich angefordert wurde oder die Projektclips nachweislich nicht für die Voiceover-Länge reichen – entsprechend der beantworteten Fallback-Frage.

Der Agent prüft Retakes anhand von Wortzeiten und Audio und erstellt den Schnittplan; bedeutungsvolle Wiederholungen bleiben erhalten. Whisper kann Versprecher auslassen. Subtitle-Edit-GUI-Postprocessing wird nicht direkt übernommen. Das lokale Tool baut kurze Captions aus Purfview-Wortzeiten.

Originale unter `project_videos/unfinished_projects/<projekt>/`, temporäre Dateien unter `project_videos/work/<projekt>/`. Nach Render-Prüfung werden nur verwendete Quellen hashgeprüft nach `project_videos/finished_projects/<projekt>/originals/` kopiert, zusammen mit `final.mp4` und Plan. Erst danach werden die ausgewählten Eingangsdateien aus `project_videos/unfinished_projects/` entfernt. Externe Quellen und B-Roll-Bibliotheken bleiben erhalten; bestehende fertige Projekte werden nicht überschrieben. Alle drei Projektordner sind ignoriert.

Tooling: uv mit Python 3.11+ und Pillow (automatisch über Script-Metadaten installiert), lokale Purfview-Installation inklusive `_models/faster-whisper-medium` und gebündeltem FFmpeg. Nach Clone lokal bereitstellen. [Workflow und Jobvorlage](skills/video_editing/ideas-by-ferdi-video-editor/references/workflow.md) beschreiben `prepare`, `plan`, `render`, `finish`. Optionaler Titel-Cutout mit lokalem RVM ist für die beiden Talking-Head-Formate verfügbar: Level 3 „Titel hinter der Person? Ja / Nein?“. Bei Ja liegt die freigestellte Person über dem Titel, Untertitel ganz vorne. Modell und Masken bleiben lokal. Siehe [Cutout-Setup und Grenzen](skills/video_editing/ideas-by-ferdi-video-editor/references/cutout.md). Handy bleibt ohne LUT; Kamera erhält zuerst CINELIKE D to REC 709_26.P1003055 mit 75 %, danach MERRY_MEN_II mit 30 %.

Effektfrage in Level 2 für alle Formate: **Pointe-Zooms mit Whoosh – Ja / Nein?** Nur bei Ja gezielte kurze Atempausen erhalten, weich 100→120 % zoomen und spätestens beim nächsten Cut/Angle-Wechsel zurück auf 100 %. Passende Rückzooms im Sprechfluss sind möglich. Whoosh: `whoosh-swift-cut-jam-fx-1-00-00.mp3`, −6 dB, zwei Halbtöne tiefer. Bei Voiceover erfolgt der Reset spätestens beim Bildwechsel; Nein aktiviert keinerlei Zoom-Effekte.

`agent_tooling/` enthält die kleinen, gemeinsam versionierten Audio-Presets:

- `background_music/`: wenige wiederverwendbare Musikbetten.
- `sound_fx/`: kurze Effekte wie Whoosh, Pop, Click oder Shutter.
- `fonts/`: Schriftdateien, Untertitel-Standard Alte Haas Grotesk Bold, Titel-Standard Alte Haas Grotesk Bold.
- `LUTs/`: zwei LUTs für den Kamera-Standard.

Folgende Inhalte bleiben bewusst lokal und werden nicht in Git aufgenommen:

- `agent_tooling/B_Roll/`: die persönliche, große B-Roll-Bibliothek.
- `agent_tooling/Purfview-Faster-Whisper-XXL/`: Purfview-Laufzeit und Whisper-Modelle. Die Laufzeit ist mehrere Gigabyte groß und enthält Dateien oberhalb des normalen GitHub-Limits.

Der spätere Skill muss diese lokalen Ordner automatisch finden oder über eine lokale, nicht eingecheckte Konfiguration erhalten. Musik und Soundeffekte werden dagegen ausdrücklich mit dem Repository versioniert. Vor einer öffentlichen Weitergabe des Repositories müssen die Nutzungsrechte und nötigen Credits dieser Audiodateien dokumentiert sein.

## Struktur

```text
agent_tooling/
|-- B_Roll/                         # lokal, von Git ignoriert
|-- Purfview-Faster-Whisper-XXL/    # lokal, von Git ignoriert
|-- background_music/               # wird versioniert
`-- sound_fx/                       # wird versioniert
project_videos/                    # vollständig lokal, ignoriert
|-- unfinished_projects/
|-- work/
`-- finished_projects/
skills/
|-- video_editing/
|   |-- ideas-by-ferdi-video-editor/
|   |-- ideas-by-ferdi-multi-video/
|   `-- ideas-by-ferdi-voiceover/
|-- ideas-by-ferdi-storytelling/
|   |-- SKILL.md
|   |-- agents/
|   `-- references/
`-- social-media-research/
    |-- SKILL.md
    |-- agents/
    |-- assets/
    |-- config/
    `-- references/
```

Die drei Video-Skills liegen zusammen unter `skills/video_editing/`; der General-Skill übernimmt das Routing. Video-Arbeitsdateien liegen unter `project_videos/work/`, Research-Reports unter `output/`. Ein `final.mp4` in `work/` ist die gerenderte Arbeitsversion zur Prüfung. Nach `finish` liegt die geprüfte Auslieferung in `project_videos/finished_projects/`; der Arbeitscache bleibt für Korrekturen erhalten und kann später separat entfernt werden.

## Beispielaufrufe

```text
Hilf mir aus diesen Notizen eine persönliche 45-Sekunden-Story zu bauen.
Research trends running der letzten 7 Tage.
Research hooks hybrid athlete.
```

Titel in Level 2 für alle Formate: genauer Wortlaut, Standarddauer 4 Sekunden oder abweichende Dauer und Snapchat / Max-Readable / Preset 1 / Preset 2 / Preset 3. Snapchat und Max-Readable bleiben unverändert. Preset 1–3 haben drei feste Slots `oben`, `mitte`, `unten`; nur deren Text wird abgefragt. `nix`, `leer`, `kein Text` oder leer blendet den jeweiligen Slot aus. Größe, Position, Font und Schatten sind pro Preset fest. Preset 1 lässt die Zeilen nacheinander 40 px von unten einsteigen; Preset 2 animiert oben von links und Mitte von oben gleichzeitig, danach die untere Sternzeile. Beide nutzen 1,0 Sekunde kubisches Ease-out plus Alpha-Fade; Preset 3 bleibt statisch. Musikstart ist formatspezifisch: Talking Head 0:30, Voiceover 0:00.
