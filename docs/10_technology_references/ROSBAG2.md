# Technology Evaluation: rosbag2

## 1. Purpose
High-performance telemetry recording and replay framework using MCAP / SQLite3 storage.

## 2. Relevant Modules
Module 1.6 Robot Communication, Module 3.5 Data & Reporting.

## 3. Installation Requirements
- **Prerequisites**: Built-in ROS 2 standard tool (`ros-humble-rosbag2`).

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Native Tier 1 ROS 2 recording system.`

## 5. Advantages
Zero-copy recording, high-throughput MCAP file format, exact timestamp replay for debugging.

## 6. Limitations
Storage files grow rapidly if uncompressed point clouds are recorded continuously.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted for simulation recording, algorithm benchmarking, and post-mission black-box logging.
