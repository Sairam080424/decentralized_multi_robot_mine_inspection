#!/usr/bin/env python3
"""
Procedural Underground Mine Tunnel Generator
Generates modular SDFormat (SDF) 1.9/1.10 compatible models and world fragments
for subterranean mine inspection simulation in Gazebo Sim.

Supports:
- Configurable tunnel width, height, segment length, wall thickness
- Straight tunnel segments, 90-degree turns, T-junctions, and inclined ramps
- Arched/horseshoe, rectangular, and trapezoidal cross-section profiles
- Repeatable generation via deterministic random seed for rock wall irregularity
- Output as standalone modular SDF models or composite world layouts
"""

import argparse
import math
import os
import random
import sys
import yaml
from pathlib import Path


class TunnelGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)

    @staticmethod
    def _xml_header() -> str:
        return '<?xml version="1.0" ?>\n'

    @staticmethod
    def _model_config(name: str, description: str) -> str:
        return f"""<?xml version="1.0"?>
<model>
  <name>{name}</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>Decentralized Multi-Robot Mine Inspection Platform</name>
    <email>dev@example.internal</email>
  </author>
  <description>{description}</description>
</model>
"""

    def generate_straight_segment(
        self,
        name: str = "tunnel_straight_10m",
        length: float = 10.0,
        width: float = 3.5,
        height: float = 3.0,
        profile: str = "arched",
        roughness: float = 0.08,
        wall_thickness: float = 0.4,
        num_subdivisions: int = 5,
    ) -> str:
        """
        Generates a straight tunnel segment with irregular rock walls and floor.
        """
        random.seed(self.seed)
        sub_len = length / num_subdivisions
        half_w = width / 2.0
        half_h = height / 2.0

        links_xml = []

        # Floor link
        links_xml.append(f"""
    <!-- Floor Section -->
    <link name="floor">
      <pose>0 0 -0.05 0 0 0</pose>
      <collision name="floor_collision">
        <geometry>
          <box>
            <size>{length:.3f} {width + 2 * wall_thickness:.3f} 0.1</size>
          </box>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>0.85</mu>
              <mu2>0.75</mu2>
            </ode>
          </friction>
        </surface>
      </collision>
      <visual name="floor_visual">
        <geometry>
          <box>
            <size>{length:.3f} {width + 2 * wall_thickness:.3f} 0.1</size>
          </box>
        </geometry>
        <material>
          <ambient>0.2 0.18 0.17 1.0</ambient>
          <diffuse>0.28 0.25 0.23 1.0</diffuse>
          <specular>0.05 0.05 0.05 1.0</specular>
        </material>
      </visual>
    </link>""")

        # Subdivided irregular rock walls
        for i in range(num_subdivisions):
            x_pos = -length / 2.0 + (i + 0.5) * sub_len
            
            # Left wall irregularity
            offset_left = (random.random() - 0.5) * 2.0 * roughness
            yaw_left = (random.random() - 0.5) * 0.06
            y_left = half_w + wall_thickness / 2.0 + offset_left

            # Right wall irregularity
            offset_right = (random.random() - 0.5) * 2.0 * roughness
            yaw_right = (random.random() - 0.5) * 0.06
            y_right = -half_w - wall_thickness / 2.0 + offset_right

            links_xml.append(f"""
    <!-- Left Wall Sub-block {i} -->
    <link name="left_wall_{i}">
      <pose>{x_pos:.3f} {y_left:.3f} {half_h:.3f} 0 0 {yaw_left:.3f}</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{sub_len * 1.02:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{sub_len * 1.02:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
          <specular>0.02 0.02 0.02 1.0</specular>
        </material>
      </visual>
    </link>

    <!-- Right Wall Sub-block {i} -->
    <link name="right_wall_{i}">
      <pose>{x_pos:.3f} {y_right:.3f} {half_h:.3f} 0 0 {yaw_right:.3f}</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{sub_len * 1.02:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{sub_len * 1.02:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
          <specular>0.02 0.02 0.02 1.0</specular>
        </material>
      </visual>
    </link>""")

        # Ceiling construction based on profile
        if profile == "arched":
            # Three-facet arch approximation
            arch_rise = 0.5
            roof_w = (width + 2 * wall_thickness) / 3.0
            
            # Left roof facet
            links_xml.append(f"""
    <!-- Arched Roof Facets -->
    <link name="roof_center">
      <pose>0 0 {height + arch_rise / 2.0:.3f} 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{length:.3f} {roof_w:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{length:.3f} {roof_w:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.15 0.14 0.13 1.0</ambient>
          <diffuse>0.20 0.18 0.17 1.0</diffuse>
        </material>
      </visual>
    </link>
    <link name="roof_left">
      <pose>0 {half_w * 0.6:.3f} {height - 0.1:.3f} 0.35 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{length:.3f} {roof_w:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{length:.3f} {roof_w:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.15 0.14 0.13 1.0</ambient>
          <diffuse>0.20 0.18 0.17 1.0</diffuse>
        </material>
      </visual>
    </link>
    <link name="roof_right">
      <pose>0 {-half_w * 0.6:.3f} {height - 0.1:.3f} -0.35 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{length:.3f} {roof_w:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{length:.3f} {roof_w:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.15 0.14 0.13 1.0</ambient>
          <diffuse>0.20 0.18 0.17 1.0</diffuse>
        </material>
      </visual>
    </link>""")
        else:
            # Flat rectangular ceiling
            links_xml.append(f"""
    <!-- Flat Ceiling -->
    <link name="ceiling">
      <pose>0 0 {height + wall_thickness / 2.0:.3f} 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{length:.3f} {width + 2 * wall_thickness:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{length:.3f} {width + 2 * wall_thickness:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.15 0.14 0.13 1.0</ambient>
          <diffuse>0.20 0.18 0.17 1.0</diffuse>
        </material>
      </visual>
    </link>""")

        joined_links = "\n".join(links_xml)
        return f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="{name}">
    <static>true</static>
{joined_links}
  </model>
