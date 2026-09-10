# Report contract

Use [the supplied Typst template](../assets/global-fitness-research.typ) for full and category reports. Save generated `.typ` and `.pdf` files under `output/research/`; this directory is intentionally ignored by Git.

## Default full report

Produce exactly these evidence sections when enough verified material exists:

1. 15 Trends
2. 15 Formate & Challenges
3. 15 virale Hooks

If a category has fewer than 15 defensible findings, show the verified count and a short coverage note. Never manufacture or weaken findings to fill the page.

## Page structure

- Compact cover with query, window, languages, platforms, candidate count, and evidence coverage.
- One visually separated section per research category.
- Direct source inside every finding card.
- Final compact methodology and limitations page only when useful.
- No source dump, content ideas, scripts, adaptations, creator outreach, shot lists, or production variants.

## Finding card

Each card should contain only:

- number and concise finding title
- platform, creator, publication date, and duration
- strongest metric or outlier signal
- one observed fact
- one short interpretation
- confidence
- direct clickable source

Keep cards readable and concise. Move detailed raw evidence into the Typst source comments or a matching structured data file when available, not into tiny type.

To keep the fixed cards stable, use a one-line title, a one-line metadata row, a one-line signal, at most two short lines for the observed fact, and at most two short lines for the interpretation. Shorten prose instead of reducing the font size.

## Language and visual style

- Write the report in German while preserving short verified English hook wording.
- Use the supplied portrait A4 template without shrinking typography to force a page target.
- Prefer whitespace, strong hierarchy, restrained blue accents, subtle borders, and consistent card heights.
- Use Segoe UI or another explicit sans-serif fallback throughout every finding card. Never use a serif font inside the 15-item grids.
- Keep body text at a readable size. Allow additional pages instead of compressing 45 findings into an unreadable grid.
