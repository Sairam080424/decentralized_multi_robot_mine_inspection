#!/usr/bin/env python3
"""
System Test: Mine World Simulation Execution, Observable State, and Lifecycle
Milestone M1: Underground Mine Simulation (TASK-M1-001)

Verifies:
1. Physics stability over bounded iterations (no NaNs, no crashes)
2. Observable simulation state:
   - Topic publishing (/clock, /stats, /world/mine_world/state)
   - Simulation time advancement (sim_time > 0, iterations > 0)
   - Entity presence in world (models loaded correctly via 'gz model --list')
3. Clean startup and shutdown lifecycle
"""

import os
import shutil
import signal
import subprocess
import time
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORLD_PATH = REPO_ROOT / "simulation" / "worlds" / "mine_world.sdf"
MODELS_DIR = REPO_ROOT / "simulation" / "models"
WORLDS_DIR = REPO_ROOT / "simulation" / "worlds"


def get_gz_env() -> dict:
    """Build environment variables required for Gazebo Sim discovery."""
    env = dict(os.environ)
    env["HOME"] = "/tmp"
    env["GZ_LOG_PATH"] = "/tmp"
    env["GZ_SIM_RESOURCE_PATH"] = f"{MODELS_DIR}:{WORLDS_DIR}:{env.get('GZ_SIM_RESOURCE_PATH', '')}"
    env["SDF_PATH"] = f"{MODELS_DIR}:{env.get('SDF_PATH', '')}"
    return env


def test_headless_simulation_physics_stability():
    """Verify Gazebo Sim loads mine_world.sdf and advances physics stably for 50 iterations."""
    if shutil.which("gz") is None:
        pytest.skip("gz CLI tool not found on system PATH")

    assert WORLD_PATH.exists(), f"World file missing: {WORLD_PATH}"
    env = get_gz_env()

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


def test_headless_simulation_observable_state_and_lifecycle():
    """
    Verify observable state of running Gazebo Sim instance:
    - Active topics (/clock, /stats, /world/mine_world/clock)
    - Simulation time progression (sim_time > 0, iterations > 0)
    - Entity presence (models loaded in simulation world)
    - Clean lifecycle shutdown
    """
    if shutil.which("gz") is None:
        pytest.skip("gz CLI tool not found on system PATH")

    assert WORLD_PATH.exists(), f"World file missing: {WORLD_PATH}"
    env = get_gz_env()

    proc = subprocess.Popen(
        ["gz", "sim", "-s", "-r", str(WORLD_PATH)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Allow Gazebo Sim to initialize world and start publishing
        time.sleep(4.0)
        assert proc.poll() is None, f"Gazebo exited prematurely with code {proc.returncode}"

        # 1. Verify Published Topics
        topic_proc = subprocess.run(
            ["gz", "topic", "-l"],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert topic_proc.returncode == 0, f"gz topic -l failed: {topic_proc.stderr}"
        topics = topic_proc.stdout.splitlines()

        expected_topics = [
            "/clock",
            "/stats",
            "/world/mine_world/clock",
            "/world/mine_world/stats",
            "/world/mine_world/state",
        ]
        for exp in expected_topics:
            assert any(exp in t for t in topics), f"Expected topic '{exp}' not found in: {topics}"

        # 2. Verify Simulation Time Advancement via /stats or /clock
        stats_proc = subprocess.run(
            ["gz", "topic", "-e", "-t", "/stats", "-n", "1"],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert stats_proc.returncode == 0, f"gz topic -e failed: {stats_proc.stderr}"
        stats_out = stats_proc.stdout

        # Verify positive iteration count or sim_time progression
        assert "sim_time" in stats_out, f"sim_time missing from /stats output: {stats_out}"
        assert "iterations:" in stats_out, f"iterations missing from /stats output: {stats_out}"

        # Parse iterations to verify > 0
        iter_line = [line for line in stats_out.splitlines() if "iterations:" in line]
        if iter_line:
            iters = int(iter_line[0].split("iterations:")[1].strip())
            assert iters > 0, f"Simulation iterations did not advance: {iters}"

        # 3. Verify Model Entity Presence
        models_proc = subprocess.run(
            ["gz", "model", "--list"],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert models_proc.returncode == 0, f"gz model --list failed: {models_proc.stderr}"
        models_out = models_proc.stdout

        expected_models = [
            "mine_portal_arch",
            "drift1_sec_a",
            "junction_drift1_crosscut",
            "ramp_15deg_section",
            "upper_drift_section",
            "crosscut_drift_sec1",
        ]
        for model in expected_models:
            assert model in models_out, f"Expected model '{model}' missing from simulation world: {models_out}"

    finally:
        # 4. Clean Shutdown Lifecycle
        if proc.poll() is None:
            proc.send_signal(signal.SIGINT)
            try:
                proc.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()

        assert proc.returncode in (0, -signal.SIGINT, -signal.SIGTERM), (
            f"Gazebo Sim did not shut down cleanly: code {proc.returncode}"
        )

