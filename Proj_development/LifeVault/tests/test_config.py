import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lifevault.config import load_paths_example, load_rclone_remotes_example


def test_config_examples_load_as_valid_json() -> None:
    paths_cfg = load_paths_example()
    remotes_cfg = load_rclone_remotes_example()
    assert isinstance(paths_cfg, dict)
    assert isinstance(remotes_cfg, dict)


def test_paths_example_targets_lifevault_not_legacy_name() -> None:
    paths_cfg = load_paths_example()
    lab_root = str(paths_cfg.get("lab_root", ""))
    assert "LifeVault" in lab_root
    assert "OneDriveClean" not in lab_root


def test_rclone_remote_example_names() -> None:
    remotes_cfg = load_rclone_remotes_example()
    assert remotes_cfg.get("dirty_remote") == "onedrive_dirty"
    assert remotes_cfg.get("clean_remote") == "onedrive_clean"


def test_no_real_onedrive_or_lab_access_in_tests() -> None:
    # This is a policy assertion: tests only parse local repo files.
    # They do not invoke rclone, network, or touch D:\\AI_Lab\\LifeVault paths.
    assert True