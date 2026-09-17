# Ideas by Ferdi Short- und Long-Form-Skills

Lokales Skill-Repository für Research, Storytelling und künftig automatisiertes Video-Editing rund um Ideas by Ferdi.

## Skills

| Skill | Aufgabe |
|---|---|
| [`short-form-ideas-by-ferdi-storytelling`](skills/short-form-ideas-by-ferdi-storytelling/SKILL.md) | Entwickelt aus echten Notizen ehrliche deutsche Short-Form-Storys inklusive Hook, Script und realistischer Drehstruktur. |
| [`short-form-social-media-research`](skills/short-form-social-media-research/SKILL.md) | Untersucht aktuelle öffentliche Short-Form-Fitness-Trends, wiederkehrende Formate und belegbare virale Hooks aus Europa, den USA und Kanada. |
| [Short Form Video Editing](skills/short-form-video-editing/ideas-by-ferdi-video-editor/SKILL.md) | „bitte editiere“: dreistufiger Intake, Routing und einzelnes Sprechvideo. |
| [Short Form Multi-Video](skills/short-form-video-editing/ideas-by-ferdi-multi-video/SKILL.md) | Mehrere Sprechclips. |
| [Short Form Voice-over](skills/short-form-video-editing/ideas-by-ferdi-voiceover/SKILL.md) | Vorhandenes Voice-over mit B-Roll. |
| [Long Form Video Editing](skills/long-form-video-editing/SKILL.md) | Startpunkt für Planung, Schnitt und QA längerer YouTube-Videos. |

## Long-Form-VideoEditor

Der Long-Form-Skill nutzt eine hybride lokale Pipeline: FFmpeg übernimmt Story-Cut, Audio-Kontinuität und die bestätigte LUT-Kette; Remotion rendert gezielte Zooms, Texte, Grafiken, SFX, mehrere Musikabschnitte und das Thumbnail. Ein Auftrag erzeugt `01_cut.mp4`, `02_animated.mp4`, `03_final.mp4` und `thumbnail.jpg`. Alle drei Videos teilen denselben Story-Cut; die späteren Versionen ergänzen nur Ebenen.

Vor dem Schnitt läuft ein dreistufiger Intake: Video/Versprechen, Look/Audio und konkrete Dateirollen/Ausnahmen. Anschließend arbeitet der Skill ohne Zwischenfreigaben bis zu allen drei Fassungen. Die analysierten Referenzen liegen in `project_videos/long_form_reference/STYLE_INDEX.md`; pro Referenz gibt es einen exakt benannten `Folder-…/Assets-…/`-Pack mit Timeline, Transkript, Bildern und übertragbaren Regeln.

Kamera-Material erhält bei Bestätigung zuerst `CINELIKE D to REC 709` mit 80 %, danach `MERRY_MEN II` mit 30 %. Alte Haas Grotesk Bold mit weichgezeichnetem Schatten ist der Standard, Child Hood markiert Notizen, Race Day setzt einzelne ein- bis zweiwortige Impact-Titel. Musik wird entlang der Spannungsanalyse gewechselt und unter Dialog abgesenkt.

## Short-Form-VideoEditor-PoC

Der minimale lokale Workflow deckt drei Fälle ab:

1. Ein durchgehender Talking-Head-Shot.
2. Mehrere Kamera- oder Positionswechsel entlang eines Skripts.
3. Talking Head plus gezielt ausgewählte B-Roll aus einer großen lokalen Bibliothek.

Trigger `bitte editiere` (auch „Video schneiden“): **Level 1 Format → Antwort abwarten → Level 2 formatspezifischer Projektstandard → Antwort abwarten → Level 3 konkrete Dateien und Ausnahmen → Antwort abwarten.** Erst danach bearbeiten. Die exakten Auswahlfragen stehen zentral im [Short-Form-Video-Editor-Skill](skills/short-form-video-editing/ideas-by-ferdi-video-editor/SKILL.md). Voiceover bedeutet immer genau eine Sprachdatei plus viele Bildclips; Level 2 fragt dort statt der Talking-Head-Schnittbereinigung nach Originalton-Unterbrechungen. Auto-Cutout wird bei Voiceover nie abgefragt.

