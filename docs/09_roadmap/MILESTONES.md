# Detailed Milestone Specifications (M0 - M13)

This document provides formal technical specifications for each of the 14 project milestones.

---

## Milestone M0: Repository and Architecture Foundation
- **Objective**: Establish the complete engineering foundation, repository structure, documentation suite for all 20 modules and 94 submodules, interface contracts, coding standards, CI validation workflows, and development roadmap.
- **Required Modules**: All modules (architectural specifications, documentation, and interface definitions).
- **Prerequisites**: None.
- **Dependencies**: Git, Python 3.10+, ROS 2 Humble base workspace.
- **Implementation Activities**:
  - Author Project Charter, System Requirements, and 3-Layer Architecture specifications.
  - Author 94 submodule technical specifications adhering to the standardized 16-section template.
  - Author formal ROS 2 interfaces, JSON schemas, and shared interface contracts.
  - Establish Architectural Decision Records (ADR-001 through ADR-006).
  - Configure automated repository verification tooling (`tools/verify_repository.py`) and GitHub Actions CI.
- **Deliverables**: Complete documentation repository, verification script, `.github/` templates, initial Git commit history on `main` and `feature/m0-project-foundation`.
- **Testing Requirements**: Verification script must validate 0 broken links, 0 template incompleteness errors, 0 unsupported Mermaid diagrams, 0 false implementation claims.
- **Acceptance Criteria**: Repository audit passes with 100% compliance; PR opened and approved by Technical Founder.
- **Completion Status**: `DONE`.

---

## Milestone M1: Underground Mine Simulation
- **Objective**: Construct a high-fidelity underground mine simulation environment in Gazebo Sim featuring irregular rock tunnels, narrow crosscuts, variable lighting, mud/rubble terrain, and simulated RF communication attenuation.
- **Required Modules**: `MOD-1.1` (Simulation Environment).
- **Prerequisites**: M0.
- **Dependencies**: Gazebo Sim (Garden/Harmonic), SDFormat 1.9+, `ros_gz_sim`.
- **Implementation Activities**:
  - Build modular subterranean tunnel meshes with realistic rock wall textures and non-uniform cross-sections.
  - Implement configurable terrain patches (loose gravel, wet mud, 15-degree inclines).
  - Integrate environmental hazards (standing water, fallen timber obstacles, low-ceiling clearance zones).
  - Implement analytical distance- and wall-attenuation RF communication simulation model (Gazebo C++ plugin deferred to M6).
- **Deliverables**: Gazebo world SDF packages (`mine_world.sdf`), procedural tunnel generation scripts, analytical RF communication model (`subterranean_rf_model.py`) and CLI tool (`simulate_rf_attenuation.py`), launch files.
- **Testing Requirements**: World loads in Gazebo Sim headless at >= 30 Hz real-time factor; analytical RF model correctly calculates signal attenuation and packet drop across rock pillars and tunnel bends; ROS-Gazebo clock bridge synchronizes simulation time.
- **Acceptance Criteria**: Simulated underground environment renders reliably without physics instability; observable simulation state advances; models spawn at designated mine coordinates.
- **Completion Status**: `IN_PROGRESS` (Tasks M1-001 through M1-004 complete; Task M1-005 analytical model complete with runtime network plugin deferred to M6).

---

## Milestone M2: Two Heterogeneous Robot Models
- **Objective**: Develop kinematic, dynamic, and sensor URDF/Xacro models for Robot A (wheeled exploration rover) and Robot B (tracked heavy inspection rover) with physical property validation and `ros2_control` integration.
- **Required Modules**: `MOD-1.2` (Robot Models).
- **Prerequisites**: M0, M1.
- **Dependencies**: URDF, Xacro, `ros2_control`, `gz_ros2_control`, sensor plugins.
- **Implementation Activities**:
  - Author Robot A URDF/Xacro: differential-drive wheeled chassis, 3D LiDAR, forward RGB camera, 9-DOF IMU, wheel encoders.
  - Author Robot B URDF/Xacro: tracked differential drive chassis, elevating inspection mast, 3D LiDAR, RGB PTZ camera, simulated radiometric thermal camera, IMU.
  - Configure `ros2_control` hardware interfaces and velocity controllers (`diff_drive_controller`).
  - Implement simulated radiometric thermal hotspot camera plugin.
