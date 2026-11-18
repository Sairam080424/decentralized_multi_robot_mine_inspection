# Module 2.8: Distributed Runtime Interface

## 1. Module Overview
Module 2.8 provides the standardized boundary interfaces for the Distributed Autonomy Layer: the Robot Agent Gateway interfacing with Layer 1, the Mission Ingestion API, the distributed publish/subscribe Event Interface, and runtime observability tracing.

## 2. Submodule Index
- [2.8.1 Robot Agent Gateway](robot_agent_gateway.md): Abstraction bridge translating Layer 2 abstract tasks to Layer 1 ROS 2 Action Goals.
- [2.8.2 Mission API](mission_api.md): Internal asynchronous API for mission submission, pausing, resuming, and aborting.
- [2.8.3 Event Interface](event_interface.md): Distributed pub/sub event bus for cluster autonomy events (TaskAssigned, HazardDetected).
- [2.8.4 Runtime Observability](runtime_observability.md): Distributed tracing, OpenTelemetry span propagation, and P2P RPC performance logging.
