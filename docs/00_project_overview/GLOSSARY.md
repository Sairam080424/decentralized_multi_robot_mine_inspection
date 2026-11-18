# Technical Glossary

| Term | Definition |
|---|---|
| **Agent** | An autonomous software entity encapsulating a physical or simulated robot, exposing standardized discovery, capability, and task execution interfaces. |
| **Auctioneer** | A temporary, peer-elected agent that initiates an auction round for unassigned tasks and clears bids under Contract Net Protocol. |
| **Bid** | A cost proposal submitted by a robot agent for a specific task, calculated from travel distance, energy budget, sensor capability match, and operational risk. |
| **Capability** | A formal semantic descriptor declaring an agent's locomotion type, sensor modalities, compute headroom, battery reserve, and certified payload operations. |
| **Contract Net Protocol (CNP)** | A decentralized negotiation protocol where tasks are announced, bid on by candidate agents, and awarded based on cost functions. |
| **CRDT (Conflict-Free Replicated Data Type)** | A data structure that can be replicated across multiple nodes, modified concurrently without coordination, and mathematically guaranteed to converge to a consistent state. |
| **Heartbeat** | A periodic, low-overhead broadcast packet transmitting an agent's UUID, sequence number, operational state, and vector clock epoch. |
| **Lease** | A time-bounded lock granting an agent exclusive right to execute a specific task. If not renewed before expiration, the task becomes eligible for reassignment. |
| **Local Safety Autarchy** | The fundamental design rule stating that each robot's Layer 1 safety manager possesses absolute, un-preemptible authority to stop motion. |
| **LWW-Element-Set** | Last-Write-Wins Element Set; a CRDT set variant using timestamps to resolve concurrent additions and deletions of task states. |
| **Mission** | A high-level operational objective structured as a Directed Acyclic Graph (DAG) of interdependent tasks. |
| **MPPI** | Model Predictive Path Integral controller; a sampling-based trajectory controller in Nav2 optimized for rough terrain navigation. |
| **OR-Set** | Observed-Remove Set; a state-based CRDT where elements are uniquely tagged to support multiple add-and-remove cycles without race conditions. |
| **SLAM** | Simultaneous Localization and Mapping; real-time estimation of robot pose and environmental geometry in GPS-denied environments. |
| **Vector Clock** | An array of logical clocks maintained by each agent to establish causal ordering of distributed events across intermittent networks. |
| **Zenoh** | Eclipse Zenoh; a zero-overhead publish/subscribe/query protocol designed for resource-constrained robotics and edge networks. |
