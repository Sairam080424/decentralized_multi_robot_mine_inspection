# Architectural Changelog

All notable architectural iterations, design decisions, and documentation releases are documented here conforming to [Keep a Changelog](https://keepachangelog.com/).

## [0.1.0] - 2026-11-18 &mdash; Milestone M0 Setup
### Added
- Complete three-layer decoupled architecture specification (Robot/Environment, Distributed Autonomy, Mission Operations).
- Full documentation suite for all 6 Layer 1 modules and 27 submodules with 16-section technical specifications.
- Full documentation suite for all 8 Layer 2 modules and 36 submodules covering Contract Net Protocol, CRDT state replication, and lease fault recovery.
- Full documentation suite for all 6 Layer 3 modules and 26 submodules covering mission planning, inspection evidence, databases, and SDK.
- Six Architectural Decision Records (ADRs): Decoupled 3-layer, CNP auctioning, Zenoh P2P, CRDT replication, Local Safety Autarchy, Behavior Trees.
- Formal JSON schemas for Robot Capabilities, Atomic Tasks, and Mission DAGs.
- Exhaustive technology evaluation of 13 open-source libraries.
- Complete development setup, coding standards, test strategy, and M0-M11 roadmap backlog.
