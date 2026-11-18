#!/usr/bin/env python3
"""
Unit Test: Subterranean RF Communication and Attenuation Model
Milestone M1: Underground Mine Simulation (TASK-M1-005)

Tests:
1. YAML configuration loading via from_yaml() and parameter consumption
2. Two robots in the same straight tunnel (LOS)
3. Two robots separated by one 90-degree bend (NLOS)
4. Two robots separated by two bends (disconnection threshold)
5. Robots positioned near tunnel intersections
6. Robots positioned near tunnel-region boundaries
7. Robots with different vertical elevations (ramp & upper drift)
8. Robots separated by physical obstacles (timber support / rock pile)
9. Robots whose direct path is visible despite being in different coordinate regions
10. Robots outside known mine layout bounds
11. Maximum distance cutoff enforcement
12. Forced blackout mode toggle
13. Latency, jitter, and bandwidth shaping
"""

import math
import sys
from pathlib import Path
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from layer1_robot_environment.communication_simulation.subterranean_rf_model import (
    SubterraneanRFModel,
    TunnelTopology,
)


def test_from_yaml_configuration():
    """Verify that configuration is loaded cleanly from YAML and all parameters are consumed."""
    cfg_path = REPO_ROOT / "config" / "simulation" / "rf_attenuation_config.yaml"
    assert cfg_path.exists(), f"RF configuration missing: {cfg_path}"

    with open(cfg_path, "r", encoding="utf-8") as f:
        raw_cfg = yaml.safe_load(f)

    model = SubterraneanRFModel.from_yaml(cfg_path)
    assert model.tx_power_dbm == raw_cfg["radio_parameters"]["tx_power_dbm"]
    assert model.rx_sensitivity_dbm == raw_cfg["radio_parameters"]["rx_sensitivity_dbm"]
    assert model.path_loss_exponent == raw_cfg["radio_parameters"]["path_loss_exponent"]
    assert model.reference_loss_db == raw_cfg["radio_parameters"]["reference_loss_db"]
    assert model.corner_diffraction_loss_db == raw_cfg["underground_attenuation"]["corner_diffraction_loss_db"]
    assert model.los_cutoff_distance_m == raw_cfg["underground_attenuation"]["los_cutoff_distance_m"]
    assert model.nlos_corner_limit == raw_cfg["underground_attenuation"]["nlos_corner_limit"]
    assert model.bandwidth_limit_kbps == raw_cfg["network_shaping"]["bandwidth_limit_kbps"]
    assert model.forced_blackout == raw_cfg["fault_injection"]["forced_blackout"]


def test_two_robots_same_straight_tunnel_los():
    """Verify two robots in the same straight tunnel have line-of-sight and low packet loss."""
    model = SubterraneanRFModel(random_seed=42)
    # Clear section of main drift (x=0 to x=4m, before the timber support at x=5m)
    link = model.evaluate_link((0.0, 0.0, 0.5), (4.0, 0.0, 0.5))

    assert link["has_line_of_sight"] is True
    assert link["corner_count"] == 0
    assert link["classification_reason"] == "CLEAR_LINE_OF_SIGHT"
    assert link["is_connected"] is True
    assert link["packet_loss_rate"] <= 0.05
    assert link["rssi_dbm"] > -50.0
    assert link["effective_bandwidth_kbps"] > 230.0


def test_two_robots_separated_by_one_bend():
    """Verify two robots separated by one 90-degree corner experience corner diffraction penalty."""
    model = SubterraneanRFModel(random_seed=42)
    # Tx in main drift (x=10, y=0), Rx in north crosscut drift (x=30, y=15)
    link = model.evaluate_link((10.0, 0.0, 0.5), (30.0, 15.0, 0.5))

    assert link["has_line_of_sight"] is False
    assert link["corner_count"] == 1
    assert "BLOCKED_BY_ROCK_WALLS" in str(link["classification_reason"])
    assert link["is_connected"] is True
    assert link["rssi_dbm"] < -65.0
    assert link["latency_ms"] > 30.0  # includes 15ms corner penalty


def test_two_robots_separated_by_two_bends():
    """Verify two robots separated by 2 bends exceed the corner limit and are disconnected."""
    model = SubterraneanRFModel(random_seed=42)
    # Tx in main drift (x=5, y=0), Rx in east drift extension (x=40, y=23)
    link = model.evaluate_link((5.0, 0.0, 0.5), (40.0, 23.0, 0.5))

    assert link["has_line_of_sight"] is False
    assert link["corner_count"] == 2
    assert link["is_connected"] is False
    assert link["status"] == "EXCEEDED_CORNER_LIMIT"
    assert link["packet_loss_rate"] == 1.0
    assert link["effective_bandwidth_kbps"] == 0.0


