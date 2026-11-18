# Founder / Principal Architect Code Review Checklist

> **Purpose**: This checklist is used by the Technical Founder / Principal Systems Architect to systematically review every Pull Request (PR) before merging into `develop` or `main`. It guarantees architectural integrity, safety autarchy, and high documentation standards as the team scales.

---

## 1. Architectural Integrity & Layer Isolation

- [ ] **Layer Dependency Direction**:
  - Layer 1 (Robot & Environment) depends only on OS, ROS 2, hardware/simulation, and math libraries. Zero dependencies on Layer 2 or Layer 3.
  - Layer 2 (Distributed Autonomy) depends only on abstract robot interfaces and middleware (Zenoh). Zero hardware or simulation engine couplings.
  - Layer 3 (Mission & Operations) depends on Layer 2 interfaces or Layer 1 state summaries. **Zero direct actuator or motor control paths**.
- [ ] **Decentralization Principle**:
  - The module does not assume or introduce a centralized single-point-of-failure mission master.
  - Distributed decisions rely on peer-to-peer negotiation (e.g., Contract Net Protocol) or replicated state (e.g., CRDTs).
- [ ] **Interface Schema Immutability**:
  - Does the PR modify any message, service, action, or schema in `interfaces/`?
  - If YES: Is there an approved Architectural RFC attached? If NO, PR is rejected immediately.

---

## 2. Safety & Fault Isolation

- [ ] **Local Safety Manager Autarchy**:
  - Confirm no modification weakens or bypasses `local_safety_manager.cpp` (50 Hz emergency stop, tilt limit, obstacle proximity brake).
  - Safety authority remains strictly local to each robot agent.
- [ ] **Communication Disruption Resilience**:
  - In Layer 2 and Layer 3 PRs: Does the code handle packet drops, network partitioning, and delay gracefully?
  - Are timeout thresholds labeled as `PROPOSED TARGET` or validated with test logs?

---

## 3. Code Quality, Standards & Testing

- [ ] **Code Standards Compliance**:
  - C++20: ROS 2 C++ style guide, `clang-format`, `clang-tidy` clean.
  - Python 3.10: PEP 8, formatted with `black`, linted with `flake8`, type annotated with `mypy`.
- [ ] **Unit & Mock Test Coverage**:
  - Are all new public methods covered by unit tests in `tests/`?
  - Unit test line coverage >= 80% for the modified package.
  - No network or physical hardware dependencies in unit tests (use mocks/stubs).
- [ ] **Lifecycle Management**:
  - If a ROS 2 node is introduced, does it conform to ROS 2 Managed Node (Lifecycle) state transitions (`unconfigured` -> `inactive` -> `active` -> `finalized`)?

---

## 4. Documentation & Verification

- [ ] **Lifecycle State Truthfulness**:
  - Does the documentation accurately represent the implementation status (`PLANNED`, `IN_PROGRESS`, `IMPLEMENTED`, `TESTED`)?
  - Reject PR if future or planned features are documented as already implemented.
- [ ] **Performance Claims**:
  - All latency, throughput, and battery duration figures are either flagged as `[PROPOSED TARGET]` or backed by reproducible test output logs.
- [ ] **Internal Link Integrity**:
  - Run `python3 tools/verify_repository.py` on the PR branch.
  - Audit output must report:
    * `Template Incompleteness Errors: 0`
    * `Broken Internal Relative Links: 0`
    * `Mermaid Diagram Syntax Errors: 0`
    * `Unimplemented Claims: 0`

---

## 5. Git Hygiene & Review Decision

- [ ] **Commit History**:
  - Commits follow Conventional Commits standard (`feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `arch`).
  - No merge commits from intermediate branches; PR is cleanly rebased on the target branch.
- [ ] **Review Decision**:
  - [ ] **APPROVE & MERGE**: All criteria fully met.
  - [ ] **REQUEST CHANGES**: Deficiencies noted above with actionable comments.
  - [ ] **REJECT**: Fundamental architectural violation or unapproved interface mutation.
