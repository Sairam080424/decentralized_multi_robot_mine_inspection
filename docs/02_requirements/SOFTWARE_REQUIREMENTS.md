# Software Requirements Specification

## 1. Operating System & Base Runtimes
- **Base OS**: Ubuntu 22.04 LTS (Jammy Jellyfish).
- **ROS Distribution**: ROS 2 Humble Hawksbill (Long Term Support).
- **Simulation Platform**: Gazebo Sim (Garden / Fortress).
- **Language Standards**: C++17 / C++20 for high-performance nodes; Python 3.10+ for autonomy algorithms, orchestration, and tools.

---

## 2. Key Software Libraries & Frameworks
- **Navigation**: Nav2 (SmacPlanner2D/Lattice, MPPI local controller, Costmap2D).
- **Localization & SLAM**: SLAM Toolbox (asynchronous 2D mapping), `robot_localization` (Dual EKF instance for IMU + Odom fusion).
- **Actuation & Hardware Abstraction**: `ros2_control`, `diff_drive_controller`, custom skid-steer controller.
- **Middleware & Networking**: Eclipse Zenoh (Zenoh-Bridge-DDS / Zenoh-C / Zenoh-Python).
- **Computer Vision**: OpenCV 4.5.4+, PCL (Point Cloud Library) 1.12+.
- **Database & Storage**: PostgreSQL 14+, MinIO S3-compatible blob store.
- **Build System**: Colcon, CMake 3.22+, `rosdep`.