- **Deliverables**: `robot_a_description`, `robot_b_description`, controller configurations, Gazebo sensor bridge launch configurations.
- **Testing Requirements**: Both robots spawn in `mine_world`; publish valid TF trees (`base_link` -> sensors); respond to `/cmd_vel` commands without tipping or wheel clipping.
- **Acceptance Criteria**: Robot A reaches target speed of 1.2 m/s; Robot B negotiates 15-degree incline and tracks velocity commands with < 5% steady-state error.
- **Completion Status**: `PLANNED`.

---

## Milestone M3: Perception, Localization and Mapping
- **Objective**: Deploy sensor processing pipelines, 3D point cloud filtering, 6-DOF odometry fusion, SLAM, and multi-robot map alignment across both robots.
- **Required Modules**: `MOD-1.3` (Perception and Localization).
- **Prerequisites**: M1, M2.
- **Dependencies**: `robot_localization`, SLAM Toolbox / Faster-LIO / Cartographer, PCL, OpenCV.
- **Implementation Activities**:
  - Configure sensor drivers and point cloud downsampling/filtering nodes for underground dust/particulate rejection.
  - Implement dual-EKF state estimation (`robot_localization`) fusing IMU, wheel/track odometry, and scan matching.
  - Deploy 2D/3D SLAM generating occupancy grids and submaps.
  - Implement peer-to-peer submap exchange and relative coordinate frame transformation alignment.
- **Deliverables**: Sensor processing packages, EKF configurations, SLAM launch setups, multi-robot map alignment node.
- **Testing Requirements**: Estimated pose drift < 2% of distance traveled; loop closure reliably detected in tunnel loop; map alignment error < 0.2 m.
- **Acceptance Criteria**: Robot A and Robot B generate consistent local maps; Robot B merges Robot A's exploration submap with correct spatial alignment.
- **Completion Status**: `PLANNED`.

---

## Milestone M4: Independent Robot Navigation
- **Objective**: Configure independent autonomous navigation stacks for both robots capable of global path planning, dynamic obstacle avoidance, narrow passage traversal, and track-slip recovery.
- **Required Modules**: `MOD-1.4` (Navigation and Motion).
- **Prerequisites**: M2, M3.
- **Dependencies**: Nav2 (Navigation 2), Smac Planner (Lattice / Hybrid-A*), MPPI Controller, Costmap 2D.
- **Implementation Activities**:
  - Configure 2D/3D voxel costmaps with inflation layers tuned for rough rock walls.
  - Deploy Smac Planner for differential-drive (Robot A) and tracked kinodynamic constraints (Robot B).
  - Deploy Model Predictive Path Integral (MPPI) local controller for smooth trajectory execution and obstacle avoidance.
  - Implement specialized recovery behaviors (backing out of blind tunnels, track slip agitation, stuck detector).
- **Deliverables**: Nav2 configuration packages for Robot A and Robot B, custom recovery behavior plugins, navigation launch scripts.
- **Testing Requirements**: Autonomous traversal of 100-meter winding mine tunnel without collisions or stall timeouts across 10 repeated simulation trials.
- **Acceptance Criteria**: Both robots achieve autonomous point-to-point goal navigation in unmapped and partially mapped drifts with 0 unhandled collisions.
- **Completion Status**: `PLANNED`.

---

