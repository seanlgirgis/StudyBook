from pathlib import Path

from onedriveclean.config import load_config


def test_load_config_prefers_local(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    (config_dir / "paths.example.json").write_text('{"lab_root":"X:/example","onboarding_dir":"onboarding","pods_dir":"onboarding/pods","staging_dir":"staging","db_dir":"db","inventory_dir":"inventory","hydrated_dir":"hydrated","reports_dir":"reports","logs_dir":"logs"}', encoding="utf-8")
    (config_dir / "paths.local.json").write_text('{"lab_root":"X:/local","onboarding_dir":"onboarding","pods_dir":"onboarding/pods","staging_dir":"staging","db_dir":"db","inventory_dir":"inventory","hydrated_dir":"hydrated","reports_dir":"reports","logs_dir":"logs"}', encoding="utf-8")
    (config_dir / "rclone_remotes.example.json").write_text('{"dirty_remote":"d_ex","clean_remote":"c_ex","excluded_remote_paths":["Personal Vault/**"]}', encoding="utf-8")
    (config_dir / "rclone_remotes.local.json").write_text('{"dirty_remote":"d_loc","clean_remote":"c_loc","excluded_remote_paths":["Personal Vault/**","Tmp/**"]}', encoding="utf-8")
    (config_dir / "batches.example.json").write_text('{"batches":{"b1":{"remote_path":"Downloads"}}}', encoding="utf-8")
    (config_dir / "batches.local.json").write_text('{"batches":{"b1":{"remote_path":"Docs"}}}', encoding="utf-8")
    (config_dir / "local_sources.example.json").write_text('{"sources":{"downloads":{"path":"X:/Downloads"}}}', encoding="utf-8")
    (config_dir / "local_sources.local.json").write_text('{"sources":{"downloads":{"path":"X:/DownloadsLocal"}}}', encoding="utf-8")
    (config_dir / "staging_batches.example.json").write_text('{"batches":{"s1":{"source_name":"downloads"}}}', encoding="utf-8")
    (config_dir / "staging_batches.local.json").write_text('{"batches":{"s1":{"source_name":"downloads","project":"P"}}}', encoding="utf-8")

    cfg = load_config(tmp_path)
    assert str(cfg.lab_root).startswith("X:")
    assert cfg.lab_path("pods_dir")
    assert cfg.dirty_remote == "d_loc"
    assert cfg.excluded_remote_paths == ["Personal Vault/**", "Tmp/**"]
