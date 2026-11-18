# Subterranean Mine Simulation Scenarios

This directory documents the inspection and validation scenarios designed for testing autonomous behaviors within `mine_world.sdf`.

---

## 1. Scenario Catalog

### Scenario 1: Portal Entry & Initial Staging (Milestone M1 Baseline)
- **Objective**: Verify stable simulation initialization, lighting conditions, and collision geometry without robot drift or NaN physics explosions.
- **Environment**: Portal staging zone `(-6.0 to 0.0, 0.0, 0.0)`.
- **Validation**: Headless simulation execution for >= 50 iterations with 0 physics errors.

### Scenario 2: Main Haulage Drift Navigation (Milestone M2 & M4)
- **Objective**: Traverse 30 meters of straight tunnel containing a gravel patch ($\mu=0.40$), low-clearance hazard (1.7m), and mud patch ($\mu=0.22$).
- **Obstacles**: Timber roof support at X=5.0m, low clearance at X=18.0m, mud at X=22.0m.

### Scenario 3: T-Junction Obstacle Deconfliction (Milestone M4 & M8)
- **Objective**: Lead robot encounters a partial rockfall obstruction at T-Junction Alpha (X=28.5m), requiring tight obstacle circumnavigation or crosscut detour.
- **Obstacles**: `fallen_rock_pile` positioned on the right flank.

### Scenario 4: Steep Incline Test Ramp (Milestone M2 & M4)
- **Objective**: Tracked rover climbs the 15-degree inclined ramp (run: 12m, rise: 3.1m) to access the upper extraction drift.
- **Validation Criteria**: Pitch angle stability, wheel/track slip evaluation.

### Scenario 5: Subterranean RF Loss & Disconnection (Milestone M6 & M10)
- **Objective**: As a robot turns into the crosscut and east drift extension, signal strength drops past 2 corners below -95 dBm, inducing packet drop and link disconnection.
- **Validation**: Trigger decentralized lease timeout and reconnect behavior upon returning to line of sight.
