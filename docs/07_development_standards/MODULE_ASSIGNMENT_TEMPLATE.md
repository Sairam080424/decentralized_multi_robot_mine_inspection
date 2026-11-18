# Module Assignment & Onboarding Template

> **Purpose**: This template defines the contract between the Principal Architect / Founder and an incoming developer assigned to design or implement a specific module or submodule within the Decentralized Multi-Robot Mine Inspection Platform.

---

## 1. Module Assignment Metadata

| Field | Value |
| :--- | :--- |
| **Module ID** | `MOD-<Layer>.<Number>` (e.g., `MOD-1.5`, `MOD-2.2`) |
| **Module Name** | [Module Full Name] |
| **Assigned Developer** | [Developer Full Name / GitHub Handle] |
| **Target Milestone** | [e.g., M2, M4, M8] |
| **Assignment Date** | YYYY-MM-DD |
| **Expected Delivery Date** | YYYY-MM-DD |
| **Architectural Reviewer** | Principal Robotics Systems Architect (Founder) |

---

## 2. Mandatory Reading & Prerequisites

Before writing any code or modifying documentation, the assignee must review and sign off on:
- [ ] [PROJECT_CHARTER.md](../../docs/00_project_overview/PROJECT_CHARTER.md) - Project scope, vision, and system boundaries.
- [ ] [SYSTEM_REQUIREMENTS.md](../../docs/02_requirements/SYSTEM_REQUIREMENTS.md) - System requirements baseline.
- [ ] [THREE_LAYER_ARCHITECTURE.md](../../docs/01_system_architecture/THREE_LAYER_ARCHITECTURE.md) - Strict layer boundaries and data flow.
- [ ] [SHARED_INTERFACE_DEFINITIONS.md](../../docs/06_interfaces_and_protocols/SHARED_INTERFACE_DEFINITIONS.md) - Core shared message and protocol schemas.
- [ ] [MODULE_OWNERSHIP_AND_INTERFACES.md](./MODULE_OWNERSHIP_AND_INTERFACES.md) - Write boundaries and prohibited paths.
- [ ] [ADR-001 through ADR-006](../../docs/10_architecture_decision_records/) - Architectural Decision Records.

---

## 3. Scope of Work & Ownership Boundaries

### Permitted Write Paths (Exclusive Ownership)
The assignee has write permission **only** within their assigned module directories:
- `docs/0X_<layer>/<module_dir>/`
- `src/<layer>/<module_pkg>/`
- `tests/<layer>/<module_pkg>/`

### Prohibited Files & Direct Access
- **STRICTLY PROHIBITED**: Modifying any file in `interfaces/` (Requires an approved Architectural RFC).
- **STRICTLY PROHIBITED**: Modifying `src/layer1_robot_environment/robot_agent/local_safety_manager.cpp`.
- **STRICTLY PROHIBITED**: Introducing upward dependencies (e.g., Layer 1 importing Layer 2, Layer 2 importing Layer 3).
- **STRICTLY PROHIBITED**: Accessing hardware/actuator topics directly from Layer 3.

---

## 4. Requirements Traceability

The assigned module must address the following requirement IDs from [SYSTEM_REQUIREMENTS.md](../../docs/02_requirements/SYSTEM_REQUIREMENTS.md):
- [Requirement ID 1]: [Short description and acceptance threshold]
- [Requirement ID 2]: [Short description and acceptance threshold]
- [Requirement ID 3]: [Short description and acceptance threshold]

---

## 5. Technical Deliverables

1. **Submodule Architecture & Design Documentation**:
   - Update all corresponding submodule Markdown files in `docs/` adhering to the standard 16-section template.
   - Status transitions from `PLANNED` to `IN_PROGRESS` and finally `IMPLEMENTED`/`TESTED`.
2. **Interface Implementations**:
   - ROS 2 node definitions, lifecycle state machine bindings, and Zenoh pub/sub handlers adhering to `SHARED_INTERFACE_DEFINITIONS.md`.
3. **Source Code**:
   - Clean, modular C++20 or Python 3.10 code complying with project linting and formatting rules.
4. **Test Suite**:
   - Unit tests (`tests/unit/`) achieving >= 80% line coverage.
   - Mock integration tests (`tests/integration/`) simulating upstream/downstream nodes.
   - Fault injection or communication disruption tests where applicable.

---

## 6. Definition of Done (DoD) Checklist

The Pull Request will not be approved or merged into `main` unless all criteria are satisfied:
- [ ] **Interface Adherence**: All published/subscribed topics conform strictly to `SHARED_INTERFACE_DEFINITIONS.md`.
- [ ] **No Unverified Claims**: Submodule status reflects actual implementation state; no unmeasured performance benchmarks.
- [ ] **Static Analysis & Linting**: Zero warnings in `clang-tidy`, `clang-format`, `flake8`, `black`, and `ament_lint`.
- [ ] **Unit Tests Passing**: 100% of unit tests pass in local and CI environments.
- [ ] **Documentation Complete**: All architectural files and user guides updated; `python3 tools/verify_repository.py` passes with 0 errors.
- [ ] **Founder Sign-off**: Pull request approved by the Principal Architect following the [CODE_REVIEW_CHECKLIST.md](./CODE_REVIEW_CHECKLIST.md).
