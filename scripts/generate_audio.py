#!/usr/bin/env python3
r"""
Generate spoken audio from a text file using OpenAI Chat Completions audio output.

Example:
    python .\scripts\generate_audio.py "D:\full\path\script.txt"
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
import shutil
import subprocess
import sys
import wave

from openai import OpenAI


SUPPORTED_FORMATS = {"wav", "aac", "mp3", "flac", "opus", "pcm", "pcm16"}
SPEAKER_LINE_RE = re.compile(
    r"^\s*(interviewer|candidate|question|answer|q\d*|a\d*|speaker\s*[ab])\s*[:\-]",
    re.IGNORECASE,
)
BRACKET_SPEAKER_RE = re.compile(r"^\s*\*\*\[(?P<speaker>[^\]]+)\]\*\*\s*$")
PLAIN_SPEAKER_RE = re.compile(r"^\s*(RAMYA|SEAN)\s*:\s*$", re.IGNORECASE)


def _safe_stem(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return cleaned.strip("._-") or "audio"


def _build_output_path(input_path: Path, output_dir: Path, fmt: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = _safe_stem(input_path.stem)
    return output_dir / f"{stem}_{timestamp}.{fmt}"


def _tts_response_format(fmt: str) -> str:
    # Audio speech endpoint uses `pcm`; keep `pcm16` as CLI alias for convenience.
    if fmt == "pcm16":
        return "pcm"
    return fmt


def _split_text_for_tts(text: str, max_chars: int) -> list[str]:
    text = text.strip()
    if len(text) <= max_chars:
        return [text]

    # Prefer dialogue-turn splitting when speaker labels exist.
    lines = [ln.rstrip() for ln in text.splitlines()]
    turns: list[str] = []
    current_turn: list[str] = []
    saw_speaker_labels = any(SPEAKER_LINE_RE.match(ln or "") for ln in lines)
    if saw_speaker_labels:
        for ln in lines:
            if SPEAKER_LINE_RE.match(ln):
                if current_turn:
                    turns.append("\n".join(current_turn).strip())
                current_turn = [ln]
            else:
                if current_turn:
                    current_turn.append(ln)
                elif ln.strip():
                    current_turn = [ln]
        if current_turn:
            turns.append("\n".join(current_turn).strip())
    else:
        turns = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    paragraphs = turns
    chunks: list[str] = []
    current = ""

    def flush_current() -> None:
        nonlocal current
        if current.strip():
            chunks.append(current.strip())
        current = ""

    for para in paragraphs:
        candidate = f"{current}\n\n{para}".strip() if current else para
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            flush_current()

        if len(para) <= max_chars:
            current = para
            continue

        sentences = re.split(r"(?<=[.!?])\s+", para)
        temp = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            sentence_candidate = f"{temp} {sentence}".strip() if temp else sentence
            if len(sentence_candidate) <= max_chars:
                temp = sentence_candidate
            else:
                if temp:
                    chunks.append(temp)
                if len(sentence) <= max_chars:
                    temp = sentence
                else:
                    # Hard split if a single sentence is too large.
                    start = 0
                    while start < len(sentence):
                        end = start + max_chars
                        chunks.append(sentence[start:end].strip())
                        start = end
                    temp = ""
        if temp:
            chunks.append(temp)

    flush_current()
    return chunks


def _normalize_for_tts(raw_text: str) -> str:
    text = raw_text.replace("\r\n", "\n").strip()
    if not text:
        return text

    # If full script markers exist, keep only the script body.
    full_match = re.search(r"## SCRIPT BEGINS\s*(.*?)\n---\s*\*\*END OF SCRIPT\*\*", text, re.DOTALL)
    if full_match:
        text = full_match.group(1).strip()

    lines = [ln.rstrip() for ln in text.split("\n")]
    cleaned: list[str] = []
    just_saw_speaker_tag = False
    for ln in lines:
        stripped = ln.strip()
        if not stripped:
            if not just_saw_speaker_tag:
                cleaned.append("")
            continue

        # Drop markdown chunk headers and separators.
        if stripped.startswith("# Chunk "):
            continue
        if stripped.startswith("Speakers:"):
            continue
        if stripped.startswith("Characters:"):
            continue
        if stripped == "---":
            continue

        # Convert speaker tags like **[RAMYA — voice: nova]** -> RAMYA:
        speaker_match = BRACKET_SPEAKER_RE.match(stripped)
        if speaker_match:
            # Do not speak speaker names; keep only a turn boundary.
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            just_saw_speaker_tag = True
            continue

        if PLAIN_SPEAKER_RE.match(stripped):
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            just_saw_speaker_tag = True
            continue

        # Remove remaining markdown emphasis markers.
        stripped = stripped.replace("**", "")
        # Pronunciation help for common proper name ambiguity.
        stripped = re.sub(r"\bSean\b", "Shawn", stripped)
        stripped = re.sub(r"\bSEAN\b", "SHAWN", stripped)
        cleaned.append(stripped)
        just_saw_speaker_tag = False

    # Normalize blank lines.
    normalized_lines: list[str] = []
    prev_blank = False
    for ln in cleaned:
        is_blank = not ln.strip()
        if is_blank and prev_blank:
            continue
        normalized_lines.append(ln)
        prev_blank = is_blank

    return "\n".join(normalized_lines).strip()


def _stitch_wav_parts(part_paths: list[Path], output_path: Path) -> None:
    if not part_paths:
        raise ValueError("No WAV parts provided.")

    with wave.open(str(part_paths[0]), "rb") as first:
        params = first.getparams()
        frames = [first.readframes(first.getnframes())]

    for part in part_paths[1:]:
        with wave.open(str(part), "rb") as wf:
            if wf.getparams()[:4] != params[:4]:
                raise RuntimeError("WAV parts have mismatched audio parameters.")
            frames.append(wf.readframes(wf.getnframes()))

    with wave.open(str(output_path), "wb") as out:
        out.setparams(params)
        for data in frames:
            out.writeframes(data)


def _stitch_with_ffmpeg(part_paths: list[Path], output_path: Path) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return False

    concat_file = output_path.with_suffix(".concat.txt")
    concat_lines = []
    for p in part_paths:
        escaped = str(p).replace("'", "'\\''")
        concat_lines.append(f"file '{escaped}'")
    concat_file.write_text("\n".join(concat_lines), encoding="utf-8")

    try:
        cmd = [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return False
        return True
    finally:
        if concat_file.exists():
            concat_file.unlink()


def _stitch_parts(part_paths: list[Path], output_path: Path, fmt: str) -> None:
    if not part_paths:
        raise ValueError("No audio parts to stitch.")

    if len(part_paths) == 1:
        shutil.move(str(part_paths[0]), str(output_path))
        return

    if _stitch_with_ffmpeg(part_paths, output_path):
        return

    # Fallbacks when ffmpeg is unavailable.
    if fmt == "wav":
        _stitch_wav_parts(part_paths, output_path)
        return

    if fmt in {"mp3", "aac", "opus", "pcm", "pcm16"}:
        with output_path.open("wb") as out:
            for part in part_paths:
                out.write(part.read_bytes())
        return

    raise RuntimeError(
        "Could not stitch parts without ffmpeg for this format. "
        "Install ffmpeg or use mp3/opus/wav."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate audio from a text file and save output to C:\\temp by default."
    )
    parser.add_argument("input_path", help="Full path to the input text/markdown/script file.")
    parser.add_argument(
        "--output-dir",
        default=r"C:\temp",
        help=r"Directory to save generated audio (default: C:\temp).",
    )
    parser.add_argument(
        "--format",
        default="opus",
        choices=sorted(SUPPORTED_FORMATS),
        help="Audio output format. Default is opus for quality/size balance.",
    )
    parser.add_argument("--voice", default="alloy", help="Voice name (default: alloy).")
    parser.add_argument(
        "--model",
        default="gpt-4o-mini-tts",
        help="Model name (default: gpt-4o-mini-tts).",
    )
    parser.add_argument(
        "--instructions",
        default=(
            "Read verbatim and do not summarize. "
            "Use a calm, natural, interview-style pace. "
            "Keep pacing consistent from start to finish and do not speed up near the end. "
            "For dialogue, make speaker turns clear with subtle tone shifts only. "
            "Never translate or switch language. Never invent, skip, or paraphrase content."
        ),
        help="Instruction prompt sent with the text.",
    )
    parser.add_argument(
        "--chunk-chars",
        type=int,
        default=1800,
        help="Maximum characters per generation chunk (default: 1800).",
    )
    parser.add_argument(
        "--max-completion-tokens",
        type=int,
        default=4000,
        help="Max completion tokens per chunk (default: 4000).",
    )
    args = parser.parse_args()

    input_path = Path(args.input_path).expanduser()
    if not input_path.exists() or not input_path.is_file():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    text = input_path.read_text(encoding="utf-8")
    if not text.strip():
        print(f"Input file is empty: {input_path}", file=sys.stderr)
        return 1
    text = _normalize_for_tts(text)
    if not text.strip():
        print("No readable script text remained after normalization.", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = _build_output_path(input_path, output_dir, args.format)
    base_prefix = output_path.with_suffix("")
    chunks = _split_text_for_tts(text, max_chars=args.chunk_chars)
    total = len(chunks)
    print(f"Input: {input_path}")
    print(f"Normalized chars: {len(text)}")
    print(f"Chunks to generate: {total}")
    print(f"Output target: {output_path}")

    client = OpenAI()
    response_format = _tts_response_format(args.format)

    if total == 1:
        response = client.audio.speech.create(
            model=args.model,
            voice=args.voice,
            input=text,
            instructions=(
                f"{args.instructions} "
                "Speak clear spoken English words only. "
                "Do not hum, sing, or produce non-speech sounds."
            ),
            response_format=response_format,
        )
        response.write_to_file(output_path)
        print(f"Saved: {output_path}")
        return 0

    part_paths: list[Path] = []
    for idx, chunk_text in enumerate(chunks, start=1):
        print(f"Generating chunk {idx}/{total}...")
        part_path = output_dir / f"{base_prefix.name}_part{idx:02d}.{args.format}"
        response = client.audio.speech.create(
            model=args.model,
            voice=args.voice,
            input=chunk_text,
            instructions=(
                f"{args.instructions} "
                "Read verbatim and do not summarize. "
                f"This is segment {idx} of {total}. "
                "Speak clear spoken English words only. "
                "Do not hum, sing, or produce non-speech sounds."
            ),
            response_format=response_format,
        )
        response.write_to_file(part_path)
        part_paths.append(part_path)
        print(f"Saved part {idx}/{total}: {part_path}")

    manifest_path = output_dir / f"{base_prefix.name}_parts.txt"
    m3u_path = output_dir / f"{base_prefix.name}.m3u8"
    manifest_path.write_text("\n".join(str(p) for p in part_paths), encoding="utf-8")
    m3u_path.write_text("\n".join(str(p) for p in part_paths), encoding="utf-8")
    print(f"Saved parts manifest: {manifest_path}")
    print(f"Saved playlist: {m3u_path}")

    _stitch_parts(part_paths=part_paths, output_path=output_path, fmt=args.format)
    print(f"Saved stitched file: {output_path}")

    recycle_root = Path(r"C:\temp\recycle")
    recycle_root.mkdir(parents=True, exist_ok=True)
    recycle_batch = recycle_root / output_path.stem
    recycle_batch.mkdir(parents=True, exist_ok=True)

    for p in part_paths:
        if p.exists():
            shutil.move(str(p), str(recycle_batch / p.name))
    for p in (manifest_path, m3u_path):
        if p.exists():
            shutil.move(str(p), str(recycle_batch / p.name))

    print(f"Moved parts to recycle folder: {recycle_batch}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
