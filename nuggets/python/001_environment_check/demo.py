from __future__ import annotations

from pathlib import Path
import os
import sys


def collect_environment_info(output_folder_name: str = "output") -> dict[str, str | bool]:
    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / output_folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    return {
        "python_version": sys.version.split()[0],
        "cwd": str(Path(os.getcwd()).resolve()),
        "script_directory": str(script_dir),
        "output_directory": str(output_dir),
        "output_dir_created": output_dir.exists() and output_dir.is_dir(),
    }


def main() -> None:
    info = collect_environment_info()
    print(f"Python version: {info['python_version']}")
    print(f"Current working directory: {info['cwd']}")
    print(f"Script directory: {info['script_directory']}")
    print(f"Output directory: {info['output_directory']}")
    print(f"Output directory created: {info['output_dir_created']}")


if __name__ == "__main__":
    main()
