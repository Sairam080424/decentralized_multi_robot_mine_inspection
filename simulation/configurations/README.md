# Simulation Configurations

This directory documents the YAML configuration schemas used for simulation parameters, procedural tunnel generation, and subterranean communication evaluation.

---

## 1. Configuration Files

### `config/simulation/mine_world_config.yaml`
Central configuration for the subterranean mine world:
- Physics engine type (`dartsim`), time step (`0.001 s`), update rate (`1000 Hz`).
- Subterranean ambient lighting and background color.
- Coordinate offsets and layout specification for all tunnel segments.
- Pre-allocated robot spawn coordinates at the portal entrance.
- Friction parameters for loose gravel and wet mud patches.
- Obstacle placement poses.

### `config/simulation/tunnel_layout_config.yaml`
Input schema for `scripts/generate_mine_tunnels.py`:
- `seed`: Deterministic pseudo-random seed for wall roughness generation.
- `output_directory`: Directory path where generated SDF models are written.
- `models`: List of segment configurations (`straight`, `turn_90deg`, `t_junction`, `ramp`) including width, height, length, roughness, and profile shape.

### `config/simulation/rf_attenuation_config.yaml`
Parameters for `SubterraneanRFModel`:
- `tx_power_dbm`: 20.0 dBm (100 mW standard Wi-Fi / mesh transceiver).
- `rx_sensitivity_dbm`: -95.0 dBm.
- `path_loss_exponent`: 2.4 (subterranean tunnel waveguide exponent).
- `corner_attenuation_db`: 18.0 dB per 90° rock bend.
- `base_latency_ms`: 8.0 ms.
- `max_jitter_ms`: 12.0 ms.
- `forced_blackout`: Boolean flag for fault-injection testing.
