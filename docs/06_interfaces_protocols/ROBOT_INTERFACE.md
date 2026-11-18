# Robot Interface Contract (Layer 1 <-> Layer 2)

## 1. Overview
The Robot Interface defines the strict, decoupled boundary between each physical/simulated robot platform (Layer 1) and its distributed autonomy kernel (Layer 2).

## 2. Topic & Action Interface Definitions

All topics and actions are strictly scoped within the robot's assigned namespace (`/robot_a` or `/robot_b`).

### Actions (Commands from Layer 2 to Layer 1)
- `execute_task` (`interfaces/action/ExecuteTask.action`):
  - **Goal**: `string task_id`, `string task_type`, `geometry_msgs/PoseStamped target_pose`, `string[] required_sensors`, `float32 dwell_time`, `string lease_token`.
  - **Feedback**: `float32 percent_complete`, `float32 distance_remaining`, `duration time_elapsed`, `string current_substate`.
  - **Result**: `uint8 status_code` (0=SUCCESS, 1=SAFETY_ABORT, 2=TIMEOUT, 3=STALLED), `string evidence_uri`, `string message`.

### Topics Published by Layer 1 to Layer 2
- `telemetry` (`interfaces/msg/RobotTelemetry.msg`): 5 Hz composite state containing EKF pose, twist, battery SoC, FSM state, and active task ID.
- `safety/status` (`interfaces/msg/SafetyStatus.msg`): 50 Hz proximity and tilt warnings, override active flag.
- `capabilities` (`interfaces/msg/RobotCapabilities.msg`): Broadcast on boot and status change declaring available sensors and operational payloads.

### Topics Subscribed by Layer 1 from Layer 2
- `task_command` (`interfaces/msg/TaskAssignment.msg`): Dispatched task assignments with lease tokens.
- `emergency_abort` (`std_msgs/msg/Empty`): Instant emergency brake command.