def test_robots_near_tunnel_intersections():
    """Verify RF evaluation when robots approach the T-Junction intersection."""
    model = SubterraneanRFModel(random_seed=42)
    # Robot A approaching T-junction from west (x=27.0, y=0), Robot B at junction center (x=30.0, y=0)
    link = model.evaluate_link((27.0, 0.0, 0.5), (30.0, 0.0, 0.5))

    assert link["has_line_of_sight"] is True
    assert link["corner_count"] == 0
    assert link["is_connected"] is True


def test_robots_near_tunnel_region_boundaries():
    """Verify link evaluation when robots are near transition boundaries (e.g. crosscut to turn)."""
    model = SubterraneanRFModel(random_seed=42)
    # Robot A in crosscut drift (x=30.0, y=18.0), Robot B in curved bend entry (x=30.0, y=21.0)
    link = model.evaluate_link((30.0, 18.0, 0.5), (30.0, 21.0, 0.5))

    assert link["has_line_of_sight"] is True
    assert link["corner_count"] == 0
    assert link["is_connected"] is True


def test_robots_with_different_vertical_elevations():
    """Verify link evaluation along the 15-degree ramp with vertical elevation change."""
    model = SubterraneanRFModel(random_seed=42)
    # Robot A on lower ramp approach (x=38.0, y=0.0, z=0.5)
    # Robot B on upper level drift (x=58.0, y=0.0, z=3.7)
    link = model.evaluate_link((38.0, 0.0, 0.5), (58.0, 0.0, 3.7))

    assert link["has_line_of_sight"] is True
    assert link["corner_count"] == 0
    expected_3d_dist = math.sqrt((58.0 - 38.0)**2 + (3.7 - 0.5)**2)  # ~20.25m
    assert math.isclose(float(link["distance_m"]), expected_3d_dist, rel_tol=1e-2)
    assert link["is_connected"] is True


def test_robots_separated_by_physical_obstacle():
    """Verify that an opaque obstacle (timber support) blocks direct optical LOS and adds shadow loss."""
    model = SubterraneanRFModel(random_seed=42)
    # Ray between x=2.0 and x=8.0 passes through timber_roof_support at x=5.0m
    link_blocked = model.evaluate_link((2.0, 0.0, 0.5), (8.0, 0.0, 0.5))

    assert link_blocked["has_line_of_sight"] is False
    assert link_blocked["corner_count"] == 0
    assert "TIMBER_ROOF_SUPPORT" in str(link_blocked["classification_reason"])

    # Clear ray with equal distance (x=6.0 to x=12.0)
    link_clear = model.evaluate_link((6.0, 0.0, 0.5), (12.0, 0.0, 0.5))
    assert link_clear["has_line_of_sight"] is True

    # Obstacle shadowing penalty (12 dB) should be reflected in RSSI difference
    rssi_diff = float(link_clear["rssi_dbm"]) - float(link_blocked["rssi_dbm"])
    assert pytest.approx(rssi_diff, abs=1.0) == model.obstacle_shadow_loss_db


def test_direct_path_visible_despite_different_regions():
    """Verify ray-caster recognizes clear sightline between different corridors when sightline is open."""
    model = SubterraneanRFModel(random_seed=42)
    # Robot A in main drift (x=31.0, y=0.5), Robot B in crosscut (x=31.0, y=2.5)
    # East of the fallen rock pile; sightline through T-junction opening is physically clear
    link = model.evaluate_link((31.0, 0.5, 0.5), (31.0, 2.5, 0.5))

    assert link["has_line_of_sight"] is True
    assert link["corner_count"] == 0
    assert link["classification_reason"] == "CLEAR_LINE_OF_SIGHT"
    assert link["is_connected"] is True


def test_robots_outside_known_mine_layout():
    """Verify coordinates outside the defined mine corridors are flagged and disconnected."""
    model = SubterraneanRFModel(random_seed=42)
    # Pos B is far outside underground mine bounds
    link = model.evaluate_link((0.0, 0.0, 0.0), (100.0, 100.0, 0.0))

    assert link["has_line_of_sight"] is False
    assert link["status"] == "OUTSIDE_MINE_BOUNDS"
    assert link["classification_reason"] == "OUTSIDE_MINE_BOUNDS"
    assert link["is_connected"] is False
    assert link["packet_loss_rate"] == 1.0
    assert link["effective_bandwidth_kbps"] == 0.0
    assert link["latency_ms"] == float("inf")


def test_distance_cutoff_enforcement():
    """Verify that exceeding los_cutoff_distance_m terminates the communication link."""
    model = SubterraneanRFModel(los_cutoff_distance_m=60.0, random_seed=42)
    # Pos B at 65m exceeds 60m threshold
    link = model.evaluate_link((0.0, 0.0, 0.5), (65.0, 0.0, 0.5))

    assert link["is_connected"] is False
    assert "EXCEEDED" in str(link["status"])
    assert link["packet_loss_rate"] == 1.0
    assert link["effective_bandwidth_kbps"] == 0.0


