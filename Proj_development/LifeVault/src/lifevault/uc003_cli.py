from __future__ import annotations

import argparse

from .uc003_pod import create_onboarding_pod


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="UC_003 Create Onboarding Pod")
    parser.add_argument("--proposal-path", required=True)
    parser.add_argument("--approved", action="store_true")
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--approved-pod-name", default=None)
    args = parser.parse_args(argv)

    try:
        result = create_onboarding_pod(
            proposal_path=args.proposal_path,
            approved=args.approved,
            output_root=args.output_root,
            approved_pod_name=args.approved_pod_name,
        )
    except Exception as exc:
        print(f"UC_003 failed: {exc}")
        return 2

    print(f"UC_003 pod created: {result['pod_dir']}")
    print(f"pod_id={result['pod_id']}")
    print(f"pod_status={result['pod_status']}")
    print(f"file_count={result['file_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())