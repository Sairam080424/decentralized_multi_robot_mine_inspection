# ADR-002: Distributed Contract Net Protocol (CNP) for Task Allocation

- **Status**: ACCEPTED
- **Date**: 2026-11-18
- **Context**: Subterranean radio frequency attenuation and line-of-sight tunnel corners prevent relying on a permanent central task dispatcher.
- **Decision**: Deploy an ad-hoc Contract Net Protocol (CNP) where tasks are broadcast to candidate peers and awarded to the lowest-cost capable bidder using multi-factor cost functions ($D_{travel}, E_{battery}, T_{risk}, C_{fit}$).
- **Consequences**:
  - Eliminates single point of failure in mission assignment.
  - Requires bounded auction windows (200-500 ms) and deterministic tie-breaking (lowest UUID hash).
