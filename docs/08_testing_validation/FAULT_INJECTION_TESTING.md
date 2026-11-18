# Fault Injection Testing Specification

## 1. Test Suite: RF Mesh Degradation
- **Synthetic Packet Drop**: Inject 10%, 30%, 50%, and 80% packet loss over Zenoh inter-robot links.
- **Evaluation**: Verify anti-entropy gossip achieves complete CRDT state convergence without crashing or stalling.

## 2. Test Suite: Catastrophic Robot Crash & Lease Revocation
- **Injection**: Send `SIGKILL` to Robot A while actively executing an inspection task.
- **Evaluation**:
  1. Robot B detects missing heartbeat within 5.0 seconds ($\phi \ge 8.0$).
  2. Robot B marks Robot A as `UNREACHABLE`.
  3. Robot B revokes Robot A's task lease upon expiration.
  4. Robot B re-auctions task to itself and completes the mission autonomously.
