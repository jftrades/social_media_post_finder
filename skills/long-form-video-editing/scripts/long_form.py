#!/usr/bin/env python3
"""Hybrid FFmpeg + Remotion renderer for Ideas by Ferdi long-form projects."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
PROJECTS = ROOT / "project_videos"
TOOLS = ROOT / "agent_tooling"
SKILL = ROOT / "skills" / "long-form-video-editing"
REMOTION = SKILL / "remotion"
FFMPEG = TOOLS / "Purfview-Faster-Whisper-XXL" / "ffmpeg.exe"
NPM = shutil.which("npm.cmd") or shutil.which("npm") or "npm"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(args: list[str | Path], cwd: Path | None = None) -> str:
    proc = subprocess.run(
        [str(arg) for arg in args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode:
        raise RuntimeError((proc.stderr or proc.stdout)[-12000:])
    return proc.stdout + proc.stderr


def probe_duration(path: Path) -> float:
    proc = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-i", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", proc.stderr)
    if not match:
        raise ValueError(f"Could not read media duration: {path}")
    hours, minutes, seconds = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def resolved_inside(path: Path, parent: Path) -> Path:
    resolved = path.resolve()
    root = parent.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"Path is outside {root}: {resolved}")
    return resolved


def atempo(speed: float) -> str:
    if speed <= 0:
        raise ValueError("Segment speed must be positive")
    factors: list[float] = []
    remaining = speed
    while remaining > 2:
        factors.append(2.0)
        remaining /= 2
    while remaining < 0.5:
        factors.append(0.5)
        remaining /= 0.5
    factors.append(remaining)
    return ",".join(f"atempo={factor:.8g}" for factor in factors)


def validate(job: dict) -> None:
    required = ["project", "intake", "segments", "output"]
    missing = [key for key in required if key not in job]
    if missing:
        raise ValueError(f"Missing job keys: {', '.join(missing)}")
    if not job["segments"]:
        raise ValueError("At least one segment is required")
    intake = job["intake"]
    for level in ("level1", "level2", "level3"):
        if not intake.get(level, {}).get("confirmed"):
            raise ValueError(f"Long-form intake {level} is not confirmed")
    output = job["output"]
    for key in ("width", "height", "fps"):
        if int(output.get(key, 0)) <= 0:
            raise ValueError(f"Invalid output {key}")
    for index, segment in enumerate(job["segments"]):
        for key in ("source", "start", "end"):
            if key not in segment:
                raise ValueError(f"Segment {index} is missing {key}")
        if float(segment["end"]) <= float(segment["start"]):
            raise ValueError(f"Segment {index} end must be after start")
        atempo(float(segment.get("speed", 1)))


def project_paths(job: dict) -> tuple[Path, Path, Path]:
    project = job["project"]
    unfinished = resolved_inside(PROJECTS / "long_form_unfinished_projects" / project, PROJECTS / "long_form_unfinished_projects")
    work = resolved_inside(PROJECTS / "long_form_work" / project, PROJECTS / "long_form_work")
    finished = resolved_inside(PROJECTS / "long_form_finished_projects" / project, PROJECTS / "long_form_finished_projects")
    return unfinished, work, finished


def segment_source(segment: dict, unfinished: Path) -> Path:
    source = Path(segment["source"])
    if not source.is_absolute():
        source = unfinished / source
    return resolved_inside(source, unfinished)


def filter_path(path: Path) -> str:
    relative = path.resolve().relative_to(ROOT.resolve()).as_posix()
    return relative.replace("'", "\\'")


def render_base(job: dict, job_path: Path) -> Path:
    validate(job)
    unfinished, work, _ = project_paths(job)
    if not unfinished.is_dir():
        raise ValueError(f"Missing input project folder: {unfinished}")
    work.mkdir(parents=True, exist_ok=True)
    width = int(job["output"]["width"])
    height = int(job["output"]["height"])
    fps = int(job["output"]["fps"])
    all_camera = bool(job["intake"]["level2"].get("all_files_are_camera", False))
    excluded = {str(value).casefold() for value in job["intake"]["level2"].get("non_camera_files", [])}
    apply_luts = bool(job["intake"]["level2"].get("apply_camera_luts", False))
    lut1 = TOOLS / "LUTs" / "CINELIKE D to REC 709_26.P1003055.cube"
    lut2 = TOOLS / "LUTs" / "MERRY_MEN_II.cube"
    if apply_luts and (not lut1.exists() or not lut2.exists()):
        raise ValueError("The two required camera LUTs are missing")

    command: list[str | Path] = [FFMPEG, "-hide_banner", "-y"]
    sources: list[Path] = []
    for segment in job["segments"]:
        source = segment_source(segment, unfinished)
        if not source.exists():
            raise ValueError(f"Missing source: {source}")
        sources.append(source)
        command += ["-i", source]

    filters: list[str] = []
    concat_inputs: list[str] = []
    for index, (segment, source) in enumerate(zip(job["segments"], sources)):
        start = float(segment["start"])
        end = float(segment["end"])
        speed = float(segment.get("speed", 1))
        base = f"vb{index}"
        filters.append(
            f"[{index}:v]trim=start={start:.6f}:end={end:.6f},setpts=(PTS-STARTPTS)/{speed:.8g},"
            f"fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,setsar=1[{base}]"
        )
        relative_name = source.relative_to(unfinished).as_posix().casefold()
        is_camera = bool(segment.get("camera", all_camera and relative_name not in excluded))
        video_label = base
        if apply_luts and is_camera:
            lut1_path = filter_path(lut1)
            lut2_path = filter_path(lut2)
            filters += [
                f"[{base}]split=2[o1{index}][l1i{index}]",
                f"[l1i{index}]lut3d=file='{lut1_path}'[l1{index}]",
                f"[o1{index}][l1{index}]blend=all_expr='A*0.20+B*0.80'[m1{index}]",
                f"[m1{index}]split=2[o2{index}][l2i{index}]",
                f"[l2i{index}]lut3d=file='{lut2_path}'[l2{index}]",
                f"[o2{index}][l2{index}]blend=all_expr='A*0.70+B*0.30'[v{index}]",
            ]
            video_label = f"v{index}"
        filters.append(
            f"[{index}:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS,{atempo(speed)},"
            f"aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a{index}]"
        )
        concat_inputs.append(f"[{video_label}][a{index}]")
    filters.append("".join(concat_inputs) + f"concat=n={len(sources)}:v=1:a=1[vout][ajoin]")
    filters.append("[ajoin]loudnorm=I=-16:TP=-2:LRA=11[aout]")

    output = work / "01_cut.mp4"
    filter_script = work / "base-filter-complex.txt"
    filter_script.write_text(";".join(filters), encoding="utf-8")
    command += [
        "-filter_complex_script", filter_script,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", output,
    ]
    run(command, cwd=ROOT)
    stored_job = work / "job.json"
    if job_path.resolve() != stored_job.resolve():
        shutil.copy2(job_path, stored_job)
    return output


def copy_runtime_asset(source: Path, category: str) -> str:
    if not source.exists():
        raise ValueError(f"Missing runtime asset: {source}")
    digest = hashlib.sha256(str(source.resolve()).encode("utf-8")).hexdigest()[:8]
    target_name = f"{source.stem}-{digest}{source.suffix}"
    target = REMOTION / "public" / "runtime" / category / target_name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return f"runtime/{category}/{target_name}"


def stage_remotion(job: dict, cut: Path) -> Path:
    _, work, _ = project_paths(job)
    runtime_media = REMOTION / "public" / "runtime" / "media"
    runtime_media.mkdir(parents=True, exist_ok=True)
    base_target = runtime_media / "base.mp4"
    shutil.copy2(cut, base_target)
    for font in ("AlteHaasGroteskBold.ttf", "Child Hood.otf", "Raceday.otf"):
        source = TOOLS / "fonts" / font
        if not source.exists():
            raise ValueError(f"Missing required font: {source}")
        shutil.copy2(source, REMOTION / "public" / "runtime" / "fonts" / font)

    thumbnail = job.get("thumbnail", {})
    thumb_source = runtime_media / "thumbnail-source.jpg"
    source_value = thumbnail.get("source")
    if source_value:
        source = Path(source_value)
        if not source.is_absolute():
            unfinished, _, _ = project_paths(job)
            source = unfinished / source
        source = resolved_inside(source, project_paths(job)[0])
        if source.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            shutil.copy2(source, thumb_source)
        else:
            run([FFMPEG, "-hide_banner", "-y", "-ss", str(thumbnail.get("time", 0)), "-i", source, "-frames:v", "1", "-q:v", "2", thumb_source])
    else:
        run([FFMPEG, "-hide_banner", "-y", "-ss", str(thumbnail.get("time", 0)), "-i", cut, "-frames:v", "1", "-q:v", "2", thumb_source])

    duration_seconds = probe_duration(cut)
    fps = int(job["output"]["fps"])
    props = {
        "baseVideo": "runtime/media/base.mp4",
        "durationInFrames": max(1, round(duration_seconds * fps)),
        "fps": fps,
        "width": int(job["output"]["width"]),
        "height": int(job["output"]["height"]),
        "overlays": job.get("overlays", []),
        "zooms": job.get("zooms", []),
        "soundEffects": [],
        "music": [],
        "counters": job.get("counters", []),
        "imageOverlays": [],
        "videoOverlays": [],
        "thumbnailSource": "runtime/media/thumbnail-source.jpg",
        "thumbnailTitle": thumbnail.get("title", job["intake"]["level1"].get("working_title", job["project"])),
        "thumbnailAccent": thumbnail.get("accent", ""),
    }
    for source_item, destination in ((job.get("sound_effects", []), props["soundEffects"]), (job.get("music", []), props["music"])):
        for item in source_item:
            asset = Path(item["path"])
            if not asset.is_absolute():
                asset = ROOT / asset
            runtime_item = dict(item)
            runtime_item.pop("path")
            runtime_item["src"] = copy_runtime_asset(asset, "audio")
            destination.append(runtime_item)
    for item in job.get("image_overlays", []):
        asset = Path(item["path"])
        if not asset.is_absolute():
            asset = project_paths(job)[0] / asset
        asset = resolved_inside(asset, project_paths(job)[0])
        runtime_item = dict(item)
        runtime_item.pop("path")
        runtime_item["src"] = copy_runtime_asset(asset, "images")
        props["imageOverlays"].append(runtime_item)
    for item in job.get("video_overlays", []):
        asset = Path(item["path"])
        if not asset.is_absolute():
            asset = project_paths(job)[0] / asset
        asset = resolved_inside(asset, project_paths(job)[0])
        runtime_item = dict(item)
        runtime_item.pop("path")
        runtime_item["src"] = copy_runtime_asset(asset, "video")
        props["videoOverlays"].append(runtime_item)
    props_path = work / "remotion-props.json"
    save_json(props_path, props)
    return props_path


def render_remotion(job: dict, props_path: Path) -> None:
    _, work, _ = project_paths(job)
    run([NPM, "run", "render", "--", "--props", props_path, "--output-dir", work], cwd=REMOTION)
    render_final_music(job)


def render_final_music(job: dict) -> Path:
    _, work, _ = project_paths(job)
    animated = work / "02_animated.mp4"
    final = work / "03_final.mp4"
    music = job.get("music", [])
    if not music:
        shutil.copy2(animated, final)
        return final

    fps = int(job["output"]["fps"])
    total_frames = round(sum((float(item["end"]) - float(item["start"])) / float(item.get("speed", 1)) for item in job["segments"]) * fps)
    command: list[str | Path] = [FFMPEG, "-hide_banner", "-y", "-i", animated]
    filters = []
    labels = ["[0:a]"]
    for index, item in enumerate(music, start=1):
        asset = Path(item["path"])
        if not asset.is_absolute():
            asset = ROOT / asset
        if not asset.exists():
            raise ValueError(f"Missing music asset: {asset}")
        command += ["-stream_loop", "-1", "-i", asset]
        start_frame = int(item.get("startFrame", 0))
        end_frame = int(item.get("endFrame", total_frames))
        duration = max(0.04, (end_frame - start_frame) / fps)
        start_seconds = start_frame / fps
        volume = float(item.get("volume", 1))
        chain = f"[{index}:a]atrim=duration={duration:.6f},asetpts=PTS-STARTPTS"
        fade_in = int(item.get("fadeInFrames", 0)) / fps
        fade_out = int(item.get("fadeOutFrames", 0)) / fps
        if fade_in > 0:
            chain += f",afade=t=in:st=0:d={fade_in:.6f}"
        if fade_out > 0:
            chain += f",afade=t=out:st={max(0, duration-fade_out):.6f}:d={fade_out:.6f}"
        chain += f",volume={volume:.6f},adelay={round(start_seconds * 1000)}:all=1[m{index}]"
        filters.append(chain)
        labels.append(f"[m{index}]")
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=first:normalize=0[aout]")
    mix_script = work / "music-filter-complex.txt"
    mix_script.write_text(";".join(filters), encoding="utf-8")
    command += [
        "-filter_complex_script", mix_script,
        "-map", "0:v:0", "-map", "[aout]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", final,
    ]
    run(command, cwd=ROOT)
    return final


def qa(job: dict) -> dict:
    _, work, _ = project_paths(job)
    expected = probe_duration(work / "01_cut.mp4")
    report = {"expected_duration_seconds": expected, "outputs": []}
    for filename in ("01_cut.mp4", "02_animated.mp4", "03_final.mp4"):
        path = work / filename
        if not path.exists() or path.stat().st_size < 1024:
            raise ValueError(f"Missing or empty render: {path}")
        run([FFMPEG, "-v", "error", "-i", path, "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"])
        digest = sha256_file(path)
        report["outputs"].append({
            "file": filename,
            "bytes": path.stat().st_size,
            "planned_duration_seconds": expected,
            "required_streams": ["video", "audio"],
            "sha256": digest,
            "decode_check": "passed",
        })
    thumbnail = work / "thumbnail.jpg"
    if not thumbnail.exists() or thumbnail.stat().st_size < 1024:
        raise ValueError("Missing thumbnail")
    report["thumbnail"] = {
        "file": thumbnail.name,
        "bytes": thumbnail.stat().st_size,
        "sha256": sha256_file(thumbnail),
    }
    save_json(work / "qa.json", report)
    return report


def finish(job: dict) -> Path:
    _, work, finished = project_paths(job)
    if finished.exists() and any(finished.iterdir()):
        raise ValueError(f"Finished project already exists and is not empty: {finished}")
    finished.mkdir(parents=True, exist_ok=True)
    for filename in (
        "01_cut.mp4", "02_animated.mp4", "03_final.mp4", "thumbnail.jpg",
        "job.json", "remotion-props.json", "qa.json", "tension-curve.md", "edit-report.md",
    ):
        source = work / filename
        if source.exists():
            shutil.copy2(source, finished / filename)
    return finished


def one_shot(job_path: Path) -> Path:
    job = load_json(job_path)
    cut = render_base(job, job_path)
    props = stage_remotion(job, cut)
    render_remotion(job, props)
    qa(job)
    return finish(job)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "render-base", "render-all", "qa", "finish"))
    parser.add_argument("job", type=Path)
    args = parser.parse_args()
    job = load_json(args.job)
    if args.command == "validate":
        validate(job)
        print("Job is valid")
    elif args.command == "render-base":
        print(render_base(job, args.job))
    elif args.command == "render-all":
        print(one_shot(args.job))
    elif args.command == "qa":
        print(json.dumps(qa(job), indent=2))
    elif args.command == "finish":
        print(finish(job))
    return 0


if __name__ == "__main__":
    sys.exit(main())