Defaults: Purfview Faster Whisper **Medium**, Deutsch, ohne API-Key. Alte Haas Grotesk Bold, weiß mit dezentem, weichgezeichnetem Schatten; fett und Buchstabenabstand −1, kurze Caption-Blöcke, y=1200 bei 1080×1920. Talking Head: **Phrygian Drift ab 0:30 mit −20 dB**. Voiceover: **Warm Relaxed Groove ab 0:00 mit −20 dB**. Für Sprache wird WAV/PCM mit 48 kHz bevorzugt. Bei bestätigter Audio-Normalisierung erfolgt nur eine schnelle Messung plus konstanter Gain bis maximal −16 LUFS/−2 dBTP – ohne Kompression, Entrauschung, Gate oder EQ. Zwischenstufen bleiben 24-Bit-PCM; erst der finale MP4-Export kodiert einmalig als AAC mit 256 kbit/s. Master-Limiter schützt nur gegen Übersteuerung.

Voiceover-Bildregel: Jeder verwendete Originalclip über 5 Sekunden wird als mehrere unterschiedliche 1-Sekunden-Schnipsel geschnitten. Zusätzliche B-Roll aus der Bibliothek ist nur erlaubt, wenn sie ausdrücklich angefordert wurde oder die Projektclips nachweislich nicht für die Voiceover-Länge reichen – entsprechend der beantworteten Fallback-Frage.

Der Agent prüft Retakes anhand von Wortzeiten und Audio und erstellt den Schnittplan; bedeutungsvolle Wiederholungen bleiben erhalten. Whisper kann Versprecher auslassen. Subtitle-Edit-GUI-Postprocessing wird nicht direkt übernommen. Das lokale Tool baut kurze Captions aus Purfview-Wortzeiten.

Short-Form-Originale liegen unter `project_videos/short_form_unfinished_projects/<projekt>/`, temporäre Dateien unter `project_videos/short_form_work/<projekt>/`. Nach Render-Prüfung werden nur verwendete Quellen hashgeprüft nach `project_videos/short_form_finished_projects/<projekt>/originals/` kopiert, zusammen mit `final.mp4` und Plan. Erst danach werden die ausgewählten Eingangsdateien aus `project_videos/short_form_unfinished_projects/` entfernt. Externe Quellen und B-Roll-Bibliotheken bleiben erhalten; bestehende fertige Projekte werden nicht überschrieben. Long-Form-Projekte verwenden die parallelen `long_form_*`-Ordner.

Tooling: uv mit Python 3.11+ und Pillow (automatisch über Script-Metadaten installiert), lokale Purfview-Installation inklusive `_models/faster-whisper-medium` und gebündeltem FFmpeg. Nach Clone lokal bereitstellen. [Workflow und Jobvorlage](skills/short-form-video-editing/ideas-by-ferdi-video-editor/references/workflow.md) beschreiben `prepare`, `plan`, `render`, `finish`. Optionaler Titel-Cutout mit lokalem RVM ist für die beiden Talking-Head-Formate verfügbar: Level 3 „Titel hinter der Person? Ja / Nein?“. Bei Ja liegt die freigestellte Person über dem Titel, Untertitel ganz vorne. Modell und Masken bleiben lokal. Siehe [Cutout-Setup und Grenzen](skills/short-form-video-editing/ideas-by-ferdi-video-editor/references/cutout.md). Handy bleibt ohne LUT; Kamera erhält zuerst CINELIKE D to REC 709_26.P1003055 mit 75 %, danach MERRY_MEN_II mit 30 %.

Effektfrage in Level 2 für alle Formate: **Pointe-Zooms mit Whoosh – Ja / Nein?** Nur bei Ja gezielte kurze Atempausen erhalten, weich 100→120 % zoomen und spätestens beim nächsten Cut/Angle-Wechsel zurück auf 100 %. Passende Rückzooms im Sprechfluss sind möglich. Whoosh: `whoosh-swift-cut-jam-fx-1-00-00.mp3`, −6 dB, zwei Halbtöne tiefer. Bei Voiceover erfolgt der Reset spätestens beim Bildwechsel; Nein aktiviert keinerlei Zoom-Effekte.

`agent_tooling/` enthält die kleinen, gemeinsam versionierten Audio-Presets:

- `background_music/`: wenige wiederverwendbare Musikbetten.
- `sound_fx/`: kurze Effekte wie Whoosh, Pop, Click oder Shutter.
- `fonts/`: Schriftdateien, Untertitel-Standard Alte Haas Grotesk Bold, Titel-Standard Alte Haas Grotesk Bold.
- `LUTs/`: zwei LUTs für den Kamera-Standard.

