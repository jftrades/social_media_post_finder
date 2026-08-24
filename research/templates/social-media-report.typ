#set page(
  paper: "a4",
  margin: (top: 1.65cm, bottom: 1.55cm, left: 1.75cm, right: 1.75cm),
  numbering: "1",
)
#set text(size: 10pt, lang: "de")
#set par(justify: false, leading: 0.68em)
#set heading(numbering: none)

#let ink = rgb("#202124")
#let muted = rgb("#697386")
#let accent = rgb("#3D5AFE")
#let soft = rgb("#F4F6FA")

#let field(label, value) = [
  #text(size: 8pt, weight: "bold", fill: muted)[#label] \
  #text(fill: ink)[#value]
]

#let section-title(title) = [
  #v(0.75em)
  #text(size: 8.5pt, weight: "bold", fill: accent)[#title]
  #v(0.2em)
  #line(length: 100%, stroke: 0.5pt + rgb("#D9DEE8"))
  #v(0.3em)
]

#align(right)[
  #text(size: 8pt, fill: muted)[SOCIAL MEDIA RESEARCH]
]

#v(0.35em)
= Research Trends
#text(size: 9pt, fill: muted)[24.08.2026 · letzte 7 Tage · DACH · Deutsch]

#v(0.9em)
#box(fill: soft, inset: 10pt, width: 100%)[
  #text(weight: "bold")[Kurzfazit]
  \
  Wiederkehrendes Muster: ...
  \
  Stärkste relevante Beobachtung: ...
  \
  Unsicherheit: ...
]

#section-title("Rahmen")
#table(
  columns: (2.7cm, 1fr, 2.7cm, 1fr),
  gutter: 0.35cm,
  inset: 0pt,
  stroke: none,
  [#field("Plattformen", "TikTok · Reels · Shorts")], [#field("Kandidaten", "50 geprüft")],
  [#field("Auswahl", "max. 10 Items")], [#field("Own-Video-Vergleich", "deaktiviert")],
)

#section-title("Fundstück SM-YYYYMMDD-001")
#table(
  columns: (2.7cm, 1fr),
  gutter: 0.35cm,
  inset: 0pt,
  stroke: none,
  [#field("Plattform", "TikTok")], [#field("Thema", "Sport x Studentenalltag")],
  [#field("Veröffentlicht", "unknown")], [#field("Confidence", "medium")],
  [#field("Link", link("https://example.com")[Direkter öffentlicher Link])], [#field("Format", "...")],
)

#section-title("Beobachtung")
Titel/Caption: ...  \
Hook-Mechanismus: ...  \
Versprechen in den ersten Sekunden: ...  \
Pattern Interrupt: ...  \
Sichtbare Viralitätssignale: ...

#section-title("Einordnung")
Beobachtete Fakten: ...  \
Interpretation: ...  \
Aktualität: ...  \
Relevanz für Ferdis Themen: ...

#section-title("Eigenständige Adaption")
Kernidee: ...  \
Kamera-/Postproduktions-Variante für #link("https://www.tiktok.com/@ideas_by_ferdi")[#text(fill: accent)[#raw("@ideas_by_ferdi")]]: ...  \
Talking-Head-Variante für #link("https://www.tiktok.com/@ferdifun7")[#text(fill: accent)[#raw("@ferdifun7")]]: ...

#section-title("Synthese")
Wiederkehrende Muster: ...  \
Offene Unsicherheiten: ...  \
Nächster sinnvoller Befehl: `research ...`
