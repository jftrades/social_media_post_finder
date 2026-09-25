---
name: short-form-video-editing
description: 'Bei Short-Form bitte editiere oder Video schneiden: dreistufiger Pflicht-Intake und lokaler Schnitt; routet Single Shot, Multi Shot und Voiceover.'
---

# Short Form Video Editing

Trigger `bitte editiere` (auch „Video schneiden“): strikt Level 1 → Antwort abwarten → Level 2 → Antwort abwarten → Level 3 → Antwort abwarten. Nur Fragen des aktuellen Levels stellen. Unvollständige Antworten innerhalb dieses Levels klären; kein Transkribieren, Planen oder Rendern vor Abschluss aller drei Levels. Keine Zustimmung aus Defaults ableiten. Explizite Vorab-Angaben merken und im jeweiligen Level bestätigen lassen; keine Levels überspringen. Eine Diskussion über den Trigger oder Skill-Änderung startet keinen Videoauftrag.

## Level 1 – Material

Welches Basis-Format liegt vor?

1. Talking Head (Single Shot)
2. Talking Head (Multi Shot)
3. Voiceover

## Level 2 – Projektstandard

Nur den zum Format passenden Block fragen.

**Talking Head (Single/Multi):**

1. Schnitt: Pausen, Versprecher und verworfene Anläufe entfernen und jeweils den letzten vollständigen Take behalten? Ja / Nein / nur benannte Stellen?
2. Aufnahme pro Clip: Handy ohne LUT / Kamera mit CINELIKE→Rec.709 75 % plus MERRY MEN II 30 % / bereits farbkorrigiert ohne LUT?
3. Sprache: jeden Originalclip klangneutral per konstantem Gain auf bis zu −16 LUFS und höchstens −2 dBTP angleichen? Ja / Nein? Keine Kompression, Entrauschung oder EQ; Sicherheits-Limiter bleibt aktiv.
4. Titel: keiner / exakter Text + Standarddauer 4 Sekunden oder abweichende Dauer + Snapchat / Max-Readable / Preset 1 / Preset 2 / Preset 3? Bei Preset 1–3 zusätzlich getrennt fragen: Was steht oben, in der Mitte und unten? `nix`, `leer`, `kein Text` oder eine leere Antwort lässt nur diese Zeile weg.
5. Untertitel: Standard (Alte Haas Grotesk Bold, weiß, weicher Schatten, y=1200) / keine / genaue Abweichung?
6. Musik: Standard (Phrygian Drift ab 0:30, −20 dB) / keine / anderer Song mit Startzeit und Lautstärke?
7. Pointe-Zooms: Whoosh und weich 100→120 %, am nächsten Cut zurück auf 100 %? Ja / Nein?

**Voiceover:**

1. Originalton-Einschübe: Gibt es Bildclips, deren gesprochener Originalton das Voiceover unterbrechen und vollständig hörbar bleiben soll? Nein / ja – welche Clips und welcher Satz oder Take? Das übrige Voiceover wird standardmäßig von Pausen und verworfenen Anläufen bereinigt.
2. Aufnahme pro Bildclip: Handy ohne LUT / Kamera mit CINELIKE→Rec.709 75 % plus MERRY MEN II 30 % / bereits farbkorrigiert ohne LUT?
3. Sprache: Voiceover und jeden Originalton-Einschub klangneutral per konstantem Gain auf bis zu −16 LUFS und höchstens −2 dBTP angleichen? Ja / Nein? Keine Kompression, Entrauschung oder EQ; Sicherheits-Limiter bleibt aktiv.
4. Titel: keiner / exakter Text + Standarddauer 4 Sekunden oder abweichende Dauer + Snapchat / Max-Readable / Preset 1 / Preset 2 / Preset 3? Bei Preset 1–3 zusätzlich getrennt fragen: Was steht oben, in der Mitte und unten? `nix`, `leer`, `kein Text` oder eine leere Antwort lässt nur diese Zeile weg.
5. Untertitel: Standard (Alte Haas Grotesk Bold, weiß, weicher Schatten, y=1200) / keine / genaue Abweichung?
6. Musik: Standard (Warm Relaxed Groove ab 0:00, −20 dB) / keine / anderer Song mit Startzeit und Lautstärke?
7. Bild-Zooms auf Pointen: Whoosh und weich 100→120 %, beim nächsten Bildschnitt zurück auf 100 %? Ja / Nein?

