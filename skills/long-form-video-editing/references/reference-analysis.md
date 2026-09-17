# Reference analysis contract

## Exact folder naming

For each root-level `<Video name>.mp4`, keep the MP4 in place and create:

```text
Folder-<Video name>/
`-- Assets-<Video name>/
    |-- analysis.md
    |-- style-rules.md
    |-- timeline.json
    |-- contact-sheet.jpg
    |-- contact-sheet-detailed-*.jpg
    |-- snapshots/
    |-- transitions/
    |-- text-and-fonts/
    |-- training-overlays/
    |-- audio-notes/
    `-- transcript/
```

`<Video name>` is the exact MP4 stem. Only characters Windows forbids in folder names may be minimally replaced. A run of trailing periods becomes the single Unicode ellipsis `…`, because Win32 and Git cannot address a folder whose final character is a period.

## Required analysis

`analysis.md` must include timestamped evidence for:

- cold open, promise, chapters, re-hooks, setback, escalation, payoff, and ending;
- talking-head cut rhythm, retained pauses, visible jump cuts, J/L cuts, and breathing room;
- B-roll categories, training montage construction, original-sound moments, and voice-over coverage;
- zoom-ins/outs, reframes, speed ramps, freeze frames, transitions, overlays, titles, notes, and training data;
- font roles, hierarchy, placement, animation, duration, shadow, and legibility;
- SFX categories and why they land; music entry/exit, mood changes, tension function, and dialogue ducking;
- recurring mechanisms that transfer to Ferdi and creator-specific surface elements that must not be copied.

Separate **Observed** from **Inferred**. A final export can reveal retained silence, jump cuts, and audio discontinuities, but cannot prove how many raw pauses were removed.

## Images and machine-readable evidence

- Link snapshots directly beside the note they support.
- Transition strips must show frames immediately before, at, and after selected cuts.
- `timeline.json` stores measured scene changes and retained silences; it is evidence, not a semantic classification by itself.
- `style-rules.md` distills the reusable rules and anti-copy limits.
- Update `STYLE_INDEX.md` after every new reference so a future edit can select references by story type and mechanism.

Run:

```text
python -X utf8 skills/long-form-video-editing/scripts/analyze_references.py
```

Then curate the generated evidence into `analysis.md`; automated cut detection alone is not a completed analysis.
