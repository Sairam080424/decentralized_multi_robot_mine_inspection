# Project Backlog & Task Tracking

This backlog tracks all engineering activities across the 14 project milestones (**M0 through M13**).

---

## Milestone M0: Repository and Architecture Foundation
- [x] `TASK-M0-001`: Inspect existing workspace and create modular directory structure. (Priority: P0, Status: DONE)
- [x] `TASK-M0-002`: Author root README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, .gitignore, .editorconfig. (Priority: P0, Status: DONE)
- [x] `TASK-M0-003`: Author project vision, problem statement, objectives, scope, and technical glossary. (Priority: P0, Status: DONE)
- [x] `TASK-M0-004`: Author system architecture, 3-layer architecture, block diagrams, data/control flows, ADRs. (Priority: P0, Status: DONE)
- [x] `TASK-M0-005`: Author system, functional, non-functional, and software requirements. (Priority: P0, Status: DONE)
- [x] `TASK-M0-006`: Author all Layer 1 module and submodule documentation (16 sections each). (Priority: P0, Status: DONE)
- [x] `TASK-M0-007`: Author all Layer 2 module and submodule documentation (16 sections each). (Priority: P0, Status: DONE)
- [x] `TASK-M0-008`: Author all Layer 3 module and submodule documentation (16 sections each). (Priority: P0, Status: DONE)
- [x] `TASK-M0-009`: Author interface contracts, JSON schemas, protocol specs, error codes. (Priority: P0, Status: DONE)
- [x] `TASK-M0-010`: Author development setup, coding standards, build instructions, test guidelines. (Priority: P0, Status: DONE)
- [x] `TASK-M0-011`: Author test strategy, unit, integration, system, and fault-injection test specs. (Priority: P0, Status: DONE)
- [x] `TASK-M0-012`: Author open-source technology references for 13 foundational libraries. (Priority: P0, Status: DONE)
- [x] `TASK-M0-013`: Author development roadmap, milestones M0-M13, backlog, changelog. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-014`: Verify all files, validate links and Mermaid syntax, initialize Git repository. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-015`: Author Phase 0E Shared Interface Definitions and Module Ownership matrix. (Priority: P0, Status: DONE)
- [x] `TASK-M0-016`: Author Phase 0F Module Assignment Template and Code Review Checklist. (Priority: P0, Status: DONE)

---

## Milestone M1: Underground Mine Simulation
- [ ] `TASK-M1-001`: Create Gazebo Sim subterranean mine world SDF with irregular rock walls and dim lighting. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M1-002`: Author procedural mine tunnel generation script with customizable cross-sections. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M1-003`: Model terrain roughness, mud patches, and 15-degree incline ramps in SDF. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M1-004`: Model physical mine obstacles (fallen rock piles, timber roof supports, standing water). (Priority: P1, Status: PLANNED)
- [ ] `TASK-M1-005`: Implement Gazebo RF communication attenuation plugin simulating underground line-of-sight loss. (Priority: P2, Status: PLANNED)

---

## Milestone M2: Two Heterogeneous Robot Models
- [ ] `TASK-M2-001`: Build Robot A differential-drive wheeled URDF/Xacro model with 3D LiDAR, RGB camera, IMU. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M2-002`: Build Robot B tracked chassis URDF/Xacro model with PTZ camera, thermal camera, LiDAR, IMU. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M2-003`: Implement simulated radiometric thermal hotspot camera sensor plugin. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M2-004`: Configure `ros2_control` velocity controllers and hardware interfaces for Robot A. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M2-005`: Configure `ros2_control` tracked skid-steer controllers for Robot B. (Priority: P0, Status: PLANNED)

---

## Milestone M3: Perception, Localization and Mapping
- [ ] `TASK-M3-001`: Deploy LiDAR point cloud filtering and ground plane segmentation nodes. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M3-002`: Configure dual `robot_localization` EKF instances fusing wheel/track odometry, IMU, and scan matching. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M3-003`: Configure 3D SLAM (SLAM Toolbox / Faster-LIO) for subterranean tunnel mapping. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M3-004`: Implement submap serialization and peer-to-peer occupancy grid sharing node. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M3-005`: Implement multi-robot map alignment and relative frame calibration. (Priority: P2, Status: PLANNED)

---

## Milestone M4: Independent Robot Navigation
- [ ] `TASK-M4-001`: Configure Nav2 2D/3D costmaps with inflation layers tuned for irregular mine rock surfaces. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M4-002`: Deploy Smac Planner (Lattice) for differential-drive Robot A. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M4-003`: Deploy Smac Planner (2D/Hybrid-A*) for tracked Robot B. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M4-004`: Deploy Model Predictive Path Integral (MPPI) local controller on both robots. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M4-005`: Implement specialized mine recovery behaviors (blind reverse, track de-snag, stuck spin). (Priority: P1, Status: PLANNED)

---

## Milestone M5: Common Robot-Agent Abstraction
- [ ] `TASK-M5-001`: Implement `RobotAgentNode` with ROS 2 Lifecycle state machine. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M5-002`: Implement `ExecuteTask.action` server bridging high-level tasks to Nav2 and tool controllers. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M5-003`: Implement authoritative 50 Hz `local_safety_manager` with un-preemptible `/cmd_vel` override. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M5-004`: Implement standardized `RobotState.msg` telemetry publisher at 10 Hz. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M5-005`: Implement local capability profile reader loading JSON descriptors. (Priority: P1, Status: PLANNED)

---

## Milestone M6: Robot Discovery and Capability Exchange
- [ ] `TASK-M6-001`: Deploy Eclipse Zenoh peer-to-peer session management on robot agents. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M6-002`: Implement peer discovery beaconing and neighbor registration protocol. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M6-003`: Implement 2 Hz compact gossip heartbeat broadcaster. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M6-004`: Implement Phi Accrual adaptive failure detection class. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M6-005`: Implement Zenoh queryable capability exchange and local caching. (Priority: P1, Status: PLANNED)

---

## Milestone M7: Mission and Task Management
- [ ] `TASK-M7-001`: Implement Mission DAG JSON parser with schema validation. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M7-002`: Implement Kahn's algorithm cycle detection and topological sorting. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M7-003`: Implement task decomposition engine expanding mission goals into atomic tasks. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M7-004`: Implement in-degree prerequisite unblocking engine for downstream tasks. (Priority: P1, Status: PLANNED)

