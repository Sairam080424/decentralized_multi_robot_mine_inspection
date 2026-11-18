# ADR-001: Three-Layer Decoupled Architecture

- **Status**: ACCEPTED
- **Date**: 2026-11-18
- **Context**: Autonomous mine inspection requires coordinating physical robotics, distributed multi-agent negotiation, and surface human observability without architectural entanglement.
- **Decision**: Establish a strict three-layer architecture:
  1. Layer 1: Robot and Environment Layer (Physical/simulated robotics, Nav2, SLAM, local safety).
  2. Layer 2: Distributed Autonomy Layer (P2P mesh, discovery, CNP task allocation, CRDT state).
  3. Layer 3: Mission and Operations Layer (Surface planning, telemetry dashboard, database, ERP).
- **Consequences**:
  - Downward-only dependencies: Layer 3 &rarr; Layer 2 &rarr; Layer 1.
  - Zero direct actuation commands from Layer 3 to Layer 1 motors.
  - Enables independent developer workflows on separate layers.
