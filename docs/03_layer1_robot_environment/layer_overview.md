# Layer 1 Architectural Overview

## 1. Scope and Responsibilities
Layer 1 is responsible for the physical existence and local autonomy of each robot. Its core responsibilities are:
1. Simulating high-fidelity subterranean mine environments with physically realistic contact, light attenuation, and sensor noise.
2. Modeling the mechanical kinematics, inertia, and sensor rigging of **Robot A** (differential drive) and **Robot B** (tracked skid-steer).
3. Ingesting raw sensor telemetry (LiDAR, optical RGB, radiometric thermal, IMU, wheel/track encoders) and deriving drift-resilient ego-motion estimates in GPS-denied environments.
4. Performing 2D/3D occupancy grid generation, global path planning along mine tunnels, and dynamic obstacle avoidance.
5. Providing an un-preemptible **Local Safety Manager** that guarantees collision avoidance, tip-over prevention, and thermal runaway halts.
6. Translating high-level task goals from Layer 2 into Nav2 action invocations and returning structured inspection evidence.

## 2. Invariants & Safety Autarchy
- **Local Safety Authority**: Layer 1 holds absolute, un-preemptible authority over motor velocities (`/cmd_vel`). If a rock fall or unexpected personnel appears within safety buffer zones, the safety manager cuts motor output independently of Layer 2 task state.
- **Hardware Isolation**: No code in Layer 2 or Layer 3 may import `ros2_control` hardware handles or publish raw velocity commands directly.
