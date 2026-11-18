# Module 2.5: Distributed Coordination

## 1. Module Overview
Module 2.5 enables peer-to-peer spatial and temporal coordination between robots in narrow subterranean mine tunnels, temporary coordinator elections without a persistent master, right-of-way conflict resolution, and barrier synchronization.

## 2. Submodule Index
- [2.5.1 Peer-to-Peer Coordination](peer_to_peer_coordination.md): Direct robot-to-robot rendezvous, spatial deconfliction, and intent sharing.
- [2.5.2 Temporary Coordinator Election](temporary_coordinator_election.md): Bully / Raft-inspired ephemeral leader election for specific mission epochs.
- [2.5.3 Conflict Resolution](conflict_resolution.md): Right-of-way rules in single-lane drifts (loaded/inspecting robot takes priority).
- [2.5.4 Mission Synchronization](mission_synchronization.md): Distributed barrier synchronization (e.g. Robot A verifies tunnel clearance before Robot B enters).
