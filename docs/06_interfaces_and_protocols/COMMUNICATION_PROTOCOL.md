# Communication Protocol Specification

## 1. Multi-Tier Protocol Fabric
1. **Intra-Robot Communication**: ROS 2 DDS (CycloneDDS / FastDDS) operating on local robot loopback interfaces and separate `ROS_DOMAIN_ID`s (Robot A: Domain 10, Robot B: Domain 11).
2. **Inter-Robot P2P Mesh Communication**: Eclipse Zenoh peer-to-peer gossip protocol over ad-hoc wireless mesh (802.11s), providing low overhead (wire overhead marked TBD pending empirical benchmark) and built-in routing.
3. **Surface Observability Communication**: Asynchronous WebSockets and HTTP REST API for operations console connectivity.

## 2. Zenoh Key Expression Taxonomy
- `mine/discovery/scout`: Multicast peer discovery beacons.
- `mine/peers/{uuid}/heartbeat`: 2 Hz binary gossip heartbeat.
- `mine/peers/{uuid}/capabilities`: Queryable peer capability manifests.
- `mine/auctions/{task_id}/announce`: Auction task announcements.
- `mine/auctions/{task_id}/bid`: Submitted cost proposals.
- `mine/auctions/{task_id}/award`: Task award decisions.
- `mine/auctions/{task_id}/ack`: Winner task acknowledgment.
- `mine/auctions/{task_id}/lease`: Issued lease tokens.
- `mine/state/delta`: CRDT state mutation deltas.
- `mine/state/digest`: Anti-entropy version digest queries.
- `mine/coordination/intent`: Spatiotemporal 4D path intent.
- `mine/events/{category}/{type}`: Cluster event notifications.
