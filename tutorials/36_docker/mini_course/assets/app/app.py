#!/usr/bin/env python3
"""Tiny Docker mini-course pipeline: read lines from /data/sample.txt and write /data/output.txt."""

import pathlib


def main() -> None:
    input_path = pathlib.Path("/data/sample.txt")
    output_path = pathlib.Path("/data/output.txt")

    input_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print("Creating sample input at /data/sample.txt")
        input_path.write_text("hello\ndocker\npipeline\n", encoding="utf-8")

    lines = input_path.read_text(encoding="utf-8").splitlines()
    output_path.write_text(f"Line count: {len(lines)}\n", encoding="utf-8")

    print(f"Processed {len(lines)} lines -> {output_path}")


if __name__ == "__main__":
    main()
