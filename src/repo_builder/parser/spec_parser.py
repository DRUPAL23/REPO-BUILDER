"""Convert a natural-language brief into a validated baseline project spec.

This deterministic parser establishes a stable input contract. LLM-assisted
requirement extraction is added by the provider/generator stages later.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from repo_builder.models import ProjectSpec

_FEATURE_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("user authentication", ("auth", "authentication", "login", "sign up", "signup")),
    ("admin dashboard", ("admin", "dashboard", "back office")),
    ("payments", ("payment", "checkout", "billing", "mpesa", "m-pesa")),
    ("search", ("search", "filter")),
    ("notifications", ("notification", "email alert", "sms alert")),
    ("analytics", ("analytics", "reports", "reporting", "metrics")),
    ("file uploads", ("upload", "file attachment", "media library")),
    ("API integration", ("api", "integration", "webhook")),
)


def slugify(value: str) -> str:
    """Return a filesystem- and URL-friendly slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:80].strip("-") or "generated-project"


def parse_project_spec(
    prompt: str,
    *,
    name: str | None = None,
    stack: str = "nextjs-fastapi",
    requirements: Sequence[str] | None = None,
) -> ProjectSpec:
    """Create a baseline ProjectSpec from a user's natural-language prompt."""
    brief = prompt.strip()
    if not brief:
        raise ValueError("Project prompt cannot be empty")
    if stack != "nextjs-fastapi":
        raise ValueError("Only the 'nextjs-fastapi' stack is supported")

    project_name = (name or _infer_name(brief)).strip()
    features = [label for label, keywords in _FEATURE_KEYWORDS if any(k in brief.lower() for k in keywords)]
    normalized_requirements = list(requirements or [])
    return ProjectSpec(
        name=project_name,
        slug=slugify(project_name),
        description=brief,
        stack="nextjs-fastapi",
        requirements=normalized_requirements,
        features=features,
    )


def _infer_name(prompt: str) -> str:
    """Infer a concise project label from the opening words of a brief."""
    cleaned = re.sub(r"\s+", " ", prompt).strip(" .!?\n\t")
    cleaned = re.sub(r"^(please\s+)?(build|create|develop|make|generate)\s+", "", cleaned, flags=re.I)
    first_clause = re.split(r"[.!?;\n]", cleaned, maxsplit=1)[0]
    first_clause = re.split(r"\s+(?:with|for|that|which|including|featuring)\s+", first_clause, maxsplit=1, flags=re.I)[0]
    words = first_clause.split()[:6]
    candidate = " ".join(words).strip(" ,:-")
    return candidate[:1].upper() + candidate[1:] if candidate else "Generated Project"
