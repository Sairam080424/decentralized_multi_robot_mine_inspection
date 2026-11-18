#!/usr/bin/env python3
"""
Unit Test: Mine Simulation Launch Entry Point and /clock Bridge
Verifies that clock_bridge_process is included in LaunchDescription,
properly configured with the ros_gz_bridge parameter_bridge syntax,
and registers clean shutdown handlers on simulation exit.
"""

import ast
from pathlib import Path
import shutil
import subprocess
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LAUNCH_FILE = REPO_ROOT / "launch" / "mine_simulation.launch.py"


def test_clock_bridge_ast_inclusion():
    """Verify statically via AST that clock_bridge_process is instantiated and included in LaunchDescription list."""
    assert LAUNCH_FILE.exists(), f"Launch file not found: {LAUNCH_FILE}"
    source = LAUNCH_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # Verify clock_bridge_process definition
    has_clock_bridge_def = False
    has_clock_bridge_in_return = False
    has_clock_bridge_topic = "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock" in source

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "clock_bridge_process":
                    has_clock_bridge_def = True
        elif isinstance(node, ast.Return):
            # Check if clock_bridge_process is inside the returned LaunchDescription list
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Name) and subnode.id == "clock_bridge_process":
                    has_clock_bridge_in_return = True

    assert has_clock_bridge_def, "clock_bridge_process variable assignment not found in launch file"
    assert has_clock_bridge_in_return, (
        "clock_bridge_process is defined but omitted from the returned LaunchDescription list!"
    )
    assert has_clock_bridge_topic, "Expected parameter_bridge topic syntax for /clock not found in launch file"


def test_clock_bridge_ros2_launch_inspection():
    """Verify through 'ros2 launch -p' that clock_bridge_process and shutdown handler appear in execution tree."""
    ros_setup = Path("/opt/ros/humble/setup.bash")
    ros2_bin = Path("/opt/ros/humble/bin/ros2")
    if not ros_setup.exists() or not ros2_bin.exists():
        pytest.skip("ROS 2 humble environment not present on host")

    cmd = f"source {ros_setup} && ros2 launch {LAUNCH_FILE} -p"
    result = subprocess.run(
        ["bash", "-c", cmd],
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, f"ros2 launch -p failed with return code {result.returncode}:\n{result.stderr}"
    output = result.stdout

    # Verify ExecuteProcess for ros_gz_bridge parameter_bridge
    assert "ros_gz_bridge" in output, "ros_gz_bridge parameter_bridge missing from launch actions"
    assert "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock" in output, (
        "ROS-Gazebo clock bridge rule not found in launch execution tree"
    )

    # Verify RegisterEventHandler with OnProcessExit and Shutdown
    assert "OnProcessExit" in output, "OnProcessExit event handler missing from launch actions"
    assert "Shutdown" in output, "Shutdown action missing from OnProcessExit event handler"