Folgende Inhalte bleiben bewusst lokal und werden nicht in Git aufgenommen:

- `agent_tooling/short_form_b_roll/`: die persönliche Short-Form-B-Roll-Bibliothek.
- `agent_tooling/long_form_b_roll/`: die separate Long-Form-B-Roll-Bibliothek.
- `agent_tooling/Purfview-Faster-Whisper-XXL/`: Purfview-Laufzeit und Whisper-Modelle. Die Laufzeit ist mehrere Gigabyte groß und enthält Dateien oberhalb des normalen GitHub-Limits.

Der spätere Skill muss diese lokalen Ordner automatisch finden oder über eine lokale, nicht eingecheckte Konfiguration erhalten. Musik und Soundeffekte werden dagegen ausdrücklich mit dem Repository versioniert. Vor einer öffentlichen Weitergabe des Repositories müssen die Nutzungsrechte und nötigen Credits dieser Audiodateien dokumentiert sein.

## Struktur

```text
agent_tooling/
|-- short_form_b_roll/              # lokal, von Git ignoriert
|-- long_form_b_roll/               # lokal, von Git ignoriert
|-- Purfview-Faster-Whisper-XXL/    # lokal, von Git ignoriert
|-- background_music/               # wird versioniert
`-- sound_fx/                       # wird versioniert
project_videos/                    # vollständig lokal, ignoriert
|-- short_form_unfinished_projects/
|-- short_form_work/
|-- short_form_finished_projects/
|-- long_form_reference/
|-- long_form_unfinished_projects/
|-- long_form_work/
`-- long_form_finished_projects/
skills/
|-- short-form-video-editing/
|   |-- ideas-by-ferdi-video-editor/
|   |-- ideas-by-ferdi-multi-video/
|   `-- ideas-by-ferdi-voiceover/
|-- short-form-ideas-by-ferdi-storytelling/
|   |-- SKILL.md
|   |-- agents/
|   `-- references/
|-- short-form-social-media-research/
|   |-- SKILL.md
|   |-- agents/
|   |-- assets/
|   |-- config/
|   `-- references/
`-- long-form-video-editing/
    |-- SKILL.md
    `-- agents/
```

Die drei Short-Form-Video-Skills liegen zusammen unter `skills/short-form-video-editing/`; der General-Skill übernimmt das Routing. Short-Form-Arbeitsdateien liegen unter `project_videos/short_form_work/`, Long-Form-Arbeitsdateien unter `project_videos/long_form_work/`. Research-Reports liegen unter `output/`. Nach `finish` liegt eine geprüfte Short-Form-Auslieferung in `project_videos/short_form_finished_projects/`; der Arbeitscache bleibt für Korrekturen erhalten und kann später separat entfernt werden.

## Beispielaufrufe

```text
Hilf mir aus diesen Notizen eine persönliche 45-Sekunden-Story zu bauen.
Research trends running der letzten 7 Tage.
Research hooks hybrid athlete.
```

Titel in Level 2 für alle Formate: genauer Wortlaut, Standarddauer 4 Sekunden oder abweichende Dauer und Snapchat / Max-Readable / Preset 1 / Preset 2 / Preset 3. Snapchat und Max-Readable bleiben unverändert. Preset 1–3 haben drei feste Slots `oben`, `mitte`, `unten`; nur deren Text wird abgefragt. `nix`, `leer`, `kein Text` oder leer blendet den jeweiligen Slot aus. Größe, Position, Font und Schatten sind pro Preset fest. Preset 1 lässt die Zeilen nacheinander 40 px von unten einsteigen; Preset 2 animiert oben von links und Mitte von oben gleichzeitig, danach die untere Sternzeile. Beide nutzen 1,0 Sekunde kubisches Ease-out plus Alpha-Fade; Preset 3 bleibt statisch. Musikstart ist formatspezifisch: Talking Head 0:30, Voiceover 0:00.

Nur Voiceover fragt in Level 3 zusätzlich nach `FlashShutterIntro`. Bei Ja ersetzen sieben chronologisch verteilte Projektclips mit mittigen 0,28-Sekunden-Snippets die ersten etwa 1,97 Sekunden der Bildspur. Der Kauasilbershlachparodes-Shutter startet bei −6 dB jeweils 0,2 Sekunden vor jedem Cut und läuft vollständig aus. Voiceover und Musik beginnen unverändert bei 0:00; Titel und Untertitel bleiben frei wählbar und werden unabhängig darübergelegt.
