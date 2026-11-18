# System Requirements Specification

## 1. Onboard Compute Specifications (Target Hardware & Simulation Host)

### Target Host Development Machine
- **CPU**: x86_64 8-core / 16-thread processor (AMD Ryzen 7 / Intel Core i7 11th Gen or higher).
- **RAM**: Minimum 32 GB DDR4/DDR5 system memory.
- **GPU**: Dedicated NVIDIA GPU with minimum 8 GB VRAM, supporting Vulkan and OpenGL 4.5+ for Gazebo Sim ray-tracing and point cloud rendering.
- **Storage**: Minimum 100 GB fast NVMe SSD storage.

### Target Simulated Robot Compute
- **Robot A Onboard Compute**: Equivalent to NVIDIA Jetson Orin Nano (6-core ARM Cortex-A78AE, 8 GB unified memory, 40 TOPS AI compute).
- **Robot B Onboard Compute**: Equivalent to NVIDIA Jetson AGX Orin (8-core/12-core ARM, 32 GB memory, 200 TOPS AI compute).

---

## 2. Simulated Network Environment
- **Simulated Wireless Mesh**: Ad-hoc 802.11s or mobile ad-hoc network (MANET) emulation.
- **Bandwidth**: Variable channel model from 250 kbps to 5 Mbps.
- **Latency / Jitter**: Base latency 10&ndash;50 ms with intermittent jitter up to 500 ms.
- **Packet Loss Profile**: Periodic synthetic drop rates ranging from 0% (clear LOS) to 80% (around rock corners).
