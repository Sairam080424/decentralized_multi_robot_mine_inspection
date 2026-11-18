# Problem Statement: Subterranean Multi-Robot Coordination

## 1. Industrial Background
Underground mining operations require periodic, rigorous inspection of structural rock faces, ventilation bulkheads, electrical enclosures, conveyor belt systems, and drainage networks. Today, these inspections often mandate human entry into hazardous, unsupported underground drifts or rely on single tethered mobile platforms with limited range.

---

## 2. Failure Modes of Centralized Multi-Robot Architectures

Conventional multi-robot systems typically employ a centralized coordinator node that gathers global world states, computes optimal task allocations, and streams velocity commands to subordinate robots. In underground mines, this approach fails categorically due to:

1. **RF Propagation Disruption**: Mine tunnels act as lossy waveguides with high attenuation at standard Wi-Fi frequencies (2.4 GHz and 5 GHz). Corner diffraction and rock absorptivity limit line-of-sight communication to 30&ndash;80 meters. A centralized system experiences complete operational paralysis as soon as robots round a tunnel corner.
2. **Single Point of Failure (SPOF)**: If the centralized server fails, hangs, or loses connectivity, the entire fleet stalls, posing severe entrapment and safety hazards.
3. **High Communication Bandwidth Demand**: Streaming raw point clouds, thermal arrays, and camera feeds to a central server saturates scarce subterranean bandwidth.
4. **Latency Vulnerability**: Safety-critical collision avoidance and trajectory adjustments cannot tolerate network round-trip latencies over degraded wireless mesh hops.

---

## 3. Engineering Challenges Solved by this Platform

| Challenge | Impact on Traditional Systems | Our Decentralized Solution |
|---|---|---|
| **Frequent Partitioning** | Mission halts; robots stall waiting for heartbeat | Delay-Tolerant Task Leases & CRDT State Reconciliation |
| **Heterogeneous Capabilities** | Sub-optimal task assignment; manual role assignment | Declarative Capability Schema & Automated Task Matching |
| **GPS Absence** | Drift accumulation; localization divergence | Cooperative Multi-Robot SLAM & Topological Anchor Points |
| **Narrow Tunnel Contention** | Deadlocks where robots block each other | Distributed Right-of-Way Coordination & Tunnel Yield Protocols |
| **Catastrophic Robot Failure** | Lost mission progress; orphaned tasks | Peer Heartbeat Monitoring & Dynamic Task Auction Reassignment |
