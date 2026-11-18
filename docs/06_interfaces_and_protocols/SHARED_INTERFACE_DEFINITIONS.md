# Shared Interface Definitions Specification

## 1. Overview & Architectural Role
To ensure that multiple robotics, perception, controls, and distributed systems developers can develop modules independently without causing integration conflicts, all cross-module and cross-layer interactions must strictly adhere to the standardized shared interfaces documented herein.

### Separation of Schema Ownership and Data Production
A foundational governance invariant in this platform is the explicit distinction between **Schema Ownership** and **Data Production / Publishing**:
- **Schema Ownership**: Vested in exactly one designated module lead who maintains the ROS 2 IDL message, service, action, or JSON schema specification, guarantees field type integrity, enforces semantic validation rules, and manages SemVer evolution. No other module or developer may modify or extend the schema definition without an approved Architectural RFC signed off by the Technical Founder.
- **Data Production & Publishing**: Other functional modules may be explicitly authorized to produce, serialize, aggregate, or publish data conforming to that schema, strictly bound by the owner's interface contract. Authorized publishers cannot alter, omit required fields, or mutate the underlying interface contract.

Every interface defined in this repository has:
1. **Exactly One Schema Owner**: The designated module lead responsible for schema changes and backward compatibility.
2. **Defined Producers & Publishers**: The explicit software components authorized to originate and publish data under this contract.
3. **Defined Consumers**: The explicit software components authorized to subscribe, query, or ingest this data.
4. **Strict Data Types**: Fully defined primitive types, message fields, and schemas.
5. **Formal Versioning Rules**: Explicit Semantic Versioning (SemVer) guidelines and breaking change deprecation procedures.

These interfaces are currently **PROPOSED** specifications subject to empirical verification during milestone integration testing.

---

## 2. Shared Interface Catalog

### 2.1 Interface: `RobotTelemetry` (`interfaces/msg/RobotTelemetry.msg`)
- **Purpose**: Represents the real-time kinematic, physical, and operational state of an individual robot.
- **Single Schema Owner**: **Module 1.5 (Local Autonomy & Safety Lead)**. Module 1.5 possesses exclusive schema ownership over `interfaces/msg/RobotTelemetry.msg`, maintaining field definitions, coordinate frame semantics, and SemVer version evolution.
- **Data Production & Publishing Roles**:
  - **State Originator / Primary Producer**: **Module 1.5 Robot Agent**. Module 1.5 originates the robot's lifecycle FSM state, active task binding, and core operational status.
  - **Authorized Network Publisher**: **Module 1.6 State Publisher / Robot Communication Interface**. Module 1.6 is authorized to serialize, schedule, and publish `RobotTelemetry` messages over local ROS 2 topics (`/{robot_name}/telemetry` at 5 Hz) and bridge them over Eclipse Zenoh (`mine/peers/{uuid}/telemetry`) according to the approved Module 1.5 interface contract. Module 1.6 has no authority to alter message fields or schema structure.
- **Defined Consumers**: Module 2.1 Peer Discovery, Module 2.4 Distributed Task Allocation, Module 2.6 State Management, Module 3.4 Monitoring Dashboard.
- **Data Types & Fields** (`interfaces/msg/RobotTelemetry.msg`):
  - `std_msgs/Header header`: Monotonic timestamp and coordinate frame reference (`map` or `odom`).
  - `string robot_id`: UUIDv4 string uniquely identifying the platform.
  - `string archetype`: Categorization (`EXPLORATION_SCOUT` or `INSPECTION_SPECIALIST`).
  - `geometry_msgs/PoseWithCovariance pose`: Estimated 3D Cartesian position and quaternion orientation with covariance matrix.
  - `geometry_msgs/Twist velocity`: Current linear and angular velocities ($v_x, v_y, v_z, \omega_x, \omega_y, \omega_z$).
  - `float32 battery_soc_percent`: Battery state-of-charge percentage (0.0 to 100.0%).
  - `string fsm_state`: Active lifecycle state (`UNINITIALIZED`, `IDLE`, `READY`, `EXECUTING_TASK`, `PAUSED`, `FAULT`, `EMERGENCY_STOP`).
  - `string active_task_id`: UUIDv4 string of currently active task, or empty string if idle.
