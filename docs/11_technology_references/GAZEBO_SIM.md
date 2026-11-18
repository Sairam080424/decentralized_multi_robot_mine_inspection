# Technology Evaluation: Gazebo Sim (Garden / Fortress)

## 1. Purpose
High-fidelity physics simulation engine with physically based rendering (PBR), sensor plugins, and contact dynamics.

## 2. Relevant Modules
Module 1.1 Simulation Environment, Module 1.2 Robot Models.

## 3. Installation Requirements
- **Prerequisites**: Ubuntu 22.04 packages via OSRF repository.

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Integrated via `ros_gz_bridge` and `gz_ros2_control`.`

## 5. Advantages
Modern DART/ODE physics engines, scalable sensor simulation (GPU raytracing), modular system plugins.

## 6. Limitations
Heavy GPU load when simulating multiple concurrent 3D LiDAR and thermal sensors on standard laptops.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted as the primary virtual test bench for subterranean mine drifts and heterogeneous robot models.
