# Module 1.6: Robot Communication Interface

## 1. Module Overview
Module 1.6 establishes the namespaced ROS 2 communication infrastructure for each robot. It standardizes topic naming conventions, quality-of-service (QoS) profiles, telemetry state publishing, task command subscriptions, and local link health diagnostics.

## 2. Submodule Index
- [1.6.1 ROS 2 Interface](ros2_interface.md): Strict namespace isolation (`/robot_a/...`, `/robot_b/...`), ROS domain IDs, and QoS profiles.
- [1.6.2 State Publisher](state_publisher.md): High-frequency telemetry broadcasting (pose, velocities, battery, diagnostics).
- [1.6.3 Task Subscriber](task_subscriber.md): Task goal ingestion, lease token validation, and preemption listeners.
- [1.6.4 Action Interface](action_interface.md): Standardized ROS 2 Action servers for complex long-duration robotic behaviors.
- [1.6.5 Communication Health](communication_health.md): Link quality monitoring, packet loss calculation, and ping-RTT tracking.
