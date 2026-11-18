# Technology Evaluation: ROS 2 Humble Hawksbill

## 1. Purpose
Underlying robotics publish/subscribe, service, action, and lifecycle middleware for intra-robot nodes.

## 2. Relevant Modules
All Layer 1 modules, Layer 2 runtime interfaces.

## 3. Installation Requirements
- **Prerequisites**: Ubuntu 22.04 LTS binary packages (`ros-humble-desktop`).

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Native (Target LTS release).`

## 5. Advantages
DDS-based distributed architecture, strong lifecycle management, multi-platform, vast ecosystem.

## 6. Limitations
Default DDS discovery multicast generates high network traffic over lossy subterranean wireless mesh.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted as the foundational intra-robot software platform. Inter-robot mesh communications bridge through Eclipse Zenoh to prevent DDS multicast saturation.
