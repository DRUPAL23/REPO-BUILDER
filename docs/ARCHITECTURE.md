# Universal Application Factory Architecture

**Status:** Proposed baseline  
**Architecture decision:** Hybrid modular platform  
**Repository:** REPO-BUILDER

## 1. Purpose

Evolve the existing CLI-first repository builder into a modular application factory. A central control plane will coordinate independently testable engines. Engines will expose stable contracts and may later run in-process, as CLI workers, or as remote services.

The first release remains a Python CLI. A web management dashboard is a later client of the same application services; it is not a prerequisite for the core generator.

## 2. Architectural principles

1. Modular monolith first: keep deployment and operations simple while enforcing module boundaries.
2. Contracts before implementations: define typed inputs, outputs, errors, and capability metadata.
3. Deterministic generation: identical specifications and template versions should produce identical output, excluding explicitly generated metadata.
4. Safe-by-default: never execute generated code automatically; never expose secrets in logs or generated frontend bundles.
5. Provider independence: AI providers, Git hosts, build tools, and deployment targets are adapters.
6. Testability: each engine must be testable without network access.
7. Extensibility: new platforms and templates should be added through registries, not changes to orchestration logic.
8. Human approval gates: publishing, production deployment, destructive actions, and paid external services require explicit approval.

## 3. High-level architecture

```text
                 CLI / Future Web Dashboard
                            |
                     Application API
                            |
                    Workflow Orchestrator
                            |
      +-----------+---------+---------+-----------+
      |           |         |         |           |
  Project      Template  Generation  Validation  Integrations
  Planner      Registry   Engine      Engine      Manager
      |           |         |         |           |
      +-----------+---------+---------+-----------+
                            |
                      Artifact Store
                            |
              Git / Build / Deploy Adapters
                            |
                 External providers/services
```

## 4. Control plane and engines

### Control plane

Owns project lifecycle, configuration, workflow state, job coordination, policy checks, audit events, and user-facing commands.

### Engines

- **Planning Engine:** normalizes a brief into a validated ProjectSpec and implementation plan.
- **Template Engine:** discovers templates and validates template metadata.
- **Generation Engine:** renders deterministic files from a ProjectSpec and selected template.
- **Validation Engine:** runs static checks, tests, and build commands in an isolated workspace.
- **Integration Manager:** coordinates optional AI, GitHub, payment, storage, and notification adapters.
- **Build Engine:** creates reproducible development or release artifacts.
- **Deployment Engine:** deploys to configured targets only after approval.
- **Publication Manager:** prepares store metadata and release packages; store submission remains an explicit user-controlled step initially.

## 5. Suggested package boundaries

```text
src/repo_builder/
  api/                 # application-facing service interfaces
  core/                # shared types, errors, settings, policies
  planning/            # brief parsing and project plans
  registry/            # template and engine registries
  generation/          # scaffold planning and rendering
  validation/          # validators and test orchestration
  integrations/
    llm/
    github/
    payments/
    storage/
  build/               # local/cloud build adapters
  deployment/          # deployment adapters and approvals
  publication/         # store metadata and release checks
  cli/                 # Typer commands
  templates/            # versioned starter templates
tests/
  unit/
  integration/
  contract/
  fixtures/
docs/
```

This is a target structure, not an instruction to move existing files immediately. Refactoring will happen incrementally with compatibility tests.

## 6. Core contracts

### ProjectSpec

A validated, serializable description of an application. It should include:
- project name and slug
- description and target audience
- application type: web, mobile, API, SaaS, or hybrid
- platforms and supported deployment targets
- selected stack and template identifier/version
- features and integrations
- non-functional requirements
- constraints and generation options

### Engine contract

Each engine should expose:
- stable engine identifier and version
- supported capabilities
- input schema
- output/artifact references
- structured errors
- health/readiness information where applicable

### Artifact

Every generated file or package should record:
- relative path
- content or storage reference
- content hash
- generator and template versions
- originating project specification hash
- validation status

## 7. Workflow lifecycle

```text
BRIEF
  -> PLAN
  -> REVIEW PLAN
  -> SELECT TEMPLATE
  -> GENERATE
  -> VALIDATE
  -> REVIEW ARTIFACTS
  -> PACKAGE
  -> PUBLISH / DEPLOY (approval required)
  -> MONITOR
```

A failed stage must preserve diagnostics and must not silently advance the workflow.

## 8. Data and persistence

For the initial CLI, project specifications and run manifests may be stored as JSON files in the workspace. Avoid introducing a database before concurrent users or remote job execution require one.

When a management API is introduced, use PostgreSQL for durable project/job metadata and object storage for large artifacts. Do not store secrets in project manifests.

## 9. Security boundaries

- Validate and normalize all generated paths; reject traversal and absolute paths.
- Render only within a designated workspace.
- Never run generated scripts by default.
- If execution is enabled later, use an isolated container or sandbox with resource limits, no privileged access, and restricted network access.
- Keep credentials in environment variables or a secret manager.
- Redact secrets from logs and diagnostics.
- Pin and audit dependencies for release builds.
- Require approval before external publication, deployment, payments, or destructive operations.

## 10. Quality attributes and initial targets

These are initial engineering targets to validate, not current measured performance:
- CLI startup should remain lightweight.
- Generation should be deterministic for a fixed template and specification.
- Unit tests should run offline.
- Every built-in template should have a smoke test.
- Errors should identify the failing stage and actionable cause.
- A failed generation must not leave a partially written final project; generate into a temporary directory and atomically finalize.

## 11. Deployment evolution

**Phase 1:** Python CLI, local filesystem workspace, deterministic templates.  
**Phase 2:** Optional AI planning adapter and GitHub repository adapter.  
**Phase 3:** Validation/build workers with isolated execution.  
**Phase 4:** API and web dashboard; PostgreSQL and object storage.  
**Phase 5:** deployment and publication adapters with approval workflows.

## 12. Out of scope for the first implementation

- Autonomous production deployment.
- Automatic app-store submission.
- Arbitrary generated-code execution on the host.
- Multi-tenant hosted service.
- Billing and subscription management.
- Kubernetes orchestration.

These capabilities require separate threat modelling, operational design, and product validation.
