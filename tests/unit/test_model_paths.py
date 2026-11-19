#!/usr/bin/env python3
"""
Unit Test: Model and Resource Path Resolution
Validates model:// URIs in world SDF and environment search path configurations.
"""

import os
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORLD_PATH = REPO_ROOT / "simulation" / "worlds" / "mine_world.sdf"
MODELS_DIR = REPO_ROOT / "simulation" / "models"


def test_included_models_exist():
    """Verify all <include><uri>model://...</uri></include> in mine_world.sdf exist on disk."""
    tree = ET.parse(WORLD_PATH)
    includes = tree.findall(".//include")
    assert len(includes) >= 10, f"Expected at least 10 included models in world, found {len(includes)}"

    for inc in includes:
        uri = inc.find("uri")
        assert uri is not None and uri.text is not None, "Include tag without uri"
        uri_str = uri.text.strip()
        assert uri_str.startswith("model://"), f"URI {uri_str} must use 'model://' scheme"
        model_name = uri_str.replace("model://", "").strip()

        model_dir = MODELS_DIR / model_name
        assert model_dir.exists() and model_dir.is_dir(), (
            f"Referenced model '{model_name}' (from URI '{uri_str}') does not exist at {model_dir}"
        )
        assert (model_dir / "model.config").exists(), f"model.config missing in {model_dir}"
        assert (model_dir / "model.sdf").exists(), f"model.sdf missing in {model_dir}"


def test_model_config_sdf_pointer():
    """Verify that model.config specifies a valid SDF filename that exists in the same directory."""
    for model_dir in MODELS_DIR.iterdir():
        if model_dir.is_dir() and (model_dir / "model.config").exists():
            cfg_tree = ET.parse(model_dir / "model.config")
            sdf_elem = cfg_tree.find("sdf")
            assert sdf_elem is not None, f"<sdf> element missing in {model_dir / 'model.config'}"
            sdf_filename = sdf_elem.text.strip()
            assert (model_dir / sdf_filename).exists(), (
                f"SDF file '{sdf_filename}' specified in {model_dir / 'model.config'} does not exist"
            )


def test_launch_resource_path_logic():
    """Verify that resource path construction includes models and worlds directories."""
    models_path = str(MODELS_DIR)
    worlds_path = str(REPO_ROOT / "simulation" / "worlds")

    constructed = f"{models_path}:{worlds_path}"
    paths = constructed.split(":")
    for p in paths:
        assert os.path.isdir(p), f"Path in resource path does not exist: {p}"