- **Communication Mechanism**: Published locally via ROS 2 Topic `/{robot_name}/telemetry` at 5 Hz; bridged over Eclipse Zenoh as `mine/peers/{uuid}/telemetry`.
- **Validation Rules**:
  - `battery_soc_percent` must be between $0.0$ and $100.0$.
  - Pose covariance diagonal elements must be positive semi-definite.
  - `robot_id` must conform to UUIDv4 regex `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`.
- **Versioning Rules**:
  - Current Version: `v1.0.0` (SemVer).
  - Backwards-compatible additions: New optional fields may be appended at the end of the message definition with minor version bumps (`v1.1.0`).
  - Breaking changes: Renaming, reordering, deleting fields, or modifying types requires a major version bump (`v2.0.0`), an approved Architectural RFC, and a 2-milestone deprecation cycle.

---

### 2.2 Interface: `SafetyStatus` (`interfaces/msg/SafetyStatus.msg`)
- **Purpose**: Exposes instantaneous hardware safety watchdog status, collision clearances, and tip-over diagnostics.
- **Single Clear Owner**: Module 1.5 (Local Autonomy & Safety Lead).
- **Defined Producers**: Module 1.5 Local Safety Manager (authoritative 50 Hz watchdog).
- **Defined Consumers**: Module 1.4 Navigation & Motion (velocity override clamp), Module 1.6 Communication Interface, Module 3.4 Monitoring Dashboard.
- **Data Types & Fields** (`interfaces/msg/SafetyStatus.msg`):
  - `std_msgs/Header header`: Monotonic timestamp and base link frame.
  - `bool override_active`: True if local safety reflex has overridden motion commands to zero velocity.
  - `float32 min_obstacle_distance`: Minimum measured obstacle distance in meters from LiDAR/depth sensors.
  - `float32 roll_deg`: Current chassis roll inclination in degrees.
  - `float32 pitch_deg`: Current chassis pitch inclination in degrees.
  - `string fault_reason`: Diagnostic description (`NONE`, `OBSTACLE_ENVELOPE_BREACH`, `EXCESSIVE_TILT`, `HEARTBEAT_TIMEOUT`).
- **Communication Mechanism**: Published locally via ROS 2 Topic `/{robot_name}/safety/status` at 50 Hz.
- **Validation Rules**:
  - `min_obstacle_distance >= 0.0`.
  - `roll_deg` and `pitch_deg` within $[-180.0, +180.0]$.
- **Versioning Rules**:
  - Current Version: `v1.0.0`.
  - Additive diagnostic fields permitted in minor releases. Modifying existing field definitions requires major version increment and Technical Founder approval.

---

### 2.3 Interface: `CapabilityProfile` (`interfaces/schemas/capability_schema.json`)
- **Purpose**: Formally declares the physical locomotion capabilities, installed sensor payloads, allowable actions, and dynamic resource limits of a robot.
- **Single Clear Owner**: Module 2.2 (Capability Management Lead).
- **Defined Producers**: Module 2.2 Capability Model (with Module 1.5 local hardware introspection).
- **Defined Consumers**: Module 2.4 Distributed Task Allocation (Constraint Matcher), Module 3.1 Mission Planning Studio.
- **Data Types & Fields** (`interfaces/schemas/capability_schema.json`):
  - `robot_id` (`string`, UUIDv4): Unique robot identifier.
  - `archetype` (`string`): `EXPLORATION_SCOUT` or `INSPECTION_SPECIALIST`.
  - `locomotion` (`object`):
    - `type` (`string`): `DIFFERENTIAL_DRIVE`, `TRACKED_SKID_STEER`, or `LEGGED`.
    - `max_linear_speed_mps` (`number`): Maximum velocity in meters per second.
    - `max_incline_deg` (`number`): Maximum slope negotiable in degrees.
    - `obstacle_clearance_m` (`number`): Maximum step height clearance in meters.
  - `sensors` (`array of strings`): Active sensor modalities (`LIDAR_3D`, `RGB_OPTICAL`, `RADIOMETRIC_THERMAL`, `IMU_6DOF`, `GAS_DETECTOR`).
  - `certified_actions` (`array of strings`): Supported high-level tasks (`EXPLORE_FRONTIER`, `NAVIGATE_WAYPOINT`, `INSPECT_THERMAL`, `INSPECT_VISUAL`, `RENDEZVOUS`).
  - `resource_headroom` (`object`): Minimum battery reserve threshold percentage and storage capacity.
