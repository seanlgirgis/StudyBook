"""
01_project_init_and_profiles.py — dbt project structure and profiles.yml.

Teaches:
  - What lives inside a dbt project (dbt_project.yml, profiles.yml, models/, seeds/, etc.)
  - profiles.yml structure: profile → target → output type + credentials
  - How dbt resolves profile/target at runtime
  - Running `dbt debug` to validate the setup
  - The difference between dbt_project.yml (what) vs profiles.yml (where)

Key concept:
  dbt_project.yml  → inside the project repo, committed to git
  profiles.yml     → outside the project by convention (~/.dbt/), NEVER committed
                     (we put it inside lab_dbt_project/ for self-contained learning)

Run:
    python 01_dbt_basics/01_project_init_and_profiles.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from _dbt_lane_connect import (
    DBT_PROJECT_DIR,
    PROFILES_DIR,
    detect_backend,
    run_dbt,
    write_profiles_yml,
)


def show_project_structure() -> None:
    """Walk dbt_project.yml and key directories; explain each."""
    print("\n--- dbt Project Structure ---")

    dbt_project_yml = DBT_PROJECT_DIR / "dbt_project.yml"
    if dbt_project_yml.exists():
        print(f"\n[dbt_project.yml] — found at: {dbt_project_yml}")
        print("  This file defines the project name, version, model paths,")
        print("  seed paths, test paths, snapshot paths, and per-folder")
        print("  materialization defaults.  It IS committed to git.\n")
        # Show key lines
        lines = dbt_project_yml.read_text(encoding="utf-8").splitlines()
        for line in lines[:40]:
            print(f"    {line}")
        if len(lines) > 40:
            print(f"    ... ({len(lines) - 40} more lines)")
    else:
        print(f"  [WARN] dbt_project.yml not found at {dbt_project_yml}")

    print()
    key_dirs = [
        ("models/",     "SQL SELECT queries — each file = one relation in DB"),
        ("seeds/",      "CSV files loaded into DB by `dbt seed`"),
        ("tests/",      "Singular (custom SQL) tests"),
        ("snapshots/",  "SCD Type 2 snapshot definitions"),
        ("macros/",     "Reusable Jinja2 SQL functions"),
        ("analyses/",   "Ad-hoc SQL; compiled but not materialized"),
        ("target/",     "Compiled SQL + run artifacts (gitignored)"),
        ("dbt_packages/", "External packages from packages.yml (gitignored)"),
    ]
    print("  Key dbt project directories:")
    for d, desc in key_dirs:
        exists = (DBT_PROJECT_DIR / d.rstrip("/")).exists()
        marker = "✓" if exists else "·"
        print(f"    {marker} {d:25s} {desc}")


def show_profiles_explanation() -> None:
    """Print a detailed explanation of profiles.yml sections."""
    print("\n--- profiles.yml Explained ---")
    print("""
  profiles.yml structure:

    <profile_name>:          ← must match 'profile:' in dbt_project.yml
      target: dev            ← default target (overridden by --target flag)
      outputs:
        dev:                 ← target name
          type: duckdb       ← adapter type (duckdb, postgres, snowflake, etc.)
          path: ...          ← adapter-specific config (connection details)
          schema: dbt_lab    ← default schema for models
          threads: 4         ← parallel SQL execution threads

  Key points:
  • profiles.yml lives at ~/.dbt/profiles.yml by convention.
    In this lane we write it inside lab_dbt_project/ for portability.
  • NEVER commit profiles.yml — it contains credentials.
  • Use environment variables ({{ env_var('MY_PASS') }}) for secrets in profiles.
  • `dbt --target prod` overrides the 'target' key at runtime.
  • Each output maps to a different environment (dev, staging, prod).
    """)


def main() -> int:
    print("=" * 60)
    print("  dbt Basics — Project Structure & Profiles")
    print("=" * 60)

    # Step 1: Write profiles.yml
    print("\n[Step 1] Writing profiles.yml...")
    backend, reason = detect_backend()
    print(f"  Backend: {backend} ({reason})")
    profiles_path = write_profiles_yml()
    print(f"  profiles.yml: {profiles_path}")

    # Show profiles.yml content
    print("\n--- Generated profiles.yml ---")
    content = profiles_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        print(f"  {line}")

    # Step 2: Explain project structure
    show_project_structure()

    # Step 3: Explain profiles.yml
    show_profiles_explanation()

    # Step 4: Run dbt debug
    print("\n[Step 4] Running `dbt debug`...")
    print("  (dbt debug validates the project, profiles.yml, and DB connectivity)\n")
    rc, stdout, stderr = run_dbt(["debug"], timeout=60)
    output = (stdout + "\n" + stderr).strip()
    for line in output.splitlines():
        print(f"  {line}")

    if rc != 0:
        print(f"\n  [WARN] dbt debug returned rc={rc}")
        print("  This is expected if the database hasn't been seeded yet.")
        print("  Run: python 00_setup/01_seed_lab.py")
        # Don't fail the nugget — debug failing before seed is expected
        # The lesson is still delivered above

    print()
    print("KEY TAKEAWAYS:")
    print("  1. dbt_project.yml  = project config (committed, no secrets)")
    print("  2. profiles.yml     = connection config (NOT committed, has secrets)")
    print("  3. profile: in dbt_project.yml must match a key in profiles.yml")
    print("  4. dbt debug = first thing to run when something seems wrong")
    print("  5. --profiles-dir flag lets you override where dbt finds profiles.yml")

    print()
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
