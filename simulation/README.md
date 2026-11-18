# Subterranean Mine Simulation Assets (Milestone M1)

This directory contains the simulation assets, Gazebo Sim worlds, procedural generators, terrain configurations, and modular hazard models for Milestone M1 of the **Decentralized Multi-Robot Mine Inspection Platform**.

---

## 1. Directory Structure

```text
simulation/
├── configurations/          # Simulation configuration guides and notes
│   └── README.md
├── models/                  # Reusable SDFormat (SDF) 1.9/1.10 models
│   ├── fallen_rock_pile/
│   ├── low_clearance_hazard/
│   ├── mine_debris/
│   ├── standing_water/
│   ├── terrain_gravel_patch/
│   ├── terrain_mud_patch/
│   ├── timber_roof_support/
│   ├── tunnel_ramp_15deg/
│   ├── tunnel_straight_10m/
│   ├── tunnel_straight_20m_narrow/
│   ├── tunnel_t_junction/
│   ├── tunnel_turn_90deg/
│   └── README.md
├── scenarios/               # Test scenario descriptions and setups
│   └── README.md
├── worlds/                  # Gazebo Sim world descriptions
│   ├── mine_world.sdf
│   └── README.md
└── README.md
```

---

## 2. World Overview: `mine_world.sdf`

`mine_world.sdf` defines a loadable subterranean mine environment (> 125 meters of interconnected drifts) in Gazebo Sim (Harmonic 8.15.0 / SDFormat 14):
- **World Origin & Portal**: Staging area located at `(0.0, 0.0, 0.0)` with three designated robot spawn locations outside the portal entrance.
- **Main Haulage Drift**: 30-meter straight haulage tunnel with irregular rock walls and dim point lights.
- **T-Junction Alpha**: 3-way intersection at `(30.0, 0.0, 0.0)` connecting the main drift to the north crosscut.
- **Crosscut Drift & 90° Turn**: Perpendicular 20-meter drift turning eastward into the east exploration drift.
- **15° Inclined Test Ramp**: 12-meter ramp climbing 3.1 meters to an upper extraction level.
  > [!NOTE]
  > The 15-degree incline represents an architectural test configuration for slope negotiation, not empirical proof of robot traversability. Hardware/chassis validation occurs in Milestone M2.
- **Dim Subterranean Lighting**: Subdued ambient illumination (`0.04 0.04 0.04 1.0`) with localized mine lantern point lights at key junctions.
- **Physics Configuration**: DART physics engine with a 1 ms step size (`0.001 s`), 1000 Hz real-time update rate, and ground contact dynamics.
- **Robots**: No robot models are spawned in Milestone M1 (prepared for Milestone M2).

---

## 3. Modular Terrain & Hazard Models

| Model | Type | Dimensions / Specs | Physical Properties |
| :--- | :--- | :--- | :--- |
| `tunnel_straight_10m` | Tunnel Segment | 10.0m × 3.5m × 3.0m | Arched cross-section, irregular rock walls |
| `tunnel_straight_20m_narrow` | Tunnel Segment | 20.0m × 2.8m × 2.6m | Rectangular cross-section, narrow haulage drift |
| `tunnel_turn_90deg` | Tunnel Segment | 6.0m radius, 90° arc | Faceted curved rock walls, 3.5m width |
| `tunnel_t_junction` | Tunnel Segment | 12.0m main × 6.0m branch | 3-way subterranean intersection |
| `tunnel_ramp_15deg` | Tunnel Segment | 12.0m run, 15° incline | Rise: 3.11m, run: 12.0m, pitch: 0.2618 rad |
| `terrain_gravel_patch` | Terrain | 4.0m × 2.5m × 0.04m | Rough loose gravel ($\mu_1=0.40, \mu_2=0.35$) |
| `terrain_mud_patch` | Terrain | 4.0m × 2.5m × 0.03m | Low-friction wet mud ($\mu_1=0.22, \mu_2=0.20$) |
| `fallen_rock_pile` | Obstacle | 2.5m × 1.8m × 0.85m | Irregular rubble pile obstructing navigation corridor |
| `timber_roof_support` | Obstacle | 3.6m × 0.35m × 2.9m | Timber posts and crossbeam with physical collision |
| `standing_water` | Hazard | 5.0m × 2.2m × 0.02m | Visual water surface overlay with collision base |
| `mine_debris` | Obstacle | 2.0m × 1.2m × 0.55m | Scrapped piping, timbers, and mechanical debris |
| `low_clearance_hazard` | Hazard | 3.8m × 1.5m × 0.9m | Overhanging rock brow reducing clearance to 1.7m |

