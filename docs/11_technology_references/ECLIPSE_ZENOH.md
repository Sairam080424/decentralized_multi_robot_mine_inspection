# Technology Evaluation: Eclipse Zenoh

## 1. Purpose
Zero-overhead publish/subscribe/query protocol optimized for edge robotics and lossy wireless mesh networks.

## 2. Relevant Modules
All Layer 2 Distributed Autonomy modules.

## 3. Installation Requirements
- **Prerequisites**: Debian packages from Eclipse Zenoh repository; Python pip package `eclipse-zenoh`.

## 4. ROS 2 Compatibility
- **Compatibility Status**: `Integrates via `zenoh-bridge-dds` and direct C/Python APIs.`

## 5. Advantages
Compact wire format (wire overhead marked TBD pending reproducible benchmark), native P2P mesh support, built-in queryables, zero multicast storms.

## 6. Limitations
Requires installing Zenoh router/bridge binaries alongside standard ROS 2 packages.

## 7. Adoption Decision
- **Status**: `ADOPTED`
- **Architectural Rationale**: Adopted as the core peer-to-peer transport protocol for Layer 2 multi-robot distributed autonomy.
