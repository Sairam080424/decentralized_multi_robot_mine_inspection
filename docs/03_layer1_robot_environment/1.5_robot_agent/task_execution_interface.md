# Submodule 1.5.4: Task Execution Interface

## 1. Purpose
Provides a standardized ROS 2 Action Server that consumes high-level task goals from Layer 2, dispatches them to Nav2 and sensor pipelines, and reports execution progress.

## 2. Responsibility
Accept abstract task goals (`EXPLORE_FRONTIER`, `NAVIGATE_TO_WAYPOINT`, `INSPECT_THERMAL`, `INSPECT_VISUAL`), orchestrate lower-level execution, monitor progress, and return results.

## 3. Scope
### In-Scope
`ExecuteTask.action` server, goal validation, Nav2 client dispatching, camera capture triggering, and execution feedback publishing.

### Out-of-Scope
Decentralized task bidding and negotiation (handled by Layer 2).

## 4. System Architecture
```mermaid
flowchart TD
    L2_Alloc["Layer 2 Task Allocator"] -->|Send Goal| ActionServer["ExecuteTask.action Server"]
    ActionServer --> Validate["Validate Task Lease & Params"]
    Validate --> Dispatcher{"Task Type Dispatcher"}
    Dispatcher -->|NAVIGATE| Nav2Client["Nav2 Action Client"]
    Dispatcher -->|INSPECT_THERMAL| ThermalClient["Thermal Inspection Trigger"]
    Dispatcher -->|EXPLORE| ExploreClient["Frontier Exploration Client"]
    Nav2Client --> ActionServer
    ThermalClient --> ActionServer
    ActionServer -->|Feedback (Progress %)| L2_Alloc
    ActionServer -->|Result (SUCCESS / FAIL)| L2_Alloc
```

## 5. Internal Submodules
- **Task Action Dispatcher**: Routes incoming task goals to appropriate local subsystem action clients.
- **Progress & Feedback Monitor**: Calculates distance-to-goal, estimated time of arrival (ETA), and streams feedback at 2 Hz.

## 6. Functional Requirements
- **REQ-1.5-007**: Action server shall accept or reject incoming task goals within `[PROPOSED TARGET: < 50 ms]`.
- **REQ-1.5-008**: Action server shall support asynchronous goal cancellation from Layer 2.

## 7. Technical Approach
Implement `rclcpp_action::Server<ExecuteTask>` node in C++. Translate high-level task coordinates into Nav2 `NavigateToPose` goals, monitoring execution and handling preemption cleanly.

## 8. Open-Source Resources
### rclcpp_action
- **What it provides**: ROS 2 Action Client and Server C++ API.
- **Why it is relevant**: Standard ROS 2 paradigm for long-running preemptible tasks.
- **What we can reuse**: Core action server templates.
- **What we must develop ourselves**: Execution state machine mapping abstract task parameters to Nav2.


## 9. Prerequisites
Submodule 1.5.3 State Manager, Submodule 1.4.2 Navigation, `interfaces` package.

## 10. Dependencies
- **Upstream Dependencies**: Submodule 1.5.3 Robot State Manager, Module 1.4 Navigation.
- **Downstream Dependencies**: Module 2.8 Distributed Runtime Interface.
- **Interfaces with Other Modules**: ROS 2 Action `ExecuteTask.action`.

## 11. Development Phases
### Phase 1: Action Server Implementation
- **Objective**: Implement ExecuteTask action server.
- **Activities**: Code action callbacks, bridge to Nav2 action client.
- **Required resources**: C++, ROS 2.
- **Input**: ExecuteTask.action definition.
- **Output**: TaskExecutionServer node.
- **Dependencies**: None.
- **Validation**: Send test action goal via CLI; verify Nav2 executes path.
- **Completion criteria**: Action returns SUCCESS upon waypoint arrival.


## 12. Interfaces
### Actions
- `/robot_a/execute_task`: Custom ExecuteTask action accepting task_id, task_type, coordinates, and lease_token.


## 13. Testing Strategy
Send task goal with 5.0m waypoint; cancel goal halfway through execution; verify robot decelerates to stop and reports PREEMPTED result.

## 14. Known Challenges
- **Goal Preemption Race Conditions**: Cancelling a task while Nav2 is transitioning recovery behaviors requires rigorous mutex locking to prevent stale velocity commands.

## 15. Implementation Status
`PLANNED`

## 16. References
- [ROS 2 Actions Documentation](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Cpp.html)
