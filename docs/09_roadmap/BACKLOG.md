# Project Backlog & Task Tracking

## Milestone M0: Repository and Documentation Setup
- [x] `TASK-M0-001`: Inspect existing workspace and create modular directory structure. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-002`: Author root README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, .gitignore, .editorconfig. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-003`: Author project vision, problem statement, objectives, scope, and technical glossary. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-004`: Author system architecture, 3-layer architecture, block diagrams, data/control flows, ADRs. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-005`: Author system, functional, non-functional, and software requirements. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-006`: Author all Layer 1 module and submodule documentation (16 sections each). (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-007`: Author all Layer 2 module and submodule documentation (16 sections each). (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-008`: Author all Layer 3 module and submodule documentation (16 sections each). (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-009`: Author interface contracts, JSON schemas, protocol specs, error codes. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-010`: Author development setup, coding standards, build instructions, test guidelines. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-011`: Author test strategy, unit, integration, system, and fault-injection test specs. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-012`: Author open-source technology references for 13 foundational libraries. (Priority: P0, Status: IN_PROGRESS)
- [x] `TASK-M0-013`: Author development roadmap, milestones M0-M11, backlog, changelog. (Priority: P0, Status: IN_PROGRESS)
- [ ] `TASK-M0-014`: Verify all files, validate links and Mermaid syntax, initialize Git repository. (Priority: P0, Status: PLANNED)

---

## Milestone M1: Mine Simulation and Two Robot Models
- [ ] `TASK-M1-001`: Create Gazebo Sim subterranean mine world SDF with uneven rock walls and dark lighting. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M1-002`: Build Robot A differential-drive URDF/Xacro model with 3D LiDAR, RGB, IMU, odom. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M1-003`: Build Robot B tracked chassis URDF/Xacro model with thermal camera, PTZ mast, LiDAR, IMU. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M1-004`: Configure `ros_gz_bridge` and `ros2_control` velocity controllers for both robots. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M1-005`: Implement thermal hotspot emitter and simulated camera plugin. (Priority: P1, Status: PLANNED)

---

## Milestone M2: Independent Robot Navigation
- [ ] `TASK-M2-001`: Configure SLAM Toolbox asynchronous mapping for Robot A. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M2-002`: Configure `robot_localization` dual EKF instances for IMU and wheel/track odometry fusion. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M2-003`: Configure Nav2 Smac global planner and MPPI local controller for Robot A. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M2-004`: Configure Nav2 stack with slip-compensated controller for Robot B. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M2-005`: Validate independent 100m tunnel navigation in simulation. (Priority: P1, Status: PLANNED)

---

## Milestone M3: Robot Agent Abstraction
- [ ] `TASK-M3-001`: Implement Robot Identity Manager and capability descriptor loader. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M3-002`: Implement Robot State Manager FSM (`UNINITIALIZED` to `EMERGENCY_STOP`). (Priority: P0, Status: PLANNED)
- [ ] `TASK-M3-003`: Implement `ExecuteTask.action` server bridging to Nav2. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M3-004`: Implement authoritative Layer 1 Local Safety Manager watchdog. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M3-005`: Implement namespaced ROS 2 telemetry publisher and health monitor. (Priority: P1, Status: PLANNED)

---

## Milestone M4: Discovery and Capability Exchange
- [ ] `TASK-M4-001`: Deploy Eclipse Zenoh session management on simulated robot nodes. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M4-002`: Implement peer discovery scouting and registration handshake. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M4-003`: Implement 2 Hz compact gossip heartbeat broadcaster. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M4-004`: Implement Phi Accrual adaptive failure detector class. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M4-005`: Implement Zenoh queryable capability exchange and local caching. (Priority: P1, Status: PLANNED)

---

## Milestone M5: Mission and Task Management
- [ ] `TASK-M5-001`: Implement Mission DAG parser and Kahn's algorithm cycle detector. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M5-002`: Implement task decomposition engine expanding objectives into atomic tasks. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M5-003`: Implement in-degree prerequisite dependency unblocking engine. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M5-004`: Implement multi-tier priority scheduler with preemption arbitration. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M5-005`: Implement formal Task Lifecycle FSM ledger. (Priority: P1, Status: PLANNED)

---

## Milestone M6: Distributed Task Allocation
- [ ] `TASK-M6-001`: Implement Contract Net Protocol auction announcement and bidding workers. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M6-002`: Implement multi-factor cost evaluation function ($D_{travel}, E_{battery}, T_{risk}, C_{fit}$). (Priority: P0, Status: PLANNED)
- [ ] `TASK-M6-003`: Implement ephemeral auctioneer bid ranking and deterministic tie-breaking. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M6-004`: Implement two-phase commit assignment confirmation (Award -> Ack -> Lease). (Priority: P0, Status: PLANNED)
- [ ] `TASK-M6-005`: Implement time-bounded lease locks preventing duplicate task execution. (Priority: P0, Status: PLANNED)

---

## Milestone M7: Distributed Coordination and State Management
- [ ] `TASK-M7-001`: Implement in-memory replicated state store with Write-Ahead Log. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M7-002`: Implement delta-state CRDT replication (LWW-Element-Set and OR-Set). (Priority: P0, Status: PLANNED)
- [ ] `TASK-M7-003`: Implement causal vector clocks for mutation ordering. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M7-004`: Implement automated anti-entropy reconciliation on peer reconnection. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M7-005`: Implement single-lane tunnel right-of-way conflict resolution. (Priority: P1, Status: PLANNED)

---

## Milestone M8: Communication Failure and Task Recovery
- [ ] `TASK-M8-001`: Implement multi-signal failure detection and severity classifier. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M8-002`: Implement offline execution policy and rendezvous navigation during blackout. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M8-003`: Implement lease expiration watchdog and automatic task re-auctioning. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M8-004`: Implement dynamic costmap keep-out injection for disabled robot hulls. (Priority: P1, Status: PLANNED)

---

## Milestone M9: Mission Operations Interface
- [ ] `TASK-M9-001`: Deploy PostgreSQL relational database and TimescaleDB hypertable schema. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M9-002`: Deploy MinIO S3 object storage for visual and thermal evidence. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M9-003`: Develop FastAPI REST and WebSocket telemetry gateway. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M9-004`: Build React operator dashboard with Deck.gl mine map and live robot trails. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M9-005`: Build automated Jinja2 / WeasyPrint PDF inspection report compiler. (Priority: P1, Status: PLANNED)

---

## Milestone M10: Complete Collaborative Inspection Demonstration
- [ ] `TASK-M10-001`: Conduct end-to-end simulated mission in complex mine world. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M10-002`: Verify Robot A frontier exploration and inspection target discovery. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M10-003`: Verify automated auction award of thermal inspection to Robot B. (Priority: P0, Status: PLANNED)
- [ ] `TASK-M10-004`: Verify radiometric thermal capture and MSHA-compliant report generation. (Priority: P0, Status: PLANNED)

---

## Milestone M11: Additional Robot Integration and SDK Evaluation
- [ ] `TASK-M11-001`: Publish Python Public SDK (`antigravity_mine_sdk`). (Priority: P1, Status: PLANNED)
- [ ] `TASK-M11-002`: Implement HAL adapter plugin for third simulated commercial robot. (Priority: P1, Status: PLANNED)
- [ ] `TASK-M11-003`: Verify 3-robot collaborative task allocation in simulation. (Priority: P1, Status: PLANNED)
