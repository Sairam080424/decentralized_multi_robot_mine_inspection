# Project Acceptance Criteria

## 1. Milestone Acceptance Matrix

| Milestone | Deliverable | Acceptance Criteria | Status |
|---|---|---|---|
| **M0** | Documentation & Repository Setup | Complete repository structure, 3-layer docs, all submodules documented with 16 sections, valid Mermaid diagrams, and backlog tracking. | **IN_PROGRESS** |
| **M1** | Mine Simulation & Robot Models | Gazebo mine world spawns; URDF models for Robot A and B load with all sensors publishing ROS 2 topics. | PLANNED |
| **M2** | Independent Robot Navigation | Robot A and B independently map and navigate simulated tunnels using SLAM Toolbox and Nav2 without collisions. | PLANNED |
| **M3** | Robot Agent Abstraction | Common Robot Agent gateway successfully exposes uniform state management and `ExecuteTask.action` servers. | PLANNED |
| **M4** | Discovery & Capability Exchange | Robots discover each other over Zenoh mesh and exchange capability JSON documents within `[PROPOSED TARGET: < 2.0 s]`. | PLANNED |
| **M5** | Mission & Task Management | Mission DAG parsed, validated, and decomposed into atomic tasks with explicit dependency resolution. | PLANNED |
| **M6** | Distributed Task Allocation | Contract Net Protocol allocates tasks to Robot A and B based on cost evaluation without duplicate assignments. | PLANNED |
| **M7** | Distributed Coordination & State | CRDT state replication synchronizes mission state between robots; narrow tunnel yielding executes successfully. | PLANNED |
| **M8** | Fault Recovery & Communication Loss | Simulated crash of Robot A triggers lease revocation and automatic task reallocation to Robot B within `[PROPOSED TARGET: < 8.0 s]`. | PLANNED |
| **M9** | Mission Operations Interface | Web dashboard displays live robot positions, task status, and visual/thermal inspection evidence. | PLANNED |
| **M10** | Collaborative Demonstration | Full autonomous multi-robot mission: Robot A maps and identifies hot spot; Robot B executes thermal inspection. | PLANNED |
| **M11** | External SDK & Additional Robots | Public SDK integrates a simulated third robot using the standard agent interface. | PLANNED |
