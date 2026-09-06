#let ink = rgb("#172033")
#let muted = rgb("#6E7890")
#let accent = rgb("#5575E7")
#let accent-soft = rgb("#E9EEFF")
#let cyan = rgb("#A7E6EF")
#let canvas = rgb("#F4F6FB")
#let paper = rgb("#FFFFFF")
#let line = rgb("#DCE2EE")

#set page(
  paper: "a4",
  margin: (top: 1.35cm, bottom: 1.25cm, left: 1.35cm, right: 1.35cm),
  fill: canvas,
  footer: context [
    #grid(
      columns: (1fr, auto),
      align(left)[#text(size: 7.5pt, fill: muted)[IDEAS BY FERDI / GLOBAL FITNESS RESEARCH]],
      align(right)[#text(size: 7.5pt, fill: muted)[#counter(page).display("01")]],
    )
  ],
)

#set text(font: ("Alte Haas Grotesk", "Arial"), size: 9.5pt, fill: ink, lang: "de")
#set par(justify: false, leading: 0.58em, spacing: 0.35em)

#let confidence-color(level) = if level == "high" {
  accent
} else if level == "medium" {
  rgb("#D28A36")
} else {
  muted
}

#let eyebrow(body) = text(
  size: 7.2pt,
  weight: "bold",
  tracking: 0.11em,
  fill: accent,
  body,
)

#let stat(label, value) = block(
  width: 100%,
  fill: paper,
  stroke: 0.7pt + line,
  radius: 7pt,
  inset: 10pt,
)[
  #text(size: 18pt, weight: "bold", fill: ink)[#value]
  #linebreak()
  #text(size: 7.4pt, fill: muted)[#label]
]

#let report-cover(
  title: "Global Fitness",
  accent-title: "Research",
  summary: "Aktuelle externe Signale. Keine Ideen, Skripte oder Eigenanalyse.",
  date: none,
  window: "7 Tage",
  candidates: "unknown",
  verified: "unknown",
  scope: "Global / Englisch + Deutsch / Videos ab 30 Sekunden",
) = [
  #v(0.45cm)
  #eyebrow([SOCIAL SIGNAL REPORT])
  #v(0.35cm)
  #text(size: 29pt, weight: "bold", fill: ink)[#title]
  #linebreak()
  #text(size: 29pt, weight: "bold", fill: accent)[#accent-title]

  #v(0.75cm)
  #text(size: 11pt, fill: muted)[#summary]

  #v(1.1cm)
  #grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 10pt,
    stat("Research-Fenster", window),
    stat("Kandidaten geprüft", candidates),
    stat("Verifizierte Befunde", verified),
  )

  #v(1.05cm)
  #block(
    width: 100%,
    fill: accent,
    radius: 8pt,
    inset: 18pt,
  )[
    #eyebrow(text(fill: white)[SCOPE])
    #v(0.3cm)
    #text(size: 16pt, weight: "bold", fill: white)[#scope]
    #if date != none [
      #v(0.35cm)
      #text(size: 8.5pt, fill: rgb("#DDE5FF"))[Stand #date]
    ]
  ]

  #v(1fr)
  #grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 18pt,
    [
      #eyebrow([01])
      #v(0.18cm)
      #text(size: 12pt, weight: "bold")[Trends]
      #text(size: 8pt, fill: muted)[Wiederkehrende Themen und Verhaltenssignale.]
    ],
    [
      #eyebrow([02])
      #v(0.18cm)
      #text(size: 12pt, weight: "bold")[Formate]
      #text(size: 8pt, fill: muted)[Neue Challenges und wiederholbare Strukturen.]
    ],
    [
      #eyebrow([03])
      #v(0.18cm)
      #text(size: 12pt, weight: "bold")[Hooks]
      #text(size: 8pt, fill: muted)[Verifizierte Einstiege starker Outlier-Videos.]
    ],
  )
  #v(0.6cm)
]

#let finding(
  n,
  title,
  meta,
  signal,
  observed,
  interpretation,
  confidence,
  source-label,
  source-url,
) = block(
  width: 100%,
  height: 4.45cm,
  breakable: false,
  fill: paper,
  stroke: 0.7pt + line,
  radius: 7pt,
  inset: 9pt,
)[
  #let number-label = if n < 10 { "0" + str(n) } else { str(n) }
  #let confidence-label = if confidence == "high" {
    "HIGH"
  } else if confidence == "medium" {
    "MEDIUM"
  } else {
    "LOW"
  }
  #grid(
    columns: (1fr, auto),
    eyebrow(number-label),
    align(right)[
      #text(
        size: 6.8pt,
        weight: "bold",
        fill: confidence-color(confidence),
      )[#confidence-label]
    ],
  )

  #v(0.14cm)
  #text(size: 11pt, weight: "bold", fill: ink)[#title]
  #v(0.1cm)
  #text(size: 7.8pt, fill: muted)[#meta]

  #v(0.22cm)
  #text(size: 8.4pt, weight: "bold", fill: accent)[#signal]
  #v(0.1cm)
  #text(size: 8pt, fill: ink)[#observed]
  #text(size: 7.8pt, fill: muted, style: "italic")[#interpretation]

  #v(1fr)
  #link(source-url)[
    #text(size: 7.8pt, weight: "bold", fill: accent)[#source-label  ->]
  ]
]

#let section-header(
  number,
  title,
  subtitle,
  continuation: false,
  note: none,
) = [
  #grid(
    columns: (auto, 1fr),
    column-gutter: 12pt,
    align(top)[#text(size: 23pt, weight: "bold", fill: accent)[#number]],
    [
      #text(size: 20pt, weight: "bold", fill: ink)[#title]
      #if continuation [
        #h(5pt)
        #text(size: 8pt, fill: muted)[FORTSETZUNG]
      ]
      #linebreak()
      #text(size: 8.5pt, fill: muted)[#subtitle]
    ],
  )

  #if note != none [
    #v(0.35cm)
    #block(width: 100%, fill: accent-soft, radius: 5pt, inset: 8pt)[
      #text(size: 7.8pt, fill: ink)[#note]
    ]
  ]

  #v(0.45cm)
]

#let card-grid(items) = grid(
  columns: (1fr, 1fr),
  gutter: 10pt,
  ..items,
)

#let section-page(
  number,
  title,
  subtitle,
  items,
  note: none,
) = {
  let split = calc.min(8, items.len())
  let first-page = items.slice(0, split)
  let remaining = items.slice(split)

  [
    #pagebreak()
    #section-header(number, title, subtitle, note: note)
    #card-grid(first-page)
  ]

  if remaining.len() > 0 {
    [
      #pagebreak()
      #section-header(number, title, subtitle, continuation: true)
      #card-grid(remaining)
    ]
  }
}

#let methodology(title: "Methodik & Grenzen", body) = [
  #pagebreak()
  #eyebrow([METHODIK])
  #v(0.3cm)
  #text(size: 22pt, weight: "bold")[#title]
  #v(0.7cm)
  #block(width: 100%, fill: paper, stroke: 0.7pt + line, radius: 8pt, inset: 16pt)[
    #text(size: 9.2pt)[#body]
  ]
]
