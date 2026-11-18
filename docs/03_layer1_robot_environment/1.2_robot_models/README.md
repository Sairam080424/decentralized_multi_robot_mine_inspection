# Module 1.2: Robot Models

## 1. Module Overview
Module 1.2 specifies the physical, kinematic, dynamic, visual, collision, and sensor integration definitions for the heterogeneous multi-robot team:
- **Robot A**: Differential-drive mobile scout optimized for agile, high-speed tunnel exploration and topological mapping.
- **Robot B**: Tracked heavy chassis optimized for traversing rough rubble, carrying multi-modal payloads, and performing radiometric thermal inspection.

## 2. Submodule Index
- [1.2.1 Robot A Specification](robot_a.md): Differential-drive exploration platform mechanics, kinematics, and payload.
- [1.2.2 Robot B Specification](robot_b.md): Tracked inspection platform mechanics, skid-steer dynamics, and thermal payload.
- [1.2.3 Robot Description](robot_description.md): Parametric URDF/Xacro macros, joint limits, inertial tensors, and collision bounds.
- [1.2.4 Sensor Models](sensor_models.md): 3D LiDAR, optical RGB cameras, radiometric thermal camera, IMU, and encoder models.
- [1.2.5 Robot Controllers](robot_controllers.md): `ros2_control` configurations for differential drive and slip-compensated tracked locomotion.
