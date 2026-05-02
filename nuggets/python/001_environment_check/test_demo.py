from demo import collect_environment_info


def test_collect_environment_info_has_expected_keys() -> None:
    info = collect_environment_info()
    expected_keys = {
        "python_version",
        "cwd",
        "script_directory",
        "output_directory",
        "output_dir_created",
    }

    assert expected_keys.issubset(info.keys())
