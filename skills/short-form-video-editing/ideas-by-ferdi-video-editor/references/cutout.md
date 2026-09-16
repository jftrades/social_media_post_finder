# Titel hinter der Person

Nur single/multi mit Titel und ausdrücklicher Antwort in Level 3: `intake.cutout: "ja"|"nein"`, dazu passend `title_behind_person: true|false`. Nein braucht weder Modell noch Laufzeit; bei Voiceover niemals abfragen oder aktivieren. Keine automatische Zustimmung bei älteren Jobs.

Reihenfolge: Schnitt und ggf. LUTs → Zooms → B-Roll → textfreies Bild/Personenmaske → Titel → Originalperson durch Maske darüber → Untertitel. Originalton wird nicht dupliziert. Whoosh/Musik und bisherige Lautstärkeregeln bleiben erhalten. B-Roll-Zeiten haben eine vollständig transparente Personenmaske: keine Talking-Head-Person über der B-Roll.

`scripts/cutout.py` verwendet RVM MobileNetV3 FP32 über ONNX Runtime (CPU, vier Threads). Abhängigkeiten werden mit `uv run` isoliert geladen. Kein API-Key, kein Video-Upload. Modell lokal installieren, nicht ins Repo committen:

Performance-Grenze: Dieser integrierte CPU-Pfad ist langsam und noch nicht durch den separat getesteten GPU-Prototyp ersetzt. Bei einem neuen Cutout-Auftrag vor langem Rendering auf die Laufzeit hinweisen und kurz testen; keine CapCut-ähnliche Geschwindigkeit versprechen.

- Quelle: https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx
- Ziel: `agent_tooling/RobustVideoMatting/rvm_mobilenetv3_fp32.onnx`
- SHA256: `88d4531297118f595bf2fd60f6f566aec2e559393802d1f436c380f0cbbd2828`
- Projekt und Lizenz: https://github.com/PeterL1n/RobustVideoMatting (GPL-3.0; nicht als uneingeschränkt lizenzfreies eingebettetes Produkt weitergeben).

`render` ruft den Cutout bei Ja automatisch auf. Die 1080×1920-Maske wird mit 30 fps verlustfrei in `cutout-alpha.mkv` gespeichert. `downsample_ratio=0.25`; RVM nutzt vorherige Frames, setzt seinen Zustand aber an jedem Schnitt und nach B-Roll zurück. `cutout-cache.json` prüft Bildquelle, Modell, Schnittgrenzen, B-Roll und Maskenhash. Nur Titel-/Font-/Untertiteländerungen können dieselbe Maske wiederverwenden; Bildänderungen erzwingen Neuberechnung. Vordergrundpixel kommen aus exakt demselben gezoomten Bild wie der Hintergrund, damit keine Skalierungs- oder Farbabweichung entsteht.

QA: Vergleichsframes an Haaren, Händen, schnellen Bewegungen, Zooms und Clipwechseln prüfen; Frames in B-Roll müssen ohne alte Person bleiben. Personenmaske ist keine Garantie für perfekte Haare oder mitgehaltene Gegenstände. Bei Aussetzern nicht stillschweigend freigeben. Titel kann verdeckt werden: falls die Aussage unlesbar wird, Rückfrage zu kürzerem Text/anderer Platzierung statt eigenmächtiger Änderungen.

Text-Tracking ist noch nicht enthalten: RVM liefert eine weiche Personenmaske pro Frame, keine stabilen Ankerpunkte für Textpositionen. Später separat Kopf-/Körper- oder Punkttracking mit Glättung ergänzen und die gleiche Maskenebene zur Verdeckung nutzen.
