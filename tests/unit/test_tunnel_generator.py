#!/usr/bin/env python3
"""
Unit Test: Tunnel Generator Configuration and Generation
Tests configuration validation, procedural generation logic, and repeatability.
"""

import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from generate_mine_tunnels import TunnelGenerator


def test_generator_config_loading():
    """Verify that the standard tunnel_layout_config.yaml loads and conforms to schema."""
    config_path = REPO_ROOT / "config" / "simulation" / "tunnel_layout_config.yaml"
    assert config_path.exists(), f"Missing config file: {config_path}"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    assert "seed" in cfg
    assert isinstance(cfg["seed"], int)
    assert "models" in cfg
    assert len(cfg["models"]) >= 4

    required_types = {"straight", "turn_90deg", "t_junction", "ramp"}
    present_types = {m.get("type") for m in cfg["models"]}
    assert required_types.issubset(present_types), f"Missing required segment types: {required_types - present_types}"


def test_generator_repeatability():
    """Verify that generation is strictly deterministic for a fixed seed."""
    gen1 = TunnelGenerator(seed=12345)
    sdf1 = gen1.generate_straight_segment(name="test_drift", length=10.0, width=3.5, height=3.0, roughness=0.1)

    gen2 = TunnelGenerator(seed=12345)
    sdf2 = gen2.generate_straight_segment(name="test_drift", length=10.0, width=3.5, height=3.0, roughness=0.1)

    assert sdf1 == sdf2, "Generator output must be deterministic when given identical seeds"


def test_generate_straight_profiles():
    """Verify straight tunnel generation across arched, rectangular, and trapezoidal profiles."""
    gen = TunnelGenerator(seed=42)
    for profile in ["arched", "rectangular", "trapezoidal"]:
        sdf = gen.generate_straight_segment(
            name=f"test_straight_{profile}",
            length=15.0,
            width=3.2,
            height=2.8,
            profile=profile,
        )
        # Verify valid XML
        root = ET.fromstring(sdf)
        assert root.tag == "sdf"
        model = root.find("model")
        assert model is not None
        assert model.get("name") == f"test_straight_{profile}"
        # Links should include floor, ceiling/roof, and wall blocks
        link_names = {l.get("name") for l in model.findall("link")}
        assert "floor" in link_names
        has_roof_or_ceiling = any("roof" in name or "ceiling" in name for name in link_names)
        assert has_roof_or_ceiling, f"No roof or ceiling link found for profile {profile}: {link_names}"
        assert any("left_wall" in name for name in link_names)
        assert any("right_wall" in name for name in link_names)


def test_generate_turn_segment():
    """Verify 90-degree turn segment generation produces valid curved wall links."""
    gen = TunnelGenerator(seed=42)
    sdf = gen.generate_turn_90deg_segment(
        name="test_turn",
        radius=7.0,
        width=3.5,
        height=3.0,
        num_steps=6,
    )
    root = ET.fromstring(sdf)
    model = root.find("model")
    assert model is not None
    link_names = {l.get("name") for l in model.findall("link")}
    assert "bend_floor_0" in link_names
    assert "bend_inner_wall_0" in link_names
    assert "bend_outer_wall_0" in link_names


def test_generate_t_junction_segment():
    """Verify T-junction generation produces interconnected main and branch drifts."""
    gen = TunnelGenerator(seed=42)
    sdf = gen.generate_t_junction_segment(
        name="test_t_junction",
        main_length=14.0,
        branch_length=7.0,
        width=3.5,
        height=3.0,
    )
    root = ET.fromstring(sdf)
    model = root.find("model")
    assert model is not None
    link_names = {l.get("name") for l in model.findall("link")}
    assert "main_floor" in link_names
    assert "branch_floor" in link_names
    assert "main_ceiling" in link_names
    assert "branch_ceiling" in link_names


def test_generate_ramp_segment():
    """Verify ramp generation configures correct incline geometry."""
    gen = TunnelGenerator(seed=42)
    sdf = gen.generate_ramp_segment(
        name="test_ramp_15",
        run_length=10.0,
        incline_deg=15.0,
        width=3.5,
        height=3.0,
    )
    root = ET.fromstring(sdf)
    model = root.find("model")
    assert model is not None
    link_names = {l.get("name") for l in model.findall("link")}
    assert "ramp_floor" in link_names
    assert "ramp_ceiling" in link_names
    assert "ramp_left_wall" in link_names
    assert "ramp_right_wall" in link_names
