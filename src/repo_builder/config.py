"""Application configuration loaded from environment variables and .env."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr, field_validator


class Settings(BaseModel):
    """Validated runtime settings for repo-builder."""

    llm_provider: Literal["anthropic", "openai"] = "anthropic"
    anthropic_api_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None
    llm_model: str = "claude-3-5-sonnet-latest"
    github_token: SecretStr | None = None
    github_owner: str | None = None
    github_private: bool = False
    validate_python: bool = True
    validate_js: bool = True

    @field_validator("llm_model")
    @classmethod
    def model_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("LLM_MODEL cannot be empty")
        return value

    @classmethod
    def load(cls, env_file: str | Path | None = ".env") -> "Settings":
        """Load settings, optionally reading a dotenv file first."""
        if env_file is not None:
            load_dotenv(dotenv_path=Path(env_file), override=False)
        return cls(
            llm_provider=os.getenv("LLM_PROVIDER", "anthropic").strip().lower(),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY") or None,
            openai_api_key=os.getenv("OPENAI_API_KEY") or None,
            llm_model=os.getenv("LLM_MODEL", "claude-3-5-sonnet-latest"),
            github_token=os.getenv("GITHUB_TOKEN") or None,
            github_owner=os.getenv("GITHUB_OWNER") or None,
            github_private=_env_bool("GITHUB_PRIVATE", False),
            validate_python=_env_bool("VALIDATE_PYTHON", True),
            validate_js=_env_bool("VALIDATE_JS", True),
        )

    def has_llm_credentials(self) -> bool:
        if self.llm_provider == "anthropic":
            return bool(self.anthropic_api_key and self.anthropic_api_key.get_secret_value())
        return bool(self.openai_api_key and self.openai_api_key.get_secret_value())


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value (true/false)")
