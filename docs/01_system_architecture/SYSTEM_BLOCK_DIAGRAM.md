# System Block Diagram

## 1. Intra-Robot and Inter-Robot Block Diagram

The block diagram below illustrates the exact structural layout of components onboard each robot and their inter-layer interfaces:

```mermaid
graph TB
    subgraph Operations["Operator Base Station (Layer 3)"]
        UI["Mission Dashboard & Web Console"]
        DB[("PostgreSQL & Evidence Store")]
        SDK["Mission Ingestion SDK"]
    end

    subgraph Robot_A_Node["Robot A: Differential-Drive Explorer"]
        subgraph R2A_L2["Layer 2: Distributed Autonomy"]
            A_Disc["Peer Discovery"]
            A_Alloc["Task Allocator (CNP)"]
            A_State["CRDT State Engine"]
            A_Fault["Lease Monitor"]
        end
        subgraph R2A_L1["Layer 1: Robot & Environment"]
            A_Gate["Agent Gateway"]
            A_Nav["Nav2 Stack"]
            A_SLAM["SLAM Toolbox"]
            A_Safe["Local Safety Manager"]
            A_Motors["ros2_control Diff Drive"]
        end
    end

    subgraph Robot_B_Node["Robot B: Tracked Inspector"]
        subgraph R2B_L2["Layer 2: Distributed Autonomy"]
            B_Disc["Peer Discovery"]
            B_Alloc["Task Allocator (CNP)"]
            B_State["CRDT State Engine"]
            B_Fault["Lease Monitor"]
        end
        subgraph R2B_L1["Layer 1: Robot & Environment"]
            B_Gate["Agent Gateway"]
            B_Nav["Nav2 Stack"]
            B_Loc["Localization / Alignment"]
            B_Safe["Local Safety Manager"]
            B_Motors["ros2_control Track Drive"]
            B_Thermal["Thermal Inspection Pipeline"]
        end
    end

    SDK -->|Mission Ingestion| A_Alloc
    SDK -->|Mission Ingestion| B_Alloc
    A_State -.->|Telemetry & State Sync| DB
    B_State -.->|Telemetry & State Sync| DB

    A_Disc <===>|Ad-hoc P2P Zenoh Mesh| B_Disc
    A_Alloc <===>|Task Bids & Awards| B_Alloc
    A_State <===>|Anti-Entropy CRDT Gossip| B_State

    A_Alloc -->|Task Goals| A_Gate
    A_Gate -->|Action Goals| A_Nav
    A_Nav -->|Velocity Cmds| A_Safe
    A_Safe -->|Validated Cmds| A_Motors

    B_Alloc -->|Task Goals| B_Gate
    B_Gate -->|Action Goals| B_Nav
    B_Nav -->|Velocity Cmds| B_Safe
    B_Safe -->|Validated Cmds| B_Motors
    B_Gate -->|Trigger Capture| B_Thermal
```