- **Communication Mechanism**: Zenoh Queryable on `mine/peers/{uuid}/capabilities` with local TTL caching.
- **Validation Rules**: Validated strictly against JSON Schema Draft-07 (`interfaces/schemas/capability_schema.json`).
- **Versioning Rules**:
  - Current Version: `v1.0.0`.
  - Additive optional properties permitted under `v1.x`. Changes to required properties or allowed enum values require a major schema version bump (`v2.0.0`).

---

### 2.4 Interface: `TaskDefinition` (`interfaces/schemas/task_schema.json`)
- **Purpose**: Defines an atomic, independently actionable, and verifiable unit of work within a mission DAG.
- **Single Clear Owner**: Module 2.3 (Mission & Task Management Lead).
- **Defined Producers**: Module 2.3 Mission & Task Management (DAG decomposition) / Module 3.1 Mission Planning.
- **Defined Consumers**: Module 2.4 Distributed Task Allocation, Module 1.5 Robot Agent (`ExecuteTask.action` server).
- **Data Types & Fields** (`interfaces/schemas/task_schema.json`):
  - `task_id` (`string`, UUIDv4): Unique task identifier.
  - `task_type` (`string`): `EXPLORE_FRONTIER`, `NAVIGATE_WAYPOINT`, `INSPECT_THERMAL`, `INSPECT_VISUAL`, or `RENDEZVOUS`.
  - `target_pose` (`object`): 3D Cartesian coordinates (`x, y, z`) and orientation quaternion (`x, y, z, w`).
  - `required_sensors` (`array of strings`): Modalities required to complete the task (e.g. `["RADIOMETRIC_THERMAL"]`).
  - `priority` (`integer`, 1 to 100): Priority tier where 1 is highest emergency and 100 is background exploration.
  - `dwell_time_sec` (`number`): Required observation duration at target waypoint.
  - `arrival_tolerance_m` (`number`): Spatial acceptance radius (default 0.3m).
  - `prerequisite_task_ids` (`array of strings`): Task UUIDs that must complete before this task can be auctioned.
- **Communication Mechanism**: Embedded in mission DAG payloads; announced over Zenoh topic `mine/auctions/{task_id}/announce`.
- **Validation Rules**: Validated against JSON Schema Draft-07 (`interfaces/schemas/task_schema.json`). Coordinates must lie within surveyed mine operational boundaries.
- **Versioning Rules**:
  - Current Version: `v1.0.0`.
  - New optional parameters (e.g. custom sensor exposure time) may be added in minor versions. Modifications to task type enums require major version bump.

---

### 2.5 Interface: `TaskAssignment` (`interfaces/msg/TaskAssignment.msg`)
- **Purpose**: Formal contract granting a specific robot exclusive authority to execute a designated task under a time-bounded lease.
- **Single Clear Owner**: Module 2.4 (Distributed Task Allocation Lead).
- **Defined Producers**: Module 2.4 Distributed Task Allocation (Auctioneer Node).
- **Defined Consumers**: Module 1.5 Robot Agent (ExecuteTask action server), Module 2.6 Distributed State Management (CRDT lease registry), Module 2.7 Fault Tolerance.
- **Data Types & Fields** (`interfaces/msg/TaskAssignment.msg`):
  - `string task_id`: UUIDv4 of the assigned task.
  - `string task_type`: Task category matching `task_schema.json`.
  - `string assigned_robot_id`: UUIDv4 of the winning bidder.
  - `geometry_msgs/PoseStamped target_pose`: Spatial waypoint.
  - `string lease_token`: Cryptographic lease token authorizing execution.
  - `uint64 lease_expiration_epoch_ms`: Monotonic millisecond timestamp when lease expires unless renewed.
