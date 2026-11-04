# ADR-0001: Adopt a Hybrid Modular Application Factory

- **Status:** Accepted
- **Date:** 2026-11-04
- **Decision owner:** Project owner
- **Context:** The project needs one coordinated development platform without coupling all capabilities into one large codebase or requiring distributed services too early.

## Decision

Adopt a hybrid architecture consisting of:
1. A central control plane for project lifecycle and orchestration.
2. Independently testable engines with stable contracts.
3. Adapters for external providers and infrastructure.
4. A CLI as the first client.
5. A future API/dashboard that reuses the same application services.

Start as a modular monolith. Extract engines into separate processes or services only when scaling, isolation, or deployment requirements justify it.

## Consequences

### Positive
- Centralized project management.
- Clear separation of responsibilities.
- Engines can be tested and upgraded independently.
- Avoids premature microservice complexity.
- Supports future web and mobile clients.

### Trade-offs
- Requires discipline around module boundaries.
- Contracts and version compatibility need maintenance.
- A single deployment initially limits independent scaling.

## Alternatives considered

- **Single tightly coupled application:** simplest initially, but risks entangling generation, validation, deployment, and publication.
- **Microservices from day one:** offers independent deployment but adds operational overhead before demand exists.
- **Independent standalone tools only:** modular, but weakens orchestration and shared project state.

## Revisit when

Reassess if remote concurrent jobs, independent scaling, stronger execution isolation, or multiple teams require separate engine deployment.
