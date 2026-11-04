# Application Factory Delivery Roadmap

## Delivery strategy

Build a reliable modular CLI first, then expose the same services through an API and dashboard. Each sprint must deliver a testable increment.

| Sprint | Focus | Main deliverables | Exit criteria |
|---|---|---|---|
| 0 | Foundation audit | Existing package audit, architecture decision, engineering standards | Baseline documented; open foundation PR reviewed |
| 1 | Project specification | Typed ProjectSpec, parser normalization, schema/version tests | Valid and invalid specs tested |
| 2 | Template registry | Template metadata, discovery, validation, built-in template registration | Registry lists and validates templates |
| 3 | Scaffold planner | Deterministic file/node plan, safe path handling | Same input yields same plan; traversal rejected |
| 4 | Rendering engine | Jinja rendering, static files, generated manifest | Rendered fixture tests pass |
| 5 | Starter templates | Web/API starter template and smoke tests | One sample project generated end-to-end |
| 6 | Validation engine | Python/JS checks, command allowlist, isolated execution design | Validation reports structured results |
| 7 | AI planning adapter | Optional provider interface and structured output validation | Offline mode works; provider failure is handled |
| 8 | GitHub integration | Repository creation/push adapter and dry-run mode | No write without explicit confirmation |
| 9 | Build and packaging | Build manifests, reproducible archives | Build artifact validated |
| 10 | Deployment adapters | Staging deployment integration and approval gate | Staging deployment tested |
| 11 | Publication preparation | Android/web release checklist and metadata generation | Release readiness report produced |
| 12 | Control dashboard | API, job status, project inventory, audit trail | Dashboard uses existing application services |

## Sprint 0 tasks

- [x] Confirm hybrid architecture: central control plane plus modular engines.
- [x] Verify repository metadata and existing foundation branch.
- [x] Inspect open foundation pull request metadata and README scope.
- [x] Record architecture and phased roadmap.
- [ ] Review and merge the foundation pull request.
- [ ] Establish CI checks and contribution standards.
- [ ] Confirm Sprint 1 acceptance tests.

## Sprint execution rules

1. Work on a dedicated branch.
2. Keep changes within the sprint's scope.
3. Add or update tests with each feature.
4. Run the full test suite before opening a pull request.
5. Record commands and results; do not claim tests passed unless executed.
6. Keep generated artifacts and secrets out of source control.
7. Use pull requests for review; do not merge without an explicit release decision.

## Definition of Done

A sprint is complete only when:
- acceptance criteria are met;
- automated tests pass;
- documentation is updated;
- security implications are reviewed;
- changes are committed to a dedicated branch;
- a pull request is available for review.
