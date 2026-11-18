# ADR-003: Eclipse Zenoh for Distributed P2P Mesh Communication

- **Status**: ACCEPTED (PROPOSED baseline for verification)
- **Date**: 2026-11-18
- **Context**: Standard ROS 2 CycloneDDS/FastDDS discovery produces high multicast discovery traffic that floods low-bandwidth, high-jitter subterranean wireless mesh radios.
- **Decision**: Adopt Eclipse Zenoh as the peer-to-peer transport protocol for Layer 2 inter-robot communication, while retaining standard ROS 2 DDS for intra-robot communication within Layer 1.
- **Consequences**:
  - Wire overhead reduced to < 5 bytes header.
  - Native support for ad-hoc routing and network partitions.
  - Requires deploying `zenoh-bridge-dds` or direct Zenoh client libraries.
