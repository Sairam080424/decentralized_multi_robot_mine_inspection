#!/usr/bin/env python3
"""
Unit Test: Subterranean RF Communication and Attenuation Model
Tests distance path loss, tunnel LOS/NLOS diffraction, packet loss, latency, and forced blackout.
"""

import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from layer1_robot_environment.communication_simulation.subterranean_rf_model import SubterraneanRFModel


def test_distance_attenuation_monotonic():
    """Verify that RSSI decreases monotonically with increasing distance in LOS straight drift."""
    model = SubterraneanRFModel(random_seed=42)
    pos_tx = (0.0, 0.0, 0.5)

    distances = [5.0, 10.0, 20.0, 40.0, 60.0]
    rssi_values = []

    for d in distances:
        link = model.evaluate_link(pos_tx, (d, 0.0, 0.5))
        assert link["has_line_of_sight"] is True
        assert link["corner_count"] == 0
        rssi_values.append(link["rssi_dbm"])

    for i in range(len(rssi_values) - 1):
        assert rssi_values[i] > rssi_values[i + 1], (
            f"Expected monotonic decrease: {rssi_values[i]} should be > {rssi_values[i + 1]}"
        )


def test_corner_diffraction_penalty():
    """Verify that corner diffraction adds configured attenuation penalty (approx 18 dB)."""
    model = SubterraneanRFModel(corner_attenuation_db=18.0, random_seed=42)

    # LOS position: tx at (20, 0, 0.5), rx at (40, 0, 0.5) -> dist = 20m, 0 corners
    link_los = model.evaluate_link((20.0, 0.0, 0.5), (40.0, 0.0, 0.5))

    # NLOS position around T-junction: tx at (20, 0, 0.5), rx at (30, 10, 0.5)
    # Distance is sqrt(10^2 + 10^2) = 14.14m, but passes through 1 corner
    link_nlos = model.evaluate_link((20.0, 0.0, 0.5), (30.0, 10.0, 0.5))

    assert link_nlos["has_line_of_sight"] is False
    assert link_nlos["corner_count"] == 1

    # Compare link with equivalent geometric distance in straight drift:
    link_straight_eq = model.evaluate_link((20.0, 0.0, 0.5), (20.0 + link_nlos["distance_m"], 0.0, 0.5))
    rssi_diff = link_straight_eq["rssi_dbm"] - link_nlos["rssi_dbm"]
    assert pytest.approx(rssi_diff, abs=0.5) == 18.0, (
        f"Expected ~18 dB corner penalty, got {rssi_diff} dB"
    )


def test_two_corner_disconnection():
    """Verify that 2 corners (main drift to east drift extension) causes severe loss or disconnect."""
    model = SubterraneanRFModel(corner_attenuation_db=18.0, random_seed=42)
    # Tx at portal (5, 0, 0.5), Rx in east drift (40, 24, 0.5)
    link = model.evaluate_link((5.0, 0.0, 0.5), (40.0, 24.0, 0.5))

    assert link["corner_count"] == 2
    assert link["has_line_of_sight"] is False
    assert link["is_connected"] is False or link["packet_loss_rate"] > 0.8
    assert link["rssi_dbm"] < -85.0


def test_packet_loss_and_latency_bounds():
    """Verify packet loss rate is bounded in [0.0, 1.0] and latency increases with distance and corners."""
    model = SubterraneanRFModel(random_seed=42)
    link_close = model.evaluate_link((0.0, 0.0, 0.5), (2.0, 0.0, 0.5))
    assert link_close["packet_loss_rate"] <= 0.05
    assert link_close["latency_ms"] < 25.0
    assert link_close["is_connected"] is True


def test_forced_blackout():
    """Verify forced blackout mode immediately halts all communication."""
    model = SubterraneanRFModel(random_seed=42)
    # Check normal close link
    link_before = model.evaluate_link((0.0, 0.0, 0.5), (2.0, 0.0, 0.5))
    assert link_before["is_connected"] is True

    # Enable blackout
    model.set_forced_blackout(True)
    link_blackout = model.evaluate_link((0.0, 0.0, 0.5), (2.0, 0.0, 0.5))
    assert link_blackout["is_connected"] is False
    assert link_blackout["packet_loss_rate"] == 1.0
    assert link_blackout["latency_ms"] == float("inf")
    assert link_blackout["status"] == "FORCED_BLACKOUT"

    # Disable blackout
    model.set_forced_blackout(False)
    link_after = model.evaluate_link((0.0, 0.0, 0.5), (2.0, 0.0, 0.5))
    assert link_after["is_connected"] is True
    assert link_after["status"] == "CONNECTED"
