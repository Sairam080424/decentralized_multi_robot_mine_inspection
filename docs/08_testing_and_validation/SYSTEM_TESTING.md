# System Testing Scenarios

## 1. Scenario 1: Collaborative Mine Inspection
- **Objective**: Validate autonomous collaborative inspection between Robot A and Robot B.
- **Flow**:
  1. Mission DAG submitted containing 1 exploration task and 1 thermal inspection task.
  2. Robot A claims exploration task; navigates unmapped drift; discovers overheating transformer.
  3. New inspection task injected dynamically into DAG.
  4. Robot B wins auction for thermal inspection; navigates to transformer; captures 14-bit radiometric image.
  5. Mission marked COMPLETED; PDF report generated.

## 2. Scenario 2: Narrow Tunnel Spatial Deconfliction
- **Objective**: Validate right-of-way resolution in single-lane drifts.
- **Flow**:
  1. Robot A and Robot B commanded to travel in opposite directions along a 2.5m wide drift.
  2. Intent collision detected at $t = 15$s before encounter.
  3. Robot A yields into cross-cut; Robot B transits open drift; Robot A resumes nominal path.
