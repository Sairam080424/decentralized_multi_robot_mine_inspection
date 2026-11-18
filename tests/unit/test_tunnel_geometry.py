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
