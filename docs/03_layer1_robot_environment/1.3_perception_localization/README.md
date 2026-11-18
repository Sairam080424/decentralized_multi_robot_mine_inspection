# Module 1.3: Perception and Localization

## 1. Module Overview
Module 1.3 provides robust state estimation, point cloud processing, computer vision, Simultaneous Localization and Mapping (SLAM), and multi-robot map alignment in GPS-denied subterranean mine tunnels.

## 2. Submodule Index
- [1.3.1 Sensor Acquisition](sensor_acquisition.md): Synchronized raw telemetry ingestion, time-stamping, and frame transformation.
- [1.3.2 LiDAR Processing](lidar_processing.md): 3D point cloud filtering, ground plane removal, voxel downsampling, and obstacle clustering.
- [1.3.3 Camera Processing](camera_processing.md): Optical RGB enhancement in low light, feature extraction, and thermal radiometric parsing.
- [1.3.4 SLAM](slam.md): Drift-resilient 2D/3D subterranean SLAM using SLAM Toolbox and scan matching.
- [1.3.5 Localization](localization.md): Extended Kalman Filter (EKF) state fusion combining wheel/track odometry, IMU, and SLAM poses.
- [1.3.6 Map Alignment](map_alignment.md): Sub-map exchange, shared coordinate registration, and inter-robot anchor point alignment.
