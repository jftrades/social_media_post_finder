---
name: ideas-by-ferdi-voiceover
description: Schneidet vorhandenes Voice-over mit lokalen B-Roll-Clips, Untertiteln und Musik nach dem Video-schneiden-Intake.
---

# Voice-over mit B-Roll

Ohne die drei nacheinander beantworteten Levels aus `../ideas-by-ferdi-video-editor/SKILL.md` dorthin zurückleiten und beim ersten offenen Level warten. Alle globalen Standards inklusive Titelstil, Audio und Effekten abfragen. Auto-Cutout niemals abfragen oder aktivieren.
Gemeinsames Tooling und Vorgehen: `../ideas-by-ferdi-video-editor/references/workflow.md` lesen.
`mode: voiceover` verwendet genau eine Voiceover-Datei in `sources`; die vielen Bildclips stehen in `visuals`. Stimme transkribieren und bereinigen, keinen Text oder künstliche Stimme erfinden. Bildclips über 5 Sekunden immer als mindestens zwei unterschiedliche, chronologische 1-Sekunden-Schnipsel derselben Datei schneiden. Nicht dieselbe Bewegung wiederholen oder einen zusammenhängenden Abschnitt nur formal zerteilen. Clips bis 5 Sekunden dürfen einen einzelnen passenden Ausschnitt liefern. Erst wenige verteilte Frames prüfen, nur interessante Stellen genauer ansehen.

Bildmaterial zuerst aus dem bestätigten Projektordner anhand Dateinamen und Inhalt passend zur Aussage wählen. Zusätzliche Bibliotheks-B-Roll nur gemäß `voiceover_broll_policy`: ausdrücklich angefordert, wegen nachgewiesener Lücke, beides oder gar nicht. Nur erlaubte Ordner durchsuchen. Keine Clips stillschweigend wiederholen/verlangsamen; B-Roll-Originalton bleibt stumm.

Bestätigte Originalton-Einschübe in `voiceover_inserts` dokumentieren. Den letzten vollständigen Take bzw. die genannte Aussage kompakt einsetzen, das Voiceover dort entfernen/pausieren und danach fortsetzen. Voiceover und jeden Einschub vor dem Zusammenfügen separat normalisieren, damit die Lautstärke nicht springt. Passende Videoeinträge mit `original_audio: true` markieren; diese dürfen für die Aussage zusammenhängend länger als eine Sekunde bleiben. Die zusammengesetzte Sprachspur ist die einzige Renderquelle; das unveränderte Voiceover unter `archive_sources` bewahren.

Standardmusik ist `warm relaxed groove.mp3` ab 0:00 mit −20 dB. Zooms nur bei bestätigtem Ja anhand der Sprache planen und an jedem Bildwechsel zurücksetzen. Fehlt Bildmaterial und ist keine Fallback-B-Roll erlaubt, nachfragen statt Lücken zu füllen.
