# Functional Requirements Specification

## 1. System-Level Functional Requirements

| Requirement ID | Description | Traceability | Verification Method |
|---|---|---|---|
| `REQ-SYS-001` | The platform shall operate without reliance on a persistent central mission coordinator node. | PROJECT_VISION.md | Multi-robot partition test |
| `REQ-SYS-002` | The system shall support heterogeneous mobile ground robots with distinct locomotion and sensor payloads. | SCOPE.md | Gazebo simulation test |
| `REQ-SYS-003` | The platform shall maintain authoritative local physical safety reflexes on each robot independently. | ADR-005 | Obstacle collision injection |
| `REQ-SYS-004` | The system shall capture, geotag, and store visual and radiometric thermal inspection evidence. | SCOPE.md | Inspection pipeline test |

---

## 2. Layer 1: Robot and Environment Requirements

| Requirement ID | Description | Traceability | Verification Method |
|---|---|---|---|
| `REQ-L1-001` | The simulation environment shall model multi-level mine tunnels with irregular terrain and obstacles. | Module 1.1 | Gazebo world validation |
| `REQ-L1-002` | Robot A shall model a differential-drive chassis equipped with 3D LiDAR, RGB camera, IMU, and odom. | Module 1.2 | URDF / Xacro inspection |
| `REQ-L1-003` | Robot B shall model a tracked chassis equipped with LiDAR, RGB, radiometric thermal camera, and IMU. | Module 1.2 | URDF / Xacro inspection |
| `REQ-L1-004` | The perception module shall provide real-time 2D/3D SLAM and localization in GPS-denied environments. | Module 1.3 | SLAM trajectory error test |
| `REQ-L1-005` | The navigation module shall execute Nav2 collision-free trajectories and automatic recovery behaviors. | Module 1.4 | Nav2 waypoint navigation test |
| `REQ-L1-006` | The local safety manager shall override velocity commands within `[PROPOSED TARGET: < 50 ms]` upon obstacle detection. | Module 1.5 | Software-in-the-loop reflex benchmark |
| `REQ-L1-007` | The robot agent gateway shall expose standard ROS 2 Action interfaces for task execution. | Module 1.6 | ROS 2 Action test client |

---

## 3. Layer 2: Distributed Autonomy Requirements

| Requirement ID | Description | Traceability | Verification Method |
|---|---|---|---|
| `REQ-L2-001` | The peer discovery module shall automatically detect available robot peers within `[PROPOSED TARGET: < 2.0 s]`. | Module 2.1 | Zenoh discovery test |
| `REQ-L2-002` | The capability manager shall filter candidate tasks against declarative robot sensor and mobility profiles. | Module 2.2 | Capability matching unit tests |
| `REQ-L2-003` | The mission manager shall represent missions as Directed Acyclic Graphs (DAGs) with dependencies. | Module 2.3 | DAG parser unit tests |
| `REQ-L2-004` | The task allocator shall execute Contract Net Protocol auctions and resolve bids within `[PROPOSED TARGET: < 500 ms]`. | Module 2.4 | Auction clearance benchmark |
| `REQ-L2-005` | The system shall prevent duplicate task execution using distributed lease tokens and mutual exclusion. | Module 2.4 | Dual-claim contention test |
| `REQ-L2-006` | The coordination module shall deconflict robots encountering each other in narrow single-lane tunnels. | Module 2.5 | Tunnel yield scenario test |
| `REQ-L2-007` | The state manager shall replicate mission state across peers using CRDTs with causal vector clocks. | Module 2.6 | Partition reconciliation test |
| `REQ-L2-008` | The fault recovery module shall detect dead peers and reassign expired leases within `[PROPOSED TARGET: < 8.0 s]`. | Module 2.7 | Simulated crash recovery test |

---

## 4. Layer 3: Mission and Operations Requirements

| Requirement ID | Description | Traceability | Verification Method |
|---|---|---|---|
| `REQ-L3-001` | The mission planner shall validate mission DAGs for cycles and reachable capability constraints before submission. | Module 3.1 | Validation test suite |
| `REQ-L3-002` | The monitoring module shall display real-time robot poses, task status, and topological maps. | Module 3.4 | Web UI / RViz2 visual verification |
| `REQ-L3-003` | The evidence store shall persist visual and thermal datasets with relational metadata and spatial stamps. | Module 3.5 | Database query integration test |
| `REQ-L3-004` | The platform shall provide a public Python SDK and REST API for external dispatch systems. | Module 3.6 | SDK integration test client |