def test_forced_blackout():
    """Verify forced blackout mode immediately halts all communication."""
    model = SubterraneanRFModel(random_seed=42)
    link_before = model.evaluate_link((0.0, 0.0, 0.5), (2.0, 0.0, 0.5))
    assert link_before["is_connected"] is True

    model.set_forced_blackout(True)
    link_blackout = model.evaluate_link((0.0, 0.0, 0.5), (2.0, 0.0, 0.5))
    assert link_blackout["is_connected"] is False
    assert link_blackout["packet_loss_rate"] == 1.0
    assert link_blackout["latency_ms"] == float("inf")
    assert link_blackout["effective_bandwidth_kbps"] == 0.0
    assert link_blackout["status"] == "FORCED_BLACKOUT"

    model.set_forced_blackout(False)
    link_after = model.evaluate_link((0.0, 0.0, 0.5), (2.0, 0.0, 0.5))
    assert link_after["is_connected"] is True
    assert link_after["status"] == "CONNECTED"


# ==============================================================================
# Issue 2 & Issue 3 Required Regression & Geometry Tests
# ==============================================================================

def test_segments_intersect_collinear_overlapping():
    """Verify _segments_intersect detects overlapping collinear segments."""
    # Collinear along y=0: [0, 5] and [3, 8] overlap on [3, 5]
    p1, p2 = (0.0, 0.0), (5.0, 0.0)
    q1, q2 = (3.0, 0.0), (8.0, 0.0)
    assert SubterraneanRFModel._segments_intersect(p1, p2, q1, q2) is True

    # Collinear along y=0: [0, 2] and [3, 5] do NOT overlap
    q3, q4 = (3.0, 0.0), (5.0, 0.0)
    p3, p4 = (0.0, 0.0), (2.0, 0.0)
    assert SubterraneanRFModel._segments_intersect(p3, p4, q3, q4) is False


def test_segments_intersect_endpoint_contact():
    """Verify _segments_intersect detects T-contact and shared endpoint contact."""
    # T-contact: q1 touches midpoint of [p1, p2]
    p1, p2 = (0.0, 0.0), (10.0, 0.0)
    q1, q2 = (5.0, 0.0), (5.0, 5.0)
    assert SubterraneanRFModel._segments_intersect(p1, p2, q1, q2) is True

    # Shared endpoint: p2 == q1
    p3, p4 = (0.0, 0.0), (4.0, 4.0)
    q3, q4 = (4.0, 4.0), (8.0, 0.0)
    assert SubterraneanRFModel._segments_intersect(p3, p4, q3, q4) is True


def test_segments_intersect_parallel_and_near_parallel():
    """Verify _segments_intersect rejects parallel disjoint segments and handles tolerances."""
    # Parallel disjoint segments
    p1, p2 = (0.0, 0.0), (10.0, 0.0)
    q1, q2 = (0.0, 1.0), (10.0, 1.0)
    assert SubterraneanRFModel._segments_intersect(p1, p2, q1, q2) is False

    # Standard crossing segments
    p3, p4 = (0.0, 0.0), (10.0, 10.0)
    q3, q4 = (0.0, 10.0), (10.0, 0.0)
    assert SubterraneanRFModel._segments_intersect(p3, p4, q3, q4) is True


def test_obstacle_intersection_3d_above_obstacle():
    """Verify that a path passing entirely above an obstacle volume does not register a collision."""
    # Obstacle AABB: x in [4.0, 6.0], y in [-1.0, 1.0], z in [0.0, 2.0]
    aabb = (4.0, 6.0, -1.0, 1.0, 0.0, 2.0)

    # Path from x=0 to x=10 passing at z=2.5m (entirely above obstacle)
    p0 = (0.0, 0.0, 2.5)
    p1 = (10.0, 0.0, 2.5)
    assert SubterraneanRFModel._segment_intersects_aabb_3d(p0, p1, aabb) is False


def test_obstacle_intersection_3d_through_obstacle():
    """Verify that a path penetrating the 3D obstacle volume registers a collision."""
    aabb = (4.0, 6.0, -1.0, 1.0, 0.0, 2.0)

    # Horizontal path passing directly through obstacle at z=1.0m
    p0 = (0.0, 0.0, 1.0)
    p1 = (10.0, 0.0, 1.0)
    assert SubterraneanRFModel._segment_intersects_aabb_3d(p0, p1, aabb) is True


