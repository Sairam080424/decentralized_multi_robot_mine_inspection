#!/usr/bin/env python3
"""
Unit Test: SDF and XML Parsing for Subterranean Mine Simulation
Tests XML syntactic validity and SDFormat compliance for mine_world.sdf and all models.
"""

import os
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORLD_PATH = REPO_ROOT / "simulation" / "worlds" / "mine_world.sdf"
MODELS_DIR = REPO_ROOT / "simulation" / "models"


def test_mine_world_xml_structure():
    """Verify mine_world.sdf parses cleanly as valid XML with expected root and world elements."""
    assert WORLD_PATH.exists(), f"World file does not exist: {WORLD_PATH}"
    tree = ET.parse(WORLD_PATH)
    root = tree.getroot()
    assert root.tag == "sdf", f"Expected root tag <sdf>, got <{root.tag}>"
    world = root.find("world")
    assert world is not None, "World tag <world> missing from mine_world.sdf"
    assert world.get("name") in ["subterranean_mine", "mine_world"], f"Unexpected world name: {world.get('name')}"

    # Verify essential physics and scene tags
    physics = world.find("physics")
    assert physics is not None, "Physics element missing from world"
    max_step = physics.find("max_step_size")
    assert max_step is not None and float(max_step.text) == 0.001, "Expected 0.001 max step size"

    scene = world.find("scene")
    assert scene is not None, "Scene element missing from world"
    ambient = scene.find("ambient")
    assert ambient is not None, "Ambient lighting missing from scene"


def test_all_models_xml_structure():
    """Verify all model.config and model.sdf files parse cleanly as XML."""
    model_dirs = [d for d in MODELS_DIR.iterdir() if d.is_dir()]
    assert len(model_dirs) >= 10, f"Expected at least 10 models, found {len(model_dirs)}"

    for model_dir in model_dirs:
        config_path = model_dir / "model.config"
        sdf_path = model_dir / "model.sdf"

        assert config_path.exists(), f"model.config missing in {model_dir.name}"
        assert sdf_path.exists(), f"model.sdf missing in {model_dir.name}"

        # Parse config
        config_tree = ET.parse(config_path)
        config_root = config_tree.getroot()
        assert config_root.tag == "model", f"Config root must be <model> in {model_dir.name}"
        assert config_root.find("name") is not None, f"<name> missing in {config_path}"
        assert config_root.find("sdf") is not None, f"<sdf> missing in {config_path}"

        # Parse SDF
        sdf_tree = ET.parse(sdf_path)
        sdf_root = sdf_tree.getroot()
        assert sdf_root.tag == "sdf", f"SDF root must be <sdf> in {model_dir.name}"
        model_tag = sdf_root.find("model")
        assert model_tag is not None, f"<model> tag missing in {sdf_path}"

        # Verify links, visual, collision
        links = model_tag.findall("link")
        assert len(links) >= 1, f"Model {model_dir.name} has no <link> elements"
        for link in links:
            visuals = link.findall("visual")
            collisions = link.findall("collision")
            assert len(visuals) >= 1, f"Link {link.get('name')} in {model_dir.name} has no visual"
            assert len(collisions) >= 1, f"Link {link.get('name')} in {model_dir.name} has no collision"


def test_gz_sdf_validation():
    """Verify all models and the mine world pass 'gz sdf -k' check."""
    env = dict(os.environ)
    env["SDF_PATH"] = f"{MODELS_DIR}:{env.get('SDF_PATH', '')}"

    # Check world
    res = subprocess.run(["gz", "sdf", "-k", str(WORLD_PATH)], env=env, capture_output=True, text=True)
    assert res.returncode == 0, f"gz sdf -k failed on {WORLD_PATH}:\n{res.stderr}\n{res.stdout}"

    # Check each model
    for model_dir in MODELS_DIR.iterdir():
        if model_dir.is_dir() and (model_dir / "model.sdf").exists():
            sdf_file = model_dir / "model.sdf"
            m_res = subprocess.run(["gz", "sdf", "-k", str(sdf_file)], env=env, capture_output=True, text=True)
            assert m_res.returncode == 0, f"gz sdf -k failed on {sdf_file}:\n{m_res.stderr}\n{m_res.stdout}"
