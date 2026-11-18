# Technology Evaluation: OpenCV 4.x

## 1. Purpose
Real-time computer vision, image processing, radiometric conversion, and feature extraction.

## 2. Relevant Modules
Module 1.3 Perception (Submodule 1.3.3), Module 3.3 Inspection Management.

## 3. Installation Requirements
- **Prerequisites**: Ubuntu package (`libopencv-dev`) and Python package (`opencv-python`).

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Native integration via `cv_bridge`.`

## 5. Advantages
Comprehensive image processing filters (CLAHE, edge detection), SIMD acceleration, radiometric support.

## 6. Limitations
Does not provide out-of-the-box multi-robot coordination logic.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted for low-light camera enhancement and radiometric thermal matrix temperature parsing.
