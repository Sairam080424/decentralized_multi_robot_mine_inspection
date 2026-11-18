# Architecture Decision Records (ADRs)

This directory records all significant architectural and engineering decisions made throughout the lifecycle of the Decentralized Multi-Robot Mine Inspection Platform.

In accordance with Phase 0 review standards, architectural candidates for middleware, task allocation, state replication, safety arbitration, and execution frameworks remain **UNDER EVALUATION** until empirically validated through milestone testing.

## Index of Decisions

| ADR | Title | Status | Evaluation Milestone |
|---|---|---|---|
| [ADR-001](ADR-001_three_layer_architecture.md) | Three-Layer Decoupled Architecture | **ACCEPTED** | Foundation (M0) |
| [ADR-002](ADR-002_contract_net_protocol.md) | Distributed Contract Net Protocol (CNP) for Task Allocation | **UNDER EVALUATION** | Milestone M8 |
| [ADR-003](ADR-003_eclipse_zenoh_p2p_mesh.md) | Eclipse Zenoh for Distributed P2P Mesh Communication | **UNDER EVALUATION** | Milestone M4 / M7 |
| [ADR-004](ADR-004_crdt_state_replication.md) | CRDT State Synchronization via Causal Vector Clocks | **UNDER EVALUATION** | Milestone M6 / M8 |
| [ADR-005](ADR-005_local_safety_autarchy.md) | Authoritative Local Safety Autarchy in Layer 1 | **UNDER EVALUATION** | Milestone M3 / M5 |
| [ADR-006](ADR-006_behaviortree_task_execution.md) | BehaviorTree.CPP for Task Execution and Nav2 Recoveries | **UNDER EVALUATION** | Milestone M3 / M5 |
