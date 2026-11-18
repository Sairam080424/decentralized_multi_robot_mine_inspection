# Multi-Tier Test Strategy

## 1. Testing Philosophy
In subterranean multi-robot systems, physical testing is expensive, dangerous, and difficult to instrument. The testing strategy mandates:
1. **Aggressive Unit Testing**: Pure functions (CRDT merges, cost functions, DAG validators) are validated with exhaustive property-based unit tests.
2. **Deterministic Middleware Testing**: Networking logic is validated with synthetic network traffic shapers (`netem` / Zenoh router filters).
3. **Continuous Simulation Verification**: Every release milestone is benchmarked inside the Gazebo Sim subterranean mine world.

```mermaid
flowchart TD
    Tier1["Tier 1: Unit Tests (GTest / pytest)"] -->|Pass| Tier2["Tier 2: Component Integration Tests (launch_testing)"]
    Tier2 -->|Pass| Tier3["Tier 3: Hardware-in-the-Loop Simulation (Gazebo Sim)"]
    Tier3 -->|Pass| Tier4["Tier 4: Fault-Injection & Stress Scenarios"]
```
