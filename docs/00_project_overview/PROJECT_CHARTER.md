# Project Charter: Decentralized Multi-Robot Mine Inspection Platform

## 1. Project Introduction
The **Decentralized Multi-Robot Mine Inspection Platform** is an open, modular, autonomous multi-robot coordination system engineered to conduct environmental mapping, structural integrity assessment, and thermal anomaly inspection in subterranean, communication-degraded underground mining drifts.

The platform coordinates heterogeneous mobile robots without reliance on a single permanent central mission coordinator. Local robot safety authority is preserved independently on each platform, while multi-robot collaboration, task negotiation, and mission state replication occur peer-to-peer over an intermittent wireless mesh.

---

## 2. Problem Statement
Underground hard-rock and coal mining drifts are hazardous, GPS-denied, and structurally dynamic environments. Periodic inspection of rock faces, ventilation bulkheads, conveyor bearings, electrical distribution kiosks, and water sumps is critical to prevent catastrophic roof falls, equipment fires, and toxic gas buildup.

Existing inspection methods suffer from acute operational limitations:
1. **Manual Inspection Risks**: Human inspectors must enter unsupported or poorly ventilated drifts, exposing personnel to roof falls, noxious gases, and extreme heat.
2. **Centralized Autonomy Brittleness**: Commercial multi-robot and C2 (Command and Control) systems rely on continuous Wi-Fi/LTE infrastructure and centralized dispatchers. In underground tunnels, rock attenuation and non-line-of-sight geometry create pervasive communication dead zones. A centralized system stalls whenever robots round a corner or enter a drift shadow.
3. **Homogeneous Fleet Limitations**: Differential-wheel scouts are agile and fast at mapping, but lack traction for heavy rough rubble or the payload capacity for multi-sensor turrets. Tracked heavy robots carry extensive sensor suites but have slower traversal speeds and higher power consumption. A single robot type cannot satisfy both long-range mapping and intensive contact/thermal inspection.

---

## 3. Industry Context & Target Application
- **Industry Sector**: Underground Metal/Non-Metal Mining, Deep Coal Mining, Subterranean Civil Infrastructure, and Tunnel Boring Operations.
- **Target Application**: Autonomous pre-shift and post-blast inspection of underground drifts, haulage ramps, cross-cuts, and machinery alcoves.
- **Regulatory Reference**: Alignment with Mine Safety and Health Administration (MSHA) guidelines, NIOSH mining automation standards, and ISO 18434-1 condition monitoring.

---

## 4. Intended Users
1. **Mine Safety Engineers & Inspectors**: Define inspection objectives, review visual and thermal evidence scorecards, and sign off on drift safety.
2. **Operations & Maintenance Personnel**: Receive automated alerts regarding overheating conveyor bearings, water pooling, or rockfall barriers requiring clearance.
3. **Robotics Software Engineers & Contributors**: Develop, test, and integrate independent software modules (locomotion, SLAM, task auctioning, CRDT state) using standard interfaces.

---

## 5. Project Vision & Initial MVP

### Project Vision
To establish a fully autonomous, scalable subterranean multi-robot fleet capable of collaborative exploration, inspection, and hazard management across kilometers of uninstrumented mine networks, operating resiliently despite severe communication loss, partial fleet casualties, and complex terrain.

### Initial MVP Scope (Simulation Demonstration)
The initial Minimum Viable Product (MVP) focuses on a high-fidelity simulation demonstration:
- **Environment**: Simulated Gazebo Sim underground mine world with uneven rock walls, multi-level drifts, rubble obstacles, lighting attenuation, and synthetic RF signal drop.
- **Fleet**: Two heterogeneous ground mobile robots:
  - **Robot A (Exploration Scout)**: Differential-drive, 3D LiDAR, RGB camera, IMU, wheel odometry. Optimized for high-speed tunnel traversal, frontier exploration, and candidate target detection.
  - **Robot B (Inspection Specialist)**: Heavy tracked chassis with skid-steer locomotion, 2-DOF pan-tilt unit, optical zoom camera, simulated radiometric thermal camera, solid-state LiDAR, and IMU.
- **Autonomy Objectives**:
  1. Independent mapping and navigation using SLAM Toolbox and Nav2.
  2. Peer discovery and capability exchange over P2P mesh (Eclipse Zenoh).
  3. Decentralized task allocation via Contract Net Protocol (CNP) matching thermal tasks strictly to Robot B and exploration tasks to Robot A.
  4. Collaborative mission execution and state synchronization via CRDTs.
  5. Communication loss tolerance and autonomous task lease revocation/reassignment upon simulated robot failure.
  6. Consolidated inspection scorecard and PDF report generation.

---

## 6. Distinguishing Simulated MVP from Production Industrial System

