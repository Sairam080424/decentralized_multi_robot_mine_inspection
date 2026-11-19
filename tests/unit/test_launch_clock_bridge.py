#!/usr/bin/env python3
"""
Unit Test: Mine Simulation Launch Entry Point and /clock Bridge
Verifies that clock_bridge_process is included in LaunchDescription,
properly configured with the ros_gz_bridge parameter_bridge syntax,
conditioned on the bridge_clock launch argument (IfCondition),
and registers clean shutdown handlers on simulation exit.
"""

import ast
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LAUNCH_FILE = REPO_ROOT / "launch" / "mine_simulation.launch.py"


def test_clock_bridge_ast_inclusion():
    """Verify statically via AST that clock_bridge_process is conditioned on bridge_clock and returned."""
    assert LAUNCH_FILE.exists(), f"Launch file not found: {LAUNCH_FILE}"
    source = LAUNCH_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)

    has_clock_bridge_def = False
    has_clock_bridge_in_return = False
    has_if_condition = "IfCondition" in source
    has_bridge_clock_arg = "bridge_clock" in source
    has_clock_bridge_topic = "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock" in source

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "clock_bridge_process":
                    has_clock_bridge_def = True
        elif isinstance(node, ast.Return):
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Name) and subnode.id == "clock_bridge_process":
                    has_clock_bridge_in_return = True

    assert has_clock_bridge_def, "clock_bridge_process variable assignment not found in launch file"
    assert has_clock_bridge_in_return, (
        "clock_bridge_process is defined but omitted from the returned LaunchDescription list!"
    )
    assert has_if_condition, "IfCondition missing from launch file imports/usage"
    assert has_bridge_clock_arg, "bridge_clock argument declaration missing from launch file"
    assert has_clock_bridge_topic, "Expected parameter_bridge topic syntax for /clock not found in launch file"


def test_clock_bridge_condition_evaluation():
    """Verify through LaunchContext that IfCondition enables bridge when true and disables when false."""
    ros_setup = Path("/opt/ros/humble/setup.bash")
    if not ros_setup.exists():
        pytest.skip("ROS 2 humble environment not present on host")

    ros_py = "/opt/ros/humble/lib/python3.10/site-packages"
    if ros_py not in sys.path:
        sys.path.insert(0, ros_py)

    from launch import LaunchContext
    from launch.actions import ExecuteProcess
    from launch.conditions import IfCondition

    # Load launch module without path conflict
    spec = importlib.util.spec_from_file_location("mine_sim_launch", str(LAUNCH_FILE))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ld = mod.generate_launch_description()

    # Find the clock bridge process action
    bridge_actions = [
        a for a in ld.entities
        if isinstance(a, ExecuteProcess) and getattr(a, "condition", None) is not None
    ]
    assert len(bridge_actions) == 1, f"Expected 1 conditioned ExecuteProcess action, found {len(bridge_actions)}"
    bridge_action = bridge_actions[0]

    assert isinstance(bridge_action.condition, IfCondition), "clock_bridge_process condition must be an IfCondition"

    # Test 1: bridge_clock := "true" evaluates to True
    ctx_true = LaunchContext()
    ctx_true._LaunchContext__launch_configurations["bridge_clock"] = "true"
    assert bridge_action.condition.evaluate(ctx_true) is True, "bridge_clock:=true must enable the bridge process"

    # Test 2: bridge_clock := "1" evaluates to True
    ctx_one = LaunchContext()
    ctx_one._LaunchContext__launch_configurations["bridge_clock"] = "1"
    assert bridge_action.condition.evaluate(ctx_one) is True, "bridge_clock:=1 must enable the bridge process"

    # Test 3: bridge_clock := "false" evaluates to False
    ctx_false = LaunchContext()
    ctx_false._LaunchContext__launch_configurations["bridge_clock"] = "false"
    assert bridge_action.condition.evaluate(ctx_false) is False, "bridge_clock:=false must disable the bridge process"

    # Test 4: bridge_clock := "0" evaluates to False
    ctx_zero = LaunchContext()
    ctx_zero._LaunchContext__launch_configurations["bridge_clock"] = "0"
    assert bridge_action.condition.evaluate(ctx_zero) is False, "bridge_clock:=0 must disable the bridge process"


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
