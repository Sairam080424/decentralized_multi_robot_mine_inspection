# ADR-005: Authoritative Local Safety Autarchy in Layer 1

- **Status**: PROPOSED / UNDER EVALUATION
- **Date**: 2026-11-18 (Updated: 2026-11-19)
- **Context**: High-level distributed consensus or delayed remote commands must never compromise the instantaneous physical safety of the robot hardware.
- **Decision**: Propose an Authoritative Local Safety Autarchy architecture in Layer 1. The local safety manager executes at a proposed rate of 50 Hz and has absolute authority to override motor velocities to zero upon detecting obstacle envelope breaches, excessive chassis tilt, or software heartbeat stalls.
- **Evaluation Criteria & Alternatives**:
  - **Status**: Concrete arbitration mechanism and numerical thresholds are under empirical evaluation; invariant principle is foundational.
  - **Implementation Alternatives Under Evaluation**:
    - Software multiplexer (`twist_mux` priority arbitration with lock-out node).
    - Dedicated safety FSM lifecycle node with hardware-level relay cut-off.
    - Dual-channel safety watchdog (micro-ROS / safety PLC hardware supervisor).
  - **Empirical Evaluation Plan (Milestone M3 & M5)**:
    - Validate emergency stop latency ($< 50\text{ ms}$ proposed target) under maximum velocity.
    - Calibrate tilt threshold ($25^\circ$ proposed) and cliff/scree detection thresholds in Gazebo physics.
    - Measure processor utilization and safety watchdog jitter under heavy SLAM/Nav2 compute loads.
- **Consequences**:
  - Physical collision avoidance is treated as an architectural safety objective requiring rigorous simulation and hardware validation, independent of upper-layer faults or network stalls.
  - Upward layers cannot disable or override local safety reflexes.
  - Final safety arbitration implementation to be verified and accepted following fault-injection trials in Milestone M3.
