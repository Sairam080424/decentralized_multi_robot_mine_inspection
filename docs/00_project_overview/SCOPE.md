# Project Scope

## 1. In-Scope Disciplines & Deliverables

### Layer 1: Robot & Environment Layer
- Development of a modular Gazebo Sim underground mine simulation world with irregular rock walls, tunnels, inclines, obstacles, and lighting conditions.
- Kinematic and dynamic URDF/Xacro models for **Robot A** (differential drive) and **Robot B** (tracked skid-steer).
- Realistic sensor plugins: 3D LiDAR, RGB cameras, simulated radiometric thermal camera, IMU, and wheel/track odometry.
- Full ROS 2 Humble Nav2 integration with Smac Planner, MPPI controller, and SLAM Toolbox.
- Authoritative Layer 1 Local Safety Manager enforcing independent collision prevention and emergency stops.
- Standardized ROS 2 Robot Agent gateway interface.

### Layer 2: Distributed Autonomy Layer
- Zero-configuration peer discovery, liveliness monitoring, and heartbeat gossip.
- Declarative robot capability schema and constraint-based task matcher.
- Contract Net Protocol (CNP) distributed task bidding and auction clearing house.
- Ephemeral coordinator election for consensus synchronization.
- CRDT-based mission state replication and conflict resolution.
- Dynamic task lease management and failure-driven task reassignment.

### Layer 3: Mission & Operations Layer
- Declarative mission definition format (JSON/YAML) and validation engine.
- Web-based monitoring UI and RViz2 visualization configuration.
- Relational schema for mission state, inspection evidence, and hazard logs.
- Python Public SDK and REST API specification for external integration.

---

## 2. Out-of-Scope (Deferred or Explicitly Excluded)

- Physical hardware fabrication, machining, and physical mine field deployment (addressed in subsequent hardware development phases).
- Subterranean radio-frequency physical layer antenna modeling (simulated via packet drop and range attenuation models in software).
- Direct motor velocity control from Layer 3 (strictly forbidden by architectural safety rules).
- Monolithic central database serving as a live operational decision-maker during missions.
- Autonomous explosive deployment or heavy rock excavation functions.
