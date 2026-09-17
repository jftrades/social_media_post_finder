---
name: long-form-video-editing
description: Analyze local reference edits and one-shot longer Ideas by Ferdi YouTube videos into a clean cut, an animated/SFX cut, a fully scored final MP4, and a thumbnail. Use for long-form editing, not Shorts/Reels or creator imitation.
---

# Long Form Video Editing

Create a truthful, entertaining YouTube edit from Ferdi's local footage. Learn reusable mechanisms from the local reference analyses, then adapt them to this video's real story rather than copying a creator's exact sequence, jokes, branding, or premise.

## Load only the needed context

1. Read [references/intake.md](references/intake.md) and complete its three levels strictly in order. Ask only missing questions and wait after each level.
2. Read [references/reference-analysis.md](references/reference-analysis.md). Inspect `project_videos/long_form_reference/STYLE_INDEX.md` and the `analysis.md` for every reference Ferdi names. If he names none, select the best one or two by story type and say which mechanisms will guide the edit.
3. Read [references/style-system.md](references/style-system.md) before planning text, color, sound, music, or thumbnail.
4. Read [references/workflow.md](references/workflow.md) before creating the job, rendering, or finishing.

Do not start transcription, edit planning, or rendering until Levels 1–3 are confirmed. After Level 3, work one-shot through all outputs unless files are missing, instructions conflict, or a render failure requires a choice.

## Workspace contract

- Inputs: `project_videos/long_form_unfinished_projects/<project>/`
- Intermediates: `project_videos/long_form_work/<project>/`
- Deliverables: `project_videos/long_form_finished_projects/<project>/`
- Reference MP4s and analysis packs: `project_videos/long_form_reference/`
- Shared long-form B-roll: `agent_tooling/long_form_b_roll/`
- Shared music, SFX, fonts, LUTs, transcription, FFmpeg, and Remotion: `agent_tooling/` plus this skill's `remotion/` runtime

Never use a Short-Form project folder or Short-Form B-roll unless Ferdi explicitly names an asset. Never delete long-form originals automatically. Never overwrite a non-empty finished project.

## Story and tension plan

Before cutting, make a timestamped tension curve in the work folder. It must identify the cold open, promise, setup, first obstacle, progress, setback or uncertainty, escalation, decisive attempt, payoff, and brief reflection when those beats exist. For every section specify:

- the viewer's current question and what changes their prediction;
- cut density and intentional breathing room;
- talking head, live audio, voice-over, training montage, or explanatory B-roll;
- planned zooms, text, graphics, transitions, SFX, and music function;
- the visible proof that earns the next beat.

Do not force every video into the same arc. Use the reference analyses to distinguish diary/progression, challenge, update, relationship, and investigation structures.

## Required outputs

Every successful one-shot edit produces:

1. `01_cut.mp4`: approved story/dialogue cut only; no SFX, zooms, motion graphics, or music. Apply the approved camera LUT chain because it is the common color base for all three versions.
2. `02_animated.mp4`: the same cut plus SFX, purposeful zooms, Remotion text/graphics, and transitions; no music.
3. `03_final.mp4`: the animated version plus multiple music cues chosen against the tension curve, with fades and dialogue-safe mixing.
4. `thumbnail.jpg`: 1280×720, derived from the actual project footage and the same click promise.
5. `edit-report.md`, `job.json`, `remotion-props.json`, and `qa.json` so every decision is inspectable.

The three MP4s must share the same underlying story cut. Later stages add layers; they must not silently change the narrative edit.

## Style invariants

- Default text font: Alte Haas Grotesk Bold with a blurred shadow.
- Handwritten note, thought, label, or annotation: Child Hood.
- One- or two-word impact heading: Race Day.
- Ask whether all inputs are camera footage. When LUTs are approved, treat files as camera by default and exclude only the files Ferdi names as non-camera or already graded.
- Camera order: `CINELIKE D to REC 709_26.P1003055.cube` at 80%, then `MERRY_MEN_II.cube` at 30%.
- Use more than one music track when the story changes emotional function. Never loop one song across the whole video merely for convenience.
- Use zooms and effects only when they sharpen a reaction, reveal, joke, proof, or escalation. Do not import Short-Form frequency as a default.

## One-shot completion gate

Finish only after:

- every output decodes without errors and contains expected audio/video streams;
- full-length playback inspection confirms sync, pacing, no black gaps, no missing media, no accidental repeated clips, and no clipped words;
- text uses the intended font role, remains readable, and does not cover the important action;
- LUT exclusions and reference-derived choices match the confirmed intake;
- dialogue remains intelligible through all SFX and music changes;
- the thumbnail promise matches the actual payoff;
- final copies and hashes are verified while all inputs remain intact.
