# System Architecture Specification

## 1. Architectural Philosophy
The Decentralized Multi-Robot Mine Inspection Platform is architected to survive and excel in communication-degraded subterranean operations. It replaces fragile centralized client-server paradigms with an autonomous, layered, peer-to-peer distributed systems model.

---

## 2. Core Architectural Principles

1. **Unidirectional Layered Abstraction**: Layer 3 relies on Layer 2; Layer 2 relies on Layer 1. Lower layers never import or depend on upper layers.
2. **Local Safety Autarchy**: Physical safety is autonomous and un-preemptible. A remote command can never override an active local safety reflex.
3. **Decentralized Consensus**: Task assignment and mission progression proceed through local peer negotiation without requiring global cluster quorum.
4. **Partition Tolerance (CAP Theorem Priority)**: The platform prioritizes Availability and Partition Tolerance (AP), utilizing CRDTs to achieve eventual consistency.
5. **Hardware Agnosticism**: Heterogeneous locomotion and payloads are normalized through declarative capability descriptors.

---

## 3. High-Level System Architecture Diagram

```mermaid
flowchart TB
    subgraph L3["Layer 3: Mission & Operations Layer"]
        M_Plan["Mission Planner & Task Decomposer"]
        M_Mon["Monitoring Dashboard & RViz2"]
        M_DB[("Mission & Evidence Database")]
        M_SDK["Public SDK & REST Gateway"]
    end

    subgraph L2_Mesh["Layer 2: Distributed Autonomy Layer (P2P Gossip Mesh)"]
        subgraph Agent_A["Autonomy Core: Robot A"]
            Disc_A["Peer Discovery & Liveliness"]
            Cap_A["Capability Matcher"]
            Alloc_A["Task Allocator (CNP Engine)"]
            State_A["CRDT Replicated Mission State"]
            Fault_A["Fault Detector & Lease Monitor"]
            Coord_A["P2P Spatial Deconfliction"]
        end
        subgraph Agent_B["Autonomy Core: Robot B"]
            Disc_B["Peer Discovery & Liveliness"]
            Cap_B["Capability Matcher"]
            Alloc_B["Task Allocator (CNP Engine)"]
            State_B["CRDT Replicated Mission State"]
            Fault_B["Fault Detector & Lease Monitor"]
            Coord_B["P2P Spatial Deconfliction"]
        end
        Agent_A <===>|Eclipse Zenoh P2P Mesh| Agent_B
    end

    subgraph L1_Physical["Layer 1: Robot & Environment Layer"]
        subgraph Platform_A["Robot A: Differential-Drive Explorer"]
            L1_A_Bridge["Robot Agent Gateway"]
            L1_A_Nav["Nav2 Stack (Smac / MPPI)"]
            L1_A_SLAM["SLAM Toolbox (3D LiDAR)"]
            L1_A_Safety["Local Safety Manager (Authoritative)"]
            L1_A_Hw["ros2_control Diff-Drive Motors"]
        end
        subgraph Platform_B["Robot B: Tracked Inspector"]
            L1_B_Bridge["Robot Agent Gateway"]
            L1_B_Nav["Nav2 Stack (Tracked Skid-Steer)"]
            L1_B_SLAM["Localization & Map Alignment"]
            L1_B_Safety["Local Safety Manager (Authoritative)"]
            L1_B_Hw["ros2_control Tracked Motors + Thermal PTZ"]
        end
    end

    M_Plan -->|Inject Mission DAG| Agent_A
    M_Plan -->|Inject Mission DAG| Agent_B
    State_A -.->|Async Telemetry Sync| M_DB
    State_B -.->|Async Telemetry Sync| M_DB

    Alloc_A -->|Execute Task Action| L1_A_Bridge
    Alloc_B -->|Execute Task Action| L1_B_Bridge

    L1_A_Bridge --> L1_A_Nav
    L1_B_Bridge --> L1_B_Nav

    L1_A_Nav --> L1_A_Hw
    L1_B_Nav --> L1_B_Hw

    L1_A_Safety ==>|Safety Override Stop| L1_A_Hw
    L1_B_Safety ==>|Safety Override Stop| L1_B_Hw
```
