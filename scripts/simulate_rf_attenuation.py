#!/usr/bin/env python3
"""
Subterranean RF Communication Attenuation Simulator CLI & Bridge
Milestone M1: Underground Mine Simulation (TASK-M1-005)

Can be executed standalone to evaluate link quality between coordinates,
or invoked in automation pipelines to verify RF attenuation across the mine network.
Loads parameters dynamically from YAML configuration.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.layer1_robot_environment.communication_simulation.subterranean_rf_model import (
    SubterraneanRFModel,
)


def main():
    default_config = REPO_ROOT / "config" / "simulation" / "rf_attenuation_config.yaml"

    parser = argparse.ArgumentParser(
        description="Subterranean Mine RF Attenuation and Link Evaluator"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=str(default_config),
        help=f"Path to RF attenuation YAML configuration (default: {default_config})",
    )
    parser.add_argument(
        "--pos-a",
        nargs=3,
        type=float,
        default=[0.0, 0.0, 0.0],
        metavar=("X", "Y", "Z"),
        help="Position of Robot A (default: 0 0 0)",
    )
    parser.add_argument(
        "--pos-b",
        nargs=3,
        type=float,
        default=[20.0, 0.0, 0.0],
        metavar=("X", "Y", "Z"),
        help="Position of Robot B (default: 20 0 0)",
    )
    parser.add_argument(
        "--force-blackout",
        action="store_true",
        help="Force 100%% communication loss (blackout test mode)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output evaluation results as JSON",
    )
    args = parser.parse_args()

    cfg_path = Path(args.config)
    if cfg_path.exists():
        model = SubterraneanRFModel.from_yaml(cfg_path)
    else:
        print(f"Warning: Config file {cfg_path} not found. Using default parameters.", file=sys.stderr)
        model = SubterraneanRFModel()

    if args.force_blackout:
        model.set_forced_blackout(True)

    pos_a = tuple(args.pos_a)
    pos_b = tuple(args.pos_b)

    result = model.evaluate_link(pos_a, pos_b)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=== Subterranean Communication Link Evaluation ===")
        print(f"Node A Position:        {pos_a}")
        print(f"Node B Position:        {pos_b}")
        print(f"Distance:               {result['distance_m']} m")
        print(f"Line of Sight (LOS):    {result['has_line_of_sight']}")
        print(f"Corner Obstructions:    {result['corner_count']}")
        print(f"Classification Reason:  {result['classification_reason']}")
        print(f"Estimated RSSI:         {result['rssi_dbm']} dBm")
        print(f"Packet Loss Rate:       {result['packet_loss_rate'] * 100:.1f} %")
        print(f"Estimated Latency:      {result['latency_ms']} ms")
        print(f"Effective Bandwidth:    {result['effective_bandwidth_kbps']} kbps")
        print(f"Link Status:            {result['status']}")


if __name__ == "__main__":
    main()
