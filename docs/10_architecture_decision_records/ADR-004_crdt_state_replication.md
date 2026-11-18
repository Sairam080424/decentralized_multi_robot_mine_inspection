# ADR-004: CRDT State Synchronization via Causal Vector Clocks

- **Status**: ACCEPTED
- **Date**: 2026-11-18
- **Context**: Network partitions cause robots to update task states independently. Consensus protocols requiring continuous quorums (e.g. Raft) stall when partitioned.
- **Decision**: Deploy state-based and delta-based Conflict-Free Replicated Data Types (LWW-Element-Set and OR-Set) paired with causal vector clocks.
- **Consequences**:
  - High availability: Robots continue execution during total disconnection.
  - Mathematical convergence: Rejoining radio range triggers automated delta reconciliation without split-brain locks.
