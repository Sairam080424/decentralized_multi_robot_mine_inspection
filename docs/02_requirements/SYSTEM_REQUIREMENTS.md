# System Requirements Specification (SRS)

## Overview
This document defines the formal system requirements for the **Decentralized Multi-Robot Mine Inspection Platform**. Requirements are organized into nine functional and non-functional categories (A through I).

All numerical performance parameters are explicitly marked as `PROPOSED` or `TBD` until empirically validated through milestone testing.

---

## A. Functional Requirements (System-Level)

| Requirement ID | Description | Priority | Verification Method | Dependencies | Status |
|---|---|---|---|---|---|
| `FR-001` | The system shall support collaborative operation of at least two heterogeneous mobile ground robots. | P0 | Simulation Test | None | PROPOSED |
| `FR-002` | Robots shall autonomously discover available peer agents across the subterranean wireless mesh without a central directory. | P0 | Integration Test | `COM-001` | PROPOSED |
| `FR-003` | Robots shall dynamically exchange declarative capability profiles declaring locomotion, sensors, and resources. | P0 | Unit / Integration Test | `FR-002` | PROPOSED |
| `FR-004` | The system shall allocate tasks among candidate robots using decentralized Contract Net Protocol (CNP) auctions. | P0 | Simulation Benchmark | `FR-003`, `AUT-001` | PROPOSED |
| `FR-005` | Robots shall plan and execute collision-free navigation trajectories independently in unmapped tunnels. | P0 | Simulation Test | `ROB-001`, `ROB-003` | PROPOSED |
| `FR-006` | The system shall detect peer communication failures and network partitions using adaptive heartbeat tracking. | P0 | Fault Injection Test | `COM-002`, `AUT-005` | PROPOSED |
| `FR-007` | The system shall revoke expired task leases and autonomously reassign uncompleted tasks upon robot failure. | P0 | Fault Injection Test | `FR-006`, `AUT-006` | PROPOSED |
| `FR-008` | The system shall capture, geotag, and store visual optical and radiometric thermal inspection evidence. | P1 | Integration Test | `INS-001`, `INS-002` | PROPOSED |
| `FR-009` | The system shall automatically compile comprehensive inspection scorecards and compliance reports upon mission completion. | P1 | End-to-End Test | `FR-008` | PROPOSED |

---

## B. Non-Functional Requirements

| Requirement ID | Description | Priority | Verification Method | Dependencies | Status |
|---|---|---|---|---|---|
| `NFR-001` | Modules shall be architecturally decoupled to support independent development by separate engineers. | P0 | Code Architecture Review | None | PROPOSED |
| `NFR-002` | System components shall expose observable, inspectable states through standardized telemetry and diagnostic topics. | P0 | Integration Test | None | PROPOSED |
| `NFR-003` | The platform shall maintain zero single points of failure in subterranean mission decision-making. | P0 | Architectural Fault Test | `AUT-001`, `AUT-003` | PROPOSED |
| `NFR-004` | Inter-robot coordination messaging overhead shall not exceed `[PROPOSED TARGET: 250 kbps]` aggregate bandwidth per robot. | P1 | Network Profiling | `COM-003` | PROPOSED |
| `NFR-005` | The software architecture shall support scaling from 2 robots to at least 10 robots without exponential message explosion. | P2 | Benchmark Simulation | `AUT-002` | PROPOSED |
| `NFR-006` | All core packages shall build cleanly under ROS 2 Humble on Ubuntu 22.04 LTS with zero compiler warnings. | P0 | CI Build Pipeline | None | PROPOSED |

---

## C. Robotics and Navigation Requirements

