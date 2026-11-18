# Non-Functional Requirements Specification

## 1. Reliability & Fault Tolerance
- `NFR-REL-001`: The multi-robot system shall suffer zero unrecoverable mission deadlocks when communication is lost indefinitely between robots.
- `NFR-REL-002`: Local safety reflexes shall operate deterministically with zero dependence on network connectivity.
- `NFR-REL-003`: In the event of a Layer 2 process crash, the Layer 1 watchdog shall bring the robot base to a safe, controlled stop within `[PROPOSED TARGET: < 200 ms]`.

---

## 2. Performance & Timing
- `NFR-PERF-001`: Local odometry and safety sensor pipelines shall execute at `>= 50 Hz`.
- `NFR-PERF-002`: SLAM and costmap updates shall maintain an update rate of `>= 5 Hz` under nominal compute loads.
- `NFR-PERF-003`: Inter-robot gossip messages shall not exceed `[PROPOSED TARGET: 250 kbps]` aggregate bandwidth per robot.

---

## 3. Portability & Modularity
- `NFR-MOD-001`: All software packages shall conform strictly to ROS 2 package guidelines and Colcon build conventions.
- `NFR-MOD-002`: Software components shall run natively on Ubuntu 22.04 LTS and containerized Docker environments.
- `NFR-MOD-003`: Upstream hardware interfaces shall be isolated through `ros2_control` hardware abstraction layers.

---

## 4. Scalability
- `NFR-SCA-001`: The distributed task allocation algorithm shall scale seamlessly from 2 robots to at least 10 robots without exponential message explosion (adhering to $O(N)$ message complexity per auction).
