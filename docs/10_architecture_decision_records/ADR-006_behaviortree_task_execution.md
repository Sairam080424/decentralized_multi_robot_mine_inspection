# ADR-006: BehaviorTree.CPP for Task Execution and Nav2 Recoveries

- **Status**: ACCEPTED
- **Date**: 2026-11-18
- **Context**: Nav2 navigation and long-duration inspection actions require reactive decision-making, fallback recoveries, and clean preemption.
- **Decision**: Deploy BehaviorTree.CPP v4 for managing single-robot action execution pipelines and navigation recovery behaviors.
- **Consequences**:
  - Highly maintainable XML behavior trees decoupled from C++ action implementations.
  - Supports visual tree inspection and debugging via Groot.
