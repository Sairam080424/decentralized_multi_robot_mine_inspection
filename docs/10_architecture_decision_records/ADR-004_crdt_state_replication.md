# ADR-004: CRDT State Synchronization via Causal Vector Clocks

- **Status**: PROPOSED / UNDER EVALUATION
- **Date**: 2026-11-18 (Updated: 2026-11-19)
- **Context**: Network partitions cause robots to update task states independently. Consensus protocols requiring continuous quorums (e.g. Raft) stall when partitioned.
- **Decision**: Propose state-based and delta-based Conflict-Free Replicated Data Types (specifically LWW-Element-Set and OR-Set) paired with causal vector clocks for distributed mission state replication.
- **Evaluation Criteria & Alternatives**:
  - **Status**: Under active architectural evaluation; not a final binding decision.
  - **Alternatives Considered**: Quorum consensus (Raft/Paxos), periodic anti-entropy hash-tree exchange (Merkle trees), and primary-replica lease synchronization.
  - **Empirical Evaluation Plan (Milestone M6 & M8)**:
    - Measure state convergence latency ($< 1.0\text{ s}$ target) upon RF partition merger.
    - Profile memory growth and tombstone garbage collection overhead in long-duration subterranean missions.
    - Verify deterministic conflict resolution with zero split-brain data corruption.
- **Consequences**:
  - High availability: Robots continue execution during total disconnection.
  - Mathematical convergence: Rejoining radio range triggers automated delta reconciliation without split-brain locks.
  - Requires tombstone pruning mechanism to prevent unbounded memory growth over extended sorties.
  - Final architectural commitment reserved until empirical state synchronization benchmarks complete in Milestone M6.
