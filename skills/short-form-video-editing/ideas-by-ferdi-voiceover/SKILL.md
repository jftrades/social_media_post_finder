---
name: short-form-voiceover-editing
description: Schneidet vorhandenes Short-Form-Voice-over mit lokalen B-Roll-Clips, Untertiteln und Musik nach dem Video-schneiden-Intake.
---

# Short Form Voice-over mit B-Roll

Ohne die drei nacheinander beantworteten Levels aus `../ideas-by-ferdi-video-editor/SKILL.md` dorthin zurückleiten und beim ersten offenen Level warten. Alle globalen Standards inklusive Titelstil, Audio und Effekten abfragen. Auto-Cutout niemals abfragen oder aktivieren.
Gemeinsames Tooling und Vorgehen: `../ideas-by-ferdi-video-editor/references/workflow.md` lesen.
`mode: voiceover` verwendet genau eine Voiceover-Datei in `sources`; die vielen Bildclips stehen in `visuals`. Stimme transkribieren und bereinigen, keinen Text oder künstliche Stimme erfinden. Erst wenige verteilte Frames prüfen, nur interessante Stellen genauer ansehen.

Plane die Bildspur in dieser Reihenfolge:

1. Voiceover bereinigen und dessen fertige Länge bestimmen. Jeden bestätigten Tagesclip zuerst anhand Aussage, Dateiname und Prüfframes in der tatsächlichen Tagesreihenfolge einplanen. Das FlashShutterIntro ist nur ein vorgeschalteter Teaser und ersetzt nicht die spätere Verwendung eines Tagesclips.
2. Bei `keine B-Roll` zunächst die Laufzeit aller sinnvoll nutzbaren Tagesclips nach dem Intro ermitteln. Diese vollständige Tagesabfolge ist der verbindliche Mindestumfang an Quellen: keinen Tagesclip auslassen und noch keinen Clip nur deshalb verwerfen, weil die erste Aneinanderreihung länger als das Voiceover ist.
3. Jeden Originalclip über 5 Sekunden als zwei bis fünf unterschiedliche, chronologische Schnipsel von etwa 0,8 bis 1,0 Sekunden derselben Datei verwenden. Anzahl nach benötigter Gesamtlänge und inhaltlich verschiedenen Bewegungen wählen; längere oder wichtigere Aktionen eher mit drei bis fünf Ausschnitten zeigen. Nicht dieselbe Bewegung wiederholen oder einen zusammenhängenden Abschnitt nur formal zerteilen.
4. Nur wenn der Nutzer einen Clip ausdrücklich zum Beschleunigen markiert, die bestätigte vollständige Clipstrecke statt dieser Schnipselregel zusammenhängend mit exakt 5× abspielen. Kein anderes Retiming ableiten.
5. Erst nachdem alle Tagesclips verteilt und die langen Clips ausgeschöpft sind, Clips bis einschließlich 5 Sekunden an Anfang und Ende minimal kürzen, bis Bildspur und bereinigtes Voiceover exakt gleich lang sind. Handlung und Aussage müssen erkennbar bleiben. Erst danach nötigenfalls weniger wichtige lange Schnipsel reduzieren, jedoch nie unter zwei pro verwendetem langen Clip.

Ziel ist zuerst vollständige, chronologische und tonpassende Tagesabdeckung; danach ein kompakter, abwechslungsreicher Rhythmus. Nicht vorschnell Material kürzen und die dadurch entstandene Lücke anschließend mit Laufmaterial oder Bibliotheks-B-Roll füllen.

Bildmaterial zuerst aus dem bestätigten Projektordner anhand Dateinamen und Inhalt passend zur Aussage wählen. Zusätzliche Bibliotheks-B-Roll nur gemäß `voiceover_broll_policy`: ausdrücklich angefordert, wegen einer nach obigem Ablauf nachgewiesenen Lücke, beides oder gar nicht. Bei `none` ist Bibliotheks-B-Roll strikt verboten; eine Restlücke nach vollständiger Nutzung des Projektmaterials muss dem Nutzer gemeldet werden. Nur erlaubte Ordner durchsuchen. Keine Clips stillschweigend wiederholen/verlangsamen; B-Roll-Originalton bleibt stumm.

`FlashShutterIntro` ausschließlich nach der Voiceover-Level-3-Frage aktivieren. Bei Ja sieben unterschiedliche, chronologisch über den Tag verteilte Clips aus dem bestätigten Projektordner in `flash_shutter_intro_clips` festhalten. Keine Bibliotheks-B-Roll dafür verwenden. Das Tool ersetzt die ersten 59 Frames der normalen Bildspur durch sieben mittige Snippets mit zusammen etwa 1,97 Sekunden, lässt Voiceover und Musik ab 0:00 unverändert laufen und mischt `kauasilbershlachparodes-shutter-click-2-494026.mp3` bei −6 dB jeweils exakt 0,2 Sekunden vor den sechs Cuts vollständig ein. Titel und Untertitel werden anschließend unabhängig darübergelegt.

Bestätigte Originalton-Einschübe in `voiceover_inserts` dokumentieren. Den letzten vollständigen Take bzw. die genannte Aussage kompakt einsetzen, das Voiceover dort entfernen/pausieren und danach fortsetzen. Voiceover und jeden Einschub vor dem Zusammenfügen separat ausschließlich per konstantem Gain angleichen, damit die Lautstärke nicht springt und Klang/Dynamik erhalten bleiben. Passende Videoeinträge mit `original_audio: true` markieren; diese dürfen für die Aussage zusammenhängend länger als eine Sekunde bleiben. Die zusammengesetzte Sprachspur ist die einzige Renderquelle; das unveränderte Voiceover unter `archive_sources` bewahren.

Standardmusik ist `warm relaxed groove.mp3` ab 0:00 mit −20 dB. Zooms nur bei bestätigtem Ja anhand der Sprache planen und an jedem Bildwechsel zurücksetzen. Fehlt Bildmaterial und ist keine Fallback-B-Roll erlaubt, nachfragen statt Lücken zu füllen.
