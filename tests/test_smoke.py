from pathlib import Path

from typer.testing import CliRunner

from repo_builder import __version__
from repo_builder.cli import app
from repo_builder.config import Settings
from repo_builder.parser import parse_project_spec, slugify

runner = CliRunner()


def test_package_version() -> None:
    assert __version__ == "0.1.0"


def test_slugify() -> None:
    assert slugify("My Amazing App!") == "my-amazing-app"


def test_parse_project_spec_extracts_features() -> None:
    spec = parse_project_spec("Build a marketplace with login, M-Pesa payments and admin dashboard")
    assert spec.stack == "nextjs-fastapi"
    assert spec.slug
    assert "payments" in spec.features
    assert "admin dashboard" in spec.features
    assert "user authentication" in spec.features


def test_parse_rejects_empty_prompt() -> None:
    try:
        parse_project_spec("   ")
    except ValueError as exc:
        assert "cannot be empty" in str(exc)
    else:
        raise AssertionError("Expected empty prompt to be rejected")


def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "repo-builder 0.1.0" in result.stdout


def test_cli_parse_writes_json(tmp_path: Path) -> None:
    target = tmp_path / "specs" / "project.json"
    result = runner.invoke(app, ["parse", "Build a booking app", "--output", str(target)])
    assert result.exit_code == 0
    assert target.exists()
    assert '"stack": "nextjs-fastapi"' in target.read_text(encoding="utf-8")


def test_settings_defaults_without_dotenv(monkeypatch) -> None:
    for key in (
        "LLM_PROVIDER", "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "LLM_MODEL",
        "GITHUB_TOKEN", "GITHUB_OWNER", "GITHUB_PRIVATE", "VALIDATE_PYTHON", "VALIDATE_JS",
    ):
        monkeypatch.delenv(key, raising=False)
    settings = Settings.load(env_file=None)
    assert settings.llm_provider == "anthropic"
    assert settings.validate_python is True
    assert settings.validate_js is True
