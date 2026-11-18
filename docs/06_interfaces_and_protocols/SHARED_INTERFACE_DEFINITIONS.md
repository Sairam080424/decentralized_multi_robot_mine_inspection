# Shared Interface Definitions Specification

## 1. Overview & Architectural Role
To ensure that multiple robotics and distributed systems developers can develop modules independently without causing integration conflicts, all cross-module and cross-layer interactions must strictly adhere to the standardized shared interfaces documented herein.

These interfaces are currently **PROPOSED** specifications subject to empirical verification during milestone integration testing.

---

## 2. Shared Interface Catalog

### 2.1 Interface: `RobotState`
- **Purpose**: Represents the real-time kinematic, physical, and operational state of an individual robot.
- **Data Fields & Types**:
  - `header` (`std_msgs/Header`): Monotonic timestamp and coordinate frame reference (`map` or `odom`).
  - `robot_id` (`string`): UUIDv4 string uniquely identifying the platform.
  - `archetype` (`string`): Categorization (`EXPLORATION_SCOUT` or `INSPECTION_SPECIALIST`).
  - `pose` (`geometry_msgs/PoseWithCovariance`): Estimated 3D Cartesian position and quaternion orientation with covariance matrix.
  - `velocity` (`geometry_msgs/Twist`): Current linear and angular velocities ($v_x, v_y, v_z, \omega_x, \omega_y, \omega_z$).
  - `battery_soc_percent` (`float32`): Battery state-of-charge percentage (0.0 to 100.0%).
  - `fsm_state` (`string`): Active lifecycle state (`UNINITIALIZED`, `IDLE`, `READY`, `EXECUTING_TASK`, `PAUSED`, `FAULT`, `EMERGENCY_STOP`).
  - `active_task_id` (`string`): UUIDv4 string of currently active task, or empty string if idle.
- **Producer**: Module 1.5 Robot Agent / Module 1.6 State Publisher (running locally on each robot).
- **Consumers**: Module 2.1 Discovery, Module 2.4 Task Allocation, Module 2.6 State Management, Module 3.4 Monitoring Dashboard.
- **Ownership**: Module 1.5 (Robot Agent Team).
- **Communication Mechanism**: Published locally via ROS 2 Topic `/robot_name/telemetry` at 5 Hz; bridged over Eclipse Zenoh as `mine/peers/{uuid}/telemetry`.
- **Validation Rules**:
  - `battery_soc_percent` must be between $0.0$ and $100.0$.
  - Pose covariance diagonal elements must be positive semi-definite.
  - `robot_id` must match regex `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`.
- **Versioning Considerations**: SemVer 1.0.0. Backwards-compatible field additions only; removal of existing fields requires an Architectural RFC.

---

### 2.2 Interface: `CapabilityProfile`
- **Purpose**: Formally declares the physical locomotion capabilities, installed sensor payloads, allowable actions, and dynamic resource limits of a robot.
- **Data Fields & Types**:
  - `robot_id` (`string`): UUIDv4 string of the declaring robot.
  - `archetype` (`string`): `EXPLORATION_SCOUT` or `INSPECTION_SPECIALIST`.
  - `locomotion` (`object`):
    - `type` (`string`): `DIFFERENTIAL_DRIVE`, `TRACKED_SKID_STEER`, or `LEGGED`.
    - `max_linear_speed_mps` (`float32`): Maximum velocity in meters per second.
    - `max_incline_deg` (`float32`): Maximum slope negotiable in degrees.
    - `obstacle_clearance_m` (`float32`): Maximum step height clearance in meters.
  - `sensors` (`string[]`): Array of active sensor modalities (`LIDAR_3D`, `RGB_OPTICAL`, `RADIOMETRIC_THERMAL`, `IMU_6DOF`, `GAS_DETECTOR`).
  - `certified_actions` (`string[]`): Array of supported high-level tasks (`EXPLORE_FRONTIER`, `NAVIGATE_WAYPOINT`, `INSPECT_THERMAL`, `INSPECT_VISUAL`, `RENDEZVOUS`).
  - `resource_headroom` (`object`): Minimum battery reserve threshold (e.g. 20%) and storage capacity.
- **Producer**: Module 1.5 Robot Agent / Module 2.2 Capability Management.
- **Consumers**: Module 2.4 Task Allocation (Constraint Matcher), Module 3.1 Mission Planning Studio.
- **Ownership**: Module 2.2 (Capability Management Team).
- **Communication Mechanism**: Zenoh Queryable on `mine/peers/{uuid}/capabilities` with local TTL caching.
- **Validation Rules**: Validated against JSON Schema `interfaces/schemas/capability_schema.json`.
- **Versioning Considerations**: Dynamic capabilities (e.g., sensor failure) publish delta updates removing the defective modality without changing schema version.

---

### 2.3 Interface: `TaskDefinition`
- **Purpose**: Defines an atomic, independently actionable, and verifiable unit of work within a mission DAG.
- **Data Fields & Types**:
  - `task_id` (`string`): UUIDv4 unique task identifier.
  - `task_type` (`string`): `EXPLORE_FRONTIER`, `NAVIGATE_WAYPOINT`, `INSPECT_THERMAL`, `INSPECT_VISUAL`, or `RENDEZVOUS`.
  - `target_pose` (`geometry_msgs/PoseStamped`): 3D Cartesian coordinates and desired sensor orientation.
  - `required_sensors` (`string[]`): Modalities required to complete the task (e.g. `["RADIOMETRIC_THERMAL"]`).
  - `priority` (`uint8`): Priority tier from 1 (Emergency) to 100 (Exploration).
  - `dwell_time_sec` (`float32`): Required observation duration at target waypoint.
  - `arrival_tolerance_m` (`float32`): Spatial acceptance radius (default 0.3m).
  - `prerequisite_task_ids` (`string[]`): List of task UUIDs that must reach `COMPLETED` before this task can be auctioned.
