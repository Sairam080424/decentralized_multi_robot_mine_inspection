# Technology Evaluation: Nav2 (ROS 2 Navigation Stack)

## 1. Purpose
Industrial 2D/3D autonomous mobile robot navigation, costmaps, global planning, trajectory control, and recoveries.

## 2. Relevant Modules
Module 1.4 Navigation and Motion.

## 3. Installation Requirements
- **Prerequisites**: Binary package (`ros-humble-navigation2`).

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Native Tier 1 standard navigation stack.`

## 5. Advantages
Highly modular behavior-tree architecture, advanced controllers (MPPI), robust recovery behaviors.

## 6. Limitations
Requires tuning for narrow subterranean corridors to prevent wall oscillation and dead-end traps.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted for all local navigation and trajectory execution on both Robot A and Robot B.
