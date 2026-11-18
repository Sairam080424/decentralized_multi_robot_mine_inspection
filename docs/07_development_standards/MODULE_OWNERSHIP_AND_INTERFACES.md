# Module Ownership & Interface Boundaries Matrix

## 1. Architectural Purpose
To allow multiple robotics and distributed systems software engineers to develop, test, and refactor code concurrently without merge conflicts or broken dependencies, this matrix establishes explicit boundaries:
- **Module Ownership**: Designated lead engineer or engineering group.
- **Write Permissions**: Specific packages and files the module owner has authority to modify.
- **Modification Prohibitions**: Core shared files the module must **never** modify directly without an approved Architectural RFC.
- **Upstream & Downstream Dependencies**: Explicit contracts governing interactions.

---

## 2. Complete 20-Module Ownership Matrix

### Layer 1: Robot and Environment Layer

| Module ID & Name | Designated Owner | Core Responsibilities | Permitted Write Files | Prohibited Files | Upstream Dependencies | Downstream Consumers | Shared Interface Ownership |
|---|---|---|---|---|---|---|---|
| **1.1 Simulation Environment** | Simulation Engineer | Mine world SDF, procedural tunnels, rock scree, simulated RF attenuation | `simulation/worlds/**`, `simulation/models/**`, `src/layer1_robot_environment/sim_plugins/**` | `src/layer2_*`, `interfaces/*` | None | Module 1.2, Module 1.3 | None |
| **1.2 Robot Models** | Mechatronics / ROS Control Lead | Robot A diff-drive and Robot B tracked URDF/Xacro, sensor rigging, `ros2_control` velocity controllers | `simulation/models/robot_a/**`, `simulation/models/robot_b/**`, `config/nav2/**` | `interfaces/*`, `src/layer2_*` | Module 1.1 | Module 1.3, Module 1.4 | None |
| **1.3 Perception & Localization** | Perception & SLAM Engineer | Point cloud filtering (PCL), camera/thermal parsing (OpenCV), SLAM Toolbox, dual EKF localization | `src/layer1_robot_environment/perception/**`, `config/slam/**`, `config/ekf/**` | `interfaces/*`, `src/layer2_*` | Module 1.2 | Module 1.4, Module 1.5 | None |
| **1.4 Navigation & Motion** | Navigation & Controls Lead | Nav2 Smac global planner, MPPI trajectory controller, obstacle avoidance, recovery behaviors | `src/layer1_robot_environment/navigation/**`, `config/nav2/**` | `interfaces/*`, `src/layer2_*` | Module 1.3 | Module 1.5 | None |
| **1.5 Robot Agent** | Local Autonomy & Safety Lead | Platform identity, capability loader, FSM state manager, `ExecuteTask.action` server, Authoritative Local Safety Manager (50 Hz) | `src/layer1_robot_environment/robot_agent/**` | `simulation/*`, `src/layer2_*` | Module 1.4 | Module 2.8 | **`RobotTelemetry`**, **`SafetyStatus`**, **`ExecuteTask`**, **`ExecuteInspectionTask`** |
| **1.6 Robot Communication Interface** | Embedded Middleware Engineer | Namespaced ROS 2 publishers/subscribers, telemetry aggregation (5 Hz), link health diagnostics; authorized publisher of `RobotTelemetry` per Module 1.5 interface contract | `src/layer1_robot_environment/communication/**` | `interfaces/*`, `src/layer3_*` | Module 1.5 | Module 2.1, Module 2.8 | None (authorized publisher of `RobotTelemetry`) |

---

### Layer 2: Distributed Autonomy Layer

