# Module 1.5: Robot Agent Interface

## 1. Module Overview
Module 1.5 provides the decoupling bridge between Layer 1 (physical platform/simulation) and Layer 2 (distributed multi-robot autonomy). It encapsulates hardware-specific specifics behind an abstract, standardized Robot Agent interface.

## 2. Submodule Index
- [1.5.1 Robot Identity](robot_identity.md): Unique cryptographic UUID, hardware fingerprinting, and archetype role declaration.
- [1.5.2 Capability Description](capability_description.md): Declarative capability model declaring sensor payloads, speed, battery, and operational limits.
- [1.5.3 Robot State Manager](robot_state_manager.md): Formal lifecycle finite state machine (FSM) governing robot operational states.
- [1.5.4 Task Execution Interface](task_execution_interface.md): Action server consuming assigned tasks from Layer 2 and dispatching them to Nav2.
- [1.5.5 Local Safety Manager](local_safety_manager.md): Authoritative, un-preemptible local safety watchdog overriding velocity commands during hazards.
