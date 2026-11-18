# Technology Evaluation: Gazebo Sim (Harmonic / Garden)

## 1. Purpose
High-fidelity physics simulation engine with physically based rendering (PBR), sensor simulation, and contact dynamics for multi-robot subterranean mine inspection.

## 2. Relevant Modules
Module 1.1 Simulation Environment, Module 1.2 Robot Models.

## 3. Installation Requirements & Environment Configuration
- **Host OS**: Ubuntu 22.04.5 LTS (Jammy Jellyfish) x86_64.
- **Installed Gazebo Sim Distribution**: Gazebo Sim 8.15.0 (Gazebo Harmonic, package `gz-sim8` 8.15.0-1~jammy).
- **SDFormat Version**: `libsdformat14` version 14.9.0.
- **ROS 2 Integration Packages**:
  - `ros-humble-ros-gzharmonic`
  - `ros-humble-ros-gzharmonic-sim`
  - `ros-humble-ros-gzharmonic-bridge`
  - `ros-humble-gz-ros2-control`

### Version & Compatibility Notes
- While early M0 documentation referenced Gazebo Garden/Fortress, the verified development environment uses **Gazebo Harmonic 8.15.0** alongside ROS 2 Humble.
- SDFormat 14 natively parses and validates `<sdf version="1.9">` and `<sdf version="1.10">` specification standards without translation warnings.
- System plugins in Harmonic follow the `gz-sim-*-system` naming convention (e.g. `gz-sim-physics-system`, `gz-sim-scene-broadcaster-system`, `gz-sim-user-commands-system`, `gz-sim-sensors-system`) under the `gz::sim::systems::*` namespace.
- Model resource path resolution requires exporting both `GZ_SIM_RESOURCE_PATH` (for simulation runtime) and `SDF_PATH` (for standalone `gz sdf -k` command validation).
- When running in containerized or headless environments, `GZ_LOG_PATH=/tmp` prevents write-permission crashes inside `gz::common::FileLogger::Init`.

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Integrated via ros-humble-ros-gzharmonic-bridge and gz-ros2-control.`

## 5. Advantages
Modern DART physics engine, scalable sensor simulation (GPU raytracing), modular system plugins, PBR materials, and robust multi-robot namespace support.

## 6. Limitations
Heavy GPU load when simulating multiple concurrent 3D LiDAR and thermal sensors on standard laptops. Headless simulation (`-s -r`) should be used for automated testing and CI pipelines.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted as the primary virtual test bench for subterranean mine drifts, modular terrain elements, and heterogeneous robot models.
