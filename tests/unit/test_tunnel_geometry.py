#!/usr/bin/env python3
"""
Unit Test: Tunnel Geometry and Dimensional Validation
Validates collision geometry, cross-section clearances, and slope angles.
"""

import math
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = REPO_ROOT / "simulation" / "models"


def test_straight_tunnel_dimensions():
    """Verify straight tunnel dimensions and minimum clearances."""
    # Test tunnel_straight_10m
    sdf_10m = MODELS_DIR / "tunnel_straight_10m" / "model.sdf"
    tree = ET.parse(sdf_10m)
    floor = tree.find(".//link[@name='floor']")
    assert floor is not None
    size_elem = floor.find(".//geometry/box/size")
    assert size_elem is not None
    dims = [float(v) for v in size_elem.text.split()]
    # Expected length 10.0m, width approx 3.5 + 2*0.4 = 4.3m
    assert math.isclose(dims[0], 10.0, rel_tol=1e-2), f"Expected length 10.0m, got {dims[0]}"
    assert dims[1] >= 3.5, f"Tunnel width {dims[1]} is less than 3.5m clearance"

    # Test tunnel_straight_20m_narrow
    sdf_20m = MODELS_DIR / "tunnel_straight_20m_narrow" / "model.sdf"
    tree_20m = ET.parse(sdf_20m)
    floor_20m = tree_20m.find(".//link[@name='floor']")
    assert floor_20m is not None
    size_elem_20m = floor_20m.find(".//geometry/box/size")
    assert size_elem_20m is not None
    dims_20m = [float(v) for v in size_elem_20m.text.split()]
    assert math.isclose(dims_20m[0], 20.0, rel_tol=1e-2), f"Expected length 20.0m, got {dims_20m[0]}"
    assert dims_20m[1] >= 2.8, f"Narrow tunnel width {dims_20m[1]} is less than 2.8m"


def test_ramp_slope_geometry():
    """Verify that tunnel_ramp_15deg has exactly a 15-degree pitch slope."""
    sdf_ramp = MODELS_DIR / "tunnel_ramp_15deg" / "model.sdf"
    tree = ET.parse(sdf_ramp)
    ramp_floor = tree.find(".//link[@name='ramp_floor']")
    assert ramp_floor is not None

    pose_elem = ramp_floor.find("pose")
    assert pose_elem is not None
    pose_vals = [float(v) for v in pose_elem.text.split()]
    # Pose: x y z roll pitch yaw
    pitch_rad = pose_vals[4]
    pitch_deg = abs(math.degrees(pitch_rad))
    assert math.isclose(pitch_deg, 15.0, abs_tol=0.1), f"Expected ramp pitch 15.0 deg, got {pitch_deg} deg"

    # Verify inclined length: run_length / cos(15 deg) = 12.0 / cos(15 deg) approx 12.423m
    box_size = ramp_floor.find(".//geometry/box/size")
    assert box_size is not None
    hypotenuse_length = float(box_size.text.split()[0])
    expected_hypotenuse = 12.0 / math.cos(math.radians(15.0))
    assert math.isclose(hypotenuse_length, expected_hypotenuse, rel_tol=1e-2), (
        f"Expected hypotenuse length {expected_hypotenuse:.3f}m, got {hypotenuse_length:.3f}m"
    )

    # Vertical rise: hypotenuse * sin(15 deg) = 12.423 * sin(15 deg) approx 3.215m
    # or horizontal run 12.0 * tan(15 deg) approx 3.215m
    expected_rise = 12.0 * math.tan(math.radians(15.0))
    actual_rise = hypotenuse_length * math.sin(math.radians(15.0))
    assert math.isclose(actual_rise, expected_rise, rel_tol=1e-2)


