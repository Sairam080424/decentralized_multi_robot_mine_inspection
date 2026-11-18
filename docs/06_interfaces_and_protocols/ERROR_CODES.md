# Standardized System Error Codes

All subsystems utilize a standardized 16-bit hexadecimal error code taxonomy:

| Code Range | Subsystem Category |
|---|---|
| `0x1000 - 0x1FFF` | Layer 1: Hardware, Actuation, and Low-Level Safety |
| `0x2000 - 0x2FFF` | Layer 1: Perception, Sensors, SLAM, and Navigation |
| `0x3000 - 0x3FFF` | Layer 2: Peer Discovery and Capability Management |
| `0x4000 - 0x4FFF` | Layer 2: Task Allocation, Bidding, and Leases |
| `0x5000 - 0x5FFF` | Layer 2: Distributed Coordination and Conflict Resolution |
| `0x6000 - 0x6FFF` | Layer 2: State Replication and CRDT Reconciliation |
| `0x7000 - 0x7FFF` | Layer 2: Fault Recovery and Failure Detection |
| `0x8000 - 0x8FFF` | Layer 3: Mission Ingestion, Database, and Reporting |

## Specific Error Code Index
- `0x1001`: `SAFETY_OBSTACLE_COLLISION_REFLEX` &mdash; Emergency stop asserted due to immediate obstacle.
- `0x1002`: `SAFETY_TILT_LIMIT_EXCEEDED` &mdash; Platform pitch/roll exceeded 25 degrees.
- `0x1003`: `MOTOR_CONTROLLER_COMM_TIMEOUT` &mdash; Lost communication with `ros2_control` hardware handles.
- `0x2001`: `LIDAR_PACKET_DROP_EXCESSIVE` &mdash; 3D LiDAR drop rate > 50%.
- `0x2002`: `SLAM_POSE_GRAPH_DIVERGENCE` &mdash; Scan matching residual error exceeded threshold.
- `0x2003`: `NAV2_PLANNER_GOAL_BLOCKED` &mdash; Smac planner unable to find collision-free path.
- `0x2004`: `NAV2_CONTROLLER_STUCK` &mdash; Vehicle displacement < 0.1m over 10 seconds of active command.
- `0x4001`: `AUCTION_NO_CAPABLE_BIDDERS` &mdash; Zero bids received matching task requirements.
- `0x4002`: `LEASE_TOKEN_EXPIRED` &mdash; Task lease duration elapsed without renewal.
- `0x4003`: `DUPLICATE_CLAIM_BLOCKED` &mdash; Attempted concurrent claim on already leased task.
- `0x6001`: `CRDT_CONCURRENT_CONFLICT_RESOLVED` &mdash; LWW resolver arbitrated concurrent updates.
- `0x7001`: `PEER_HEARTBEAT_TIMEOUT` &mdash; Peer transition to UNREACHABLE (phi >= 8.0).
- `0x8001`: `MISSION_DAG_CYCLE_DETECTED` &mdash; Cyclic dependency rejected during validation.
