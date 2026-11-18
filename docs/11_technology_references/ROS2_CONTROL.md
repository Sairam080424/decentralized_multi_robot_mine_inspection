# Technology Evaluation: ros2_control

## 1. Purpose
Real-time robot actuator control framework and hardware abstraction layer.

## 2. Relevant Modules
Module 1.2 Robot Models (Submodule 1.2.5 Controllers).

## 3. Installation Requirements
- **Prerequisites**: Binary packages (`ros-humble-ros2-control`, `ros-humble-ros2-controllers`).

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Native Tier 1 control architecture.`

## 5. Advantages
Deterministic execution, clean hardware abstraction, standard velocity/joint controllers.

## 6. Limitations
Requires custom plugin configuration for slip-compensated tracked skid-steer drivetrains.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted for motor actuation on both differential (Robot A) and tracked (Robot B) drivetrains.