- **Producer**: Module 2.3 Mission & Task Management (via DAG decomposition) or Module 3.1 Mission Planning.
- **Consumers**: Module 2.4 Task Allocation, Module 1.5 Robot Agent (ExecuteTask action server).
- **Ownership**: Module 2.3 (Task Management Team).
- **Communication Mechanism**: Embedded inside mission DAG payloads; announced over Zenoh topic `mine/auctions/{task_id}/announce`.
- **Validation Rules**: Validated against JSON Schema `interfaces/schemas/task_schema.json`. Coordinate positions must fall within mine boundary polygon.
- **Versioning Considerations**: Compatible extensions may add optional sensor tuning parameters (e.g., thermal emissivity factor).

---

### 2.4 Interface: `TaskAssignment`
- **Purpose**: Formal contract granting a specific robot exclusive authority to execute a designated task under a time-bounded lease.
- **Data Fields & Types**:
  - `task_id` (`string`): UUIDv4 of the assigned task.
  - `assigned_robot_id` (`string`): UUIDv4 of the winning bidder.
  - `lease_token` (`string`): Cryptographic token authorizing execution.
  - `lease_granted_epoch_ms` (`uint64`): Timestamp when lease was issued.
  - `lease_expiration_epoch_ms` (`uint64`): Timestamp when lease expires unless renewed.
  - `agreed_cost` (`float32`): Winning bid cost recorded for audit.
- **Producer**: Module 2.4 Distributed Task Allocation (Auction Clearing House).
- **Consumers**: Winning robot's Module 2.8 Gateway and Module 1.5 Action Server; peer lease registries.
- **Ownership**: Module 2.4 (Task Allocation Team).
- **Communication Mechanism**: Zenoh Topic `mine/auctions/{task_id}/lease`; ROS 2 Topic `/robot_name/task_command`.
- **Validation Rules**:
  - `lease_expiration_epoch_ms` must be greater than `lease_granted_epoch_ms`.
  - `lease_token` signature must verify against auctioneer public key.
- **Versioning Considerations**: If lease renewal mechanism is upgraded, token header must encode protocol version.

---

### 2.5 Interface: `TaskResult`
- **Purpose**: Encapsulates the verified outcome, sensor evidence references, and performance metrics of a finished task.
- **Data Fields & Types**:
  - `task_id` (`string`): UUIDv4 of the completed task.
  - `executing_robot_id` (`string`): UUIDv4 of the robot that performed the task.
  - `status_code` (`uint8`): `0=STATUS_SUCCESS`, `1=STATUS_SAFETY_ABORT`, `2=STATUS_TIMEOUT`, `3=STATUS_STALLED`.
  - `completion_timestamp` (`uint64`): Monotonic timestamp of completion.
  - `evidence_uris` (`string[]`): URIs pointing to stored visual images, radiometric HDF5 files, or point clouds.
  - `peak_temperature_celsius` (`float32`): Peak measured temperature (applicable for thermal tasks).
  - `anomaly_flag` (`bool`): True if measured value exceeded asset critical threshold.
  - `failure_error_code` (`uint16`): Standardized 16-bit error code (0x0000 on success).
- **Producer**: Module 1.5 Robot Agent / Module 2.8 Runtime Gateway.
- **Consumers**: Module 2.3 Task Management (Dependency unblocking), Module 2.6 State Engine (CRDT commit), Module 3.3 Inspection Management.
- **Ownership**: Module 1.5 / Module 2.8.
- **Communication Mechanism**: ROS 2 Action Result `ExecuteTask.action`; Zenoh event `mine/events/task/completed`.
- **Validation Rules**: If `status_code == 0`, `evidence_uris` must not be empty for inspection tasks.
- **Versioning Considerations**: New sensory measurement summaries can be appended as optional fields.

---

### 2.6 Interface: `MissionStatus`
- **Purpose**: Provides aggregate cluster-wide situational awareness regarding overall mission progress, asset scorecards, and fleet status.
- **Data Fields & Types**:
  - `mission_id` (`string`): UUIDv4 of the active mission.
  - `top_level_status` (`string`): `DRAFT`, `VALIDATED`, `SUBMITTED`, `IN_PROGRESS`, `PAUSED`, `ABORTED`, `COMPLETED`.
  - `total_tasks` (`uint32`): Total number of atomic tasks in the mission DAG.
  - `completed_tasks` (`uint32`): Count of successfully completed tasks.
  - `failed_tasks` (`uint32`): Count of permanently failed tasks.
  - `active_allocations` (`object[]`): Array of `{task_id, robot_id, start_time}` for currently executing tasks.
  - `estimated_remaining_seconds` (`float32`): Critical-path projected completion time.
  - `critical_hazards_detected` (`uint32`): Count of unmitigated high-priority hazard alerts.
- **Producer**: Module 3.2 Mission Management (Progress Aggregator).
- **Consumers**: Module 3.4 Monitoring & Visualization (Web Dashboard), Enterprise API clients.
- **Ownership**: Module 3.2 (Mission Management Team).
- **Communication Mechanism**: WebSocket feed `/ws/mission_status`; REST endpoint `GET /api/v1/missions/{id}/status`.
- **Validation Rules**: `completed_tasks + failed_tasks <= total_tasks`.
- **Versioning Considerations**: Extended progress metrics (e.g. total distance traversed) can be added cleanly.
