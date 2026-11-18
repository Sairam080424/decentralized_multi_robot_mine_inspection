# Milestone Specifications (M0 - M11)

### M0: Repository and Documentation Setup (Current Milestone)
- **Objective**: Establish modular repository structure, complete 3-layer architecture, all submodule documentation with 16-section templates, valid Mermaid diagrams, interface schemas, and backlog tracking.
- **Exit Criteria**: All documentation files exist, valid syntax, zero unimplemented claims.

### M1: Mine Simulation and Two Robot Models
- **Objective**: Launch Gazebo Sim subterranean mine world; load Robot A (diff-drive) and Robot B (tracked) URDF/Xacro models with functional sensor plugins publishing ROS 2 topics.
- **Exit Criteria**: Both robots spawn in Gazebo; sensors publish at specified rates.

### M2: Independent Robot Navigation
- **Objective**: Integrate Nav2 and SLAM Toolbox independently on Robot A and Robot B.
- **Exit Criteria**: Both robots map and autonomously navigate through 100m of simulated mine drifts without collisions.

### M3: Robot Agent Abstraction
- **Objective**: Encapsulate hardware specifics behind the standardized Robot Agent Gateway exposing `ExecuteTask.action` and authoritative local safety reflexes.
- **Exit Criteria**: Dispatched task actions execute Nav2 goals; local safety manager overrides velocity during obstacle injection.

### M4: Robot Discovery and Capability Exchange
- **Objective**: Implement zero-configuration peer discovery and capability exchange over Eclipse Zenoh.
- **Exit Criteria**: Robots discover each other within < 2.0s and exchange capability JSON documents.

### M5: Mission and Task Management
- **Objective**: Ingest declarative mission DAGs; decompose into atomic tasks with precedence constraints.
- **Exit Criteria**: Cycle detection unit tests pass; task dependencies enforce sequential execution.

### M6: Distributed Task Allocation
- **Objective**: Implement Contract Net Protocol auctioning and multi-factor cost evaluation.
- **Exit Criteria**: Tasks allocated to lowest-cost capable robot; zero duplicate claims.

### M7: Distributed Coordination and State Management
- **Objective**: Deploy CRDT state replication and spatial deconfliction in narrow tunnels.
- **Exit Criteria**: Robots yield correctly in single-lane drift; state merges cleanly after partition.

### M8: Communication Failure and Task Recovery
- **Objective**: Validate fault detection, lease expiration watchdog, and task reassignment.
- **Exit Criteria**: Killing Robot A triggers lease revocation and task reassignment to Robot B within < 8.0s.

### M9: Mission Operations Interface
- **Objective**: Deploy web monitoring dashboard, PostgreSQL database, and MinIO evidence storage.
- **Exit Criteria**: Operators view live telemetry, inspection scorecards, and thermal images in browser.

### M10: Complete Collaborative Inspection Demonstration
- **Objective**: Execute end-to-end mission: Robot A maps tunnel; Robot B performs thermal inspection.
- **Exit Criteria**: High-temperature transformer detected, verified by Robot B, and logged in report.

### M11: Additional Robot Integration and SDK Evaluation
- **Objective**: Evaluate public SDK by integrating a third simulated robot using the standard HAL adapter.
- **Exit Criteria**: Third robot participates in task auctions without modifying core autonomy code.
