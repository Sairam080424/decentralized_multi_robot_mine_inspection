# Performance Metrics and Key Performance Indicators (KPIs)

> [!IMPORTANT]
> **Distinction Between Design Targets and Verified Results**:
> All numerical figures and performance thresholds documented across this repository represent **PROPOSED DESIGN TARGETS** established during the architectural formulation phase (Milestone M0).
> **As of Milestone M0, ZERO numerical targets have been experimentally verified.**
> Every metric listed below is marked as `UNVERIFIED`. Verified experimental measurements will be populated only after formal empirical benchmarks in Milestone M3 (simulation dynamics), Milestone M7 (distributed coordination), Milestone M8 (fault injection), and Milestone M11 (subterranean hardware trials).

---

## 1. Quantitative Performance & Safety Target Matrix

| Metric ID | Category | Description | Proposed Design Target | Experimentally Verified Result | Verification Milestone & Method |
|---|---|---|---|---|---|
| `KPI-PERF-001` | P2P Network | P2P Peer Discovery Latency | `< 2.0 s` | **UNVERIFIED (Pending M4)** | Milestone M4: Zenoh scout discovery timestamp delta |
| `KPI-PERF-002` | Task Allocation | Distributed Task Auction Clearance | `< 500 ms` | **UNVERIFIED (Pending M8)** | Milestone M8: Task announcement to two-phase lease commit |
| `KPI-PERF-003` | State Sync | CRDT State Reconciliation Latency | `< 1.0 s` | **UNVERIFIED (Pending M6)** | Milestone M6: Link reconnection to vector clock digest convergence |
| `KPI-PERF-004` | Local Safety | Local Safety Stop Reflex Reaction | `< 50 ms` | **UNVERIFIED (Pending M3)** | Milestone M3: Obstacle threshold breach to zero velocity hardware clamp |
| `KPI-PERF-005` | Fault Tolerance | Task Reassignment on Peer Crash | `< 8.0 s` | **UNVERIFIED (Pending M8)** | Milestone M8: Process SIGKILL injection to peer lease acquisition |
| `KPI-PERF-006` | Coordination | Narrow Drift Deconfliction Negotiation | `< 3.0 s` | **UNVERIFIED (Pending M7)** | Milestone M7: Conflict flag detection to yield agreement broadcast |
| `KPI-PERF-007` | Inspection QA | Radiometric Thermal Measurement Accuracy | `+/- 1.0°C` | **UNVERIFIED (Pending M9)** | Milestone M9: Gazebo simulated blackbody heat source comparison |
| `KPI-PERF-008` | Perception | Subterranean SLAM Trajectory Error | `< 1.0%` | **UNVERIFIED (Pending M2)** | Milestone M2: Loop-closure trajectory residual vs ground truth |
| `KPI-PERF-009` | Communication | Aggregate Inter-Robot Gossip Bandwidth | `< 250 kbps` | **UNVERIFIED (Pending M4)** | Milestone M4: Wireshark / pcap wire payload audit per node |
| `KPI-PERF-010` | Safety Watchdog | Local Safety Manager Loop Execution Rate | `50 Hz` nominal | **UNVERIFIED (Pending M3)** | Milestone M3: Monotonic timer jitter audit in ROS 2 executor |

---

## 2. Experimental Verification Protocol
When empirical tests are executed in subsequent milestones:
1. Benchmark data must be logged via `rosbag2` or test harness artifact logs.
2. The `Experimentally Verified Result` column will be updated with the empirical mean, standard deviation, and test conditions (e.g., `Mean: 32 ms +/- 4 ms [Tested in Gazebo Sim M3]`).
3. If an empirical result fails to meet the proposed design target, an Architectural RFC must be filed to either optimize the implementation or adjust the target with technical justification.
