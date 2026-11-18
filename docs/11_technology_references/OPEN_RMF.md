# Technology Evaluation: Open-RMF (Robotics Middleware Framework)

## 1. Purpose
Centralized and distributed fleet coordination, traffic scheduling, and door/lift integration.

## 2. Relevant Modules
Module 2.5 Distributed Coordination.

## 3. Installation Requirements
- **Prerequisites**: Binary package (`ros-humble-rmf-fleet-adapter`).

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Native ROS 2 ecosystem framework.`

## 5. Advantages
Sophisticated spatiotemporal trajectory reservation in shared corridors.

## 6. Limitations
Designed primarily for centralized facility servers with reliable Wi-Fi; heavy overhead for P2P ad-hoc mesh.

## 7. Adoption Decision
- **Status**: `INVESTIGATING`
- **Architectural Rationale**: Currently investigating its spatiotemporal collision models, but adopting custom lightweight P2P right-of-way negotiation to survive network partitions.
