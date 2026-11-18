# Architecture Decision Records (ADRs)

## ADR-001: Three-Layer Decoupled Architecture
- **Status**: ACCEPTED
- **Context**: Need clear separation between high-level operations, distributed multi-robot intelligence, and hardware control.
- **Decision**: Adopt three distinct layers (Layer 1: Robot/Environment, Layer 2: Distributed Autonomy, Layer 3: Mission Operations).
- **Consequences**: Prevents vendor lock-in, allows simulated robots to be swapped with physical robots without changing autonomy logic, and protects local safety.

---

## ADR-002: Distributed Contract Net Protocol (CNP) for Task Allocation
- **Status**: UNDER EVALUATION (Proposed Baseline)
- **Context**: Centralized dispatchers fail in subterranean RF-deprived environments.
- **Decision**: Propose a peer-to-peer Contract Net Protocol with multi-criteria cost evaluation (travel distance, battery, sensor match, risk).
- **Evaluation Criteria**: Suitability to be evaluated in Milestone M8 against CBBA and DCOP algorithms regarding message scaling ($O(N)$ vs $O(N^2)$), packet loss resilience, and auctioneer failure recovery.
- **Consequences**: Enables autonomous negotiation in small ad-hoc clusters; eliminates central coordinator bottleneck.

---

## ADR-003: Eclipse Zenoh for Distributed P2P Mesh Communication
- **Status**: UNDER EVALUATION (Proposed Baseline)
- **Context**: Standard ROS 2 CycloneDDS/FastDDS discovery produces high multicast chatter that saturates lossy, low-bandwidth underground mesh networks.
- **Decision**: Propose Eclipse Zenoh as the peer-to-peer transport bridge for Layer 2 inter-robot communication, retaining standard ROS 2 intra-robot DDS for Layer 1.
- **Evaluation Criteria**: Bandwidth overhead, discovery latency, and partition recovery to be evaluated in Milestone M4/M7 against native CycloneDDS and FastDDS Discovery Server.
- **Consequences**: Low projected wire overhead (<5 bytes header), built-in routing, and native support for intermittent connectivity.

---

## ADR-004: CRDTs for Distributed Mission State Replication
- **Status**: UNDER EVALUATION (Proposed Baseline)
- **Context**: Network partitions cause robots to update task states independently. Simple locking or raft consensus stalls when a quorum cannot be reached.
- **Decision**: Propose state-based and delta-based Conflict-Free Replicated Data Types (specifically LWW-Element-Set and OR-Set) paired with vector clocks.
- **Evaluation Criteria**: State bloat, tombstone garbage collection overhead, and delta reconciliation convergence to be evaluated in Milestone M6/M8.
- **Consequences**: Allows concurrent progress during network splits; automatic mathematical convergence when robots rejoin radio contact.

---

## ADR-005: Authoritative Local Safety Autarchy in Layer 1
- **Status**: UNDER EVALUATION (Proposed Architecture & Parameter Tuning)
- **Context**: Complex distributed logic or delayed remote commands could cause physical collisions.
- **Decision**: Propose an authoritative `local_safety_manager` running at a proposed rate of 50 Hz in Layer 1 that intercepts and overrides all velocity commands upon hazard envelope breach.
- **Evaluation Criteria**: Watchdog loop latency (< 50 ms proposed target) and dynamic obstacle/tilt thresholds to be empirically calibrated in Milestone M3/M5 through fault-injection trials.
- **Consequences**: Guarantees physical safety even during autonomy crashes or delayed network packets.

---

## ADR-006: BehaviorTree.CPP for Task Execution and Nav2 Recoveries
- **Status**: UNDER EVALUATION (Proposed Baseline)
- **Context**: Nav2 navigation and long-duration inspection actions require reactive decision-making, fallback recoveries, and clean preemption.
- **Decision**: Propose BehaviorTree.CPP v4 for managing single-robot action execution pipelines and navigation recovery behaviors.
- **Evaluation Criteria**: Tree tick overhead, XML maintainability, and recovery determinism to be evaluated against HFSMs in Milestone M3/M5.
- **Consequences**: Decoupled, modular action execution pipelines with visual inspection via Groot.
