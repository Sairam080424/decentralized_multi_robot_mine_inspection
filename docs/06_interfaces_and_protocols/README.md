# Interfaces and Protocols

This directory contains formal interface contracts, data schemas, communication protocols, and standardized error codes governing interactions across all three system layers.

## Documents
- [ROBOT_INTERFACE.md](ROBOT_INTERFACE.md): Interface specification between Layer 1 (Robot Environment) and Layer 2 (Distributed Autonomy).
- [CAPABILITY_SCHEMA.md](CAPABILITY_SCHEMA.md): JSON schema defining declarative robot capabilities, locomotion, sensors, and resources.
- [TASK_SCHEMA.md](TASK_SCHEMA.md): JSON schema defining atomic tasks, parameters, constraints, and dependencies.
- [MISSION_SCHEMA.md](MISSION_SCHEMA.md): JSON schema defining high-level missions structured as Directed Acyclic Graphs (DAGs).
- [COMMUNICATION_PROTOCOL.md](COMMUNICATION_PROTOCOL.md): Wire formats, Zenoh/DDS topic taxonomy, QoS profiles, and gossip serialization.
- [ERROR_CODES.md](ERROR_CODES.md): Standardized hexadecimal error codes across hardware, autonomy, and mission operations.
