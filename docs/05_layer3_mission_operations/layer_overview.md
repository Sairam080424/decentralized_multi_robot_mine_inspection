# Layer 3 Architectural Overview

## 1. Scope & Design Philosophy
Layer 3 operates typically on the surface control room station, operator tablets, or edge portal gateway servers. Its fundamental design principles are:
1. **Separation of Operational Planning from Autonomous Control**: Operators define *what* needs to be inspected (objectives, target equipment, acceptable temperature limits) rather than micromanaging *how* robots navigate subterranean tunnels.
2. **Non-Authoritative during Partitions**: Layer 3 is an observability and ingestion plane. It does not issue continuous heartbeat requirements to the robots.
3. **No Direct Actuation**: Layer 3 cannot directly publish to `/cmd_vel` or bypass Layer 1 physical safety. All robot actions are requested via declarative mission tasks.
4. **Comprehensive Evidence Traceability**: Every captured image, point cloud segment, and thermal temperature matrix is cryptographically tied to the capturing robot, spatial coordinate frame, and calibrated sensor metadata.
