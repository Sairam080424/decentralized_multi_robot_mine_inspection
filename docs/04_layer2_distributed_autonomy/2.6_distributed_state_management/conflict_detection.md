# Submodule 2.6.4: Conflict Detection and CRDT Resolution

## 1. Purpose
Detects concurrent conflicting mutations and resolves them deterministically using Conflict-Free Replicated Data Types (CRDTs).

## 2. Responsibility
Detect concurrent task state updates ($V_A \parallel V_B$), resolve state divergence using LWW-Element-Set (Last-Write-Wins) and OR-Set (Observed-Remove Set) semantics, and guarantee mathematical convergence.

## 3. Scope
### In-Scope
LWW-Element-Set implementation, OR-Set implementation, deterministic tie-breaking for equal timestamps, and state convergence guarantees.

### Out-of-Scope
Human operator manual conflict reconciliation.

## 4. System Architecture
```mermaid
flowchart TD
    DeltaIn["Incoming Remote State Delta"] --> CausalCheck{"Compare Vector Clocks: V_local vs V_remote"}
    CausalCheck -->|V_remote Dominates| ApplyRemote["Accept Remote: Overwrite Local State"]
    CausalCheck -->|V_local Dominates| IgnoreRemote["Ignore Remote: Local State is Newer"]
    CausalCheck -->|Concurrent (V_local || V_remote)| CRDT_Resolver["CRDT Resolution Engine"]
    CRDT_Resolver --> LWW["LWW-Element-Set: Select Mutation with Highest Physical Timestamp"]
    LWW --> EqualTime{"Timestamps Identical?"}
    EqualTime -->|YES| HashTie["Tie Breaker: Select Mutation from Lowest Robot UUID"]
    EqualTime -->|NO| Winner["Commit Winning Mutation"]
    HashTie --> Winner
    Winner --> Converged["State Converged across Both Robots"]
```

## 5. Internal Submodules
- **LWW-Element-Set Engine**: Manages state fields where the latest update takes precedence (e.g. task execution progress %).
- **OR-Set Engine**: Manages collections of discovered obstacles and completed inspection targets supporting concurrent additions.

## 6. Functional Requirements
- **REQ-2.6-007**: Conflict resolution shall execute completely deterministically with zero divergence across peer nodes.
- **REQ-2.6-008**: CRDT merge operation shall be mathematically associative, commutative, and idempotent ($A \sqcup B = B \sqcup A$, $A \sqcup A = A$).

## 7. Technical Approach
Deploy state-based and delta-based CRDT data structures in modern C++. For task status mutations, use Last-Write-Wins with hybrid logical clocks (HLC). For discovered inspection points, use Observed-Remove Sets (OR-Sets).

## 8. Open-Source Resources
### Shapiro et al., Conflict-Free Replicated Data Types
- **What it provides**: Formal mathematical proofs for distributed convergence.
- **Why it is relevant**: Ensures provably correct state merging without consensus locks.
- **What we can reuse**: CRDT convergence theorems.
- **What we must develop ourselves**: C++ robotics CRDT library.


## 9. Prerequisites
Submodule 2.6.3 Version Management.

## 10. Dependencies
- **Upstream Dependencies**: Submodule 2.6.3 Version Management.
- **Downstream Dependencies**: Submodule 2.6.5 Reconnection and Reconciliation.
- **Interfaces with Other Modules**: C++ API `CRDT::merge(state_a, state_b)`.

## 11. Development Phases
### Phase 1: CRDT Library Development
- **Objective**: Implement LWW and OR-Set CRDT classes.
- **Activities**: Code data structures, prove associativity and commutativity via property-based testing.
- **Required resources**: C++, RapidCheck / GTest.
- **Input**: Conflicting mutations.
- **Output**: Converged states.
- **Dependencies**: None.
- **Validation**: Merge conflicting states in reverse orders ($A \sqcup B$ and $B \sqcup A$); verify identical output.
- **Completion criteria**: 100% convergence in 10,000 randomized merge tests.


## 12. Interfaces
### APIs
- `crdt_engine::merge_delta(local_state, incoming_delta)`: Merges delta into local state.


## 13. Testing Strategy
Generate 100 concurrent conflicting task mutations across Robot A and B; merge states; verify both robots reach bit-for-bit identical state stores.

## 14. Known Challenges
- **Physical Clock Skew in LWW**: Extreme clock skew could cause an older event to overwrite a newer event; mitigated using Hybrid Logical Clocks (HLC) binding logical and physical time.

## 15. Implementation Status
`PLANNED`

## 16. References
- **Shapiro et al., Conflict-Free Replicated Data Types**: Symposium on Self-Stabilizing Systems, 2011
