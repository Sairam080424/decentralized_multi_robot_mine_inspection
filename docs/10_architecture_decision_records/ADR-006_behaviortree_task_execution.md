# ADR-006: BehaviorTree.CPP for Task Execution and Nav2 Recoveries

- **Status**: PROPOSED / UNDER EVALUATION
- **Date**: 2026-11-18 (Updated: 2026-11-19)
- **Context**: Nav2 navigation and long-duration inspection actions require reactive decision-making, fallback recoveries, and clean preemption.
- **Decision**: Propose BehaviorTree.CPP v4 as the primary candidate framework for managing single-robot action execution pipelines and navigation recovery behaviors.
- **Evaluation Criteria & Alternatives**:
  - **Status**: Under active architectural evaluation; not a final binding decision.
  - **Alternatives Considered**: Hierarchical Finite State Machines (HFSM, e.g., Boost.SML or SMACH), Nav2 default XML trees without custom extensions, and hardcoded C++ state machines.
  - **Empirical Evaluation Plan (Milestone M3 & M5)**:
    - Evaluate tree reactivity and memory overhead during long navigation sorties.
    - Test Groot monitoring overhead and debugging fidelity over bandwidth-limited links.
    - Verify recovery behavior determinism during simulated subterranean wheel slippage and obstacle traps.
- **Consequences**:
  - Highly maintainable XML behavior trees decoupled from C++ action implementations.
  - Supports visual tree inspection and debugging via Groot.
  - Requires maintaining XML schemas and custom action plugin nodes.
  - Final decision will be locked after Milestone M3 simulation trials confirm operational stability.
