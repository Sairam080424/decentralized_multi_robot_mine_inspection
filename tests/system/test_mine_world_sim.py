#!/usr/bin/env python3
"""
System Test: Mine World Simulation Execution and Physics Stability
Loads mine_world.sdf headlessly into Gazebo Sim and verifies stable physics execution over 50 iterations.
"""

import os
import subprocess
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORLD_PATH = REPO_ROOT / "simulation" / "worlds" / "mine_world.sdf"
MODELS_DIR = REPO_ROOT / "simulation" / "models"
WORLDS_DIR = REPO_ROOT / "simulation" / "worlds"


def test_headless_simulation_physics_stability():
    """Verify Gazebo Sim loads mine_world.sdf and advances physics stably for 50 iterations."""
    assert WORLD_PATH.exists(), f"World file missing: {WORLD_PATH}"

    env = dict(os.environ)
    env["HOME"] = "/tmp"
    env["GZ_LOG_PATH"] = "/tmp"
    env["GZ_SIM_RESOURCE_PATH"] = f"{MODELS_DIR}:{WORLDS_DIR}:{env.get('GZ_SIM_RESOURCE_PATH', '')}"
    env["SDF_PATH"] = f"{MODELS_DIR}:{env.get('SDF_PATH', '')}"

    cmd = [
        "gz", "sim",
        "-s",
        "-r",
        "--iterations", "50",
        str(WORLD_PATH),
    ]

    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)

    # Check return code
    assert result.returncode == 0, (
        f"Gazebo Sim exited with code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )

    # Ensure no segfault or abort messages
    combined_output = (result.stdout + result.stderr).lower()
    assert "segmentation fault" not in combined_output, "Segmentation fault detected in Gazebo Sim run"
    assert "core dumped" not in combined_output, "Core dump detected in Gazebo Sim run"
    assert "nan" not in combined_output, "NaN detected in Gazebo Sim state output"