## Milestone M5: Common Robot-Agent Abstraction
- **Objective**: Implement the hardware abstraction layer (HAL) and local robot-agent interface, encapsulating robot-specific navigation and sensing behind uniform action servers, lifecycle state machines, and authoritative local safety managers.
- **Required Modules**: `MOD-1.5` (Robot Agent), `MOD-1.6` (Robot Communication Interface).
- **Prerequisites**: M4.
- **Dependencies**: ROS 2 Lifecycle, `rclcpp_action`, `ExecuteTask.action`, `interfaces`.
- **Implementation Activities**:
  - Implement `RobotAgentNode` managing lifecycle states (`UNCONFIGURED`, `INACTIVE`, `ACTIVE`, `FINALIZED`).
  - Deploy `ExecuteTask.action` server translating high-level atomic tasks into Nav2 goals and inspection tool actions.
  - Deploy standalone 50 Hz `local_safety_manager` monitoring laser scans and IMU pitch/roll, holding un-preemptible authority to clamp `/cmd_vel` to zero.
  - Implement standardized telemetry and state publishing at 10 Hz (`RobotState.msg`).
- **Deliverables**: `robot_agent_core` package, `local_safety_manager` binary, task execution action server, mock test client.
- **Testing Requirements**: Task execution actions dispatch and report progress; emergency stop triggers within < 50 ms when obstacle is injected 0.5 m ahead.
- **Acceptance Criteria**: Both robots respond identically to standardized `ExecuteTask` action invocations despite heterogeneous physical platforms.
- **Completion Status**: `PLANNED`.

---

## Milestone M6: Robot Discovery and Capability Exchange
- **Objective**: Implement zero-configuration peer-to-peer discovery, periodic gossip heartbeats, failure accrual tracking, and capability exchange over Eclipse Zenoh.
- **Required Modules**: `MOD-2.1` (Peer Discovery and Registration), `MOD-2.2` (Capability Exchange and Compatibility).
- **Prerequisites**: M5.
- **Dependencies**: Eclipse Zenoh (C++ / Rust / Python bindings), `nlohmann_json`, `CapabilityProfile.json`.
- **Implementation Activities**:
  - Deploy Zenoh routerless peer-to-peer session management.
  - Implement discovery beacon broadcaster and receiver responding to `mine/discovery/**`.
  - Implement 2 Hz compact gossip heartbeat protocol with Phi Accrual failure detection algorithm.
  - Implement capability profile loader publishing structured JSON specs (`sensors`, `mobility`, `tooling`, `battery_capacity`).
- **Deliverables**: `zenoh_discovery_node`, capability querying client, simulated network disconnect test script.
- **Testing Requirements**: Peer discovery latency < 2.0 s upon network reconnection; dropped heartbeats accurately increment failure accrual metric.
- **Acceptance Criteria**: Robot A and Robot B discover each other upon entering wireless range and cache each other's full capability profiles without centralized assistance.
- **Completion Status**: `PLANNED`.

---

## Milestone M7: Mission and Task Management
- **Objective**: Author mission planning, DAG decomposition, cycle validation, and atomic task state tracking.
- **Required Modules**: `MOD-2.3` (Task Decomposition and Representation), `MOD-3.1` (Mission Definition and Specification).
- **Prerequisites**: M6.
- **Dependencies**: `nlohmann_json`, Directed Acyclic Graph (DAG) library, `MissionDefinition.json`.
- **Implementation Activities**:
  - Author mission JSON parser validating schema compliance and semantic consistency.
  - Implement DAG dependency engine with Kahn's topological sort and cycle detection.
  - Implement task unblocking logic triggering child tasks when parent prerequisites reach `COMPLETED`.
  - Deploy local task queue manager on each robot.
- **Deliverables**: `mission_decomposer` package, task state machine library, sample mine exploration & inspection mission files.
- **Testing Requirements**: Unit tests verify acyclic validation, cycle rejection, and topological prerequisite execution order.
- **Acceptance Criteria**: High-level mine inspection mission successfully decomposes into ordered atomic tasks (`EXPLORE_DRIFT`, `INSPECT_TRANSFORMER`).
- **Completion Status**: `PLANNED`.

---