- **Communication Mechanism**: Zenoh Topic `mine/auctions/{task_id}/lease`; ROS 2 Topic `/{robot_name}/task_command`.
- **Validation Rules**:
  - `lease_expiration_epoch_ms` must be strictly greater than current cluster epoch.
  - `assigned_robot_id` must match a known active peer in the discovery roster.
- **Versioning Rules**:
  - Current Version: `v1.0.0`.
  - Lease token signing algorithm updates require protocol negotiation; breaking format changes require major version increment.

---

### 2.6 Interface: `ExecuteTask` Action (`interfaces/action/ExecuteTask.action`)
- **Purpose**: Standardized ROS 2 Action interface between Layer 2 autonomy and Layer 1 robot agent for executing high-level tasks.
- **Single Clear Owner**: Module 1.5 (Local Autonomy & Safety Lead).
- **Defined Producers**: Module 2.8 Distributed Runtime Gateway (Action Client).
- **Defined Consumers**: Module 1.5 Robot Agent (Action Server).
- **Data Types & Fields** (`interfaces/action/ExecuteTask.action`):
  - **Goal**:
    - `string task_id`: Unique task UUID.
    - `string task_type`: Work category.
    - `geometry_msgs/PoseStamped target_pose`: Destination pose.
    - `string[] required_sensors`: Sensor modality constraints.
    - `float32 dwell_time_sec`: Observation duration.
    - `string lease_token`: Active lease authorization token.
  - **Result**:
    - `uint8 STATUS_SUCCESS = 0`
    - `uint8 STATUS_SAFETY_ABORT = 1`
    - `uint8 STATUS_TIMEOUT = 2`
    - `uint8 STATUS_STALLED = 3`
    - `uint8 status_code`: Execution termination status.
    - `string evidence_uri`: URI path to captured inspection artifacts.
    - `string message`: Human-readable completion or failure diagnostic.
  - **Feedback**:
    - `float32 percent_complete`: Progress percentage (0.0 to 100.0%).
    - `float32 distance_remaining`: Metric distance to target waypoint.
    - `builtin_interfaces/Duration time_elapsed`: Elapsed execution duration.
    - `string current_substate`: Lifecycle sub-state (`NAVIGATING`, `DWELLING`, `INSPECTING`).
- **Communication Mechanism**: ROS 2 Action client-server over intra-robot DDS (`/{robot_name}/execute_task`).
- **Validation Rules**: Goals rejected if `lease_token` is missing or expired, or if target coordinates are outside Nav2 costmap limits.
- **Versioning Rules**:
  - Current Version: `v1.0.0`.
  - Result status codes are strictly append-only. Modifying numeric values of existing codes is prohibited.

---

### 2.7 Interface: `ExecuteInspectionTask` Action (`interfaces/action/ExecuteInspectionTask.action`)
- **Purpose**: Specialized inspection action interface for targeted optical and radiometric thermal data collection.
- **Single Clear Owner**: Module 1.5 (Local Autonomy & Safety Lead).
- **Defined Producers**: Module 2.8 Distributed Runtime Gateway (Action Client).
- **Defined Consumers**: Module 1.5 Robot Agent (Robot B Inspection Specialist Server).
- **Data Types & Fields** (`interfaces/action/ExecuteInspectionTask.action`):
  - **Goal**:
    - `string task_id`: Task UUID.
    - `string asset_id`: Asset identifier (e.g. `PUMP_STATION_04`).
    - `geometry_msgs/PoseStamped target_pose`: Robot inspection vantage point.
    - `float32 pan_angle_deg`: Sensor pan gimbal angle.
    - `float32 tilt_angle_deg`: Sensor tilt gimbal angle.
    - `bool capture_thermal`: True to capture radiometric thermal matrix.
    - `bool capture_rgb`: True to capture high-definition optical frame.
  - **Result**:
    - `uint8 status_code`: Success/failure status.
    - `float32 peak_temperature_celsius`: Maximum detected temperature in target bounding region.
    - `bool anomaly_detected`: True if thermal threshold exceeded.
    - `string evidence_uri`: Storage path of captured radiometric file.
  - **Feedback**:
    - `float32 percent_complete`: Progress percentage.
    - `string status_message`: Inspection diagnostic.
