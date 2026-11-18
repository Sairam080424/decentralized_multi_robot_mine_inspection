# Module Dependencies and Layer Boundaries

## 1. Strict Layering Dependency Rules

1. **Rule 1 (Top-Down Dependency)**: Dependencies point strictly downwards. Layer 3 depends on Layer 2 interfaces; Layer 2 depends on Layer 1 interfaces.
2. **Rule 2 (No Upward Coupling)**: Layer 1 must have zero references to Layer 2 or Layer 3 modules, headers, or ROS topics.
3. **Rule 3 (Peer Isolation)**: Physical platforms communicate exclusively via Layer 2 distributed protocols. Robot A's Nav2 stack cannot directly send ROS 2 commands to Robot B's motor controllers.

---

## 2. Dependency Graph

```mermaid
graph TD
    subgraph L3_Deps["Layer 3 Modules"]
        L3_1["3.1 Mission Planning"] --> L3_2["3.2 Mission Management"]
        L3_3["3.3 Inspection Management"] --> L3_5["3.5 Data & Reporting"]
        L3_4["3.4 Monitoring & Visualization"]
        L3_6["3.6 External Integration"] --> L3_1
    end

    subgraph L2_Deps["Layer 2 Modules"]
        L2_1["2.1 Robot Discovery"] --> L2_2["2.2 Capability Management"]
        L2_2 --> L2_4["2.4 Distributed Task Allocation"]
        L2_3["2.3 Mission & Task Management"] --> L2_4
        L2_4 --> L2_5["2.5 Distributed Coordination"]
        L2_4 --> L2_6["2.6 Distributed State Management"]
        L2_6 --> L2_7["2.7 Fault Tolerance & Recovery"]
        L2_7 --> L2_4
        L2_8["2.8 Distributed Runtime Interface"]
    end

    subgraph L1_Deps["Layer 1 Modules"]
        L1_1["1.1 Simulation Environment"] --> L1_2["1.2 Robot Models"]
        L1_2 --> L1_3["1.3 Perception & Localization"]
        L1_3 --> L1_4["1.4 Navigation & Motion"]
        L1_4 --> L1_5["1.5 Robot Agent Interface"]
        L1_5 --> L1_6["1.6 Robot Communication"]
    end

    L3_2 -->|Consumes Runtime API| L2_8
    L3_4 -->|Subscribes Replicated State| L2_6
    L2_8 -->|Dispatches Actions to Agent| L1_5
    L2_1 -->|Queries Local Health| L1_6
```
