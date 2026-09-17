#!/usr/bin/env python3
"""Create technical timelines and visual evidence packs for long-form references."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[3]
REFERENCE_ROOT = ROOT / "project_videos" / "long_form_reference"
FFMPEG = ROOT / "agent_tooling" / "Purfview-Faster-Whisper-XXL" / "ffmpeg.exe"


def windows_safe_component(value: str) -> str:
    """Preserve the video stem, except trailing periods that Win32/Git cannot address."""
    trailing_periods = len(value) - len(value.rstrip("."))
    return value.rstrip(".") + ("…" if trailing_periods else "")


def run(args: list[str | Path]) -> str:
    proc = subprocess.run(
        [str(value) for value in args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode:
        raise RuntimeError((proc.stderr or proc.stdout)[-12000:])
    return proc.stdout + proc.stderr


def media_info(video: Path) -> dict:
    proc = subprocess.run([str(FFMPEG), "-hide_banner", "-i", str(video)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    raw = proc.stdout + proc.stderr
    duration_match = re.search(r"Duration: (\d+):(\d+):([\d.]+)", raw)
    if not duration_match:
        raise ValueError(f"Could not read duration: {video}")
    duration = int(duration_match.group(1)) * 3600 + int(duration_match.group(2)) * 60 + float(duration_match.group(3))
    resolution = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", raw)
    fps = re.search(r"([\d.]+) fps", raw)
    return {
        "duration_seconds": duration,
        "width": int(resolution.group(1)) if resolution else None,
        "height": int(resolution.group(2)) if resolution else None,
        "fps": float(fps.group(1)) if fps else None,
    }


def detect_silences(video: Path) -> list[dict]:
    output = run([FFMPEG, "-hide_banner", "-i", video, "-af", "silencedetect=noise=-38dB:d=0.28", "-f", "null", "-"])
    starts = [float(value) for value in re.findall(r"silence_start: ([\d.]+)", output)]
    ends = [(float(end), float(duration)) for end, duration in re.findall(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", output)]
    return [
        {"start": starts[index] if index < len(starts) else max(0, end - duration), "end": end, "duration": duration}
        for index, (end, duration) in enumerate(ends)
    ]


def detect_scene_changes(video: Path) -> list[float]:
    output = run([
        FFMPEG, "-hide_banner", "-i", video,
        "-vf", "scale=320:-2,select='gt(scene,0.24)',showinfo",
        "-an", "-vsync", "vfr", "-f", "null", "-",
    ])
    return sorted({round(float(value), 3) for value in re.findall(r"pts_time:([\d.]+)", output)})


def timestamp(value: float) -> str:
    minutes = int(value // 60)
    seconds = int(round(value % 60))
    return f"{minutes:02d}m{seconds:02d}s"


def extract_visuals(video: Path, assets: Path, duration: float, cuts: list[float]) -> None:
    snapshots = assets / "snapshots"
    transitions = assets / "transitions"
    snapshots.mkdir(parents=True, exist_ok=True)
    transitions.mkdir(parents=True, exist_ok=True)
    points = sorted({max(0.0, min(duration - 0.1, duration * fraction)) for fraction in (0, .04, .1, .2, .3, .4, .5, .6, .7, .8, .9, .97)})
    for index, point in enumerate(points, 1):
        target = snapshots / f"{index:02d}-{timestamp(point)}.jpg"
        run([FFMPEG, "-hide_banner", "-y", "-ss", f"{point:.3f}", "-i", video, "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "2", target])
    interval = max(0.2, duration / 24)
    run([
        FFMPEG, "-hide_banner", "-y", "-i", video,
        "-vf", f"fps=1/{interval:.6f},scale=320:-2,tile=6x4",
        "-frames:v", "1", "-q:v", "2", assets / "contact-sheet.jpg",
    ])
    detail_pattern = assets / "contact-sheet-detailed-%03d.jpg"
    run([
        FFMPEG, "-hide_banner", "-y", "-i", video,
        "-vf", "fps=1/12,scale=320:-2,tile=5x5",
        "-q:v", "3", detail_pattern,
    ])
    if cuts:
        selection = [cuts[min(len(cuts) - 1, round(index * (len(cuts) - 1) / 9))] for index in range(10)]
        for index, point in enumerate(selection, 1):
            start = max(0, point - 0.25)
            target = transitions / f"{index:02d}-{timestamp(point)}.jpg"
            run([
                FFMPEG, "-hide_banner", "-y", "-ss", f"{start:.3f}", "-i", video,
                "-t", "0.55", "-vf", "fps=6,scale=480:-2,tile=3x1",
                "-frames:v", "1", "-q:v", "2", target,
            ])


def analyze(video: Path) -> Path:
    safe_stem = windows_safe_component(video.stem)
    folder = REFERENCE_ROOT / f"Folder-{safe_stem}"
    assets = folder / f"Assets-{safe_stem}"
    assets.mkdir(parents=True, exist_ok=True)
    info = media_info(video)
    silences = detect_silences(video)
    cuts = detect_scene_changes(video)
    duration = info["duration_seconds"]
    timeline = {
        "source_video": video.name,
        "measurement_notes": {
            "scene_change_threshold": 0.24,
            "silence_threshold_db": -38,
            "minimum_silence_seconds": 0.28,
            "limitation": "Scene changes and retained silences are measured from the final export. Removed raw-footage pauses can only be inferred.",
        },
        "media": info,
        "metrics": {
            "detected_scene_changes": len(cuts),
            "scene_changes_per_minute": round(len(cuts) / (duration / 60), 2),
            "retained_silences": len(silences),
            "retained_silence_seconds": round(sum(item["duration"] for item in silences), 3),
            "retained_silence_share": round(sum(item["duration"] for item in silences) / duration, 4),
        },
        "scene_changes": cuts,
        "retained_silences": silences,
    }
    (assets / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    extract_visuals(video, assets, duration, cuts)
    return assets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("videos", nargs="*", type=Path)
    args = parser.parse_args()
    videos = args.videos or sorted(REFERENCE_ROOT.glob("*.mp4"))
    for video in videos:
        print(f"Analyzing {video.name}")
        print(analyze(video.resolve()))


if __name__ == "__main__":
    main()