def test_obstacle_intersection_3d_around_obstacle():
    """Verify that a path passing to the side of an obstacle does not register a collision."""
    aabb = (4.0, 6.0, -1.0, 1.0, 0.0, 2.0)

    # Path at y=2.0 (outside y in [-1, 1])
    p0 = (0.0, 2.0, 1.0)
    p1 = (10.0, 2.0, 1.0)
    assert SubterraneanRFModel._segment_intersects_aabb_3d(p0, p1, aabb) is False


def test_obstacle_intersection_3d_sloped_path():
    """Verify that a 3D sloped trajectory passing through an obstacle is detected."""
    aabb = (4.0, 6.0, -1.0, 1.0, 0.0, 2.0)

    # Path climbing from (0, 0, 0) to (10, 0, 3.0); at x=5, z=1.5 which is inside [0, 2]
    p0 = (0.0, 0.0, 0.0)
    p1 = (10.0, 0.0, 3.0)
    assert SubterraneanRFModel._segment_intersects_aabb_3d(p0, p1, aabb) is True

    # Path climbing steep from (0, 0, 2.2) to (10, 0, 5.0); at x=5, z=3.6 which is above [0, 2]
    p2 = (0.0, 0.0, 2.2)
    p3 = (10.0, 0.0, 5.0)
    assert SubterraneanRFModel._segment_intersects_aabb_3d(p2, p3, aabb) is False


def test_arbitrary_custom_tunnel_topology():
    """
    Verify RF model on a completely new, user-defined tunnel layout
    (Z-shaped corridor layout at arbitrary coordinates [100.0, 200.0] x [50.0, 150.0])
    proving the model does not depend on hard-coded mine coordinates.
    """
    custom_topo = TunnelTopology()
    # Node sequence forming a Z-bend corridor:
    # Segment 1: (100, 50, 0) to (140, 50, 0) [straight east]
    # Segment 2: (140, 50, 0) to (140, 90, 0) [turn north, 90 deg bend]
    # Segment 3: (140, 90, 0) to (180, 90, 0) [turn east, second 90 deg bend]
    custom_topo.add_node("node_a", (100.0, 50.0, 0.0))
    custom_topo.add_node("node_b", (140.0, 50.0, 0.0))
    custom_topo.add_node("node_c", (140.0, 90.0, 0.0))
    custom_topo.add_node("node_d", (180.0, 90.0, 0.0))

    custom_topo.add_edge("node_a", "node_b", "custom_drift_1", width=3.5, height=3.0)
    custom_topo.add_edge("node_b", "node_c", "custom_crosscut", width=3.5, height=3.0)
    custom_topo.add_edge("node_c", "node_d", "custom_drift_2", width=3.5, height=3.0)

    # Instantiate model with custom topology and arbitrary wall geometry
    custom_walls = [
        # Wall separating segment 1 from segment 3
        ((110.0, 70.0), (170.0, 70.0)),
        ((135.0, 45.0), (135.0, 85.0)),
    ]
    model = SubterraneanRFModel(
        topology=custom_topo,
        wall_segments=custom_walls,
        los_cutoff_distance_m=80.0,
        nlos_corner_limit=2,
        random_seed=42,
    )

    # 1. Straight tunnel path in custom layout (0 corners, LOS)
    link_straight = model.evaluate_link((105.0, 50.0, 0.5), (125.0, 50.0, 0.5))
    assert link_straight["has_line_of_sight"] is True
    assert link_straight["corner_count"] == 0
    assert link_straight["is_connected"] is True
    assert link_straight["status"] == "CONNECTED"

    # 2. One 90-degree bend in custom layout (1 corner, NLOS)
    link_1_bend = model.evaluate_link((120.0, 50.0, 0.5), (140.0, 70.0, 0.5))
    assert link_1_bend["has_line_of_sight"] is False
    assert link_1_bend["corner_count"] == 1
    assert link_1_bend["is_connected"] is True
    assert link_1_bend["status"] == "CONNECTED"
    assert link_1_bend["rssi_dbm"] < -60.0

    # 3. Two successive bends in custom layout (2 corners, exceeds limit)
    link_2_bends = model.evaluate_link((110.0, 50.0, 0.5), (170.0, 90.0, 0.5))
    assert link_2_bends["has_line_of_sight"] is False
    assert link_2_bends["corner_count"] == 2
    assert link_2_bends["is_connected"] is False
    assert link_2_bends["status"] == "EXCEEDED_CORNER_LIMIT"
    assert link_2_bends["packet_loss_rate"] == 1.0

    # 4. Point outside custom topology bounds
    link_outside = model.evaluate_link((100.0, 50.0, 0.5), (500.0, 500.0, 0.5))
    assert link_outside["is_connected"] is False
    assert link_outside["status"] == "OUTSIDE_MINE_BOUNDS"