## Milestone M8: Decentralised Task Allocation
- **Objective**: Implement decentralized Contract Net Protocol (CNP) auctions, multi-factor cost evaluation, and distributed task agreement with zero single points of failure.
- **Required Modules**: `MOD-2.4` (Decentralised Task Allocation).
- **Prerequisites**: M6, M7.
- **Dependencies**: Eclipse Zenoh queryables, `TaskDefinition.json`, `TaskAssignment.json`.
- **Implementation Activities**:
  - Implement CNP Auctioneer role: broadcasting Call for Proposals (CFP) to `mine/tasks/auction/<task_id>`.
  - Implement CNP Bidder role: evaluating capability suitability, remaining battery, distance to target, and current workload.
  - Implement Cost Evaluator computing normalized bid scores with deterministic tie-breaking.
  - Implement Agreement and Award confirmation protocol preventing dual assignments.
- **Deliverables**: `cnp_auctioneer` node, `cnp_bidder` node, cost evaluation library, auction stress-test suite.
- **Testing Requirements**: Auction resolution completed within < 3.0 s; Robot A wins exploration tasks; Robot B wins thermal inspection tasks.
- **Acceptance Criteria**: Tasks are autonomously and deterministically awarded to the most capable, available robot with 0 duplicate awards.
- **Completion Status**: `PLANNED`.

---

## Milestone M9: Distributed Coordination and State Management
- **Objective**: Implement Conflict-Free Replicated Data Types (CRDTs), vector clocks, and narrow tunnel spatial deconfliction for cooperative multi-robot movement.
- **Required Modules**: `MOD-2.5` (Coordination and Spatial Deconfliction), `MOD-2.6` (Distributed Mission State).
- **Prerequisites**: M8.
- **Dependencies**: State-based CRDT library (OR-Set, LWW-Element-Set), Vector Clocks, Zenoh storage.
- **Implementation Activities**:
  - Deploy state-based CRDTs replicating global task allocation tables and inspection progress across mesh peers.
  - Implement causal vector clocks tagging all state mutations to ensure eventual consistency across network partitions.
  - Implement spatial deconfliction protocol: tunnel segment reservation tokens preventing deadlocks in single-lane drifts.
  - Deploy priority-based yield maneuver behavior for oncoming robots.
- **Deliverables**: `crdt_mission_state` library, `tunnel_traffic_manager` node, network partition recovery test harness.
- **Testing Requirements**: Divergent state replicas merge into identical states upon simulated network heal; two robots entering a single tunnel drift deconflict without deadlock.
- **Acceptance Criteria**: Distributed mission state achieves eventual consistency across intermittent drops; 0 deadlock occurrences in narrow mine tunnels.
- **Completion Status**: `PLANNED`.

---

## Milestone M10: Fault Tolerance and Recovery
- **Objective**: Implement autonomous fault detection, task lease expiration watchdogs, and dynamic task recovery and reassignment when a peer fails or disconnects.
- **Required Modules**: `MOD-2.7` (Failure Detection and Health Monitoring), `MOD-2.8` (Task Reassignment and Recovery).
- **Prerequisites**: M8, M9.
- **Dependencies**: Lease watchdogs, Zenoh liveliness tokens.
- **Implementation Activities**:
  - Implement task execution lease renewals: executing robot must renew lease every 5.0 s.
  - Implement lease expiration watchdog: when a lease expires, the task reverts to `UNASSIGNED`.
  - Implement failure recovery triggers: re-announcing orphaned tasks to the active peer mesh.
  - Implement robot safe-state isolation when internal hardware or localization faults are detected.
- **Deliverables**: `task_recovery_manager` package, fault injection simulation test bench.
- **Testing Requirements**: Injecting a crash into Robot A causes Robot B to detect failure within < 8.0 s and re-auction or adopt remaining tasks.
- **Acceptance Criteria**: System recovers gracefully from simulated robot hardware crashes or prolonged communication blackouts without human intervention.
- **Completion Status**: `PLANNED`.

---

