# Integration Testing Specification

## 1. Inter-Layer Integration Tests
- `test_gateway_to_nav2`: Tests Robot Agent Gateway translating an abstract task into a Nav2 `NavigateToPose` goal and relaying feedback.
- `test_zenoh_to_ros_bridge`: Tests bidirectional telemetry mapping between ROS 2 local topics and Zenoh network key expressions.
- `test_auction_handshake`: Spins up Robot A and Robot B autonomy nodes in separate processes; executes a mock Contract Net Protocol auction; validates two-phase commit agreement.
