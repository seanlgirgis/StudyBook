from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.db import smoke_test


if __name__ == "__main__":
    df = smoke_test()
    print("=== Smoke Test ===")
    print(df.to_string(index=False))
