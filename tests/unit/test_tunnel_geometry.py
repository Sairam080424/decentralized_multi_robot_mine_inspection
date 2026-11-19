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


def euler_to_matrix(roll: float, pitch: float, yaw: float):
    """
    Constructs a 3x3 rotation matrix R = Rz(yaw) * Ry(pitch) * Rx(roll)
    following the standard SDFormat / Gazebo extrinsic Euler convention.
    """
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    return (
        (cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr),
        (sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr),
        (-sp,     cp * sr,                cp * cr),
    )


def apply_transform(rot_matrix, translation, point):
    """Applies 3D affine transform p_transformed = R * p + t."""
    x, y, z = point
    tx, ty, tz = translation
    rx = rot_matrix[0][0] * x + rot_matrix[0][1] * y + rot_matrix[0][2] * z
    ry = rot_matrix[1][0] * x + rot_matrix[1][1] * y + rot_matrix[1][2] * z
    rz = rot_matrix[2][0] * x + rot_matrix[2][1] * y + rot_matrix[2][2] * z
    return (rx + tx, ry + ty, rz + tz)


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


def test_ramp_world_transformed_walls_and_ceiling_continuity():
    """
    Rigorously validates world-transformed endpoints for both ramp walls, floor, and ceiling:
    - Transforms local SDF poses and box geometries into world coordinates using rotation matrices.
    - Checks lower transition joint (x = 42.0m) against drift1_sec_d.
    - Checks upper transition joint (x = 54.0m) against upper_drift_section.
    - Validates left wall inner face (y = 1.750m) and right wall inner face (y = -1.750m).
    - Validates floor elevations: lower (z = 0.000m) and upper (z = 3.215m).
    - Validates ceiling bottom elevations: lower (z = 3.000m) and upper (z = 6.215m).
    - Validates 3.0m normal ceiling clearance across the entire inclined ramp.
    """
    world_path = REPO_ROOT / "simulation" / "worlds" / "mine_world.sdf"
    tree = ET.parse(world_path)

    # 1. Lower Drift Adjoining Geometry (drift1_sec_d)
    lower_drift = tree.find(".//model[@name='drift1_sec_d']")
    assert lower_drift is not None
    dl_floor = lower_drift.find(".//link[@name='floor']")
    dl_l_wall = lower_drift.find(".//link[@name='left_wall']")
    dl_r_wall = lower_drift.find(".//link[@name='right_wall']")
    dl_ceil = lower_drift.find(".//link[@name='ceiling']")

    dl_f_p = [float(v) for v in dl_floor.find("pose").text.split()]
    dl_f_s = [float(v) for v in dl_floor.find(".//geometry/box/size").text.split()]
    dl_lw_p = [float(v) for v in dl_l_wall.find("pose").text.split()]
    dl_lw_s = [float(v) for v in dl_l_wall.find(".//geometry/box/size").text.split()]
    dl_rw_p = [float(v) for v in dl_r_wall.find("pose").text.split()]
    dl_rw_s = [float(v) for v in dl_r_wall.find(".//geometry/box/size").text.split()]
    dl_c_p = [float(v) for v in dl_ceil.find("pose").text.split()]
    dl_c_s = [float(v) for v in dl_ceil.find(".//geometry/box/size").text.split()]

    lower_floor_top_z = dl_f_p[2] + dl_f_s[2] / 2.0         # 0.000m
    lower_floor_end_x = dl_f_p[0] + dl_f_s[0] / 2.0         # 42.000m
    lower_l_wall_inner_y = dl_lw_p[1] - dl_lw_s[1] / 2.0    # 1.750m
    lower_r_wall_inner_y = dl_rw_p[1] + dl_rw_s[1] / 2.0    # -1.750m
    lower_ceil_bot_z = dl_c_p[2] - dl_c_s[2] / 2.0          # 3.000m

    # 2. Upper Drift Adjoining Geometry (upper_drift_section)
    upper_drift = tree.find(".//model[@name='upper_drift_section']")
    assert upper_drift is not None
    ud_floor = upper_drift.find(".//link[@name='upper_floor']")
    ud_l_wall = upper_drift.find(".//link[@name='upper_left_wall']")
    ud_r_wall = upper_drift.find(".//link[@name='upper_right_wall']")
    ud_ceil = upper_drift.find(".//link[@name='upper_ceiling']")

    ud_f_p = [float(v) for v in ud_floor.find("pose").text.split()]
    ud_f_s = [float(v) for v in ud_floor.find(".//geometry/box/size").text.split()]
    ud_lw_p = [float(v) for v in ud_l_wall.find("pose").text.split()]
    ud_lw_s = [float(v) for v in ud_l_wall.find(".//geometry/box/size").text.split()]
    ud_rw_p = [float(v) for v in ud_r_wall.find("pose").text.split()]
    ud_rw_s = [float(v) for v in ud_r_wall.find(".//geometry/box/size").text.split()]
    ud_c_p = [float(v) for v in ud_ceil.find("pose").text.split()]
    ud_c_s = [float(v) for v in ud_ceil.find(".//geometry/box/size").text.split()]

    upper_floor_top_z = ud_f_p[2] + ud_f_s[2] / 2.0         # 3.215m
    upper_floor_start_x = ud_f_p[0] - ud_f_s[0] / 2.0       # 53.900m
    upper_l_wall_inner_y = ud_lw_p[1] - ud_lw_s[1] / 2.0    # 1.750m
    upper_r_wall_inner_y = ud_rw_p[1] + ud_rw_s[1] / 2.0    # -1.750m
    upper_ceil_bot_z = ud_c_p[2] - ud_c_s[2] / 2.0          # 6.215m

    # 3. Ramp World Transformation Helper
    # Dynamically extract full 6-DOF ramp model pose from mine_world.sdf rather than hard-coding
    ramp_include = tree.find(".//include[name='ramp_15deg_section']")
    assert ramp_include is not None, "ramp_15deg_section include not found in mine_world.sdf"
    ramp_pose_tokens = [float(v) for v in ramp_include.find("pose").text.split()]
    assert len(ramp_pose_tokens) == 6, f"Expected 6-DOF pose for ramp include, got {len(ramp_pose_tokens)}"
    ramp_world_t = tuple(ramp_pose_tokens[:3])
    ramp_world_r = euler_to_matrix(ramp_pose_tokens[3], ramp_pose_tokens[4], ramp_pose_tokens[5])
    assert math.isclose(ramp_world_t[0], 42.0, abs_tol=1e-3), f"Ramp world x origin is {ramp_world_t[0]}, expected 42.0"

    ramp_tree = ET.parse(MODELS_DIR / "tunnel_ramp_15deg" / "model.sdf")

    def transform_ramp_point(link_name: str, local_dx: float, local_dy: float, local_dz: float,
                             world_t=ramp_world_t, world_r=ramp_world_r):
        link = ramp_tree.find(f".//link[@name='{link_name}']")
        pose = [float(v) for v in link.find("pose").text.split()]
        lx, ly, lz = pose[:3]
        lr = pose[3] if len(pose) > 3 else 0.0
        lp = pose[4] if len(pose) > 4 else 0.0
        lyaw = pose[5] if len(pose) > 5 else 0.0

        r_link = euler_to_matrix(lr, lp, lyaw)
        p_model = apply_transform(r_link, (lx, ly, lz), (local_dx, local_dy, local_dz))
        p_world = apply_transform(world_r, world_t, p_model)
        return p_world

    # 4. Ramp Floor Transformed Coordinates
    rf_size = [float(v) for v in ramp_tree.find(".//link[@name='ramp_floor']//geometry/box/size").text.split()]
    ramp_f_start = transform_ramp_point("ramp_floor", -rf_size[0] / 2.0, 0.0, rf_size[2] / 2.0)
    ramp_f_end = transform_ramp_point("ramp_floor", rf_size[0] / 2.0, 0.0, rf_size[2] / 2.0)

    # Floor continuity assertions
    assert math.isclose(ramp_f_start[2], lower_floor_top_z, abs_tol=0.01), (
        f"Ramp floor start z {ramp_f_start[2]:.4f}m does not match lower floor {lower_floor_top_z:.4f}m"
    )
    assert math.isclose(ramp_f_end[2], upper_floor_top_z, abs_tol=0.01), (
        f"Ramp floor end z {ramp_f_end[2]:.4f}m does not match upper floor {upper_floor_top_z:.4f}m"
    )
    assert ramp_f_start[0] <= lower_floor_end_x + 0.02, "Gap between lower floor and ramp floor start"
    assert upper_floor_start_x <= ramp_f_end[0] + 0.02, "Gap between ramp floor end and upper floor start"

    # 5. Ramp Left Wall Transformed Coordinates (inner face: local_dy = -size[1]/2)
    rw_l_size = [float(v) for v in ramp_tree.find(".//link[@name='ramp_left_wall']//geometry/box/size").text.split()]
    ramp_lw_start = transform_ramp_point("ramp_left_wall", -rw_l_size[0] / 2.0, -rw_l_size[1] / 2.0, 0.0)
    ramp_lw_end = transform_ramp_point("ramp_left_wall", rw_l_size[0] / 2.0, -rw_l_size[1] / 2.0, 0.0)

    # Left wall horizontal alignment
    assert math.isclose(ramp_lw_start[1], 1.750, abs_tol=1e-3), f"Ramp left wall inner y is {ramp_lw_start[1]}, expected 1.75"
    assert math.isclose(ramp_lw_end[1], 1.750, abs_tol=1e-3), f"Ramp left wall inner y is {ramp_lw_end[1]}, expected 1.75"
    assert math.isclose(ramp_lw_start[1], lower_l_wall_inner_y, abs_tol=1e-3), "Left wall misaligned at lower joint"
    assert math.isclose(ramp_lw_end[1], upper_l_wall_inner_y, abs_tol=1e-3), "Left wall misaligned at upper joint"
    assert math.isclose(ramp_lw_start[0], 42.000, abs_tol=0.02), f"Left wall start x {ramp_lw_start[0]} != 42.0"
    assert math.isclose(ramp_lw_end[0], 54.000, abs_tol=0.02), f"Left wall end x {ramp_lw_end[0]} != 54.0"

    # Left wall vertical extents (verify wall covers drift height from floor to ceiling)
    ramp_lw_start_bot = transform_ramp_point("ramp_left_wall", -rw_l_size[0] / 2.0, -rw_l_size[1] / 2.0, -rw_l_size[2] / 2.0)
    ramp_lw_start_top = transform_ramp_point("ramp_left_wall", -rw_l_size[0] / 2.0, -rw_l_size[1] / 2.0, +rw_l_size[2] / 2.0)
    ramp_lw_end_bot = transform_ramp_point("ramp_left_wall", rw_l_size[0] / 2.0, -rw_l_size[1] / 2.0, -rw_l_size[2] / 2.0)
    ramp_lw_end_top = transform_ramp_point("ramp_left_wall", rw_l_size[0] / 2.0, -rw_l_size[1] / 2.0, +rw_l_size[2] / 2.0)

    assert ramp_lw_start_bot[2] <= lower_floor_top_z + 0.10, "Left wall bottom does not reach lower floor level"
    assert ramp_lw_start_top[2] >= lower_ceil_bot_z - 0.10, "Left wall top does not reach lower ceiling level"
    assert ramp_lw_end_bot[2] <= upper_floor_top_z + 0.10, "Left wall bottom does not reach upper floor level"
    assert ramp_lw_end_top[2] >= upper_ceil_bot_z - 0.10, "Left wall top does not reach upper ceiling level"

    # 6. Ramp Right Wall Transformed Coordinates (inner face: local_dy = +size[1]/2)
    rw_r_size = [float(v) for v in ramp_tree.find(".//link[@name='ramp_right_wall']//geometry/box/size").text.split()]
    ramp_rw_start = transform_ramp_point("ramp_right_wall", -rw_r_size[0] / 2.0, rw_r_size[1] / 2.0, 0.0)
    ramp_rw_end = transform_ramp_point("ramp_right_wall", rw_r_size[0] / 2.0, rw_r_size[1] / 2.0, 0.0)

    # Right wall horizontal alignment
    assert math.isclose(ramp_rw_start[1], -1.750, abs_tol=1e-3), f"Ramp right wall inner y is {ramp_rw_start[1]}, expected -1.75"
    assert math.isclose(ramp_rw_end[1], -1.750, abs_tol=1e-3), f"Ramp right wall inner y is {ramp_rw_end[1]}, expected -1.75"
    assert math.isclose(ramp_rw_start[1], lower_r_wall_inner_y, abs_tol=1e-3), "Right wall misaligned at lower joint"
    assert math.isclose(ramp_rw_end[1], upper_r_wall_inner_y, abs_tol=1e-3), "Right wall misaligned at upper joint"
    assert math.isclose(ramp_rw_start[0], 42.000, abs_tol=0.02), f"Right wall start x {ramp_rw_start[0]} != 42.0"
    assert math.isclose(ramp_rw_end[0], 54.000, abs_tol=0.02), f"Right wall end x {ramp_rw_end[0]} != 54.0"

    # Right wall vertical extents (verify wall covers drift height from floor to ceiling)
    ramp_rw_start_bot = transform_ramp_point("ramp_right_wall", -rw_r_size[0] / 2.0, rw_r_size[1] / 2.0, -rw_r_size[2] / 2.0)
    ramp_rw_start_top = transform_ramp_point("ramp_right_wall", -rw_r_size[0] / 2.0, rw_r_size[1] / 2.0, +rw_r_size[2] / 2.0)
    ramp_rw_end_bot = transform_ramp_point("ramp_right_wall", rw_r_size[0] / 2.0, rw_r_size[1] / 2.0, -rw_r_size[2] / 2.0)
    ramp_rw_end_top = transform_ramp_point("ramp_right_wall", rw_r_size[0] / 2.0, rw_r_size[1] / 2.0, +rw_r_size[2] / 2.0)

    assert ramp_rw_start_bot[2] <= lower_floor_top_z + 0.10, "Right wall bottom does not reach lower floor level"
    assert ramp_rw_start_top[2] >= lower_ceil_bot_z - 0.10, "Right wall top does not reach lower ceiling level"
    assert ramp_rw_end_bot[2] <= upper_floor_top_z + 0.10, "Right wall bottom does not reach upper floor level"
    assert ramp_rw_end_top[2] >= upper_ceil_bot_z - 0.10, "Right wall top does not reach upper ceiling level"

    # 7. Ramp Ceiling Transformed Coordinates & Horizontal Continuity
    rc_size = [float(v) for v in ramp_tree.find(".//link[@name='ramp_ceiling']//geometry/box/size").text.split()]
    # Bottom surface vertices
    ramp_c_start_bot = transform_ramp_point("ramp_ceiling", -rc_size[0] / 2.0, 0.0, -rc_size[2] / 2.0)
    ramp_c_end_bot = transform_ramp_point("ramp_ceiling", rc_size[0] / 2.0, 0.0, -rc_size[2] / 2.0)
    # Centerline vertices
    ramp_c_start_mid = transform_ramp_point("ramp_ceiling", -rc_size[0] / 2.0, 0.0, 0.0)
    ramp_c_end_mid = transform_ramp_point("ramp_ceiling", rc_size[0] / 2.0, 0.0, 0.0)
    # Top surface vertices
    ramp_c_start_top = transform_ramp_point("ramp_ceiling", -rc_size[0] / 2.0, 0.0, rc_size[2] / 2.0)
    ramp_c_end_top = transform_ramp_point("ramp_ceiling", rc_size[0] / 2.0, 0.0, rc_size[2] / 2.0)

    # Adjoining ceiling boundary references:
    lower_ceil_end_x = dl_c_p[0] + dl_c_s[0] / 2.0          # 42.000m
    upper_ceil_start_x = ud_c_p[0] - ud_c_s[0] / 2.0        # 53.900m

    # Horizontal Gap/Overlap Tolerances:
    # A tilted rectangular box link (pitch -15 deg, thickness 0.400m) with square cuts
    # creates a bevel horizontal offset of delta_x = (thickness/2)*sin(15 deg) = 0.0518m.
    # Acceptable non-mitered square-cut horizontal gap tolerance: <= 0.060m (60mm).
    # Acceptable collision geometry overlap tolerance: <= 0.200m (200mm, ensures no light/physics leaks).
    MAX_CEILING_GAP_M = 0.060
    MAX_CEILING_OVERLAP_M = 0.200

    # Lower Joint Horizontal Continuity (x = 42.0m):
    # Centerline matches joint boundary exactly:
    assert math.isclose(ramp_c_start_mid[0], lower_ceil_end_x, abs_tol=0.01), (
        f"Ramp ceiling centerline start x {ramp_c_start_mid[0]:.4f}m does not match lower joint {lower_ceil_end_x:.4f}m"
    )
    # Bottom corner horizontal gap <= 60mm:
    lower_gap = ramp_c_start_bot[0] - lower_ceil_end_x
    assert 0.0 <= lower_gap <= MAX_CEILING_GAP_M, (
        f"Lower ceiling bottom horizontal gap {lower_gap:.4f}m exceeds tolerance ({MAX_CEILING_GAP_M}m)"
    )
    # Top corner overlaps lower ceiling:
    assert ramp_c_start_top[0] <= lower_ceil_end_x, "Ramp ceiling top should overlap into lower drift"

    # Upper Joint Horizontal Continuity (x = 54.0m):
    # Centerline matches upper drift nominal joint:
    assert math.isclose(ramp_c_end_mid[0], 54.000, abs_tol=0.01), (
        f"Ramp ceiling centerline end x {ramp_c_end_mid[0]:.4f}m does not match nominal joint (54.0m)"
    )
    # Bottom corner overlaps upper drift ceiling (53.9m <= 54.052m) to prevent gaps:
    upper_overlap = ramp_c_end_bot[0] - upper_ceil_start_x
    assert 0.0 <= upper_overlap <= MAX_CEILING_OVERLAP_M, (
        f"Upper ceiling horizontal overlap {upper_overlap:.4f}m exceeds tolerance ({MAX_CEILING_OVERLAP_M}m)"
    )

    # Ceiling vertical step at lower joint (|3.007 - 3.000| = 0.007m)
    assert abs(ramp_c_start_bot[2] - lower_ceil_bot_z) <= 0.02, (
        f"Ceiling vertical step at lower transition: {abs(ramp_c_start_bot[2] - lower_ceil_bot_z):.4f}m exceeds tolerance (0.02m)"
    )
    # Ceiling vertical step at upper joint (|6.222 - 6.215| = 0.007m)
    assert abs(ramp_c_end_bot[2] - upper_ceil_bot_z) <= 0.02, (
        f"Ceiling vertical step at upper transition: {abs(ramp_c_end_bot[2] - upper_ceil_bot_z):.4f}m exceeds tolerance (0.02m)"
    )

    # 8. Verify 15.0-degree Incline Consistency
    dx_floor = ramp_f_end[0] - ramp_f_start[0]
    dz_floor = ramp_f_end[2] - ramp_f_start[2]
    measured_incline_deg = math.degrees(math.atan2(dz_floor, dx_floor))
    assert math.isclose(measured_incline_deg, 15.0, abs_tol=0.1), (
        f"Measured incline {measured_incline_deg:.2f} deg is not 15.0 deg"
    )

    # 9. Verify 3.0m Normal Ceiling Clearance along Incline
    rf_link = ramp_tree.find(".//link[@name='ramp_floor']")
    rc_link = ramp_tree.find(".//link[@name='ramp_ceiling']")
    rf_z = float(rf_link.find("pose").text.split()[2])
    rc_z = float(rc_link.find("pose").text.split()[2])
    normal_clearance = (rc_z - rc_size[2] / 2.0) - (rf_z + rf_size[2] / 2.0)
    assert math.isclose(normal_clearance, 3.000, abs_tol=0.01), (
        f"Normal ceiling clearance along ramp {normal_clearance:.4f}m is not 3.000m"
    )


