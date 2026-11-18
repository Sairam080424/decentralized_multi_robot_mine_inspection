# ADR-003: Eclipse Zenoh for Distributed P2P Mesh Communication

- **Status**: PROPOSED / UNDER EVALUATION
- **Date**: 2026-11-18 (Updated: 2026-11-19)
- **Context**: Standard ROS 2 CycloneDDS/FastDDS discovery produces high multicast discovery traffic that floods low-bandwidth, high-jitter subterranean wireless mesh radios.
- **Decision**: Propose Eclipse Zenoh as candidate peer-to-peer transport protocol for Layer 2 inter-robot communication, while retaining standard ROS 2 DDS for intra-robot communication within Layer 1.
- **Evaluation Criteria & Alternatives**:
  - **Status**: Under active architectural evaluation; not a final binding decision.
  - **Alternatives Considered**: Native CycloneDDS with unicast discovery, FastDDS Discovery Server, and ZeroMQ/protobuf ad-hoc gossip.
  - **Empirical Evaluation Plan (Milestone M4 & M7)**:
    - Measure discovery time ($< 2.0\text{ s}$ target) and wire protocol overhead (marked **TBD** pending reproducible packet capture benchmarking).
    - Benchmark peer recovery latency after subterranean partition reconnection.
    - Measure CPU and memory footprint on resource-constrained embedded robot compute.
- **Consequences**:
  - Wire overhead: **[TBD - Pending Benchmark]** (projected compact framing undergoing empirical measurement against CycloneDDS in Milestone M4; no claims below 5 bytes accepted until supported by reproducible test logs).
  - Native support for ad-hoc routing and network partitions.
  - Requires maintaining `zenoh-bridge-dds` or direct Zenoh C/C++ client wrappers.
  - Final adoption decision contingent upon empirical network profiling in Milestone M4.
