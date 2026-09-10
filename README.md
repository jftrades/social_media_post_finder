# Ideas by Ferdi Skills

Lokales Skill-Repository für Research, Storytelling und künftig automatisiertes Video-Editing rund um Ideas by Ferdi.

## Skills

| Skill | Aufgabe |
|---|---|
| [`ideas-by-ferdi-storytelling`](skills/ideas-by-ferdi-storytelling/SKILL.md) | Entwickelt aus echten Notizen genau zwei ehrliche deutsche Storytelling-Varianten inklusive Hook, Script und realistischer Drehstruktur. |
| [`social-media-research`](skills/social-media-research/SKILL.md) | Untersucht aktuelle öffentliche Fitness-Trends, wiederkehrende Formate und belegbare virale Hooks aus Europa, den USA und Kanada. |
| [Video-Editor](skills/video_editing/ideas-by-ferdi-video-editor/SKILL.md) | „Video schneiden“: Pflicht-Intake, Routing und einzelnes Sprechvideo. |
| [Multi-Video](skills/video_editing/ideas-by-ferdi-multi-video/SKILL.md) | Mehrere Sprechclips. |
| [Voice-over](skills/video_editing/ideas-by-ferdi-voiceover/SKILL.md) | Vorhandenes Voice-over mit B-Roll. |

## VideoEditor-PoC

Der minimale lokale Workflow deckt drei Fälle ab:

1. Ein durchgehender Talking-Head-Shot.
2. Mehrere Kamera- oder Positionswechsel entlang eines Skripts.
3. Talking Head plus gezielt ausgewählte B-Roll aus einer großen lokalen Bibliothek.

Vor dem Editing vier Antworten abwarten: Pausen/Retakes kürzen (letzte Alternative behalten)? Clip-Art und Dateinamen/Reihenfolge? Standard-Untertitel oder Änderungen/keine? Standardmusik oder anderer Song/keine?

Defaults: Purfview Faster Whisper **Medium**, Deutsch, ohne API-Key. Alte Haas Grotesk Bold, weiß mit sanftem Schatten, kurze Caption-Blöcke, y=1280 bei 1080×1920 (ein Drittel von unten). **Phrygian_Drift_2026-09-04T124142.mp3 mit −20 dB Gain**. Stimme auf −16 LUFS mit −2 dBTP Ziel anpassen, Master-Limiter gegen Übersteuerung. Schon verzerrtes Audio wird dadurch nicht repariert.

Der Agent prüft Retakes anhand von Wortzeiten und Audio und erstellt den Schnittplan; bedeutungsvolle Wiederholungen bleiben erhalten. Whisper kann Versprecher auslassen. Subtitle-Edit-GUI-Postprocessing wird nicht direkt übernommen. Das lokale Tool baut kurze Captions aus Purfview-Wortzeiten.

Originale unter `project_videos/unfinished_projects/<projekt>/`, temporäre Dateien unter `project_videos/work/<projekt>/`. Nach Render-Prüfung werden nur verwendete Quellen hashgeprüft nach `project_videos/finished_projects/<projekt>/originals/` kopiert, zusammen mit `final.mp4` und Plan. Erst danach werden die ausgewählten Eingangsdateien aus `project_videos/unfinished_projects/` entfernt. Externe Quellen und B-Roll-Bibliotheken bleiben erhalten; bestehende fertige Projekte werden nicht überschrieben. Alle drei Projektordner sind ignoriert.

Tooling: Python 3.11+ (Standardbibliothek), lokale Purfview-Installation inklusive `_models/faster-whisper-medium` und gebündeltem FFmpeg. Nach Clone lokal bereitstellen. [Workflow und Jobvorlage](skills/video_editing/ideas-by-ferdi-video-editor/references/workflow.md) beschreiben `prepare`, `plan`, `render`, `finish`. Auto-Cutout/RVM, Zooms, LUT-Anwendung und zusätzliche Effekte folgen später.

`agent_tooling/` enthält die kleinen, gemeinsam versionierten Audio-Presets:

- `background_music/`: wenige wiederverwendbare Musikbetten.
- `sound_fx/`: kurze Effekte wie Whoosh, Pop, Click oder Shutter.
- `fonts/`: drei Schriftdateien, Standard Alte Haas Grotesk Bold.
- `LUTs/`: zwei LUTs für spätere Erweiterungen.

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