</sdf>
"""

    def generate_turn_90deg_segment(
        self,
        name: str = "tunnel_turn_90deg",
        radius: float = 6.0,
        width: float = 3.5,
        height: float = 3.0,
        wall_thickness: float = 0.4,
        num_steps: int = 6,
    ) -> str:
        """
        Generates a 90-degree curved tunnel bend using faceted polygonal segments.
        Center of curvature is at (0, radius, 0).
        Entry at (0, 0, 0) facing +X, Exit at (radius, radius, 0) facing +Y.
        """
        links_xml = []
        d_theta = (math.pi / 2.0) / num_steps
        half_w = width / 2.0

        for i in range(num_steps):
            theta = (i + 0.5) * d_theta
            chord_len = 2.0 * radius * math.sin(d_theta / 2.0)

            # Center position of this arc step
            cx = radius * math.sin(theta)
            cy = radius * (1.0 - math.cos(theta))

            # Inner wall radius and position
            r_inner = radius - half_w - wall_thickness / 2.0
            ix = r_inner * math.sin(theta)
            iy = radius - r_inner * math.cos(theta)
            inner_chord = 2.0 * r_inner * math.sin(d_theta / 2.0)

            # Outer wall radius and position
            r_outer = radius + half_w + wall_thickness / 2.0
            ox = r_outer * math.sin(theta)
            oy = radius - r_outer * math.cos(theta)
            outer_chord = 2.0 * r_outer * math.sin(d_theta / 2.0)

            # Floor segment
            links_xml.append(f"""
    <!-- Bend Segment {i} Floor -->
    <link name="bend_floor_{i}">
      <pose>{cx:.3f} {cy:.3f} -0.05 0 0 {theta:.3f}</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{chord_len * 1.05:.3f} {width + 2 * wall_thickness:.3f} 0.1</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{chord_len * 1.05:.3f} {width + 2 * wall_thickness:.3f} 0.1</size>
          </box>
        </geometry>
        <material>
          <ambient>0.2 0.18 0.17 1.0</ambient>
          <diffuse>0.28 0.25 0.23 1.0</diffuse>
        </material>
      </visual>
    </link>

    <!-- Bend Segment {i} Outer Wall -->
    <link name="bend_outer_wall_{i}">
      <pose>{ox:.3f} {oy:.3f} {height / 2.0:.3f} 0 0 {theta:.3f}</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{outer_chord * 1.05:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{outer_chord * 1.05:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
        </material>
      </visual>
    </link>

    <!-- Bend Segment {i} Inner Wall -->
    <link name="bend_inner_wall_{i}">
      <pose>{ix:.3f} {iy:.3f} {height / 2.0:.3f} 0 0 {theta:.3f}</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{inner_chord * 1.05:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{inner_chord * 1.05:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
        </material>
      </visual>
    </link>

    <!-- Bend Segment {i} Ceiling -->
    <link name="bend_ceiling_{i}">
      <pose>{cx:.3f} {cy:.3f} {height + wall_thickness / 2.0:.3f} 0 0 {theta:.3f}</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{chord_len * 1.05:.3f} {width + 2 * wall_thickness:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{chord_len * 1.05:.3f} {width + 2 * wall_thickness:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.15 0.14 0.13 1.0</ambient>
          <diffuse>0.20 0.18 0.17 1.0</diffuse>
        </material>
      </visual>
    </link>""")

        joined_links = "\n".join(links_xml)
        return f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="{name}">
    <static>true</static>
{joined_links}
  </model>
</sdf>
"""

    def generate_t_junction_segment(
        self,
        name: str = "tunnel_t_junction",
        main_length: float = 12.0,
        branch_length: float = 6.0,
        width: float = 3.5,
        height: float = 3.0,
        wall_thickness: float = 0.4,
    ) -> str:
        """
        Generates a 3-way T-junction connecting main tunnel (along X axis)
        with a perpendicular side drift branch extending along +Y.
        """
        half_w = width / 2.0
        half_h = height / 2.0
        branch_wall_x = half_w + wall_thickness / 2.0

        links_xml = [
            # Main Floor
            f"""
    <!-- Main Drift Floor -->
    <link name="main_floor">
      <pose>0 0 -0.05 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{main_length:.3f} {width + 2 * wall_thickness:.3f} 0.1</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{main_length:.3f} {width + 2 * wall_thickness:.3f} 0.1</size>
          </box>
        </geometry>
        <material>
          <ambient>0.2 0.18 0.17 1.0</ambient>
          <diffuse>0.28 0.25 0.23 1.0</diffuse>
        </material>
      </visual>
    </link>""",
            # Branch Floor
            f"""
    <!-- Branch Drift Floor -->
    <link name="branch_floor">
      <pose>0 {half_w + branch_length / 2.0:.3f} -0.05 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{width + 2 * wall_thickness:.3f} {branch_length:.3f} 0.1</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{width + 2 * wall_thickness:.3f} {branch_length:.3f} 0.1</size>
          </box>
        </geometry>
        <material>
          <ambient>0.2 0.18 0.17 1.0</ambient>
          <diffuse>0.28 0.25 0.23 1.0</diffuse>
        </material>
      </visual>
    </link>""",
            # Main South Wall (unbroken wall at -Y)
            f"""
    <!-- South Unbroken Wall -->
    <link name="south_wall">
      <pose>0 {-half_w - wall_thickness / 2.0:.3f} {half_h:.3f} 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{main_length:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{main_length:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
        </material>
      </visual>
    </link>""",
            # Main North Wall (West piece before branch opening)
            f"""
    <!-- North Wall West Segment -->
    <link name="north_wall_west">
      <pose>{-(main_length / 4.0 + half_w / 2.0):.3f} {half_w + wall_thickness / 2.0:.3f} {half_h:.3f} 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{main_length / 2.0 - half_w:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{main_length / 2.0 - half_w:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
        </material>
      </visual>
    </link>""",
            # Main North Wall (East piece after branch opening)
            f"""
    <!-- North Wall East Segment -->
    <link name="north_wall_east">
      <pose>{main_length / 4.0 + half_w / 2.0:.3f} {half_w + wall_thickness / 2.0:.3f} {half_h:.3f} 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{main_length / 2.0 - half_w:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{main_length / 2.0 - half_w:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
        </material>
      </visual>
    </link>""",
            # Branch West Wall
            f"""
    <!-- Branch West Wall -->
    <link name="branch_west_wall">
      <pose>{-branch_wall_x:.3f} {half_w + branch_length / 2.0:.3f} {half_h:.3f} 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{wall_thickness:.3f} {branch_length:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{wall_thickness:.3f} {branch_length:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
        </material>
      </visual>
    </link>""",
            # Branch East Wall
            f"""
    <!-- Branch East Wall -->
    <link name="branch_east_wall">
      <pose>{branch_wall_x:.3f} {half_w + branch_length / 2.0:.3f} {half_h:.3f} 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{wall_thickness:.3f} {branch_length:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{wall_thickness:.3f} {branch_length:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
        </material>
      </visual>
    </link>""",
            # Ceilings
            f"""
    <!-- Main Ceiling -->
    <link name="main_ceiling">
      <pose>0 0 {height + wall_thickness / 2.0:.3f} 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{main_length:.3f} {width + 2 * wall_thickness:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{main_length:.3f} {width + 2 * wall_thickness:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.15 0.14 0.13 1.0</ambient>
          <diffuse>0.20 0.18 0.17 1.0</diffuse>
        </material>
      </visual>
    </link>
    <!-- Branch Ceiling -->
    <link name="branch_ceiling">
      <pose>0 {half_w + branch_length / 2.0:.3f} {height + wall_thickness / 2.0:.3f} 0 0 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{width + 2 * wall_thickness:.3f} {branch_length:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{width + 2 * wall_thickness:.3f} {branch_length:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.15 0.14 0.13 1.0</ambient>
          <diffuse>0.20 0.18 0.17 1.0</diffuse>
        </material>
      </visual>
    </link>""",
        ]

        joined_links = "\n".join(links_xml)
        return f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="{name}">
    <static>true</static>
{joined_links}
  </model>
</sdf>
"""

    def generate_ramp_segment(
        self,
        name: str = "tunnel_ramp_15deg",
        run_length: float = 12.0,
        incline_deg: float = 15.0,
        width: float = 3.5,
        height: float = 3.0,
        wall_thickness: float = 0.4,
    ) -> str:
        """
        Generates an inclined tunnel ramp section.
        incline_deg: slope angle in degrees (e.g. 15.0 degrees).
        """
        rad = math.radians(incline_deg)
        rise = run_length * math.tan(rad)
        slope_len = math.sqrt(run_length**2 + rise**2)
        half_w = width / 2.0
        pitch = -rad  # Pitch rotation about Y-axis

        center_x = run_length / 2.0
        center_z = rise / 2.0

        return f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="{name}">
    <static>true</static>

    <!-- Inclined Ramp Floor -->
    <link name="ramp_floor">
      <pose>{center_x:.3f} 0 {center_z - 0.05 * math.cos(rad):.3f} 0 {pitch:.4f} 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{slope_len:.3f} {width + 2 * wall_thickness:.3f} 0.1</size>
          </box>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>0.9</mu>
              <mu2>0.85</mu2>
            </ode>
          </friction>
        </surface>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{slope_len:.3f} {width + 2 * wall_thickness:.3f} 0.1</size>
          </box>
        </geometry>
        <material>
          <ambient>0.22 0.20 0.18 1.0</ambient>
          <diffuse>0.29 0.26 0.24 1.0</diffuse>
        </material>
      </visual>
    </link>

    <!-- Ramp Left Wall -->
    <link name="ramp_left_wall">
      <pose>{center_x:.3f} {half_w + wall_thickness / 2.0:.3f} {center_z + height / 2.0:.3f} 0 {pitch:.4f} 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{slope_len:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{slope_len:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
        </material>
      </visual>
    </link>

    <!-- Ramp Right Wall -->
    <link name="ramp_right_wall">
      <pose>{center_x:.3f} {-half_w - wall_thickness / 2.0:.3f} {center_z + height / 2.0:.3f} 0 {pitch:.4f} 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{slope_len:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{slope_len:.3f} {wall_thickness:.3f} {height:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.18 0.16 0.15 1.0</ambient>
          <diffuse>0.22 0.20 0.19 1.0</diffuse>
        </material>
      </visual>
    </link>

    <!-- Ramp Ceiling -->
    <link name="ramp_ceiling">
      <pose>{center_x:.3f} 0 {center_z + height + wall_thickness / 2.0:.3f} 0 {pitch:.4f} 0</pose>
      <collision name="col">
        <geometry>
          <box>
            <size>{slope_len:.3f} {width + 2 * wall_thickness:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
      </collision>
      <visual name="vis">
        <geometry>
          <box>
            <size>{slope_len:.3f} {width + 2 * wall_thickness:.3f} {wall_thickness:.3f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.15 0.14 0.13 1.0</ambient>
          <diffuse>0.20 0.18 0.17 1.0</diffuse>
        </material>
      </visual>
    </link>
  </model>
</sdf>
"""

    def export_model(self, model_dir: Path, name: str, description: str, sdf_content: str):
        """Saves model.config and model.sdf into target directory."""
        model_dir.mkdir(parents=True, exist_ok=True)
        config_path = model_dir / "model.config"
        sdf_path = model_dir / "model.sdf"

        config_path.write_text(self._model_config(name, description), encoding="utf-8")
        sdf_path.write_text(sdf_content, encoding="utf-8")
        print(f"Exported model [{name}] -> {model_dir}")


def build_default_models(output_base_dir: Path, seed: int = 42):
    """Builds standard set of modular tunnel models."""
    gen = TunnelGenerator(seed=seed)
    
    # 1. Straight 10m Arched Tunnel
    straight_sdf = gen.generate_straight_segment(
        name="tunnel_straight_10m",
        length=10.0,
        width=3.5,
        height=3.0,
        profile="arched",
        roughness=0.08,
    )
    gen.export_model(
        output_base_dir / "tunnel_straight_10m",
        "tunnel_straight_10m",
        "Modular 10m straight underground mine drift with arched roof",
        straight_sdf,
    )

    # 2. 90-degree Curved Turn
    turn_sdf = gen.generate_turn_90deg_segment(
        name="tunnel_turn_90deg",
        radius=6.0,
        width=3.5,
        height=3.0,
    )
    gen.export_model(
        output_base_dir / "tunnel_turn_90deg",
        "tunnel_turn_90deg",
        "Modular 90-degree curved underground mine tunnel bend",
        turn_sdf,
    )

    # 3. 3-Way T-Junction
    t_junct_sdf = gen.generate_t_junction_segment(
        name="tunnel_t_junction",
        main_length=12.0,
        branch_length=6.0,
        width=3.5,
        height=3.0,
    )
    gen.export_model(
        output_base_dir / "tunnel_t_junction",
        "tunnel_t_junction",
        "Modular 3-way T-junction subterranean drift intersection",
        t_junct_sdf,
    )

    # 4. Inclined Ramp (15-degree test incline)
    ramp_sdf = gen.generate_ramp_segment(
        name="tunnel_ramp_15deg",
        run_length=12.0,
        incline_deg=15.0,
        width=3.5,
        height=3.0,
    )
    gen.export_model(
        output_base_dir / "tunnel_ramp_15deg",
        "tunnel_ramp_15deg",
        "Modular 15-degree inclined underground mine tunnel ramp",
        ramp_sdf,
    )


def main():
    parser = argparse.ArgumentParser(description="Procedural Subterranean Tunnel Generator for Gazebo Sim")
    parser.add_argument("--config", type=str, help="Path to YAML tunnel configuration file")
    parser.add_argument("--output-dir", type=str, default="simulation/models", help="Output directory for generated models")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for procedural wall irregularity")
    parser.add_argument("--generate-defaults", action="store_true", help="Generate default modular tunnel segment models")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    out_dir = (repo_root / args.output_dir).resolve()

    if args.config:
        cfg_path = Path(args.config).resolve()
        if not cfg_path.exists():
            print(f"Error: Config file not found: {cfg_path}", file=sys.stderr)
            sys.exit(1)
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        seed = cfg.get("seed", args.seed)
        gen = TunnelGenerator(seed=seed)
        models_cfg = cfg.get("models", [])
        for m in models_cfg:
            m_type = m.get("type", "straight")
            m_name = m.get("name", "custom_tunnel")
            if m_type == "straight":
                sdf = gen.generate_straight_segment(
                    name=m_name,
                    length=m.get("length", 10.0),
                    width=m.get("width", 3.5),
                    height=m.get("height", 3.0),
                    profile=m.get("profile", "arched"),
                    roughness=m.get("roughness", 0.08),
                )
            elif m_type == "turn_90deg":
                sdf = gen.generate_turn_90deg_segment(
                    name=m_name,
                    radius=m.get("radius", 6.0),
                    width=m.get("width", 3.5),
                    height=m.get("height", 3.0),
                )
            elif m_type == "t_junction":
                sdf = gen.generate_t_junction_segment(
                    name=m_name,
                    main_length=m.get("main_length", 12.0),
                    branch_length=m.get("branch_length", 6.0),
                    width=m.get("width", 3.5),
                    height=m.get("height", 3.0),
                )
            elif m_type == "ramp":
                sdf = gen.generate_ramp_segment(
                    name=m_name,
                    run_length=m.get("run_length", 12.0),
                    incline_deg=m.get("incline_deg", 15.0),
                    width=m.get("width", 3.5),
                    height=m.get("height", 3.0),
                )
            else:
                print(f"Warning: Unknown segment type '{m_type}', skipping.", file=sys.stderr)
                continue
            gen.export_model(out_dir / m_name, m_name, f"Procedural {m_type} tunnel model", sdf)
        print(f"Successfully generated {len(models_cfg)} models from config.")
    elif args.generate_defaults or True:
        print(f"Generating default modular tunnel models into {out_dir}...")
        build_default_models(out_dir, seed=args.seed)
        print("Default models generated successfully.")


if __name__ == "__main__":
    main()
