# Layer 2 Architectural Overview

## 1. Principles of Operation
Layer 2 executes an identical distributed autonomy kernel on every participating robot. Key operating principles include:
1. **Fully Decentralized Decision-Making**: No single master or centralized broker governs task auctions or mission decisions. Any robot can initiate an auction or act as an ephemeral clearing house.
2. **Contract Net Protocol (CNP)**: Tasks are broadcast to the ad-hoc cluster; candidate robots formulate bids using multi-factor cost functions ($Cost = w_1 D_{travel} + w_2 E_{battery} + w_3 T_{risk} - w_4 C_{fit}$); the lowest-cost capable robot is awarded the task.
3. **Partition-Tolerant State Replication**: Robot state, task claims, and completed inspection milestones are stored in Conflict-Free Replicated Data Types (CRDTs). When radio links break, robots continue autonomous local execution. When links rejoin, anti-entropy gossip merges state deltas without manual conflict resolution.
4. **Time-Bounded Task Leases**: Every task assignment is granted under a renewable lease token. If a robot crashes, stalls, or is cut off indefinitely, peer robots detect lease expiration and autonomously re-auction the task.
