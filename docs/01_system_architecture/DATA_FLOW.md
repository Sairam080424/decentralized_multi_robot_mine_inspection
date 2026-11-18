# Data Flow Architecture

## 1. End-to-End Data Flow

Data flows through three distinct communication planes within the system:
1. **Intra-Robot Sensor-Control Plane** (High frequency, local ROS 2 DDS, 10&ndash;100 Hz).
2. **Inter-Robot Autonomy Plane** (Asynchronous, event-driven, bandwidth-constrained Zenoh gossip, 1&ndash;5 Hz).
3. **Operations & Observability Plane** (Low frequency, delay-tolerant telemetry and bulk evidence sync, 0.1&ndash;1 Hz).

```mermaid
sequenceDiagram
    autonumber
    participant L3 as Layer 3: Mission Console
    participant L2_A as Robot A: Autonomy (L2)
    participant L2_B as Robot B: Autonomy (L2)
    participant L1_A as Robot A: Platform (L1)
    participant L1_B as Robot B: Platform (L1)

    Note over L3,L2_A: 1. Mission Ingestion
    L3->>L2_A: Submit Mission DAG (JSON)
    L2_A->>L2_B: Replicate Mission DAG (CRDT OR-Set)

    Note over L2_A,L2_B: 2. Distributed Task Allocation
    L2_A->>L2_B: Broadcast Task Auction (T1: Map Section 1, T2: Thermal Inspect Substation)
    L2_A->>L2_A: Compute Bid (Cost T1 = 12.4, Cost T2 = Inf [no thermal])
    L2_B->>L2_A: Submit Bid (Cost T1 = 28.1, Cost T2 = 14.2)
    L2_A->>L2_A: Clear Auction: Award T1 -> Robot A
    L2_A->>L2_B: Clear Auction: Award T2 -> Robot B
    L2_B->>L2_A: Confirm Award & Issue Lease Token

    Note over L2_A,L1_A: 3. Local Execution & Safety
    L2_A->>L1_A: Send Task Action Goal (Explore Waypoints)
    L1_A->>L1_A: Nav2 Path Planning & Continuous Safety Checks
    L1_A-->>L2_A: Task Completed (Discovered Inspection Target X)

    Note over L2_B,L1_B: 4. Inspection Evidence Gathering
    L2_B->>L1_B: Send Task Action Goal (Navigate & Thermal Inspect)
    L1_B->>L1_B: Nav2 Trajectory Execution & Thermal Capture
    L1_B-->>L2_B: Task Completed + Radiometric Evidence Blob

    Note over L2_B,L3: 5. Mission State & Evidence Synchronization
    L2_B->>L2_A: State Sync: T2 COMPLETED
    L2_B->>L3: Stream Mission Status & Compressed Evidence
```