| Requirement ID | Description | Priority | Verification Method | Dependencies | Status |
|---|---|---|---|---|---|
| `ROB-001` | Robot A shall model a differential-drive kinematics chassis capable of maximum forward velocity of `[PROPOSED TARGET: 1.2 m/s]`. | P0 | Gazebo Dynamics Test | `SIM-002` | PROPOSED |
| `ROB-002` | Robot B shall model a continuous tracked chassis capable of negotiating 30% inclines and 0.20m obstacles. | P0 | Gazebo Dynamics Test | `SIM-002` | PROPOSED |
| `ROB-003` | The navigation subsystem shall deploy Nav2 with Smac 2D global planning and MPPI local trajectory tracking. | P0 | Navigation Test | `ROB-001`, `ROB-002` | PROPOSED |
| `ROB-004` | The perception subsystem shall provide drift-resilient 2D SLAM in GPS-denied environments using SLAM Toolbox. | P0 | SLAM Error Benchmark | `ROB-001`, `SIM-003` | PROPOSED |
| `ROB-005` | The localization subsystem shall fuse wheel/track odometry, 6-DOF IMU, and SLAM poses using dual EKF instances. | P0 | Trajectory RMSE Test | `ROB-004` | PROPOSED |
| `ROB-006` | Robots shall execute automated navigation recovery routines (clear costmap, backup, spin, wait) when stalled. | P1 | Obstacle Trap Test | `ROB-003` | PROPOSED |

---

## D. Distributed Autonomy Requirements

| Requirement ID | Description | Priority | Verification Method | Dependencies | Status |
|---|---|---|---|---|---|
| `AUT-001` | Missions shall be represented as Directed Acyclic Graphs (DAGs) with explicit prerequisite dependencies. | P0 | Graph Unit Tests | None | PROPOSED |
| `AUT-002` | Task allocation shall evaluate bids using a multi-factor cost function: $Cost = w_1 D_{travel} + w_2 E_{battery} + w_3 T_{risk} - w_4 C_{fit}$. | P0 | Cost Function Unit Tests | `FR-003` | PROPOSED |
| `AUT-003` | Distributed mission state shall be maintained across robots using Conflict-Free Replicated Data Types (CRDTs). | P0 | Property-Based Tests | `COM-003` | PROPOSED |
| `AUT-004` | Event ordering across partitioned robots shall be tracked using causal vector clocks. | P0 | Causal Clock Unit Tests | `AUT-003` | PROPOSED |
| `AUT-005` | Peer liveliness shall be evaluated using an adaptive Phi-Accrual failure detector algorithm. | P1 | Jitter Injection Test | `COM-002` | PROPOSED |
| `AUT-006` | Task execution shall be guarded by time-bounded lease tokens to prevent duplicate concurrent execution. | P0 | Mutex Concurrency Test | `AUT-002` | PROPOSED |
| `AUT-007` | Robots encountering each other in single-lane drifts shall resolve right-of-way without deadlocking. | P1 | Tunnel Meeting Test | `ROB-003`, `COM-001` | PROPOSED |

---

## E. Communication Requirements

| Requirement ID | Description | Priority | Verification Method | Dependencies | Status |
|---|---|---|---|---|---|
| `COM-001` | Inter-robot peer communication shall use Eclipse Zenoh peer-to-peer transport over ad-hoc wireless mesh. | P0 | Network Packet Audit | None | PROPOSED |
| `COM-002` | Robots shall broadcast compact gossip heartbeats at a rate of `[PROPOSED TARGET: 2 Hz]` with payload <= 64 bytes. | P0 | Wireshark Packet Test | `COM-001` | PROPOSED |
| `COM-003` | State synchronization shall use delta-CRDT exchange and periodic 1 Hz anti-entropy version digest gossip. | P0 | Bandwidth Profiling | `AUT-003` | PROPOSED |
| `COM-004` | Robots shall autonomously operate in disconnected mode during total RF blackout without pausing active tasks. | P0 | Simulated Blackout Test | `AUT-006` | PROPOSED |
| `COM-005` | Intra-robot communication shall use ROS 2 DDS partitioned by distinct `ROS_DOMAIN_ID` per robot. | P0 | Topic Isolation Test | None | PROPOSED |

---

## F. Inspection Requirements