## Level 3 – Nur gewähltes Format

**Single Shot:**

- Welches ist das eine Hauptvideo (Dateiname)?
- B-Roll: Welche Ordner/Dateien sind erlaubt? Keine / bestimmte Stellen – welche / automatisch bei passenden Aussagen?

**Multi Shot:**

- Welche Sprechclips, in welcher Reihenfolge?
- Abweichungen von den eben festgelegten Standards pro Segment (Untertitel, Effekte etc.)? Keine / Clip oder Zeitbereich + konkrete Änderung?
- B-Roll: Welche Ordner/Dateien sind pro Clip erlaubt? Keine / bestimmte Stellen – welche / automatisch bei passenden Aussagen?

**Voiceover:**

- Wie heißt die eine Voiceover-Datei, und in welchem Ordner liegen die dazu aufgenommenen Bildclips?
- FlashShutterIntro: Nein / Ja? Bei Ja genau sieben unterschiedliche Tagesclips chronologisch aus dem bestätigten Projektordner auswählen. Der Renderer nimmt je etwa 0,28 Sekunden aus der Clipmitte; der Shutter startet 0,2 Sekunden vor jedem Cut bei −6 dB und läuft vollständig aus.
- Originalton-Einschübe aus Level 2: Für jeden bestätigten Clip letzten vollständigen Take bzw. Start-/Endsatz nennen; Voiceover an dieser Stelle pausieren und danach fortsetzen.
- Zusätzliche Bibliotheks-B-Roll: keine / bestimmte Aussagen / wenn passende Tagesclips nicht reichen / beides? Welche Ordner sind erlaubt?
- Bildreihenfolge: chronologisch nach Aufnahmezeit / eigene Reihenfolge? Bilder bleiben jeweils bei der erzaehlten Sache; konkrete Pflichtclips oder Stellen nennen.
- Retiming: keine Beschleunigung / welche Clips ausdrücklich beschleunigen? Bestätigte Beschleunigung bedeutet standardmäßig exakt 5× für die vollständige bestätigte Clipstrecke; keine anderen Faktoren ableiten.

Voiceover-Systemregel: genau eine Sprachdatei plus viele Bildclips; `visual_cut_policy: story_matched`. Aussage-Bild-Match hat Vorrang vor Clip-Vollstaendigkeit und schnellen Cuts. Das passende Motiv ueber die ganze Aussage halten, gerne mit mehreren unterschiedlichen Ausschnitten derselben Datei; Dauer und Anzahl sind flexibel. Chronologie bleibt Grundordnung und Intake-Frage. Details und Bildpruefung verbindlich in `../ideas-by-ferdi-voiceover/SKILL.md`; keine Pflicht, unpassende Clips einzubauen. Explizite Beschleunigung bleibt 5×, Originalton-Einschuebe zusammenhaengend. FlashShutter ersetzt bei Ja nur die ersten Bilder als Teaser; Voiceover und Musik starten bei 0:00. Titel und Untertitel bleiben unabhaengig.

Nur bei Talking Head mit Titel zusätzlich hier: Titel hinter der Person (Auto-Cutout)? Ja / Nein? Bei Voiceover niemals abfragen oder aktivieren. Projektname aus gewählter Quelle ableiten, nur bei Mehrdeutigkeit nachfragen.

Danach genau einen Ablauf verwenden:
- Ein Sprechvideo: gemeinsame Anleitung `references/workflow.md` lesen und ausführen.
- Mehrere Sprechclips: `../ideas-by-ferdi-multi-video/SKILL.md` lesen.
- Voice-over + B-Roll: `../ideas-by-ferdi-voiceover/SKILL.md` lesen.

Die Level-2-Antworten bilden die Baseline; Level-3-Abweichungen gelten ausschließlich für benannte Clips/Zeitbereiche. Zooms und Titel-Cutout nur nach ausdrücklichem Ja. Kein Hintergrundtausch, erfundener Titel oder ungefragtes Retiming. Details und technische Grenzen im gemeinsamen Workflow; keine eigene Skill-Variante pro Font.
