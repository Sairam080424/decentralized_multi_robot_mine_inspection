# Technology Evaluation: Point Cloud Library (PCL 1.12)

## 1. Purpose
3D point cloud filtering, voxel downsampling, ground segmentation, and spatial clustering.

## 2. Relevant Modules
Module 1.3 Perception (Submodule 1.3.2 LiDAR Processing).

## 3. Installation Requirements
- **Prerequisites**: Ubuntu package (`libpcl-dev`) and ROS bridge (`pcl_conversions`).

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Native ROS 2 point cloud interface support.`

## 5. Advantages
Industry standard for 3D point cloud algorithms, highly optimized RANSAC and voxel filters.

## 6. Limitations
Heavy template compilation times; high memory utilization on large uncompressed scans.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted for LiDAR preprocessing, dust filtering, and ground extraction.
