# repo-builder

A CLI-first foundation for a universal repository builder. This verified archive provides project-brief parsing, a validated Pydantic project specification, environment configuration, and a Typer CLI.

> **Current scope:** this branch contains the Sprint 0/1 foundation only. It does not yet generate application source trees, call LLM providers, or publish repositories to GitHub. Those capabilities are planned for subsequent milestones.

## Requirements

- Python 3.10+
- Dependencies listed in `pyproject.toml`

## Install

```bash
python -m pip install -e ".[dev]"
cp .env.example .env
```

## CLI

```bash
repo-builder --help
repo-builder version
repo-builder config
repo-builder parse "Build a marketplace with user login, M-Pesa payments and an admin dashboard" --output ./marketplace-spec.json
```

You can also run the CLI without installing the console script:

```bash
PYTHONPATH=src python -m repo_builder --help
```

## Foundation capabilities

- Parses a natural-language project brief into a normalized project specification.
- Infers a project name and URL/filesystem-safe slug.
- Extracts baseline feature tags such as authentication, payments, search, and analytics.
- Validates the specification with Pydantic.
- Loads configuration from environment variables and an optional `.env` file.
- Displays configuration status without printing secret values.

## Supported stack identifier

- `nextjs-fastapi` (specification metadata only; source scaffolding is not included in this branch).

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `LLM_PROVIDER` | Provider selection: `anthropic` or `openai` | `anthropic` |
| `ANTHROPIC_API_KEY` | Anthropic credential | Unset |
| `OPENAI_API_KEY` | OpenAI credential | Unset |
| `LLM_MODEL` | Provider-specific model identifier | `claude-3-5-sonnet-latest` |
| `GITHUB_TOKEN` | Reserved for future GitHub publishing | Unset |
| `GITHUB_OWNER` | Default GitHub owner for future publishing | Unset |
| `GITHUB_PRIVATE` | Future repository visibility default | `false` |
| `VALIDATE_PYTHON` | Python validation preference | `true` |
| `VALIDATE_JS` | JavaScript validation preference | `true` |

Never commit a populated `.env` file or API credentials.

## Tests

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

The included smoke suite currently covers package version, slug generation, deterministic feature extraction, empty-prompt rejection, CLI output, and configuration defaults.

## Project layout

```text
src/repo_builder/
  __init__.py
  __main__.py
  cli.py
  config.py
  models.py
  parser/
    __init__.py
    spec_parser.py
tests/
  __init__.py
  test_smoke.py
```

## Roadmap

1. AI provider abstraction and structured project planning.
2. Template registry and deterministic source-file scaffolding.
3. Validation pipeline and local build orchestration.
4. GitHub repository creation and publishing.
