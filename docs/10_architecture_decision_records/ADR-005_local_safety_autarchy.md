# ADR-005: Authoritative Local Safety Autarchy in Layer 1

- **Status**: ACCEPTED
- **Date**: 2026-11-18
- **Context**: High-level distributed consensus or delayed remote commands must never compromise the instantaneous physical safety of the robot hardware.
- **Decision**: Enforce Local Safety Autarchy. The Layer 1 `local_safety_manager` executes at 50 Hz and has absolute authority to override motor velocities to zero upon detecting obstacles (< 0.25m), excessive tilt (> 25 deg), or software stall.
- **Consequences**:
  - Physical collision avoidance is guaranteed independently of upper-layer bugs.
  - Upward layers cannot disable or override local safety reflexes.