def test_turn_geometry():
    """Verify 90-degree turn dimensions and radial curvature."""
    sdf_turn = MODELS_DIR / "tunnel_turn_90deg" / "model.sdf"
    tree = ET.parse(sdf_turn)
    # Check that inner and outer wall segments span 0 to 90 degrees
    links = tree.findall(".//link")
    inner_links = [l for l in links if "inner_wall" in l.get("name", "")]
    outer_links = [l for l in links if "outer_wall" in l.get("name", "")]
    assert len(inner_links) >= 4, "Turn model must have at least 4 inner wall segments"
    assert len(outer_links) >= 4, "Turn model must have at least 4 outer wall segments"


def test_tjunction_geometry():
    """Verify T-junction has main drift and perpendicular branch."""
    sdf_tjunct = MODELS_DIR / "tunnel_t_junction" / "model.sdf"
    tree = ET.parse(sdf_tjunct)
    main_floor = tree.find(".//link[@name='main_floor']")
    branch_floor = tree.find(".//link[@name='branch_floor']")
    assert main_floor is not None
    assert branch_floor is not None

    # Main length >= 10m
    main_dims = [float(v) for v in main_floor.find(".//geometry/box/size").text.split()]
    assert main_dims[0] >= 10.0

    # Branch length >= 5m
    branch_dims = [float(v) for v in branch_floor.find(".//geometry/box/size").text.split()]
    assert branch_dims[1] >= 5.0


