#!/usr/bin/env python3
"""
Unit Test: Terrain Elements and Obstacle Models
Tests presence, friction coefficients, and collision geometry for terrain and hazard models.
"""

from pathlib import Path
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORLD_PATH = REPO_ROOT / "simulation" / "worlds" / "mine_world.sdf"
MODELS_DIR = REPO_ROOT / "simulation" / "models"


def test_terrain_models_in_world():
    """Verify that mine_world.sdf includes gravel, mud, and ramp terrain elements."""
    tree = ET.parse(WORLD_PATH)
    include_uris = [inc.find("uri").text.strip() for inc in tree.findall(".//include") if inc.find("uri") is not None]

    assert "model://terrain_gravel_patch" in include_uris
    assert "model://terrain_mud_patch" in include_uris
    assert "model://tunnel_ramp_15deg" in include_uris


def test_obstacle_models_in_world():
    """Verify that mine_world.sdf includes all 5 required obstacle/hazard models."""
    tree = ET.parse(WORLD_PATH)
    include_uris = [inc.find("uri").text.strip() for inc in tree.findall(".//include") if inc.find("uri") is not None]

    expected_obstacles = [
        "model://fallen_rock_pile",
        "model://timber_roof_support",
        "model://standing_water",
        "model://mine_debris",
        "model://low_clearance_hazard",
    ]

    for obs in expected_obstacles:
        assert obs in include_uris, f"Obstacle model '{obs}' missing from mine_world.sdf"


def test_terrain_friction_properties():
    """Verify gravel and mud models define appropriate surface friction coefficients."""
    # Gravel patch friction
    gravel_tree = ET.parse(MODELS_DIR / "terrain_gravel_patch" / "model.sdf")
    gravel_mu1 = gravel_tree.find(".//surface/friction/ode/mu")
    gravel_mu2 = gravel_tree.find(".//surface/friction/ode/mu2")
    assert gravel_mu1 is not None and gravel_mu2 is not None
    assert pytest.approx(float(gravel_mu1.text), abs=0.05) == 0.40
    assert pytest.approx(float(gravel_mu2.text), abs=0.05) == 0.35

    # Mud patch friction
    mud_tree = ET.parse(MODELS_DIR / "terrain_mud_patch" / "model.sdf")
    mud_mu1 = mud_tree.find(".//surface/friction/ode/mu")
    mud_mu2 = mud_tree.find(".//surface/friction/ode/mu2")
    assert mud_mu1 is not None and mud_mu2 is not None
    assert pytest.approx(float(mud_mu1.text), abs=0.05) == 0.22
    assert pytest.approx(float(mud_mu2.text), abs=0.05) == 0.20


def test_obstacle_collision_geometries():
    """Verify all obstacles define non-empty physical collision geometries."""
    obstacles = [
        "fallen_rock_pile",
        "timber_roof_support",
        "standing_water",
        "mine_debris",
        "low_clearance_hazard",
    ]

    for obs_name in obstacles:
        sdf_path = MODELS_DIR / obs_name / "model.sdf"
        tree = ET.parse(sdf_path)
        collisions = tree.findall(".//collision")
        assert len(collisions) >= 1, f"Obstacle {obs_name} must define at least one <collision> element"
        for col in collisions:
            geom = col.find("geometry")
            assert geom is not None, f"Collision {col.get('name')} in {obs_name} missing geometry"
            has_shape = (
                geom.find("box") is not None
                or geom.find("cylinder") is not None
                or geom.find("sphere") is not None
                or geom.find("mesh") is not None
            )
            assert has_shape, f"Collision {col.get('name')} in {obs_name} has no recognized primitive geometry"
