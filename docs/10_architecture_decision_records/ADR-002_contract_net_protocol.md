# ADR-002: Distributed Contract Net Protocol (CNP) for Task Allocation

- **Status**: PROPOSED / UNDER EVALUATION
- **Date**: 2026-11-18 (Updated: 2026-11-19)
- **Context**: Subterranean radio frequency attenuation and line-of-sight tunnel corners prevent relying on a permanent central task dispatcher.
- **Decision**: Propose an ad-hoc Contract Net Protocol (CNP) baseline where tasks are broadcast to candidate peers and awarded to the lowest-cost capable bidder using multi-factor cost functions ($D_{travel}, E_{battery}, T_{risk}, C_{fit}$).
- **Evaluation Criteria & Alternatives**:
  - **Status**: Under active architectural evaluation; not a final binding decision.
  - **Alternatives Considered**: Consensus-Based Bundle Algorithm (CBBA), distributed constraint optimization (DCOP), and centralized master dispatchers with failover.
  - **Empirical Evaluation Plan (Milestone M8)**:
    - Benchmark message scaling ($O(N)$ vs $O(N^2)$) under lossy RF mesh (10% to 50% packet drops).
    - Measure clearance latency ($< 500\text{ ms}$ target) across 2 to 10 heterogeneous robots.
    - Validate failure recovery during auctioneer crash and network partitioning.
- **Consequences**:
  - Eliminates single point of failure in mission assignment.
  - Requires bounded auction windows (200-500 ms) and deterministic tie-breaking (lowest UUID hash).
  - Decision will be finalized only after empirical benchmarking in Milestone M8.
