# Module 1.4: Navigation and Motion

## 1. Module Overview
Module 1.4 provides autonomous subterranean path planning, obstacle avoidance, trajectory tracking, and recovery behaviors for both Robot A (differential drive) and Robot B (tracked skid-steer) using the Nav2 framework.

## 2. Submodule Index
- [1.4.1 Map Management](map_management.md): Global and local layered costmaps, static obstacles, inflation, and voxel clearance.
- [1.4.2 Global Planning](global_planning.md): Smac Planner (A* / Dijkstra) generating optimal topological paths through mine drifts.
- [1.4.3 Local Planning](local_planning.md): Model Predictive Path Integral (MPPI) controller tracking paths around dynamic obstacles.
- [1.4.4 Obstacle Avoidance](obstacle_avoidance.md): Dynamic collision avoidance, rock fall detection, and negative obstacle / pit edge avoidance.
- [1.4.5 Motion Control](motion_control.md): Velocity command smoothing, skid-steer slip compensation, and jerk limitation.
- [1.4.6 Navigation Recovery](navigation_recovery.md): Nav2 recovery behaviors: spin, backup, wait, and costmap clearance protocols.