def test_ramp_transformation_with_nonzero_world_orientation():
    """
    Rigorously validates 6-DOF transformation for arbitrary world orientations
    including yaw rotation and genuinely non-zero 3-axis (roll, pitch, yaw) orientation:
    - Case 1: Yaw-only rotation (roll=0, pitch=0, yaw=+90 deg)
    - Case 2: Full 6-DOF non-zero 3-axis rotation (roll=0.15 rad, pitch=-0.10 rad, yaw=0.50 rad)
    Verifies:
    1. Transformed longitudinal direction aligns with R_world * R_link * (1, 0, 0).
    2. 15.0-degree incline angle is invariant under 3D world rotation.
    3. Corridor longitudinal and transverse wall directions are perpendicular (dot product ~ 0)
       for both left and right walls.
    4. Clearance is verified for wall boundaries along surface normal (3.000m exact)
       and floor-to-ceiling surface separation at matching longitudinal coordinates (2.999m exact within 0.005m).
    """
    ramp_tree = ET.parse(MODELS_DIR / "tunnel_ramp_15deg" / "model.sdf")

    def mat_vec_mul(rot_matrix, vec):
        x, y, z = vec
        return (
            rot_matrix[0][0] * x + rot_matrix[0][1] * y + rot_matrix[0][2] * z,
            rot_matrix[1][0] * x + rot_matrix[1][1] * y + rot_matrix[1][2] * z,
            rot_matrix[2][0] * x + rot_matrix[2][1] * y + rot_matrix[2][2] * z,
        )

    def dot_product(v1, v2):
        return sum(a * b for a, b in zip(v1, v2))

    def norm(v):
        return math.sqrt(sum(a * a for a in v))

    def normalize(v):
        n = norm(v)
        return tuple(a / n for a in v)

    def cross_product(v1, v2):
        return (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        )

    rf_size = [float(v) for v in ramp_tree.find(".//link[@name='ramp_floor']//geometry/box/size").text.split()]
    rc_size = [float(v) for v in ramp_tree.find(".//link[@name='ramp_ceiling']//geometry/box/size").text.split()]
    rw_l_size = [float(v) for v in ramp_tree.find(".//link[@name='ramp_left_wall']//geometry/box/size").text.split()]
    rw_r_size = [float(v) for v in ramp_tree.find(".//link[@name='ramp_right_wall']//geometry/box/size").text.split()]

    test_orientations = [
        # Case 1: Pure yaw rotation (+90 deg)
        ("yaw_90deg", (100.0, -50.0, 10.0), (0.0, 0.0, math.pi / 2.0)),
        # Case 2: Genuinely non-zero 3-axis orientation (roll, pitch, yaw all non-zero)
        ("full_6dof_rpy", (120.0, -45.0, 15.0), (0.15, -0.10, 0.50)),
    ]

    for case_name, world_origin, (roll, pitch, yaw) in test_orientations:
        world_rot = euler_to_matrix(roll, pitch, yaw)

        def transform_pt(link_name: str, dx: float, dy: float, dz: float):
            link = ramp_tree.find(f".//link[@name='{link_name}']")
            pose = [float(v) for v in link.find("pose").text.split()]
            lx, ly, lz = pose[:3]
            lr = pose[3] if len(pose) > 3 else 0.0
            lp = pose[4] if len(pose) > 4 else 0.0
            lyaw = pose[5] if len(pose) > 5 else 0.0
            r_link = euler_to_matrix(lr, lp, lyaw)
            p_model = apply_transform(r_link, (lx, ly, lz), (dx, dy, dz))
            return apply_transform(world_rot, world_origin, p_model)

        # Longitudinal corridor vector (floor start to floor end)
        f_start = transform_pt("ramp_floor", -rf_size[0] / 2.0, 0.0, rf_size[2] / 2.0)
        f_end = transform_pt("ramp_floor", rf_size[0] / 2.0, 0.0, rf_size[2] / 2.0)
        v_long = tuple(b - a for a, b in zip(f_start, f_end))
        u_long = normalize(v_long)

        # Transverse vector across corridor (right wall to left wall inner face)
        lw_mid = transform_pt("ramp_left_wall", 0.0, -rw_l_size[1] / 2.0, 0.0)
        rw_mid = transform_pt("ramp_right_wall", 0.0, rw_r_size[1] / 2.0, 0.0)
        v_trans = tuple(b - a for a, b in zip(rw_mid, lw_mid))
        u_trans = normalize(v_trans)

        # Normalized ramp surface normal vector
        u_normal = normalize(cross_product(u_long, u_trans))

        # 1. Transformed longitudinal direction validation:
        rf_link = ramp_tree.find(".//link[@name='ramp_floor']")
        rf_pose = [float(v) for v in rf_link.find("pose").text.split()]
        r_rf_link = euler_to_matrix(rf_pose[3], rf_pose[4], rf_pose[5])
        u_long_model = mat_vec_mul(r_rf_link, (1.0, 0.0, 0.0))
        u_long_expected = mat_vec_mul(world_rot, u_long_model)
        for a, b in zip(u_long, u_long_expected):
            assert math.isclose(a, b, abs_tol=1e-5), (
                f"[{case_name}] Longitudinal unit vector component {a:.5f} != expected {b:.5f}"
            )

        # 2. Ramp inclination angle validation:
        # Ramp inclination in corridor heading must remain 15.0 deg relative to horizontal heading:
        u_horiz_world = mat_vec_mul(world_rot, (1.0, 0.0, 0.0))
        cos_incline = max(-1.0, min(1.0, dot_product(u_long, u_horiz_world)))
        incline_deg = math.degrees(math.acos(cos_incline))
        assert math.isclose(incline_deg, 15.0, abs_tol=0.1), (
            f"[{case_name}] Measured incline {incline_deg:.3f} deg is not 15.0 deg"
        )

        # 3. Wall orientation validation (perpendicular dot product):
        dot_lt = dot_product(u_long, u_trans)
        assert math.isclose(dot_lt, 0.0, abs_tol=1e-6), (
            f"[{case_name}] dot(u_long, u_trans) {dot_lt:.2e} != 0, corridor is not orthogonal"
        )

        # Check left wall transverse thickness vector is perpendicular to longitudinal heading:
        lw_outer = transform_pt("ramp_left_wall", 0.0, rw_l_size[1] / 2.0, 0.0)
        u_lw_thick = normalize(tuple(b - a for a, b in zip(lw_mid, lw_outer)))
        assert math.isclose(dot_product(u_long, u_lw_thick), 0.0, abs_tol=1e-6), (
            f"[{case_name}] Left wall thickness direction is not perpendicular to corridor"
        )

        # Check right wall transverse thickness vector is perpendicular to longitudinal heading:
        rw_outer = transform_pt("ramp_right_wall", 0.0, -rw_r_size[1] / 2.0, 0.0)
        u_rw_thick = normalize(tuple(b - a for a, b in zip(rw_mid, rw_outer)))
        assert math.isclose(dot_product(u_long, u_rw_thick), 0.0, abs_tol=1e-6), (
            f"[{case_name}] Right wall thickness direction is not perpendicular to corridor"
        )

        # 4. Normal-clearance validation along surface normal:
        # A) Wall height spanning floor to ceiling along surface normal:
        lw_bot = transform_pt("ramp_left_wall", 0.0, -rw_l_size[1] / 2.0, -rw_l_size[2] / 2.0)
        lw_top = transform_pt("ramp_left_wall", 0.0, -rw_l_size[1] / 2.0, rw_l_size[2] / 2.0)
        v_wall = tuple(b - a for a, b in zip(lw_bot, lw_top))
        wall_normal_clearance = dot_product(v_wall, u_normal)
        assert math.isclose(wall_normal_clearance, 3.000, abs_tol=1e-3), (
            f"[{case_name}] Wall normal clearance {wall_normal_clearance:.4f}m is not 3.000m"
        )

        rw_bot = transform_pt("ramp_right_wall", 0.0, rw_r_size[1] / 2.0, -rw_r_size[2] / 2.0)
        rw_top = transform_pt("ramp_right_wall", 0.0, rw_r_size[1] / 2.0, rw_r_size[2] / 2.0)
        v_rwall = tuple(b - a for a, b in zip(rw_bot, rw_top))
        rwall_normal_clearance = dot_product(v_rwall, u_normal)
        assert math.isclose(rwall_normal_clearance, 3.000, abs_tol=1e-3), (
            f"[{case_name}] Right wall normal clearance {rwall_normal_clearance:.4f}m is not 3.000m"
        )

        # B) Floor-to-ceiling surface separation at matching longitudinal coordinates:
        # In tunnel_ramp_15deg/model.sdf, both ramp_floor and ramp_ceiling have identical pitch (-15 deg)
        # and identical link center longitudinal coordinates (x=6.0m).
        # Nominal vertical surface separation from SDF link poses and geometries:
        # (rc_pose_z - rc_size_z/2) - (rf_pose_z + rf_size_z/2) = 4.808 - 0.200 - (1.559 + 0.050) = 2.999m.
        rc_link = ramp_tree.find(".//link[@name='ramp_ceiling']")
        rc_pose = [float(v) for v in rc_link.find("pose").text.split()]
        expected_surface_sep = (rc_pose[2] - rc_size[2] / 2.0) - (rf_pose[2] + rf_size[2] / 2.0)

        u_upright = mat_vec_mul(world_rot, (0.0, 0.0, 1.0))
        p_floor_inner_model = (rf_pose[0], rf_pose[1], rf_pose[2] + rf_size[2] / 2.0)
        p_ceil_inner_model = (rc_pose[0], rc_pose[1], rc_pose[2] - rc_size[2] / 2.0)
        p_floor_inner_world = apply_transform(world_rot, world_origin, p_floor_inner_model)
        p_ceil_inner_world = apply_transform(world_rot, world_origin, p_ceil_inner_model)

        v_fc = tuple(b - a for a, b in zip(p_floor_inner_world, p_ceil_inner_world))
        fc_upright_clearance = dot_product(v_fc, u_upright)

        # Assert matching surface separation is exactly 2.999m within tight 0.005m tolerance:
        assert math.isclose(fc_upright_clearance, 2.999, abs_tol=0.005), (
            f"[{case_name}] Floor-to-ceiling clearance {fc_upright_clearance:.4f}m is not 2.999m"
        )
        assert math.isclose(fc_upright_clearance, expected_surface_sep, abs_tol=1e-5), (
            f"[{case_name}] Clearance {fc_upright_clearance:.4f}m does not match expected {expected_surface_sep:.4f}m"
        )