---

## 4. Procedural Tunnel Generator

The tunnel generator script is located at [scripts/generate_mine_tunnels.py](../scripts/generate_mine_tunnels.py).

### Capabilities
- Configurable width, height, segment length, wall thickness, and wall roughness.
- Generates straight drifts, 90-degree turns, 3-way T-junctions, and inclined ramps.
- Arched, rectangular, and trapezoidal cross-section profiles.
- Deterministic procedural irregularity via pseudo-random seed.
- Validated SDFormat 1.9/1.10 output passing `gz sdf -k`.

### Execution
```bash
# Generate models from YAML configuration
python3 scripts/generate_mine_tunnels.py --config config/simulation/tunnel_layout_config.yaml

# Generate standard default models with seed 42
python3 scripts/generate_mine_tunnels.py --generate-defaults --seed 42
```

---

## 5. Subterranean RF Communication Attenuation Model

The subterranean RF attenuation model is implemented in [subterranean_rf_model.py](../src/layer1_robot_environment/communication_simulation/subterranean_rf_model.py) and evaluated via [scripts/simulate_rf_attenuation.py](../scripts/simulate_rf_attenuation.py).

### Theoretical Formulation
1. **Distance-Dependent Path Loss (Log-Distance Model)**:
   $$PL(d) = PL(d_0) + 10 \cdot n \cdot \log_{10}\left(\frac{d}{d_0}\right)$$
   where $d_0 = 1.0\text{ m}$, $PL(d_0) = 40.0\text{ dB}$, and path loss exponent $n = 2.4$ (subterranean waveguide mode).
2. **Tunnel Corner Diffraction Loss**:
   Adds an empirical penalty of $18.0\text{ dB}$ per 90-degree tunnel corner:
   $$PL_{\text{total}}(d, c) = PL(d) + c \cdot 18.0\text{ dB}$$
3. **Packet Loss Sigmoid**:
   Calculated based on link margin above receiver sensitivity ($P_{\text{sens}} = -95.0\text{ dBm}$):
   $$\text{Loss Rate} = \frac{1}{1 + e^{0.3 \cdot (\text{SNR}_{\text{margin}} - 5.0)}}$$
4. **Latency & Jitter**:
   $$\text{Latency} = 8.0\text{ ms} + (0.15 \times d) + (15.0 \times c) + \text{jitter}$$
5. **Forced Blackout Mode**:
   Explicit toggle for fault-injection testing, dropping RSSI to $-120\text{ dBm}$, packet loss to $100\%$, and latency to $\infty$.

### Model Limitations
> [!NOTE]
> This RF model is a simplified subterranean waveguide and diffraction approximation calibrated for straight drifts and 90° bends. It does not perform full 3D Maxwell finite-difference time-domain (FDTD) electromagnetic field simulation. It operates independently of the high-level decentralized task allocation stack.

### CLI Evaluation Example
```bash
# Evaluate link in main drift (LOS, 25m)
python3 scripts/simulate_rf_attenuation.py --pos-a 0 0 0 --pos-b 25 0 0

# Evaluate link around corner into crosscut (1 corner)
python3 scripts/simulate_rf_attenuation.py --pos-a 10 0 0 --pos-b 30 15 0

# Test forced blackout mode
python3 scripts/simulate_rf_attenuation.py --pos-a 0 0 0 --pos-b 5 0 0 --force-blackout --json
```

---

## 6. How to Launch and Validate

### Validate All SDF Assets
```bash
./scripts/run_mine_simulation.sh --validate
```

### Launch Headless Simulation
```bash
./scripts/run_mine_simulation.sh --headless
# Or run for a fixed iteration count:
./scripts/run_mine_simulation.sh --iterations 100
```

### Launch with GUI
```bash
./scripts/run_mine_simulation.sh --gui
```

### Launch via ROS 2 Launch Entry Point
```bash
source /opt/ros/humble/setup.bash
ros2 launch launch/mine_simulation.launch.py headless:=true
```

### Run Test Suite
```bash
python3 -m pytest tests/ -v
```
