#!/usr/bin/env python3
"""
Dedicated Milestone M1 Mine Simulation Launch Entry Point
Launches Gazebo Sim with the subterranean mine world without spawning robots.
Configures GZ_SIM_RESOURCE_PATH, physics parameters, and clock bridge.
"""

import os
from pathlib import Path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():
    repo_root = Path(__file__).resolve().parent.parent
    world_path = repo_root / "simulation" / "worlds" / "mine_world.sdf"
    models_path = repo_root / "simulation" / "models"
    worlds_path = repo_root / "simulation" / "worlds"

    existing_resource_path = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    resource_path = f"{models_path}:{worlds_path}:{existing_resource_path}".strip(":")
    sdf_path = f"{models_path}:{existing_resource_path}".strip(":")

    headless_arg = DeclareLaunchArgument(
        "headless",
        default_value="true",
        description="Run Gazebo Sim in headless mode (-s) without GUI",
    )

    world_arg = DeclareLaunchArgument(
        "world",
        default_value=str(world_path),
        description="Full path to subterranean mine world SDF file",
    )

    env_gz_resource = SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", resource_path)
    env_sdf_path = SetEnvironmentVariable("SDF_PATH", sdf_path)
    env_gz_log = SetEnvironmentVariable("GZ_LOG_PATH", "/tmp")

    # Command construction: gz sim [-s] -r <world>
    gz_sim_cmd = [
        "gz", "sim",
        PythonExpression(["'-s -r' if '", LaunchConfiguration("headless"), "'.lower() == 'true' else '-r'"]),
        LaunchConfiguration("world"),
    ]

    gz_sim_process = ExecuteProcess(
        cmd=gz_sim_cmd,
        output="screen",
        shell=True,
    )

    # Bridge Gazebo simulation clock to ROS 2 /clock
    clock_bridge_process = ExecuteProcess(
        cmd=[
            "ros2", "run", "ros_gz_bridge", "parameter_bridge",
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        ],
        output="screen",
        shell=False,
    )

    return LaunchDescription([
        headless_arg,
        world_arg,
        env_gz_resource,
        env_sdf_path,
        env_gz_log,
        gz_sim_process,
    ])