| Dimension | Simulated Initial MVP (M0 - M12) | Production Industrial Target |
|---|---|---|
| **Environment** | Gazebo Sim physics simulation with modeled ODE/DART contacts. | Active subterranean mine with dripping acidic water, mud, severe dust, and explosive methane atmospheres. |
| **Chassis & Hardware** | Virtual URDF/Xacro models with standard ros2_control actuators. | IP67-rated, MSHA explosion-proof (intrinsically safe / flameproof) physical enclosures. |
| **Compute Hardware** | Host x86_64 workstation running Ubuntu 22.04 LTS. | Ruggedized embedded compute (NVIDIA Jetson AGX Orin / industrial x86) with passive thermal cooling. |
| **RF Physical Layer** | Software distance-based packet drop and netem latency emulation. | Leaky feeder, 802.11s ruggedized mesh nodes, or sub-GHz subterranean radios. |
| **Sensor Payloads** | Simulated Gazebo GPU LiDAR and thermal camera plugins. | Calibrated uncooled microbolometer LWIR cameras, explosion-certified LiDARs, and electrochemical gas sensors. |
| **Safety Certifications** | Authoritative software safety watchdog (50 Hz). | Hardwired SIL-3 emergency stop circuit, mechanical fail-safe brakes, and redundant ultrasonic bumpers. |

---

## 7. System Boundaries
- **Layer 1 Boundary**: Physical and simulated hardware drivers, low-level PID/velocity controllers, sensor acquisition, and the local authoritative safety watchdog.
- **Layer 2 Boundary**: Onboard decentralized autonomy core, P2P discovery, capability matching, task bidding, coordination, CRDT state replication, and fault recovery.
- **Layer 3 Boundary**: Surface base station, mission planning studio, relational database (PostgreSQL), evidence object storage (MinIO), and external enterprise asset management APIs.

---

## 8. In-Scope vs. Out-of-Scope

### In-Scope
- Gazebo Sim mine world with modular drifts, junctions, rubble obstacles, and thermal anomalies.
- Full kinematic and sensor modeling of Robot A (diff-drive) and Robot B (tracked).
- ROS 2 Humble Nav2 and SLAM Toolbox configuration for subterranean mobility.
- Standalone Layer 1 Local Safety Manager enforcing independent collision and rollover halts.
- Peer-to-peer discovery, capability exchange, and Contract Net Protocol task allocation.
- Replicated mission state using Conflict-Free Replicated Data Types (CRDTs) and vector clocks.
- Simulated fault injection (packet loss, robot crash, stall) and autonomous task reassignment.
- Web dashboard mockups, PostgreSQL schema, MinIO evidence storage, and automated PDF reporting.

### Out-of-Scope
- Physical machining, metal fabrication, or PCB manufacturing for physical robots.
- Hardware-level explosive atmosphere (ATEX / MSHA Part 18) certification.
- Direct motor velocity control from surface Layer 3 (strictly prohibited by architecture).
- Monolithic central database operating as a real-time mission decision-maker.
- Subterranean rock drilling, blasting, or heavy rock extraction capabilities.

---

## 9. Assumptions and Constraints

### Assumptions
- Underground mine drifts have passable minimum clearances (width >= 2.5m, height >= 2.5m).
- Both robots can communicate via ad-hoc wireless mesh when within radio line-of-sight (< 50m).
- Robots possess sufficient onboard compute to run SLAM, local path planning, and autonomy independently.
- Drift slopes do not exceed 30% (17 degrees), which is within the physical climbing limit of Robot B.

### Constraints
- **Zero GPS**: Absolute positioning satellites are inaccessible; localization relies entirely on odometry, IMU, and LiDAR SLAM.
- **RF Attenuation**: Direct communication through solid rock is impossible; wireless links follow tunnel drifts and drop sharply around corners.
- **Bandwidth Limitations**: Subterranean mesh links support variable bandwidth (250 kbps - 5 Mbps); raw video streaming must be avoided during autonomous coordination.
- **Local Safety Priority**: No remote command or distributed consensus can override local obstacle avoidance reflexes.

---

## 10. Success Criteria

1. **Autonomous Collaborative Execution**: Robot A and Robot B successfully explore an unmapped simulated mine drift, discover an overheating transformer, auction the inspection task to Robot B, and collect thermal evidence without operator intervention.
2. **Resilience to Network Partition**: Robots continue executing committed tasks during a 10-minute communication blackout and successfully reconcile state upon link restoration within `[PROPOSED TARGET: < 1.0 s]`.
3. **Resilience to Robot Failure**: Killing Robot A during task execution triggers lease revocation and automated reassignment of uncompleted tasks to Robot B within `[PROPOSED TARGET: < 8.0 s]`.
4. **Zero Single Point of Failure**: System demonstrates zero mission-critical reliance on a permanent central coordinator node.
5. **Code & Architecture Modularity**: All modules possess documented owners, inputs, outputs, and unit tests, enabling independent development.

---

## 11. Future Expansion Possibilities
- Integration of autonomous aerial drones (UAVs) for vertical stope and ore-pass inspection.
- Extension of capability schema to support legged quadrupeds (e.g., Boston Dynamics Spot).
- Integration of physical electrochemical gas sensors for methane ($CH_4$), carbon monoxide ($CO$), and oxygen ($O_2$) monitoring.
- Integration of edge AI vision models for automated geological crack classification and spalling hazard prediction.
