# Module 2.6: Distributed State Management

## 1. Module Overview
Module 2.6 provides partition-tolerant mission state replication, Conflict-Free Replicated Data Types (CRDTs), causal vector clocks, concurrent conflict detection, and automated delta reconciliation across intermittent subterranean radio links.

## 2. Submodule Index
- [2.6.1 Local Mission State](local_mission_state.md): Embedded local replicated key-value state store running on each robot.
- [2.6.2 State Replication](state_replication.md): Gossip-based anti-entropy replication protocol exchanging state deltas.
- [2.6.3 Version Management](version_management.md): Causal vector clocks and Lamport timestamps tracking mutation history.
- [2.6.4 Conflict Detection](conflict_detection.md): Concurrent mutation detection, LWW-Element-Set, and OR-Set resolution.
- [2.6.5 Reconnection and Reconciliation](reconnection_reconciliation.md): Automated state merging when partitioned robots re-establish radio contact.