| Requirement ID | Description | Priority | Verification Method | Dependencies | Status |
|---|---|---|---|---|---|
| `INS-001` | Robot B shall carry a calibrated simulated radiometric thermal camera publishing 14-bit temperature arrays. | P0 | Thermal Plugin Test | `SIM-004` | PROPOSED |
| `INS-002` | Thermal inspection pipeline shall measure maximum, minimum, and mean temperatures of target assets (+/- 1.0°C). | P0 | Calibration Benchmark | `INS-001` | PROPOSED |
| `INS-003` | Visual inspection pipeline shall capture high-resolution RGB images with embedded EXIF spatial coordinates. | P1 | Metadata Inspection | `ROB-001`, `ROB-002` | PROPOSED |
| `INS-004` | Discovered thermal anomalies ($T_{max} > 80^\circ$C) shall automatically generate a `CRITICAL_HAZARD` record. | P0 | Anomaly Injection Test | `INS-002` | PROPOSED |
| `INS-005` | Inspection results shall be compiled into standardized PASS, WARN, or FAIL scorecards for each asset. | P1 | Automated Scorecard Test | `INS-004` | PROPOSED |

---

## G. Safety Requirements

| Requirement ID | Description | Priority | Verification Method | Dependencies | Status |
|---|---|---|---|---|---|
| `SAF-001` | Every robot platform shall maintain an authoritative Local Safety Manager executing at `[PROPOSED TARGET: 50 Hz]`. | P0 | Hardware Loop Timer | None | PROPOSED |
| `SAF-002` | The Local Safety Manager shall possess unconditional authority to override motor velocity commands to zero. | P0 | Override Assertion Test | `SAF-001` | PROPOSED |
| `SAF-003` | Emergency stop reflex shall halt motor output within `[PROPOSED TARGET: < 50 ms]` of obstacle envelope breach. | P0 | Response Latency Test | `SAF-002` | PROPOSED |
| `SAF-004` | Platform tilt exceeding `[PROPOSED TARGET: 25 degrees]` roll or pitch shall trigger an immediate safety halt. | P0 | Gazebo Incline Test | `SAF-001` | PROPOSED |
| `SAF-005` | Layer 3 surface operators shall possess an emergency global abort command halting all reachable robots within 100 ms. | P0 | Global Abort Injection | `COM-001` | PROPOSED |

---

## H. Simulation Requirements

| Requirement ID | Description | Priority | Verification Method | Dependencies | Status |
|---|---|---|---|---|---|
| `SIM-001` | The simulation environment shall model multi-level subterranean mine drifts using Gazebo Sim SDF assets. | P0 | Gazebo World Load | None | PROPOSED |
| `SIM-002` | Physics solver (ODE / DART) shall simulate rigid-body contacts with real-time update rate >= 1000 Hz. | P0 | Gazebo RTF Audit | `SIM-001` | PROPOSED |
| `SIM-003` | Sensor simulation shall model 3D LiDAR beam divergence, Gaussian range noise, and low-light optical attenuation. | P0 | Sensor Topic Inspection | `SIM-001` | PROPOSED |
| `SIM-004` | Gazebo world shall include configurable thermal radiation sources for overheating mining machinery. | P0 | Thermal Camera View | `SIM-001` | PROPOSED |
| `SIM-005` | The simulation environment shall provide synthetic RF attenuation, distance-based drop, and partition injection. | P0 | Packet Drop Injection | `SIM-001` | PROPOSED |

---

## I. Testing Requirements

| Requirement ID | Description | Priority | Verification Method | Dependencies | Status |
|---|---|---|---|---|---|
| `TST-001` | All algorithmic functions (CRDT merges, cost functions, DAG validation) shall achieve >= 80% line test coverage. | P0 | `colcon test` / lcov | None | PROPOSED |
| `TST-002` | Communication loss and reconnection reconciliation shall be tested under automated fault-injection scripts. | P0 | Automated Test Runner | `COM-003`, `COM-004` | PROPOSED |
| `TST-003` | End-to-end multi-robot mission demonstration shall be validated via headless simulation in automated CI pipelines. | P1 | GitHub Actions / Docker | `FR-001` - `FR-009` | PROPOSED |
