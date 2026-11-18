# Submodule 2.6.5: Reconnection and Reconciliation

## 1. Purpose
Executes automated, high-speed state synchronization when two partitioned robots re-establish radio communication after subterranean separation.

## 2. Responsibility
Detect peer reconnection, exchange compact state digests, identify divergent task and mission histories, stream missing deltas, and merge states to full convergence.

## 3. Scope
### In-Scope
Reconnection trigger handling, version digest exchange, delta backfilling, state reconciliation pipeline, and reconciliation completion events.

### Out-of-Scope
Physical vehicle path planning to rendezvous points.

## 4. System Architecture
```mermaid
sequenceDiagram
    autonumber
    participant A as Robot A (Was Partitioned)
    participant B as Robot B (Was Partitioned)

    Note over A,B: Robots enter radio range; Peer Discovery fires
    A->>B: Send State Digest: {V_A: [A:12, B:4], Task_Check: 0xA4F2}
    B->>A: Send State Digest: {V_B: [A:5, B:18], Task_Check: 0x89C1}
    Note over A,B: Detect Divergence: A is missing B:5..18, B is missing A:6..12
    A->>B: Request Deltas for Epochs B:5..18
    B->>A: Stream Deltas: [Task 2 COMPLETED, Task 3 ASSIGNED]
    B->>A: Request Deltas for Epochs A:6..12
    A->>B: Stream Deltas: [Task 1 COMPLETED, Inspection Point 4 Found]
    A->>A: Merge Remote Deltas (CRDT Engine)
    B->>B: Merge Remote Deltas (CRDT Engine)
    Note over A,B: Reconciliation Complete: Vector Clocks in Sync: [A:12, B:18]
```

## 5. Internal Submodules
- **Reconciliation Orchestrator**: Coordinates digest exchange and delta requests upon peer discovery events.
- **Digest Bloom Filter**: Uses compact bloom filters or Merkle trees to detect missing keys in large state catalogs rapidly.

## 6. Functional Requirements
- **REQ-2.6-009**: Reconciliation after a 10-minute communication partition shall complete within `[PROPOSED TARGET: < 1.0 s]` of link restoration.
- **REQ-2.6-010**: Reconciliation exchange shall not saturate more than 50% of available channel bandwidth.

## 7. Technical Approach
Trigger reconciliation automatically upon `PeerStatusChanged -> AVAILABLE` from Submodule 2.1.4. Exchange lightweight Merkle tree root hashes. If roots differ, traverse tree levels to identify and transmit only divergent deltas.

## 8. Open-Source Resources
### Merkle Tree Anti-Entropy Protocols
- **What it provides**: Logarithmic complexity divergence detection.
- **Why it is relevant**: Used in Dynamo and Cassandra for rapid reconciliation.
- **What we can reuse**: Merkle tree traversal concepts.
- **What we must develop ourselves**: Robotics-optimized state tree over Zenoh.


## 9. Prerequisites
Submodule 2.6.2 State Replication, Submodule 2.6.4 Conflict Detection.

## 10. Dependencies
- **Upstream Dependencies**: Submodule 2.6.2 State Replication, Submodule 2.6.4 Conflict Detection.
- **Downstream Dependencies**: Module 2.3 Mission Management, Module 2.4 Task Allocation.
- **Interfaces with Other Modules**: Zenoh queryables `mine/reconciliation/**`.

## 11. Development Phases
### Phase 1: Reconciliation Protocol
- **Objective**: Implement digest comparison and delta streaming.
- **Activities**: Code reconciliation handshake, simulate 10-minute network split and reconnect.
- **Required resources**: C++, Zenoh.
- **Input**: Divergent state stores.
- **Output**: Unified converged store.
- **Dependencies**: None.
- **Validation**: Disconnect robots, execute 20 tasks independently, reconnect; verify both reach identical state.
- **Completion criteria**: Reconciliation finishes in < 1.0 s.


## 12. Interfaces
### Zenoh Keys
- `mine/reconciliation/digest`: Zenoh queryable endpoint exchanging Merkle root digests.


## 13. Testing Strategy
Isolate Robot A and B in simulation; command Robot A to explore 3 frontiers and Robot B to inspect 2 targets; reconnect link; verify all 5 task results present on both robots.

## 14. Known Challenges
- **Brief Transient Connections**: Robots crossing a tunnel intersection might have only 3 seconds of radio contact; reconciliation must prioritize high-priority task status over large sensor evidence blobs.

## 15. Implementation Status
`PLANNED`

## 16. References
- **Merkle, A Digital Signature Based on a Conventional Encryption Function**: CRYPTO 1987