| Module ID & Name | Designated Owner | Core Responsibilities | Permitted Write Files | Prohibited Files | Upstream Dependencies | Downstream Consumers | Shared Interface Ownership |
|---|---|---|---|---|---|---|---|
| **2.1 Robot Discovery** | Distributed Systems Lead | Zero-conf peer scouting (Zenoh), live peer roster, 2 Hz gossip heartbeat, $\phi$-accrual failure detection | `src/layer2_distributed_autonomy/discovery/**` | `src/layer1_*`, `interfaces/*` | Module 1.6 | Module 2.2, Module 2.7 | None |
| **2.2 Capability Management** | Distributed Systems Engineer | Capability model parsing, P2P capability exchange, bitmask constraint matching, resource monitoring | `src/layer2_distributed_autonomy/capabilities/**` | `src/layer1_*`, `interfaces/*` | Module 2.1 | Module 2.4 | **`CapabilityProfile`** |
| **2.3 Mission & Task Management** | Autonomy Logic Engineer | Mission DAG parsing, task decomposition, in-degree dependency unblocking, priority queues, task FSM | `src/layer2_distributed_autonomy/tasks/**` | `src/layer1_*`, `interfaces/*` | None | Module 2.4, Module 2.6 | **`TaskDefinition`** |
| **2.4 Distributed Task Allocation** | Distributed Algorithms Lead | Contract Net Protocol (CNP) bidding workers, multi-factor cost scoring, auction clearing, 2PC lease assignment | `src/layer2_distributed_autonomy/allocation/**` | `src/layer1_*`, `interfaces/*` | Module 2.2, Module 2.3 | Module 2.5, Module 2.6 | **`TaskAssignment`** |
| **2.5 Distributed Coordination** | Multi-Agent Coordination Lead | 4D trajectory intent sharing, temporary coordinator election, single-lane drift right-of-way, barrier synchronization | `src/layer2_distributed_autonomy/coordination/**` | `src/layer1_*`, `interfaces/*` | Module 2.4 | Module 2.8 | None |
| **2.6 Distributed State Management** | Distributed Data Engineer | Replicated in-memory key-value store, WAL persistence, delta-CRDT engine (LWW / OR-Set), causal vector clocks | `src/layer2_distributed_autonomy/state/**` | `src/layer1_*`, `interfaces/*` | Module 2.4 | Module 2.7, Module 3.2 | None |
| **2.7 Fault Tolerance & Recovery** | Autonomy Resilience Engineer | Multi-tier failure classifier, offline blackout policy, last-gasp crash handler, lease revocation/re-auction loop | `src/layer2_distributed_autonomy/fault_recovery/**` | `src/layer1_*`, `interfaces/*` | Module 2.1, Module 2.6 | Module 2.4 | None |
| **2.8 Distributed Runtime Interface** | Inter-Layer Integration Lead | Robot Agent Gateway (action client to L1), Mission Ingestion API, distributed event bus, OpenTelemetry tracing | `src/layer2_distributed_autonomy/runtime_interface/**` | `simulation/*`, `src/layer3_*` | Module 1.5, Module 2.4 | Module 1.5, Module 3.2 | **`SubmitTask`** |

---

### Layer 3: Mission and Operations Layer

| Module ID & Name | Designated Owner | Core Responsibilities | Permitted Write Files | Prohibited Files | Upstream Dependencies | Downstream Consumers | Shared Interface Ownership |
|---|---|---|---|---|---|---|---|
| **3.1 Mission Planning** | Frontend / UX Engineer | Visual DAG workflow studio (ReactFlow), pre-flight validation CLI, asset objective parameterizer | `src/layer3_mission_operations/planning/**` | `src/layer1_*`, `src/layer2_*` | None | Module 3.2 | None |
| **3.2 Mission Management** | Backend Operations Lead | Mission submission gateway, progress aggregator, top-level mission lifecycle FSM, immutable audit log | `src/layer3_mission_operations/mission_management/**` | `src/layer1_*`, `src/layer2_*` | Module 2.8 | Module 3.4, Module 3.5 | **`MissionStatus`** |
| **3.3 Inspection Management** | Inspection & QA Engineer | Asset registry (PostGIS), visual RGB evidence pipeline, radiometric thermal analyzer, hazard logger, scorecards | `src/layer3_mission_operations/inspection/**` | `src/layer1_*`, `src/layer2_*` | Module 1.3, Module 2.8 | Module 3.5 | None |
| **3.4 Monitoring & Visualization** | Web Frontend Lead | Deck.gl 2D/3D mine map canvas, robot trajectory trails, Gantt auction visualizer, health telemetry gauges | `src/layer3_mission_operations/dashboard/**` | `src/layer1_*`, `src/layer2_*` | Module 3.2, Module 3.3 | External Users | None |
| **3.5 Data Management & Reporting** | Database & DevOps Engineer | PostgreSQL relational schemas, TimescaleDB hypertables, MinIO S3 evidence store, Jinja2/WeasyPrint PDF compiler | `src/layer3_mission_operations/storage/**`, `config/storage/**` | `src/layer1_*`, `src/layer2_*` | Module 3.2, Module 3.3 | Module 3.6 | None |
| **3.6 External Integration & SDK** | API & Integrations Engineer | Python Public SDK (`antigravity_mine_sdk`), OpenAPI 3.0 REST/WebSocket gateway, OEM HAL adapters, SAP/Maximo connectors | `src/layer3_mission_operations/integration/**`, `interfaces/sdk/**` | `src/layer1_*`, `src/layer2_*` | Module 3.2, Module 3.5 | External Clients | None |

---

## 3. Strict Rules for Modifying Shared Files
1. **Interface Immutability**: No developer may edit files in `interfaces/msg/`, `interfaces/srv/`, `interfaces/action/`, or `interfaces/schemas/` without an approved Architectural RFC signed off by the Technical Founder.
2. **Layer Isolation**: Layer 3 developers must never import or invoke `rclcpp` or Layer 1 hardware controller packages.
3. **Local Safety Invariant**: No developer working on Layer 2 or Layer 3 may modify or weaken the Layer 1 Local Safety Manager component (planned under Module 1.5 for Milestone M3).