## Milestone M11: Inspection Management and Visualization
- **Objective**: Deploy fleet telemetry visualization, inspection evidence collection (RGB/thermal), database logging, and an operator human-in-the-loop dashboard.
- **Required Modules**: `MOD-3.2` (Inspection Management and Reporting), `MOD-3.3` (Fleet Telemetry and Monitoring), `MOD-3.4` (Human-in-the-Loop Interaction).
- **Prerequisites**: M5, M9.
- **Dependencies**: PostgreSQL, MinIO Object Storage, WebRTC / Foxglove Studio / React Web Dashboard.
- **Implementation Activities**:
  - Implement inspection evidence collector archiving timestamped RGB and thermal images into MinIO.
  - Implement mission summary report generator producing PDF and JSON inspection scorecards.
  - Deploy web-based operator monitoring console streaming robot telemetry, map overlays, and task status.
  - Implement human-in-the-loop intervention interface (pause mission, manual teleoperation takeover, priority task injection).
- **Deliverables**: Inspection evidence ingestion service, telemetry gateway, operator web interface, database schemas.
- **Testing Requirements**: Telemetry renders at >= 5 Hz on dashboard; thermal anomalies logged with GPS/local metric coordinates and image attachments.
- **Acceptance Criteria**: Ground station operator observes live multi-robot progress, reviews inspection findings, and triggers emergency fleet stop from browser.
- **Completion Status**: `PLANNED`.

---

## Milestone M12: Complete Two-Robot Collaborative Demonstration
- **Objective**: Execute the complete, integrated multi-robot mine exploration and thermal inspection mission in simulated Gazebo subterranean mine world.
- **Required Modules**: Complete integrated platform (Layer 1, Layer 2, Layer 3).
- **Prerequisites**: M1 through M11.
- **Dependencies**: All preceding milestone deliverables.
- **Implementation Activities**:
  - Launch full simulation environment with Robot A and Robot B at mine portal.
  - Mission Operator loads exploration and inspection mission DAG.
  - Robot A autonomously explores unknown drift, generates map, and identifies a candidate electrical hazard location.
  - Robot A broadcasts candidate inspection task via CNP auction.
  - Robot B bids, wins the task, navigates through mapped tunnel to the target location.
  - Robot B elevates mast, captures thermal hotspot evidence, logs inspection report.
  - Both robots coordinate passage through narrow intersection and return to portal.
- **Deliverables**: End-to-end mission launch script, recorded video demonstration, mission inspection report, automated integration test.
- **Testing Requirements**: Full mission completes end-to-end with zero manual teleoperation in simulation; all tasks logged as `COMPLETED`.
- **Acceptance Criteria**: Collaborative inspection mission successfully finishes with verified thermal anomaly detection, zero collisions, and verified report generation.
- **Completion Status**: `PLANNED`.

---

## Milestone M13: Evaluation, Optimization and Expansion
- **Objective**: Benchmark platform scalability, conduct communication degradation stress testing, optimize compute/bandwidth utilization, and integrate a third heterogeneous robot using the open SDK.
- **Required Modules**: `MOD-3.5` (Integration, SDK and Extensibility), System Benchmarking Tools.
- **Prerequisites**: M12.
- **Dependencies**: Python/C++ SDK packages, network impairment simulator (`tc`/`netem`).
- **Implementation Activities**:
  - Measure task allocation latency and state reconciliation overhead under 0% to 50% packet drop and 500 ms latency.
  - Author developer SDK documentation and reference wrapper classes.
  - Integrate a third simulated robot (Robot C: aerial drone or quadrotor) implementing the standard Robot Agent HAL.
  - Validate 3-robot collaborative mission execution.
- **Deliverables**: Benchmarking report, Python SDK package, Robot C integration example, final project release package (`v1.0.0`).
- **Testing Requirements**: System functions reliably under 30% communication packet loss; third robot discovers mesh and wins aerial survey tasks.
- **Acceptance Criteria**: Platform extensibility proven by successful integration of a third robot type without modifying core Layer 2 autonomy algorithms.
- **Completion Status**: `PLANNED`.
