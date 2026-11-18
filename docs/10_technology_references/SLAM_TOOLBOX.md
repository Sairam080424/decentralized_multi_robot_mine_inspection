# Technology Evaluation: SLAM Toolbox

## 1. Purpose
2D Simultaneous Localization and Mapping for lifelong mapping and long-distance subterranean drifts.

## 2. Relevant Modules
Module 1.3 Perception and Localization (Submodule 1.3.4).

## 3. Installation Requirements
- **Prerequisites**: Binary package (`ros-humble-slam-toolbox`).

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Native Tier 1 standard 2D SLAM.`

## 5. Advantages
Optimized Ceres pose-graph solver, asynchronous processing, sub-map serialization, low memory footprint.

## 6. Limitations
Featureless straight tunnel drifts can produce longitudinal drift in scan matching without IMU/odom fusion.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted as the primary mapping engine, fused with EKF odometry in `robot_localization`.