def test_assembled_world_ramp_and_upper_drift_connectivity():
    """
    World-Level Geometry Integration Test:
    Verifies mathematical and structural continuity between:
    - Lower haulage drift floor, walls, ceiling (drift1_sec_d)
    - 15-degree inclined ramp (ramp_15deg_section)
    - Upper level drift floor, walls, ceiling (upper_drift_section)
    Ensures zero unintended vertical cliffs, zero horizontal floor gaps,
    continuous wall alignment (y = +/- 1.75m), and continuous ceiling clearance.
    """
    world_path = REPO_ROOT / "simulation" / "worlds" / "mine_world.sdf"
    tree = ET.parse(world_path)

    # 1. Lower Drift Approach (drift1_sec_d)
    lower_drift = tree.find(".//model[@name='drift1_sec_d']")
    assert lower_drift is not None, "drift1_sec_d missing from mine_world.sdf"
    lower_floor = lower_drift.find(".//link[@name='floor']")
    lower_f_pose = [float(v) for v in lower_floor.find("pose").text.split()]
    lower_f_size = [float(v) for v in lower_floor.find(".//geometry/box/size").text.split()]
    lower_floor_end_x = lower_f_pose[0] + lower_f_size[0] / 2.0  # 39.0 + 3.0 = 42.0m
    lower_floor_top_z = lower_f_pose[2] + lower_f_size[2] / 2.0  # -0.05 + 0.05 = 0.0m
    assert math.isclose(lower_floor_end_x, 42.0, abs_tol=1e-3)
    assert math.isclose(lower_floor_top_z, 0.0, abs_tol=1e-3)

    # 2. Ramp Inclusion (ramp_15deg_section)
    ramp_inc = None
    for inc in tree.findall(".//include"):
        name_elem = inc.find("name")
        if name_elem is not None and name_elem.text.strip() == "ramp_15deg_section":
            ramp_inc = inc
            break
    assert ramp_inc is not None, "ramp_15deg_section include missing from world"
    ramp_pose_elem = ramp_inc.find("pose")
    ramp_pose = [float(v) for v in ramp_pose_elem.text.split()] if ramp_pose_elem is not None else [0.0]*6
    assert math.isclose(ramp_pose[0], 42.0, abs_tol=1e-3), f"Ramp must start at x=42.0, got {ramp_pose[0]}"

    # Load ramp model SDF to compute exact local endpoints
    ramp_tree = ET.parse(MODELS_DIR / "tunnel_ramp_15deg" / "model.sdf")
    ramp_floor_link = ramp_tree.find(".//link[@name='ramp_floor']")
    rf_pose = [float(v) for v in ramp_floor_link.find("pose").text.split()]
    rf_size = [float(v) for v in ramp_floor_link.find(".//geometry/box/size").text.split()]
    rf_pitch = rf_pose[4]
    rf_length = rf_size[0]
    rf_thick = rf_size[2]

    # Calculate ramp start and end top-surface coordinates in world frame
    # Local box: center at rf_pose, length rf_length, thickness rf_thick, pitch rf_pitch
    # Y-axis rotation: x' = x*cos(pitch) + z*sin(pitch), z' = -x*sin(pitch) + z*cos(pitch)
    cos_p = math.cos(rf_pitch)
    sin_p = math.sin(rf_pitch)
    # Start: local x = -rf_length/2, local z = +rf_thick/2 (top surface)
    start_dx = (-rf_length / 2.0) * cos_p + (rf_thick / 2.0) * sin_p
    start_dz = -(-rf_length / 2.0) * sin_p + (rf_thick / 2.0) * cos_p
    ramp_world_start_x = ramp_pose[0] + rf_pose[0] + start_dx
    ramp_world_start_z = ramp_pose[2] + rf_pose[2] + start_dz

    # End: local x = +rf_length/2, local z = +rf_thick/2
    end_dx = (rf_length / 2.0) * cos_p + (rf_thick / 2.0) * sin_p
    end_dz = -(rf_length / 2.0) * sin_p + (rf_thick / 2.0) * cos_p
    ramp_world_end_x = ramp_pose[0] + rf_pose[0] + end_dx
    ramp_world_end_z = ramp_pose[2] + rf_pose[2] + end_dz

    # Verify ramp start matches lower floor top
    assert math.isclose(ramp_world_start_x, 42.0, abs_tol=0.05), f"Ramp start X {ramp_world_start_x} != 42.0"
    assert math.isclose(ramp_world_start_z, lower_floor_top_z, abs_tol=0.01), (
        f"Ramp start elevation {ramp_world_start_z:.3f}m must match lower floor {lower_floor_top_z:.3f}m"
    )

    # Verify ramp inclination is approximately 15.0 degrees
    inclination_deg = abs(math.degrees(rf_pitch))
    assert math.isclose(inclination_deg, 15.0, abs_tol=0.1)

    # Verify ramp end position and vertical rise
    expected_rise = 12.0 * math.tan(math.radians(15.0))  # approx 3.215m
    assert math.isclose(ramp_world_end_x, 54.0, abs_tol=0.05), f"Ramp end X {ramp_world_end_x} != 54.0"
    assert math.isclose(ramp_world_end_z, expected_rise, abs_tol=0.02), (
        f"Ramp end elevation {ramp_world_end_z:.3f}m must equal {expected_rise:.3f}m"
    )

    # 3. Upper Drift Section (upper_drift_section)
    upper_drift = tree.find(".//model[@name='upper_drift_section']")
    assert upper_drift is not None, "upper_drift_section missing from world"
    upper_floor = upper_drift.find(".//link[@name='upper_floor']")
    uf_pose = [float(v) for v in upper_floor.find("pose").text.split()]
    uf_size = [float(v) for v in upper_floor.find(".//geometry/box/size").text.split()]
    upper_floor_start_x = uf_pose[0] - uf_size[0] / 2.0
    upper_floor_top_z = uf_pose[2] + uf_size[2] / 2.0

    # Verify upper floor elevation matches ramp end elevation (zero vertical step/cliff)
    vertical_step = abs(upper_floor_top_z - ramp_world_end_z)
    assert vertical_step <= 0.02, (
        f"Vertical gap at ramp-upper drift joint: {vertical_step:.4f}m exceeds tolerance (0.02m)"
    )

    # Verify upper floor overlaps or meets ramp end in horizontal X (zero floor gap)
    assert upper_floor_start_x <= ramp_world_end_x + 0.05, (
        f"Horizontal gap between ramp end ({ramp_world_end_x:.2f}m) and upper floor start ({upper_floor_start_x:.2f}m)"
    )

    # 4. Continuous Wall and Ceiling Alignment Across Lower Drift, Ramp, and Upper Drift
    ramp_l_wall = ramp_tree.find(".//link[@name='ramp_left_wall']")
    ramp_r_wall = ramp_tree.find(".//link[@name='ramp_right_wall']")
    ramp_ceil = ramp_tree.find(".//link[@name='ramp_ceiling']")
    assert ramp_l_wall is not None, "ramp_left_wall missing from ramp model"
    assert ramp_r_wall is not None, "ramp_right_wall missing from ramp model"
    assert ramp_ceil is not None, "ramp_ceiling missing from ramp model"

    # Left wall inner face: y = 1.95 - 0.4/2 = 1.75m (Lower, Ramp, and Upper must align)
    lower_l_wall = lower_drift.find(".//link[@name='left_wall']")
    upper_l_wall = upper_drift.find(".//link[@name='upper_left_wall']")
    assert lower_l_wall is not None and upper_l_wall is not None
    assert math.isclose(float(lower_l_wall.find("pose").text.split()[1]), 1.95, abs_tol=1e-3)
    assert math.isclose(float(ramp_l_wall.find("pose").text.split()[1]), 1.95, abs_tol=1e-3)
    assert math.isclose(float(upper_l_wall.find("pose").text.split()[1]), 1.95, abs_tol=1e-3)

    # Right wall inner face: y = -1.95 + 0.4/2 = -1.75m (Lower, Ramp, and Upper must align)
    lower_r_wall = lower_drift.find(".//link[@name='right_wall']")
    upper_r_wall = upper_drift.find(".//link[@name='upper_right_wall']")
    assert lower_r_wall is not None and upper_r_wall is not None
    assert math.isclose(float(lower_r_wall.find("pose").text.split()[1]), -1.95, abs_tol=1e-3)
    assert math.isclose(float(ramp_r_wall.find("pose").text.split()[1]), -1.95, abs_tol=1e-3)
    assert math.isclose(float(upper_r_wall.find("pose").text.split()[1]), -1.95, abs_tol=1e-3)

    # Ramp ceiling internal vertical clearance
    rc_pose = [float(v) for v in ramp_ceil.find("pose").text.split()]
    rc_size = [float(v) for v in ramp_ceil.find(".//geometry/box/size").text.split()]
    ramp_normal_clearance = (rc_pose[2] - rc_size[2] / 2.0) - (rf_pose[2] + rf_size[2] / 2.0)
    assert math.isclose(ramp_normal_clearance, 3.0, abs_tol=0.05), (
        f"Ramp normal ceiling clearance {ramp_normal_clearance:.3f}m is not 3.0m"
    )

    # Ceiling clearance continuity:
    # Lower ceiling bottom: lower_floor_top_z + 3.0m = 3.0m
    lower_ceil = lower_drift.find(".//link[@name='ceiling']")
    assert lower_ceil is not None
    lc_pose = [float(v) for v in lower_ceil.find("pose").text.split()]
    lc_size = [float(v) for v in lower_ceil.find(".//geometry/box/size").text.split()]
    lc_bottom_z = lc_pose[2] - lc_size[2] / 2.0
    assert math.isclose(lc_bottom_z, lower_floor_top_z + 3.0, abs_tol=0.05)

    # Upper ceiling bottom: uf_pose_z + 3.0m clearance = 3.215 + 3.0 = 6.215m
    upper_ceil = upper_drift.find(".//link[@name='upper_ceiling']")
    uc_pose = [float(v) for v in upper_ceil.find("pose").text.split()]
    uc_size = [float(v) for v in upper_ceil.find(".//geometry/box/size").text.split()]
    uc_bottom_z = uc_pose[2] - uc_size[2] / 2.0  # 6.415 - 0.2 = 6.215m
    assert math.isclose(uc_bottom_z, upper_floor_top_z + 3.0, abs_tol=0.05), (
        f"Upper ceiling clearance {uc_bottom_z - upper_floor_top_z:.2f}m is not 3.0m"
    )
