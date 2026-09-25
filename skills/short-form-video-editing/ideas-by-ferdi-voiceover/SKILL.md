---
name: short-form-voiceover-editing
description: Schneidet vorhandenes Short-Form-Voice-over mit lokalen B-Roll-Clips, Untertiteln und Musik nach dem Video-schneiden-Intake.
---

# Short Form Voice-over mit B-Roll

Ohne die drei nacheinander beantworteten Levels aus `../ideas-by-ferdi-video-editor/SKILL.md` dorthin zurückleiten und beim ersten offenen Level warten. Alle globalen Standards inklusive Titelstil, Audio und Effekten abfragen. Auto-Cutout niemals abfragen oder aktivieren.
Gemeinsames Tooling und Vorgehen: `../ideas-by-ferdi-video-editor/references/workflow.md` lesen.
`mode: voiceover` verwendet genau eine Voiceover-Datei in `sources`; die vielen Bildclips stehen in `visuals`. Stimme transkribieren und bereinigen, keinen Text oder künstliche Stimme erfinden. Erst wenige verteilte Frames prüfen, nur interessante Stellen genauer ansehen.

Plane die Bildspur in dieser Reihenfolge:

1. Voiceover bereinigen und in zeitlich verankerte Aussagen aufteilen. Jeder Aussage anhand Dateiname und Prüfframes das passende Motiv zuordnen; `match` je Bildintervall mit Aussage und finalem Zeitbereich dokumentieren. Neue Jobs nutzen `visual_cut_policy: story_matched` und denselben Wert in `intake.visual_timing`.
2. Das passende Motiv fuer die ganze zugehoerige Aussage zeigen: Bei zehn Sekunden ueber Eis bleiben zehn Sekunden Eis-Bilder, nicht schon Gym. Tageschronologie bleibt die Grundordnung; die Reihenfolge weiterhin im Intake klaeren. Kein unpassendes Motiv erzwingen, nur um alle Dateien unterzubringen. Nicht passende/ueberzaehlige Clips duerfen entfallen; bei ausdruecklicher Pflichtclip-Auswahl einen unloesbaren Konflikt kurz klaeren.
3. Innerhalb eines Motivs gerne mehrere unterschiedliche, chronologische Ausschnitte derselben Datei verwenden und Leerlauf entfernen. Anzahl und Dauer richten sich nach Aussage und erkennbarer Handlung, nicht nach einer festen Ein-Sekunden-Regel oder maximal fuenf Schnipseln. Laengere Einstellungen sind erlaubt; keine identischen Bewegungen loopen oder Abschnitte nur formal zerteilen.
4. Nur wenn der Nutzer einen Clip ausdrücklich zum Beschleunigen markiert, die bestätigte vollständige Clipstrecke statt dieser Schnipselregel zusammenhängend mit exakt 5× abspielen. Kein anderes Retiming ableiten.
5. Bildwechsel an den Aussagenwechseln ausrichten, erst danach innerhalb dieser Abschnitte den Rhythmus straffen. Vor Export anhand der finalen Sprachzeiten Anfang/Mitte/Ende jeder konkreten Aussage mit Bildframes abgleichen: weder vorauseilen noch das passende Motiv mehrere Sekunden zu spaet zeigen. Fehlende passende Bilddauer gezielt melden bzw. nur erlaubte B-Roll nutzen.

Prioritaet: Aussage-Bild-Match → nachvollziehbare Tageschronologie → abwechslungsreicher Rhythmus. Alle Clips und schnelle Cuts sind kein Selbstzweck. FlashShutter bleibt der ausdruecklich freigegebene Teaser vor dieser aussagegebundenen Bildplanung.

Bildmaterial zuerst aus dem bestätigten Projektordner passend zur Aussage wählen. Zusätzliche Bibliotheks-B-Roll nur gemäß `voiceover_broll_policy`: ausdrücklich angefordert, bei einer nach Prüfung des passenden Projektmaterials verbleibenden inhaltlichen Bildlücke, beides oder gar nicht. Bei `none` ist Bibliotheks-B-Roll strikt verboten; fehlendes passendes Material melden, nicht durch sachfremde Tagesclips auffüllen. Nur erlaubte Ordner durchsuchen. Keine Clips stillschweigend wiederholen/verlangsamen; B-Roll-Originalton bleibt stumm.

`FlashShutterIntro` ausschließlich nach der Voiceover-Level-3-Frage aktivieren. Bei Ja sieben unterschiedliche, chronologisch über den Tag verteilte Clips aus dem bestätigten Projektordner in `flash_shutter_intro_clips` festhalten. Keine Bibliotheks-B-Roll dafür verwenden. Das Tool ersetzt die ersten 59 Frames der normalen Bildspur durch sieben mittige Snippets mit zusammen etwa 1,97 Sekunden, lässt Voiceover und Musik ab 0:00 unverändert laufen und mischt `kauasilbershlachparodes-shutter-click-2-494026.mp3` bei −6 dB jeweils exakt 0,2 Sekunden vor den sechs Cuts vollständig ein. Titel und Untertitel werden anschließend unabhängig darübergelegt.

Bestätigte Originalton-Einschübe in `voiceover_inserts` dokumentieren. Den letzten vollständigen Take bzw. die genannte Aussage kompakt einsetzen, das Voiceover dort entfernen/pausieren und danach fortsetzen. Voiceover und jeden Einschub vor dem Zusammenfügen separat ausschließlich per konstantem Gain angleichen, damit die Lautstärke nicht springt und Klang/Dynamik erhalten bleiben. Passende Videoeinträge mit `original_audio: true` markieren; diese dürfen für die Aussage zusammenhängend länger als eine Sekunde bleiben. Die zusammengesetzte Sprachspur ist die einzige Renderquelle; das unveränderte Voiceover unter `archive_sources` bewahren.

Standardmusik ist `warm relaxed groove.mp3` ab 0:00 mit −20 dB. Zooms nur bei bestätigtem Ja anhand der Sprache planen und an jedem Bildwechsel zurücksetzen. Fehlt Bildmaterial und ist keine Fallback-B-Roll erlaubt, nachfragen statt Lücken zu füllen.
