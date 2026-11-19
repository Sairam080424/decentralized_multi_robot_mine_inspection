# Subterranean Mine Simulation Worlds

This directory contains the world definition files for Gazebo Sim (Harmonic 8.15.0 / SDFormat 14).

---

## 1. Worlds Catalog

### `mine_world.sdf`
The canonical subterranean inspection world for the multi-robot platform.

- **SDF Version**: `<sdf version="1.9">`
- **Physics Engine**: DART (`dartsim`)
- **Step Size**: 1 ms (`0.001 s`)
- **Real-Time Factor Target**: 1.0 at 1000 Hz update rate
- **Gravity Vector**: `[0.0, 0.0, -9.81]` m/s²
- **Scene Lighting**:
  - Global Subterranean Ambient: `0.04 0.04 0.04 1.0` (deep underground darkness)
  - Background: `0.01 0.01 0.01 1.0`
  - Localized Point Lights:
    * `portal_lantern`: Staging portal entrance at `(0.0, 0.0, 2.5)`
    * `mid_drift_light`: Straight haulage drift midpoint at `(15.0, 0.0, 2.4)`
    * `junction_light`: T-junction Alpha intersection at `(30.0, 0.0, 2.5)`
    * `ramp_crest_light`: Crest of the 15-degree ramp at `(52.0, 0.0, 5.0)`

---

## 2. World Layout & Coordinates

The mine network extends over 125 meters of interconnected tunnels:

```text
[Portal Staging] (X: -6 to 0, Y: 0)
       |
       v
[Drift 1: Main Haulage] (X: 0 to 30, Y: 0)
       |
       +---> [T-Junction Alpha] (X: 30, Y: 0)
       |              |
       |              v
       |      [Crosscut Drift] (X: 30, Y: 0 to 20)
       |              |
       |              v
       |      [90° Turn East] (X: 30 to 36, Y: 20 to 26)
       |              |
       |              v
       |      [East Drift Extension] (X: 36 to 56, Y: 25)
       |
       v
[15° Incline Ramp] (X: 42 to 54, Y: 0, Z: 0 to 3.22)
       |
       v
[Upper Level Drift] (X: 54 to 68, Y: 0, Z: 3.22)
```

---

## 3. Spawn Points & Robot Placement

All robot spawn points are positioned outside the portal staging zone in clear terrain:

- **Robot 1 (Lead Inspector / Robot A)**:
  - Pose: `[-2.0, -1.0, 0.1, 0.0, 0.0, 0.0]`
  - Purpose: Wheeled scout entering main haulage drift.
- **Robot 2 (Secondary Explorer / Robot B)**:
  - Pose: `[-4.0, 1.0, 0.1, 0.0, 0.0, 0.0]`
  - Purpose: Tracked chassis with thermal mast for high-roughness/ramp inspection.
- **Robot 3 (Communication Relay)**:
  - Pose: `[-6.0, 0.0, 0.1, 0.0, 0.0, 0.0]`
  - Purpose: Line-of-sight portal gateway relay station.

> [!NOTE]
> In Milestone M1, no robot entities are spawned in the world SDF file. Robot URDF/Xacro models and sensor configurations are implemented in Milestone M2.

---

## 4. Verification

Validate the world file using Gazebo Sim:
```bash
SDF_PATH="$(pwd)/simulation/models" gz sdf -k simulation/worlds/mine_world.sdf
```
