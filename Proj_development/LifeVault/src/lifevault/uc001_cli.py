from __future__ import annotations

import argparse
from pathlib import Path

from .uc001_proposal import build_folder_proposal, write_proposal_package


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="UC_001 Ingest Folder Proposal (metadata-only)")
    parser.add_argument("--source-path", required=True)
    parser.add_argument("--story", default=None)
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--max-preview-files", type=int, default=200)
    args = parser.parse_args(argv)

    proposal = build_folder_proposal(
        source_path=args.source_path,
        story=args.story,
        output_root=args.output_root,
        max_preview_files=args.max_preview_files,
    )

    output_root = Path(args.output_root) if args.output_root else Path(proposal["output_root"])
    output_dir = output_root / proposal["proposal_id"]
    write_proposal_package(proposal, output_dir)

    print(f"UC_001 proposal package created: {output_dir}")
    print(f"scan_status={proposal['scan_status']}")
    print(f"recommended_next_action={proposal['recommended_next_action']}")
    if proposal["errors"]:
        print(f"errors={proposal['errors']}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())