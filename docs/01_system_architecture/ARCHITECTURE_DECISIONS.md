# Architecture Decision Records (ADRs)

## ADR-001: Three-Layer Decoupled Architecture
- **Status**: ACCEPTED
- **Context**: Need clear separation between high-level operations, distributed multi-robot intelligence, and hardware control.
- **Decision**: Adopt three distinct layers (Layer 1: Robot/Environment, Layer 2: Distributed Autonomy, Layer 3: Mission Operations).
- **Consequences**: Prevents vendor lock-in, allows simulated robots to be swapped with physical robots without changing autonomy logic, and protects local safety.

---

## ADR-002: Distributed Contract Net Protocol (CNP) for Task Allocation
- **Status**: ACCEPTED
- **Context**: Centralized dispatchers fail in subterranean RF-deprived environments.
- **Decision**: Use a peer-to-peer Contract Net Protocol with multi-criteria cost evaluation (travel distance, battery, sensor match, risk).
- **Consequences**: Enables autonomous negotiation in small ad-hoc clusters; eliminates central coordinator bottleneck.

---

## ADR-003: Eclipse Zenoh for Distributed P2P Mesh Communication
- **Status**: ACCEPTED (Investigating alongside ROS 2 DDS)
- **Context**: Standard ROS 2 CycloneDDS/FastDDS discovery produces high multicast chatter that saturates lossy, low-bandwidth underground mesh networks.
- **Decision**: Deploy Eclipse Zenoh as the peer-to-peer transport bridge for Layer 2 inter-robot communication, retaining standard ROS 2 intra-robot DDS for Layer 1.
- **Consequences**: Extremely low wire overhead (<5 bytes header), built-in routing, and native support for intermittent connectivity.

---

## ADR-004: CRDTs for Distributed Mission State Replication
- **Status**: ACCEPTED
- **Context**: Network partitions cause robots to update task states independently. Simple locking or raft consensus stalls when a quorum cannot be reached.
- **Decision**: Use state-based Conflict-Free Replicated Data Types (specifically LWW-Element-Set and OR-Set) paired with vector clocks.
- **Consequences**: Allows concurrent progress during network splits; automatic mathematical convergence when robots rejoin radio contact.

---

## ADR-005: Authoritative Local Safety Autarchy in Layer 1
- **Status**: ACCEPTED
- **Context**: Complex distributed logic or delayed remote commands could cause physical collisions.
- **Decision**: Establish an authoritative `local_safety_manager` running at 50 Hz in Layer 1 that intercepts and can override all velocity commands.
- **Consequences**: Guarantees physical safety even during autonomy crashes or delayed network packets.
