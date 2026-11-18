# Testing Guidelines & Coverage

## 1. Testing Pyramid
1. **Unit Tests (70%)**: Pure algorithmic testing (cost calculation, CRDT merge, DAG validation) without ROS middleware or physics overhead.
2. **Integration Tests (20%)**: Multi-node interaction testing using `launch_testing` and mock action servers.
3. **Simulation Tests (10%)**: End-to-end mission scenarios executed in Gazebo Sim.

## 2. Running Automated Tests
```bash
# Run all unit tests
colcon test --event-handlers console_direct+

# Check test results
colcon test-result --all --verbose
```

## 3. Code Coverage Requirements
- Target line coverage: `>= 80%` on all Layer 2 autonomy and Layer 1 safety logic.
- Coverage reports generated via `gcov` / `lcov` for C++ and `pytest-cov` for Python.