---

## Milestone M8: Decentralised Task Allocation
- [ ] `TASK-M8-001`: Implement Contract Net Protocol (CNP) Auctioneer logic broadcasting task CFPs. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M8-002`: Implement CNP Bidder evaluating distance, battery, capabilities, and workload. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M8-003`: Implement deterministic Cost Evaluator and tie-breaking logic. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M8-004`: Implement two-phase task award and confirmation handshake preventing duplicate claims. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M8-005`: Implement task allocation timeout and re-auction triggers. (Priority: P1, Status: PLANNED)

---

## Milestone M9: Distributed Coordination and State Management
- [ ] `TASK-M9-001`: Implement state-based Conflict-Free Replicated Data Types (CRDTs) for task state tables. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M9-002`: Implement causal vector clock stamping on all distributed state updates. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M9-003`: Implement tunnel segment reservation token protocol for single-lane spatial deconfliction. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M9-004`: Implement priority-based yield and passing bay navigation behaviors. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M9-005`: Implement partition recovery state reconciliation over Zenoh sync. (Priority: P1, Status: PLANNED)

---

## Milestone M10: Fault Tolerance and Recovery
- [ ] `TASK-M10-001`: Implement task execution lease renewal protocol (5.0 s lease period). (Priority: P0, Status: PLANNED)
- [ ] `TASK-M10-002`: Implement lease expiration watchdog revoking stale task ownership. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M10-003`: Implement automated task reassignment re-auctioning orphaned tasks. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M10-004`: Implement robot safe-stop and fallback isolation state when sensors fail. (Priority: P1, Status: PLANNED)

---

## Milestone M11: Inspection Management and Visualization
- [ ] `TASK-M11-001`: Implement inspection evidence ingest service saving RGB/thermal images to MinIO. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M11-002`: Deploy PostgreSQL database schema for inspection observations and mission telemetry. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M11-003`: Deploy web-based operator monitoring console streaming fleet status and map overlays. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M11-004`: Implement operator intervention interface (teleoperation override, mission abort). (Priority: P1, Status: PLANNED)
- [ ] `TASK-M11-005`: Implement automated PDF/JSON mission inspection report generator. (Priority: P2, Status: PLANNED)

---

## Milestone M12: Complete Two-Robot Collaborative Demonstration
- [ ] `TASK-M12-001`: Author end-to-end launch scripts for multi-robot mine simulation demo. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M12-002`: Validate Robot A autonomous drift exploration, 3D mapping, and obstacle detection. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M12-003`: Validate Robot A candidate inspection task generation and CNP auction broadcast. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M12-004`: Validate Robot B bid submission, award confirmation, and navigation to target. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M12-005`: Validate Robot B thermal inspection, evidence capture, and report generation. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M12-006`: Validate collaborative tunnel passage and safe return to portal. (Priority: P0, Status: PLANNED)

---

## Milestone M13: Evaluation, Optimization and Expansion
- [ ] `TASK-M13-001`: Benchmark task allocation latency and communication overhead under network packet drop. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M13-002`: Author Python and C++ Robot Agent SDK documentation and wrapper classes. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M13-003`: Integrate third simulated robot (Robot C: drone or quadrotor) via standard SDK. (Priority: P2, Status: PLANNED)
- [ ] `TASK-M13-004`: Validate 3-robot collaborative mission execution in subterranean mine world. (Priority: P2, Status: PLANNED)
- [ ] `TASK-M13-005`: Finalize platform v1.0.0 release packaging and user manual. (Priority: P1, Status: PLANNED)
