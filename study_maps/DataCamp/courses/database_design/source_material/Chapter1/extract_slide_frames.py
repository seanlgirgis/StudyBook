#!/usr/bin/env python3
r"""Extract interval screenshots from a video and keep the last frame of each slide/build sequence.

Requires:
    pip install pillow numpy
    ffmpeg available on PATH

Examples:
    python extract_slide_frames.py "Storing data.mp4"
    python extract_slide_frames.py "Storing data.mp4" --seconds 3 --change-ratio 0.04
    python extract_slide_frames.py --screenshots ".\interval_screenshots"
"""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps


def run_ffmpeg(video: Path, screenshot_dir: Path, seconds: float, overwrite: bool) -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg was not found on PATH.")

    screenshot_dir.mkdir(parents=True, exist_ok=True)
    output_pattern = screenshot_dir / "frame_%04d.jpg"

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "warning",
        "-i", str(video),
        "-vf", f"fps=1/{seconds}",
        "-q:v", "2",
    ]
    command.append("-y" if overwrite else "-n")
    command.append(str(output_pattern))

    print("Running FFmpeg:")
    print(" ".join(f'"{part}"' if " " in part else part for part in command))
    subprocess.run(command, check=True)


def load_gray(path: Path, size: tuple[int, int] = (320, 180)) -> np.ndarray:
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image).convert("L").resize(size)
        return np.asarray(image, dtype=np.int16)


def changed_pixel_ratio(previous: np.ndarray, current: np.ndarray, pixel_delta: int) -> float:
    difference = np.abs(current - previous)
    return float(np.mean(difference > pixel_delta))


def choose_slide_ends(
    files: list[Path],
    change_ratio: float,
    pixel_delta: int,
) -> tuple[list[int], list[dict[str, object]]]:
    if not files:
        return [], []

    images = [load_gray(path) for path in files]
    group_starts = [0]
    report: list[dict[str, object]] = []

    for index in range(1, len(files)):
        ratio = changed_pixel_ratio(images[index - 1], images[index], pixel_delta)
        starts_new_group = ratio > change_ratio
        if starts_new_group:
            group_starts.append(index)

        report.append(
            {
                "previous_frame": files[index - 1].name,
                "current_frame": files[index].name,
                "changed_pixel_ratio": round(ratio, 6),
                "classification": "new_slide" if starts_new_group else "same_build_sequence",
            }
        )

    group_ends = [start - 1 for start in group_starts[1:]] + [len(files) - 1]
    return group_ends, report


def copy_selected(files: list[Path], selected_indices: list[int], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    selected_paths: list[Path] = []

    for sequence, index in enumerate(selected_indices, start=1):
        source = files[index]
        destination = output_dir / f"slide_{sequence:03d}{source.suffix.lower()}"
        shutil.copy2(source, destination)
        selected_paths.append(destination)

    return selected_paths


def write_report(report: list[dict[str, object]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "previous_frame",
                "current_frame",
                "changed_pixel_ratio",
                "classification",
            ],
        )
        writer.writeheader()
        writer.writerows(report)


def make_contact_sheet(files: list[Path], path: Path, columns: int = 4) -> None:
    if not files:
        return

    thumb_width, thumb_height, label_height = 320, 180, 24
    rows = (len(files) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), "white")
    draw = ImageDraw.Draw(sheet)

    for index, file in enumerate(files):
        with Image.open(file) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            image.thumbnail((thumb_width, thumb_height))
            x = (index % columns) * thumb_width
            y = (index // columns) * (thumb_height + label_height)
            sheet.paste(image, (x + (thumb_width - image.width) // 2, y))
            draw.text((x + 6, y + thumb_height + 4), file.name, fill="black")

    sheet.save(path, quality=92)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run FFmpeg and keep the last screenshot in each slide animation/build sequence."
    )
    parser.add_argument("video", nargs="?", type=Path, help="Input video file.")
    parser.add_argument(
        "--screenshots",
        type=Path,
        help="Process an existing screenshot directory instead of running FFmpeg.",
    )
    parser.add_argument("--seconds", type=float, default=3.0, help="Seconds between screenshots. Default: 3")
    parser.add_argument(
        "--change-ratio",
        type=float,
        default=0.04,
        help="Fraction of materially changed pixels that starts a new slide. Default: 0.04",
    )
    parser.add_argument(
        "--pixel-delta",
        type=int,
        default=18,
        help="Brightness difference required for a pixel to count as changed. Default: 18",
    )
    parser.add_argument("--overwrite", action="store_true", help="Allow FFmpeg to overwrite screenshots.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.screenshots:
        screenshot_dir = args.screenshots.resolve()
        work_root = screenshot_dir.parent
    else:
        if not args.video:
            print("Provide a video file or use --screenshots.", file=sys.stderr)
            return 2
        video = args.video.resolve()
        if not video.exists():
            print(f"Video not found: {video}", file=sys.stderr)
            return 2
        work_root = video.parent
        screenshot_dir = work_root / "interval_screenshots"
        run_ffmpeg(video, screenshot_dir, args.seconds, args.overwrite)

    files = sorted(
        path for path in screenshot_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )
    if not files:
        print(f"No image files found in: {screenshot_dir}", file=sys.stderr)
        return 2

    selected_indices, report = choose_slide_ends(files, args.change_ratio, args.pixel_delta)
    output_dir = work_root / "selected_slide_frames"

    if output_dir.exists() and args.overwrite:
        shutil.rmtree(output_dir)

    selected_files = copy_selected(files, selected_indices, output_dir)
    write_report(report, output_dir / "comparison_report.csv")
    make_contact_sheet(selected_files, output_dir / "contact_sheet.jpg")

    print(f"Input screenshots: {len(files)}")
    print(f"Selected slide frames: {len(selected_files)}")
    print(f"Output directory: {output_dir}")
    print("Tip: lower --change-ratio to split more aggressively; raise it to merge more builds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