- **Communication Mechanism**: ROS 2 Action client-server over intra-robot DDS (`/{robot_name}/execute_inspection`).
- **Validation Rules**: `pan_angle_deg` and `tilt_angle_deg` clamped within hardware gimbal limits ($[-90^\circ, +90^\circ]$).
- **Versioning Rules**:
  - Current Version: `v1.0.0`.
  - Additive feedback parameters permitted under minor releases.

---

### 2.8 Interface: `SubmitTask` Service (`interfaces/srv/SubmitTask.srv`)
- **Purpose**: Synchronous service for external operators or surface planning systems to inject ad-hoc inspection tasks into the autonomy cluster.
- **Single Clear Owner**: Module 2.8 (Distributed Runtime Interface Lead).
- **Defined Producers**: Module 3.2 Mission Management / External SDK Client.
- **Defined Consumers**: Module 2.3 Mission & Task Management (via Module 2.8 Runtime Gateway).
- **Data Types & Fields** (`interfaces/srv/SubmitTask.srv`):
  - **Request**:
    - `string task_id`: UUIDv4 string.
    - `string task_json`: JSON-serialized task matching `task_schema.json`.
  - **Response**:
    - `bool accepted`: True if task schema validated and task queued for auction.
    - `string message`: Validation diagnostic or error explanation.
- **Communication Mechanism**: ROS 2 Service `/{robot_name}/submit_task` or Zenoh Queryable `mine/tasks/submit`.
- **Validation Rules**: Request `task_json` must pass validation against `interfaces/schemas/task_schema.json`.
- **Versioning Rules**:
  - Current Version: `v1.0.0`.
  - Service request/response signature is immutable without major version bump.

---

### 2.9 Interface: `MissionStatus` (`interfaces/schemas/mission_schema.json`)
- **Purpose**: Provides aggregate cluster-wide situational awareness regarding overall mission progress, asset scorecards, and fleet status.
- **Single Clear Owner**: Module 3.2 (Mission Management Lead).
- **Defined Producers**: Module 3.2 Mission Management (Progress Aggregator).
- **Defined Consumers**: Module 3.4 Monitoring & Visualization (Web Dashboard), Enterprise API clients.
- **Data Types & Fields** (`interfaces/schemas/mission_schema.json`):
  - `mission_id` (`string`, UUIDv4): Active mission identifier.
  - `top_level_status` (`string`): `DRAFT`, `VALIDATED`, `SUBMITTED`, `IN_PROGRESS`, `PAUSED`, `ABORTED`, `COMPLETED`.
  - `total_tasks` (`integer`): Total number of atomic tasks in the mission DAG.
  - `completed_tasks` (`integer`): Count of successfully completed tasks.
  - `failed_tasks` (`integer`): Count of permanently failed tasks.
  - `active_allocations` (`array of objects`): Array of `{task_id, robot_id, start_time}` for currently executing tasks.
  - `estimated_remaining_seconds` (`number`): Critical-path projected completion time.
  - `critical_hazards_detected` (`integer`): Count of unmitigated high-priority hazard alerts.
- **Communication Mechanism**: WebSocket feed `/ws/mission_status`; REST endpoint `GET /api/v1/missions/{id}/status`.
- **Validation Rules**: `completed_tasks + failed_tasks <= total_tasks`.
- **Versioning Rules**:
  - Current Version: `v1.0.0`.
  - Additional progress metrics (e.g. total distance traversed) may be added as optional fields in minor versions.
