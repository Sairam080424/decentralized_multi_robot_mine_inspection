# Submodule 2.6.3: Version Management

## 1. Purpose
Tracks causal history and event ordering across distributed robot agents using causal vector clocks and Lamport timestamps.

## 2. Responsibility
Maintain local vector clock vectors, increment clock epochs on state mutations, embed vector clocks in all state messages, and establish partial causal ordering.

## 3. Scope
### In-Scope
Vector clock data structure, Lamport timestamp generation, causal dominance comparison ($V_A < V_B, V_A > V_B, V_A \parallel V_B$), and clock serialization.

### Out-of-Scope
Wall-clock NTP network time synchronization.

## 4. System Architecture
```mermaid
flowchart LR
    LocalEvent["Local Task Mutation Event"] --> Increment["Increment Clock: V[robot_id]++"]
    Increment --> Embed["Embed Vector Clock in Mutation Delta"]
    Embed --> RemoteRecv["Remote Peer Ingests Delta"]
    RemoteRecv --> MergeClock["Merge Clock: V_local[i] = max(V_local[i], V_remote[i])"]
    MergeClock --> UpdatedClock["Updated Local Vector Clock"]
```

## 5. Internal Submodules
- **Vector Clock Manager**: Maintains map of `{robot_uuid: logical_sequence}` for all cluster members.
- **Causal Ordering Evaluator**: Compares two vector clocks to determine if one causally preceded the other or if they are concurrent ($V_A \parallel V_B$).

## 6. Functional Requirements
- **REQ-2.6-005**: Vector clock comparison shall correctly classify causal precedence and concurrency in 100% of cases.
- **REQ-2.6-006**: Vector clock serialization overhead shall scale linearly with cluster size $O(N)$ and not exceed 64 bytes for $N \le 4$.

## 7. Technical Approach
Implement a compact `VectorClock` class in C++. Vector clocks represent a partial order $\le$: $V_1 \le V_2 \iff \forall k, V_1[k] \le V_2[k]$. If neither dominates, the events are concurrent ($V_1 \parallel V_2$) and require CRDT conflict resolution.

## 8. Open-Source Resources
### Lamport Vector Clocks
- **What it provides**: Foundational distributed systems timekeeping.
- **Why it is relevant**: Guarantees causal consistency without synchronized physical clocks.
- **What we can reuse**: Vector clock comparison math.
- **What we must develop ourselves**: C++ memory-efficient implementation.


## 9. Prerequisites
Modern C++.

## 10. Dependencies
- **Upstream Dependencies**: None.
- **Downstream Dependencies**: Submodule 2.6.4 Conflict Detection, Submodule 2.6.5 Reconciliation.
- **Interfaces with Other Modules**: C++ API `VectorClock::compare(V1, V2)`.

## 11. Development Phases
### Phase 1: Vector Clock Library
- **Objective**: Implement C++ VectorClock data class.
- **Activities**: Code clock arithmetic, test causal comparison edge cases.
- **Required resources**: C++, GTest.
- **Input**: Event sequences.
- **Output**: Vector clock comparisons.
- **Dependencies**: None.
- **Validation**: Test concurrent and ordered clock pairs; verify correct comparison.
- **Completion criteria**: Passes all causal order unit tests.


## 12. Interfaces
### Data Types
- `VectorClock`: std::unordered_map<std::string, uint64_t> mapping robot UUID to logical sequence.


## 13. Testing Strategy
Generate simulated concurrent mutations across partitioned nodes; verify vector clock comparator identifies them as concurrent ($V_1 \parallel V_2$).

## 14. Known Challenges
- **Dynamic Node Churn**: Adding and removing robots dynamically requires garbage-collecting dormant robot entries from vector clock arrays.

## 15. Implementation Status
`PLANNED`

## 16. References
- **Lamport, Time, Clocks, and the Ordering of Events in a Distributed System**: Communications of the ACM, 1978
