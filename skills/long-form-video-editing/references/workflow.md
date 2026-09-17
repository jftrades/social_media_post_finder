# One-shot rendering workflow

## Prepare

1. Inventory every source and inspect duration, resolution, frame rate, orientation, audio channels, and visible content.
2. Transcribe speaking footage with word timestamps.
3. Read the selected reference analyses and create `tension-curve.md`, `edit-report.md`, and `job.json` in the work folder.
4. Keep the exact same segment list for all three outputs.

Use [job.example.json](job.example.json) as the contract. Frame values for overlays, zooms, SFX, and music refer to the finished `01_cut.mp4` timeline.

## Validate and render

From the repository root:

```text
python -X utf8 skills/long-form-video-editing/scripts/long_form.py validate project_videos/long_form_work/<project>/job.json
python -X utf8 skills/long-form-video-editing/scripts/long_form.py render-all project_videos/long_form_work/<project>/job.json
```

The renderer:

- uses FFmpeg for trims, order, speed, format normalization, audio continuity, and the two mixed LUT passes;
- renders `01_cut.mp4` without SFX, animation, zooms, or music, while retaining the approved camera LUT chain as the common color base;
- stages the cut and local assets for Remotion;
- renders `02_animated.mp4`, `03_final.mp4`, and `thumbnail.jpg` through Remotion;
- limits Remotion concurrency to 25% for a weaker laptop;
- decodes every MP4 as a QA smoke test and refuses to overwrite a non-empty finished project.

Install the Remotion runtime once with `npm install` in `skills/long-form-video-editing/remotion/`. Use `npm run studio` there only for debugging; ordinary work is headless.

## Plan requirements

- Every SFX entry states the action or editorial beat it supports.
- Every music cue states its tension function and includes deliberate fade boundaries.
- Every overlay chooses `default`, `note`, or `race` to map to Alte Haas, Child Hood, or Race Day.
- Every camera exception is explicit. Global `all_files_are_camera` never overrides `camera: false` on a segment.
- Speed ramps must remain safe, legible, and honest; do not fake exercise performance or elapsed time.

## Finish and QA

Inspect all three outputs, not only hashes or command exit codes. Compare the same timestamps across variants to verify the layer contract. Confirm full playback, sync, speech endings, music transitions, visual continuity, LUT consistency, overlay timing, thumbnail legibility, and output duration. Keep original inputs untouched.
