"""Pydantic models shared by the repository builder pipeline."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectSpec(BaseModel):
    """Normalized description of a project to be generated."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=80)
    slug: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=2000)
    stack: Literal["nextjs-fastapi"] = "nextjs-fastapi"
    requirements: list[str] = Field(default_factory=list)
    features: list[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Project name cannot be blank")
        return value

    @field_validator("slug")
    @classmethod
    def valid_slug(cls, value: str) -> str:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
            raise ValueError("Slug must contain lowercase letters, numbers, and single hyphens")
        return value

    @field_validator("requirements", "features")
    @classmethod
    def clean_list_items(cls, values: list[str]) -> list[str]:
        cleaned = [item.strip() for item in values if item and item.strip()]
        return list(dict.fromkeys(cleaned))


class BuildResult(BaseModel):
    """Summary returned by a completed local build operation."""

    project_name: str
    output_path: str
    files_created: int = 0
    validation_passed: bool = False
