#let ink = rgb("20252b")
#let muted = rgb("68727d")
#let accent = rgb("087f8c")
#let pale = rgb("eef5f5")

#set page(
  paper: "a4",
  margin: (top: 1.05cm, bottom: 1.0cm, left: 1.15cm, right: 1.15cm),
  footer: context [
    #align(center)[#text(size: 7pt, fill: muted)[#counter(page).display("1")]]
  ],
)
#set text(font: "Arial", size: 8.55pt, fill: ink)
#set par(justify: false, leading: 0.42em, spacing: 0.25em)

#let report-title(title, subtitle) = block(
  width: 100%,
  inset: (x: 9pt, y: 7pt),
  radius: 4pt,
  fill: pale,
)[
    #text(size: 14pt, weight: "bold", fill: ink)[#title]
  #linebreak()
  #text(size: 8.1pt, fill: muted)[#subtitle]
]

#let section-title(title, note: none) = {
  block(
    width: 100%,
    inset: (top: 5pt, bottom: 3pt),
    above: 5pt,
    below: 3pt,
    stroke: (bottom: 0.7pt + accent),
  )[
    #text(size: 10.5pt, weight: "bold", fill: ink)[#title]
    #if note != none [#h(5pt) #text(size: 7.6pt, fill: muted)[#note]]
  ]
}

#let idea(n, angle, value, combo) = block(
  breakable: false,
  inset: (bottom: 1.4pt),
)[
  #text(size: 6.7pt, weight: "bold", fill: accent)[#n. #angle]
  #text(size: 6.15pt, fill: muted)[ — #value · ]
  #text(size: 6.15pt, fill: accent)[#combo]
]

#let production(title, body) = block(
  breakable: false,
  inset: (bottom: 3pt),
)[
  #text(weight: "bold", fill: ink)[#title] #text(size: 8.1pt)[#body]
]

#let source(date, name, url, platform, note: none) = block(
  breakable: false,
  inset: (bottom: 2.5pt),
)[
  #text(size: 7.7pt, weight: "bold")[#date] #link(url)[#text(fill: accent)[#name]]
  #text(size: 7.5pt, fill: muted)[ · #platform#if note != none [ · #note]]
]
