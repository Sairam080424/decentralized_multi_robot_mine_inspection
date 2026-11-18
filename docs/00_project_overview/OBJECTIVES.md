# Project Objectives

## 1. Primary Autonomy Objectives

1. **Decentralized Collaborative Exploration**: Enable Robot A and Robot B to autonomously explore a simulated multi-level underground mine drift network, generating a shared consistent map without a central coordinator.
2. **Capability-Aware Distributed Task Allocation**: Automatically decompose high-level inspection missions into atomic tasks and allocate them via Contract Net Protocol (CNP) according to robot capabilities (e.g., allocating thermal inspection tasks exclusively to Robot B).
3. **Partition-Tolerant State Synchronization**: Maintain mission state consistency across robots using Conflict-Free Replicated Data Types (CRDTs), ensuring zero data loss during network splits and automatic reconciliation upon link restoration.
4. **Autonomous Fault Detection & Recovery**: Detect simulated robot hardware failure or entrapment within `[PROPOSED TARGET: < 5.0 s]`, revoke outstanding task leases, and reallocate tasks to operational peers without operator intervention.
5. **Multi-Modal Inspection Evidence Capture**: Capture, geotag, and store visual RGB and radiometric thermal evidence for all specified inspection waypoints, associating each record with spatial confidence and timestamps.

---

## 2. Quantitative Performance Targets (Proposed)

> [!NOTE]
> All quantitative metrics below are proposed design objectives to be verified in simulation during Milestone M10.

| Metric Identifier | Parameter | Proposed Target | Validation Method |
|---|---|---|---|
| `METRIC-PERF-001` | P2P Peer Discovery Time | < 2.0 s upon entering RF range | Simulated Wi-Fi loss/reconnect test |
| `METRIC-PERF-002` | Distributed Task Auction Clearance | < 500 ms (2 robots, 10 tasks) | Benchmark timing logger |
| `METRIC-PERF-003` | State Reconciliation Latency | < 1.0 s for 100 state mutations | Delta-CRDT exchange benchmark |
| `METRIC-PERF-004` | Local Safety Stop Reflex Reaction | < 50 ms from obstacle detection | Hardware-in-the-loop safety timer |
| `METRIC-PERF-005` | Task Reallocation Latency on Peer Failure | < 8.0 s after lease expiration | Fault-injection crash test |
| `METRIC-PERF-006` | Narrow Tunnel Deconfliction Convergence | < 3.0 s negotiation time | Tunnel meeting scenario test |
