from pathlib import Path


def test_streamlit_files_exist() -> None:
    assert Path("app/streamlit/lifevault_help_console.py").exists()
    assert Path("app/streamlit/README.md").exists()
    assert Path("docker/streamlit_dashboard/Dockerfile").exists()
    assert Path("docker/streamlit_dashboard/docker-compose.yml").exists()
    assert Path("scripts/run_streamlit_help_console.ps1").exists()
    assert Path("scripts/start_streamlit_help_console_docker.ps1").exists()
    assert Path("scripts/stop_streamlit_help_console_docker.ps1").exists()
    assert Path("scripts/status_streamlit_help_console_docker.ps1").exists()
    assert Path("scripts/install_streamlit_help_console_startup_task.ps1").exists()
    assert Path("scripts/uninstall_streamlit_help_console_startup_task.ps1").exists()


def test_streamlit_required_sections_present() -> None:
    text = Path("app/streamlit/lifevault_help_console.py").read_text(encoding="utf-8")
    required = [
        "Home",
        "Current Capability Status",
        "Command Builder",
        "Notes Inventory",
        "Safety",
        "Next Tasks",
    ]
    for heading in required:
        assert heading in text


def test_streamlit_has_no_obvious_destructive_execution_strings() -> None:
    text = Path("app/streamlit/lifevault_help_console.py").read_text(encoding="utf-8").lower()
    forbidden = [
        "subprocess",
        "os.system",
        "invoke-expression",
        "powershell -command",
        "remove-item",
        "move-item",
        "rename-item",
        "rclone",
    ]
    for needle in forbidden:
        assert needle not in text


def test_streamlit_does_not_read_protected_lvenc_content() -> None:
    text = Path("app/streamlit/lifevault_help_console.py").read_text(encoding="utf-8").lower()
    assert "encrypted_body.lvenc\").read_text" not in text
    assert "encrypted_body.lvenc').read_text" not in text


def test_compose_has_port_and_restart_policy() -> None:
    text = Path("docker/streamlit_dashboard/docker-compose.yml").read_text(encoding="utf-8").lower()
    assert "8501:8501" in text
    assert "restart: unless-stopped" in text
    assert "lifevault-help-console" in text


def test_install_script_has_expected_task_name() -> None:
    text = Path("scripts/install_streamlit_help_console_startup_task.ps1").read_text(encoding="utf-8")
    assert "LifeVault Streamlit Help Console" in text
