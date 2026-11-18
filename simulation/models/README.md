# Subterranean Simulation Models

This directory contains the modular SDFormat (SDF) 1.9/1.10 models for tunnel structures, terrain patches, and underground hazards.

---

## 1. Modular Model Catalog

### A. Tunnel Segments
1. **`tunnel_straight_10m`**
   - Dimensions: 10.0m length, 3.5m width, 3.0m height.
   - Profile: Arched cross-section with multi-facet faceted rock ceiling and procedural wall irregularity.
   - Friction: Floor $\mu_1 = 0.85, \mu_2 = 0.75$.
2. **`tunnel_straight_20m_narrow`**
   - Dimensions: 20.0m length, 2.8m width, 2.6m height.
   - Profile: Rectangular cross-section representing narrow unlined extraction drifts.
   - Friction: Floor $\mu_1 = 0.80, \mu_2 = 0.70$.
3. **`tunnel_turn_90deg`**
   - Dimensions: 6.0m centerline radius, 90° curve, 3.5m clearance width.
   - Profile: Polygonal arc segments with outer and inner rock walls.
4. **`tunnel_t_junction`**
   - Dimensions: 12.0m main haulage drift intersecting 6.0m perpendicular crosscut branch.
   - Profile: 3-way underground intersection with clearance height 3.0m.
5. **`tunnel_ramp_15deg`**
   - Dimensions: 12.0m horizontal run, 15° pitch slope (0.2618 rad), 3.11m vertical rise.
   - Verification: Designed as a test configuration for steep incline negotiation.

### B. Terrain Patches
6. **`terrain_gravel_patch`**
   - Dimensions: 4.0m × 2.5m × 0.04m.
   - Surface Friction: $\mu_1 = 0.40, \mu_2 = 0.35$ (simulating loose stone and ballast slippage).
7. **`terrain_mud_patch`**
   - Dimensions: 4.0m × 2.5m × 0.03m.
   - Surface Friction: $\mu_1 = 0.22, \mu_2 = 0.20$ (simulating wet subterranean slurry with low traction).

### C. Obstacles and Environmental Hazards
8. **`fallen_rock_pile`**
   - Dimensions: 2.5m × 1.8m × 0.85m.
   - Composition: Composite primitive collision clusters representing jagged collapsed rockfall.
9. **`timber_roof_support`**
   - Dimensions: 3.6m span × 0.35m depth × 2.9m height.
   - Composition: Heavy timber posts (0.25m diameter) with crossbeam header and diagonal bracing.
10. **`standing_water`**
    - Dimensions: 5.0m × 2.2m × 0.02m.
    - Surface: Specular reflective puddle visual overlay with flat floor collision geometry.
11. **`mine_debris`**
    - Dimensions: 2.0m × 1.2m × 0.55m.
    - Composition: Abandoned piping, timber scraps, and metallic debris.
12. **`low_clearance_hazard`**
    - Dimensions: 3.8m span × 1.5m depth × 0.9m drop.
    - Clearance: Reduces tunnel overhead clearance to 1.7m, forcing sensors/masts to retract.

---

## 2. Model Structure

Every model directory follows standard Gazebo Sim conventions:
```text
<model_name>/
├── model.config    # Metadata, author information, and SDF version declaration
└── model.sdf       # Links, visuals, physical collision geometries, and surface properties
```

---

## 3. Usage in SDF Worlds

Include any modular model inside a world file using the `model://` scheme:
```xml
<include>
  <uri>model://fallen_rock_pile</uri>
  <name>rock_pile_alpha</name>
  <pose>28.5 0.8 0.0 0 0 0.2</pose>
</include>
```
Make sure `SDF_PATH` or `GZ_SIM_RESOURCE_PATH` contains the directory path `simulation/models`.
