# Contributing Guidelines

Welcome to the **Decentralized Multi-Robot Mine Inspection Platform**. This document defines the engineering standards, contribution workflow, and review policies for all project contributors.

---

## 1. Core Engineering Principles

1. **Documentation Before Implementation**: Architectural documentation, interface definitions, requirement traceability, and test specifications must be merged and reviewed *before* writing production code.
2. **Never Claim Unimplemented Features**: Submodules and features must reflect their true lifecycle state (`PLANNED`, `IN_PROGRESS`, `BLOCKED`, `IMPLEMENTED`, `TESTED`, `VERIFIED`). Never mark planned functionality as implemented.
3. **No Unverified Benchmarks**: Performance metrics must be documented as `[PROPOSED TARGET]` until validated through reproducible simulation or hardware test benches.
4. **Local Safety Autarchy**: No code contribution may bypass or weaken Layer 1 local robot safety managers.
5. **Decoupled Architecture**: Layer 2 (Autonomy) must not depend on concrete hardware implementations; Layer 3 (Operations) must never command robot actuators directly.

---

## 2. Git Workflow & Branching Strategy

- **`main`**: Production-ready, fully verified milestone releases.
- **`develop`**: Primary integration branch for verified feature sets.
- **`feature/<module>-<description>`**: Scoped feature work branched from `develop`.
- **`fix/<issue-id>-<description>`**: Bug and hotfix branches.
- **`docs/<topic>`**: Documentation and architectural enhancements.

### Commit Conventions (Conventional Commits)
All commit messages must strictly adhere to the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/) format:
```text
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

Allowed types:
- `feat`: A new user-facing or architectural capability.
- `fix`: A bug fix or defect correction.
- `docs`: Documentation additions or revisions only.
- `arch`: Architectural decision records or design revisions.
- `test`: Unit, integration, or fault-injection test implementations.
- `refactor`: Code restructuring without functional behavior modification.
- `ci`: Continuous integration or build configuration adjustments.

---

## 3. Pull Request Requirements

Every Pull Request (PR) must satisfy the following checklist before merge consideration:
- [ ] Requirement Traceability: Directly references an approved issue or `REQ-X.Y-ZZZ` identifier.
- [ ] Documentation Updated: Relevant submodule documentation updated, including Development Phases and Interface specifications.
- [ ] No Circular Dependencies: Layer boundaries strictly respected.
- [ ] Linting & Formatting Passed: `flake8`, `black`, `clang-format`, and ROS 2 linters pass with zero warnings.
- [ ] Test Suite Added: Unit tests and/or simulation verification scripts included.
- [ ] Clean Git History: Linear history without merge commits; commits logically atomic.
