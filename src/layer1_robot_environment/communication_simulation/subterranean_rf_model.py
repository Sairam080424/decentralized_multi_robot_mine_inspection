"""
Subterranean Radio-Frequency (RF) Attenuation & Communication Model
Milestone M1: Underground Mine Simulation (TASK-M1-005)

Analytical, geometry-based subterranean RF propagation model:
- Evaluates line-of-sight via robust 2D/3D ray-casting against rock walls and obstacles.
- Computes waveguide path distance and tunnel bend/corner diffraction using
  a configurable, graph-based TunnelTopology representation (supporting arbitrary mine layouts).
- Employs 3D slab ray-versus-AABB intersection for physical obstacles.
- Computes distance-dependent path loss, corner diffraction, obstacle shadowing,
  packet loss via sigmoid link margin, jittered latency, and bandwidth shaping.
- Configurable dynamically from YAML (config/simulation/rf_attenuation_config.yaml).
"""

import math
import random
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union
import yaml


class TunnelTopology:
    """
    Graph-based topological representation of subterranean mine corridors and junctions.
    Supports arbitrary mine layouts (straight tunnels, turns, T-junctions, ramps, grids).
    Computes navigable waveguide path distance and counts tunnel bends (>= 45 degrees).
    """

    def __init__(self):
        # Nodes: {node_id: (x, y, z)}
        self.nodes: Dict[str, Tuple[float, float, float]] = {}
        # Edges: {node_id: [(neighbor_id, length, corridor_name)]}
        self.adj: Dict[str, List[Tuple[str, float, str]]] = {}
        # Corridors: [(name, (x1, y1, z1), (x2, y2, z2), half_width, half_height)]
        self.corridors: List[Tuple[str, Tuple[float, float, float], Tuple[float, float, float], float, float]] = []

    def add_node(self, node_id: str, pos: Tuple[float, float, float]):
        """Register a topological node (junction, portal, waypoint, or dead-end)."""
        self.nodes[node_id] = (float(pos[0]), float(pos[1]), float(pos[2]))
        if node_id not in self.adj:
            self.adj[node_id] = []

    def add_edge(self, u: str, v: str, corridor_name: str, width: float = 3.5, height: float = 3.0):
        """Add bidirectional navigable tunnel edge between node u and node v."""
        pos_u = self.nodes[u]
        pos_v = self.nodes[v]
        dx = pos_u[0] - pos_v[0]
        dy = pos_u[1] - pos_v[1]
        dz = pos_u[2] - pos_v[2]
        length = math.sqrt(dx * dx + dy * dy + dz * dz)

        self.adj[u].append((v, length, corridor_name))
        self.adj[v].append((u, length, corridor_name))

        self.corridors.append(
            (corridor_name, pos_u, pos_v, width / 2.0, height / 2.0)
        )

    def is_point_in_corridor(self, pt: Tuple[float, float, float], margin: float = 0.5) -> bool:
        """Check if 3D point lies within navigable volume of any defined corridor."""
        px, py, pz = pt
        if not self.corridors:
            return True

        # Vertical envelope across defined topology corridors
        all_z = [z for _, (x1, y1, z1), (x2, y2, z2), _, _ in self.corridors for z in (z1, z2)]
        all_h = [hh * 2.0 for _, _, _, _, hh in self.corridors]
        min_z = min(all_z) - 1.0
        max_z = max(all_z) + max(all_h) + 1.0

        if not (min_z <= pz <= max_z):
            return False

        for _, (x1, y1, z1), (x2, y2, z2), hw, _ in self.corridors:
            vx = x2 - x1
            vy = y2 - y1
            seg_len_sq = vx * vx + vy * vy
            if seg_len_sq < 1e-9:
                d = math.sqrt((px - x1)**2 + (py - y1)**2)
                if d <= hw + margin:
                    return True
                continue

            t = max(0.0, min(1.0, ((px - x1) * vx + (py - y1) * vy) / seg_len_sq))
            proj_x = x1 + t * vx
            proj_y = y1 + t * vy

            dx = px - proj_x
            dy = py - proj_y
            dist_2d = math.sqrt(dx * dx + dy * dy)

            if dist_2d <= hw + margin:
                return True

        return False

    def find_nearest_edge_projection(
        self, pos: Tuple[float, float, float]
    ) -> Tuple[Optional[Tuple[str, str]], float, Tuple[float, float, float], float]:
        """
        Finds the corridor edge whose 3D segment is closest to `pos`.
        Returns:
            ((u, v), t_param, projection_pt, perp_dist)
        """
        best_edge = None
        best_t = 0.0
        best_proj = pos
        best_dist = float("inf")

        px, py, pz = pos

        for u, v_list in self.adj.items():
            ux, uy, uz = self.nodes[u]
            for v, length, _ in v_list:
                if u > v:
                    continue
                vx, vy, vz = self.nodes[v]
                dx = vx - ux
                dy = vy - uy
                dz = vz - uz
                seg_len_sq = dx * dx + dy * dy + dz * dz
                if seg_len_sq < 1e-9:
                    continue

                t = ((px - ux) * dx + (py - uy) * dy + (pz - uz) * dz) / seg_len_sq
                t_clamped = max(0.0, min(1.0, t))

                proj_x = ux + t_clamped * dx
                proj_y = uy + t_clamped * dy
                proj_z = uz + t_clamped * dz

                dist = math.sqrt((px - proj_x)**2 + (py - proj_y)**2 + (pz - proj_z)**2)
                if dist < best_dist:
                    best_dist = dist
                    best_edge = (u, v)
                    best_t = t_clamped
                    best_proj = (proj_x, proj_y, proj_z)

        return best_edge, best_t, best_proj, best_dist

    def shortest_path(
        self, start_pos: Tuple[float, float, float], end_pos: Tuple[float, float, float]
    ) -> Tuple[float, int, List[str]]:
        """
        Calculates waveguide path distance and counts tunnel bends (>= 45 degrees)
        through the topological tunnel network.
        Returns:
            (total_path_distance, corner_count, node_sequence)
        """
        edge_a, t_a, proj_a, d_perp_a = self.find_nearest_edge_projection(start_pos)
        edge_b, t_b, proj_b, d_perp_b = self.find_nearest_edge_projection(end_pos)

        # Case 1: Both points project onto the same tunnel edge
        if edge_a is not None and edge_b is not None and edge_a == edge_b:
            u, v = edge_a
            ux, uy, uz = self.nodes[u]
            vx, vy, vz = self.nodes[v]
            edge_len = math.sqrt((vx - ux)**2 + (vy - uy)**2 + (vz - uz)**2)
            seg_dist = abs(t_a - t_b) * edge_len
            total_dist = d_perp_a + seg_dist + d_perp_b
            return total_dist, 0, [u, v]

        # Dijkstra helper on graph
        import heapq

        def dijkstra_between(src: str, dst: str) -> Tuple[float, List[str]]:
            dist = {n: float("inf") for n in self.nodes}
            prev = {n: None for n in self.nodes}
            dist[src] = 0.0
            visited: Set[str] = set()
            pq = [(0.0, src)]

            while pq:
                cur_d, u = heapq.heappop(pq)
                if u in visited:
                    continue
                visited.add(u)
                if u == dst:
                    break
                for v, length, _ in self.adj[u]:
                    if v not in visited:
                        new_d = cur_d + length
                        if new_d < dist[v]:
                            dist[v] = new_d
                            prev[v] = u
                            heapq.heappush(pq, (new_d, v))

            path = []
            curr = dst
            while curr is not None:
                path.append(curr)
                curr = prev[curr]
            path.reverse()
            if not path or path[0] != src:
                return float("inf"), []
            return dist[dst], path

        # Determine entry nodes from edge_a and exit nodes to edge_b
        candidate_entries = list(edge_a) if edge_a else list(self.nodes.keys())[:1]
        candidate_exits = list(edge_b) if edge_b else list(self.nodes.keys())[:1]

        best_total_dist = float("inf")
        best_full_nodes: List[str] = []

        for n_in in candidate_entries:
            pos_in = self.nodes[n_in]
            d_start_to_in = math.sqrt(
                (start_pos[0] - pos_in[0])**2 + (start_pos[1] - pos_in[1])**2 + (start_pos[2] - pos_in[2])**2
            )
            for n_out in candidate_exits:
                pos_out = self.nodes[n_out]
                d_out_to_end = math.sqrt(
                    (end_pos[0] - pos_out[0])**2 + (end_pos[1] - pos_out[1])**2 + (end_pos[2] - pos_out[2])**2
                )
                g_dist, g_nodes = dijkstra_between(n_in, n_out)
                cand_total = d_start_to_in + g_dist + d_out_to_end
                if cand_total < best_total_dist:
                    best_total_dist = cand_total
                    best_full_nodes = g_nodes

        if not best_full_nodes or math.isinf(best_total_dist):
            euclid = math.sqrt(
                (start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2 + (start_pos[2] - end_pos[2])**2
            )
            return euclid, 0, []

        # Construct waypoint sequence to evaluate angles
        waypoints: List[Tuple[float, float, float]] = [start_pos]
        for nid in best_full_nodes:
            pt = self.nodes[nid]
            waypoints.append(pt)
        waypoints.append(end_pos)

        # Collapse consecutive points that have negligible horizontal distance (< 0.2m)
        collapsed_wps: List[Tuple[float, float, float]] = [waypoints[0]]
        for pt in waypoints[1:]:
            d_xy = math.sqrt((pt[0] - collapsed_wps[-1][0])**2 + (pt[1] - collapsed_wps[-1][1])**2)
            if d_xy > 0.2:
                collapsed_wps.append(pt)

        # Count tunnel bends (>= 45 degrees) along horizontal corridor headings
        corners = 0
        for i in range(1, len(collapsed_wps) - 1):
            p_prev = collapsed_wps[i - 1]
            p_curr = collapsed_wps[i]
            p_next = collapsed_wps[i + 1]

            v1 = (p_curr[0] - p_prev[0], p_curr[1] - p_prev[1])
            v2 = (p_next[0] - p_curr[0], p_next[1] - p_curr[1])

            len1 = math.sqrt(v1[0]**2 + v1[1]**2)
            len2 = math.sqrt(v2[0]**2 + v2[1]**2)

            if len1 > 0.2 and len2 > 0.2:
                dot = (v1[0]*v2[0] + v1[1]*v2[1]) / (len1 * len2)
                dot = max(-1.0, min(1.0, dot))
                angle_deg = math.degrees(math.acos(dot))
                if angle_deg >= 45.0:
                    corners += 1

        return best_total_dist, corners, best_full_nodes

    @classmethod
    def create_canonical_mine_world_topology(cls) -> "TunnelTopology":
        """Builds default topological network corresponding to mine_world.sdf."""
        topo = cls()
        # Nodes along Main Drift & Incline Ramp
        topo.add_node("portal", (0.0, 0.0, 0.0))
        topo.add_node("drift_sec_a", (10.0, 0.0, 0.0))
        topo.add_node("drift_sec_b", (20.0, 0.0, 0.0))
        topo.add_node("t_junction", (30.0, 0.0, 0.0))
        topo.add_node("drift_sec_d", (42.0, 0.0, 0.0))
        topo.add_node("ramp_crest", (54.0, 0.0, 3.215))
        topo.add_node("upper_drift_end", (68.0, 0.0, 3.215))

        # Nodes along North Crosscut & East Drift
        topo.add_node("crosscut_mid", (30.0, 10.0, 0.0))
        topo.add_node("crosscut_turn", (30.0, 20.0, 0.0))
        topo.add_node("east_drift_entry", (36.0, 23.0, 0.0))
        topo.add_node("east_drift_mid", (45.0, 23.0, 0.0))
        topo.add_node("east_drift_end", (56.0, 23.0, 0.0))

        # Edges (Main Drift & Ramp)
        topo.add_edge("portal", "drift_sec_a", "main_drift_portal")
        topo.add_edge("drift_sec_a", "drift_sec_b", "main_drift_mid")
        topo.add_edge("drift_sec_b", "t_junction", "main_drift_approach")
        topo.add_edge("t_junction", "drift_sec_d", "main_drift_east")
        topo.add_edge("drift_sec_d", "ramp_crest", "tunnel_ramp_15deg")
        topo.add_edge("ramp_crest", "upper_drift_end", "upper_drift")

        # Edges (Crosscut & East Drift)
        topo.add_edge("t_junction", "crosscut_mid", "crosscut_drift_lower")
        topo.add_edge("crosscut_mid", "crosscut_turn", "crosscut_drift_upper")
        topo.add_edge("crosscut_turn", "east_drift_entry", "crosscut_turn_90deg")
        topo.add_edge("east_drift_entry", "east_drift_mid", "east_drift_extension")
        topo.add_edge("east_drift_mid", "east_drift_end", "east_drift_face")

        return topo


class SubterraneanRFModel:
    """
    Subterranean RF propagation model for underground tunnels.
    Evaluates line-of-sight via exact 2D/3D geometric intersection,
    waveguide distance and bend attenuation via configurable TunnelTopology,
    and applies physical obstacle shadowing and packet loss modeling.
    """

    def __init__(
        self,
        tx_power_dbm: float = 20.0,
        rx_sensitivity_dbm: float = -95.0,
        path_loss_exponent: float = 2.4,
        reference_distance_m: float = 1.0,
        reference_loss_db: float = 40.0,
        corner_diffraction_loss_db: float = 18.0,
        corner_attenuation_db: Optional[float] = None,
        obstacle_shadow_loss_db: float = 12.0,
        los_cutoff_distance_m: float = 60.0,
        nlos_corner_limit: int = 2,
        base_latency_ms: float = 8.0,
        max_jitter_ms: float = 12.0,
        bandwidth_limit_kbps: float = 250.0,
        forced_blackout: bool = False,
        random_seed: Optional[int] = 42,
        topology: Optional[TunnelTopology] = None,
        wall_segments: Optional[List[Tuple[Tuple[float, float], Tuple[float, float]]]] = None,
        obstacles_3d: Optional[List[Tuple[str, Tuple[float, float, float, float, float, float]]]] = None,
    ):
        self.tx_power_dbm = tx_power_dbm
        self.rx_sensitivity_dbm = rx_sensitivity_dbm
        self.path_loss_exponent = path_loss_exponent
        self.reference_distance_m = reference_distance_m
        self.reference_loss_db = reference_loss_db
        self.corner_diffraction_loss_db = (
            corner_attenuation_db if corner_attenuation_db is not None else corner_diffraction_loss_db
        )
        self.corner_attenuation_db = self.corner_diffraction_loss_db  # backwards compatibility alias
        self.obstacle_shadow_loss_db = obstacle_shadow_loss_db
        self.los_cutoff_distance_m = los_cutoff_distance_m
        self.nlos_corner_limit = nlos_corner_limit
        self.base_latency_ms = base_latency_ms
        self.max_jitter_ms = max_jitter_ms
        self.bandwidth_limit_kbps = bandwidth_limit_kbps
        self.forced_blackout = forced_blackout

        if random_seed is not None:
            random.seed(random_seed)

        # Topology graph
        self.topology = topology if topology is not None else TunnelTopology.create_canonical_mine_world_topology()

        # Build or assign rock wall segments and obstacle bounding volumes
        if wall_segments is not None:
            self.wall_segments = list(wall_segments)
        else:
            self.wall_segments = []

        if obstacles_3d is not None:
            self.obstacles_3d = list(obstacles_3d)
        else:
            self.obstacles_3d = []

        if wall_segments is None and obstacles_3d is None and topology is None:
            self._init_mine_geometry()

    @classmethod
    def from_yaml(
        cls,
        yaml_path: Union[str, Path],
        random_seed: Optional[int] = 42,
        topology: Optional[TunnelTopology] = None,
    ) -> "SubterraneanRFModel":
        """Construct model dynamically from a YAML configuration file."""
        cfg_path = Path(yaml_path).resolve()
        if not cfg_path.exists():
            raise FileNotFoundError(f"RF config file not found: {cfg_path}")

        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

        radio = cfg.get("radio_parameters", {})
        atten = cfg.get("underground_attenuation", {})
        net = cfg.get("network_shaping", {})
        fault = cfg.get("fault_injection", {})

        return cls(
            tx_power_dbm=float(radio.get("tx_power_dbm", 20.0)),
            rx_sensitivity_dbm=float(radio.get("rx_sensitivity_dbm", -95.0)),
            path_loss_exponent=float(radio.get("path_loss_exponent", 2.4)),
            reference_distance_m=float(radio.get("reference_distance_m", 1.0)),
            reference_loss_db=float(radio.get("reference_loss_db", 40.0)),
            corner_diffraction_loss_db=float(atten.get("corner_diffraction_loss_db", 18.0)),
            obstacle_shadow_loss_db=float(atten.get("obstacle_shadow_loss_db", 12.0)),
            los_cutoff_distance_m=float(atten.get("los_cutoff_distance_m", 60.0)),
            nlos_corner_limit=int(atten.get("nlos_corner_limit", 2)),
            base_latency_ms=float(net.get("base_latency_ms", 8.0)),
            max_jitter_ms=float(net.get("max_jitter_ms", 12.0)),
            bandwidth_limit_kbps=float(net.get("bandwidth_limit_kbps", 250.0)),
            forced_blackout=bool(fault.get("forced_blackout", False)),
            random_seed=random_seed,
            topology=topology,
        )

    def _init_mine_geometry(self):
        """
        Rock walls and 3D bounding obstacles for canonical mine_world.sdf layout.
        """
        # 2D line segments for solid rock walls: ((x1, y1), (x2, y2))
        self.wall_segments: List[Tuple[Tuple[float, float], Tuple[float, float]]] = [
            # Main drift south wall
            ((-6.0, -1.75), (68.2, -1.75)),
            # Main drift north wall west of T-junction
            ((-6.0, 1.75), (28.25, 1.75)),
            # Main drift north wall east of T-junction
            ((31.75, 1.75), (68.2, 1.75)),
            # Upper drift dead-end rock face
            ((68.2, -1.75), (68.2, 1.75)),
            # Crosscut west wall
            ((28.25, 1.75), (28.25, 24.75)),
            # Crosscut east wall south of east drift opening
            ((31.75, 1.75), (31.75, 21.25)),
            # East drift south wall
            ((31.75, 21.25), (56.0, 21.25)),
            # East drift north wall
            ((28.25, 24.75), (56.0, 24.75)),
            # East drift dead-end rock face
            ((56.0, 21.25), (56.0, 24.75)),
        ]

        # 3D Axis-Aligned Bounding Boxes (AABB) for physical obstacles:
        # (name, (min_x, max_x, min_y, max_y, min_z, max_z))
        self.obstacles_3d: List[Tuple[str, Tuple[float, float, float, float, float, float]]] = [
            ("fallen_rock_pile", (27.25, 29.75, 0.25, 1.45, 0.0, 0.85)),
            ("timber_roof_support", (4.8, 5.2, -1.75, 1.75, 0.0, 2.9)),
            ("mine_debris", (41.0, 43.0, 24.0, 25.4, 0.0, 0.55)),
        ]

    def set_forced_blackout(self, enabled: bool):
        """Forces total communication blackout for fault-injection testing."""
        self.forced_blackout = enabled

    @staticmethod
    def calculate_distance(
        pos_a: Tuple[float, float, float], pos_b: Tuple[float, float, float]
    ) -> float:
        """Euclidean 3D distance between two positions."""
        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]
        dz = pos_a[2] - pos_b[2]
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    @staticmethod
    def _segments_intersect(
        p1: Tuple[float, float], p2: Tuple[float, float],
        q1: Tuple[float, float], q2: Tuple[float, float],
        tol: float = 1e-6
    ) -> bool:
        """
        Robust 2D line segment intersection with defined numerical tolerance.
        Handles proper crossing, collinear overlap, endpoint contact,
        parallel segments, and near-parallel floating point cases.
        """
        # Bounding box pre-check
        min_p_x, max_p_x = min(p1[0], p2[0]), max(p1[0], p2[0])
        min_p_y, max_p_y = min(p1[1], p2[1]), max(p1[1], p2[1])
        min_q_x, max_q_x = min(q1[0], q2[0]), max(q1[0], q2[0])
        min_q_y, max_q_y = min(q1[1], q2[1]), max(q1[1], q2[1])

        if max_p_x < min_q_x - tol or max_q_x < min_p_x - tol:
            return False
        if max_p_y < min_q_y - tol or max_q_y < min_p_y - tol:
            return False

        # 2D cross product: (b - a) x (c - a)
        def cross(a, b, c):
            return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

        cp1 = cross(p1, p2, q1)
        cp2 = cross(p1, p2, q2)
        cp3 = cross(q1, q2, p1)
        cp4 = cross(q1, q2, p2)

        # Collinear checks
        def point_on_segment(pt, seg_a, seg_b):
            px, py = pt
            ax, ay = seg_a
            bx, by = seg_b
            return (
                min(ax, bx) - tol <= px <= max(ax, bx) + tol
                and min(ay, by) - tol <= py <= max(ay, by) + tol
            )

        # Collinear check
        if abs(cp1) <= tol and abs(cp2) <= tol:
            # Segments are collinear; check if intervals overlap
            return (
                point_on_segment(q1, p1, p2)
                or point_on_segment(q2, p1, p2)
                or point_on_segment(p1, q1, q2)
                or point_on_segment(p2, q1, q2)
            )

        # Endpoint contact checks
        if abs(cp1) <= tol and point_on_segment(q1, p1, p2):
            return True
        if abs(cp2) <= tol and point_on_segment(q2, p1, p2):
            return True
        if abs(cp3) <= tol and point_on_segment(p1, q1, q2):
            return True
        if abs(cp4) <= tol and point_on_segment(p2, q1, q2):
            return True

        # Proper crossing check
        return (
            ((cp1 > tol and cp2 < -tol) or (cp1 < -tol and cp2 > tol))
            and ((cp3 > tol and cp4 < -tol) or (cp3 < -tol and cp4 > tol))
        )

    @staticmethod
    def _segment_intersects_aabb_3d(
        p0: Tuple[float, float, float],
        p1: Tuple[float, float, float],
        aabb: Tuple[float, float, float, float, float, float],
        tol: float = 1e-6
    ) -> bool:
        """
        Exact 3D segment vs Axis-Aligned Bounding Box (AABB) intersection using the 3D Slab method.
        aabb: (min_x, max_x, min_y, max_y, min_z, max_z).
        Tests whether the parametric line segment P(t) = p0 + t*(p1 - p0), t in [0, 1]
        intersects the 3D obstacle volume.
        """
        min_x, max_x, min_y, max_y, min_z, max_z = aabb
        x0, y0, z0 = p0
        x1, y1, z1 = p1

        dx = x1 - x0
        dy = y1 - y0
        dz = z1 - z0

        t_min = 0.0
        t_max = 1.0

        for p_start, delta, b_min, b_max in [
            (x0, dx, min_x, max_x),
            (y0, dy, min_y, max_y),
            (z0, dz, min_z, max_z),
        ]:
            if abs(delta) < tol:
                # Segment is parallel to slab; check if starting point is outside
                if p_start < b_min - tol or p_start > b_max + tol:
                    return False
            else:
                t1 = (b_min - p_start) / delta
                t2 = (b_max - p_start) / delta
                if t1 > t2:
                    t1, t2 = t2, t1
                t_min = max(t_min, t1)
                t_max = min(t_max, t2)
                if t_min > t_max + tol:
                    return False

        return t_min <= t_max + tol

    def check_line_of_sight(
        self,
        pos_a: Tuple[float, float, float],
        pos_b: Tuple[float, float, float],
    ) -> Tuple[bool, int, str]:
        """
        Evaluates geometric line-of-sight and corner count.
        Returns:
            (has_los: bool, corner_count: int, classification_reason: str)
        """
        # 1. Containment check within active topology
        if not self.topology.is_point_in_corridor(pos_a) or not self.topology.is_point_in_corridor(pos_b):
            return False, 99, "OUTSIDE_MINE_BOUNDS"

        p1_2d = (pos_a[0], pos_a[1])
        p2_2d = (pos_b[0], pos_b[1])

        # 2. Geometric Ray-Casting against Rock Wall Segments
        wall_intersections = 0
        for w1, w2 in self.wall_segments:
            if self._segments_intersect(p1_2d, p2_2d, w1, w2):
                wall_intersections += 1

        # 3. Geometric 3D Ray-Casting against Physical Obstacles
        obstacle_hit: Optional[str] = None
        for obs_name, aabb in self.obstacles_3d:
            if self._segment_intersects_aabb_3d(pos_a, pos_b, aabb):
                obstacle_hit = obs_name
                break

        # If direct ray is completely clear of walls and obstacles
        if wall_intersections == 0 and obstacle_hit is None:
            return True, 0, "CLEAR_LINE_OF_SIGHT"

        # If direct ray does not intersect rock walls but intersects a 3D obstacle
        if wall_intersections == 0 and obstacle_hit is not None:
            return False, 0, f"BLOCKED_BY_OBSTACLE_{obstacle_hit.upper()}"

        # If direct ray intersects rock walls, determine bend count via topology graph
        _, corner_count, _ = self.topology.shortest_path(pos_a, pos_b)
        # In a wall-blocked situation, ensure at least 1 corner if turning between corridors
        corner_count = max(1, corner_count)

        return False, corner_count, f"BLOCKED_BY_ROCK_WALLS_{wall_intersections}_INTERSECTIONS"

    def evaluate_link(
        self,
        pos_a: Tuple[float, float, float],
        pos_b: Tuple[float, float, float],
    ) -> Dict[str, Union[float, bool, int, str]]:
        """
        Evaluates communication link quality between two coordinates.
        Computes distance, LOS classification, corner count, RSSI,
        packet drop probability, jittered latency, effective bandwidth, and status.
        """
        euclid_dist = max(self.calculate_distance(pos_a, pos_b), 0.1)
        has_los, corner_count, reason = self.check_line_of_sight(pos_a, pos_b)

        # 1. Forced Blackout Test Mode
        if self.forced_blackout:
            return {
                "distance_m": round(euclid_dist, 2),
                "has_line_of_sight": False,
                "corner_count": corner_count,
                "rssi_dbm": -120.0,
                "packet_loss_rate": 1.0,
                "latency_ms": float("inf"),
                "effective_bandwidth_kbps": 0.0,
                "is_connected": False,
                "status": "FORCED_BLACKOUT",
                "classification_reason": reason,
            }

        # 2. Outside Defined Mine Topology
        if reason == "OUTSIDE_MINE_BOUNDS":
            return {
                "distance_m": round(euclid_dist, 2),
                "has_line_of_sight": False,
                "corner_count": corner_count,
                "rssi_dbm": -120.0,
                "packet_loss_rate": 1.0,
                "latency_ms": float("inf"),
                "effective_bandwidth_kbps": 0.0,
                "is_connected": False,
                "status": "OUTSIDE_MINE_BOUNDS",
                "classification_reason": reason,
            }

        # 3. Waveguide Path Distance
        if has_los or "BLOCKED_BY_OBSTACLE" in reason:
            path_dist = euclid_dist
        else:
            topo_dist, _, _ = self.topology.shortest_path(pos_a, pos_b)
            path_dist = max(euclid_dist, topo_dist)

        # 4. Path Loss and Attenuation
        path_loss_db = self.reference_loss_db + 10.0 * self.path_loss_exponent * math.log10(
            path_dist / self.reference_distance_m
        )

        total_attenuation = path_loss_db

        if has_los:
            pass
        elif "BLOCKED_BY_OBSTACLE" in reason:
            total_attenuation += self.obstacle_shadow_loss_db
        else:
            total_attenuation += corner_count * self.corner_diffraction_loss_db

        rssi_dbm = self.tx_power_dbm - total_attenuation

        # 5. Disconnection Thresholds
        is_cutoff = False
        cutoff_status = ""

        if corner_count >= self.nlos_corner_limit:
            is_cutoff = True
            cutoff_status = "EXCEEDED_CORNER_LIMIT"
        elif path_dist > self.los_cutoff_distance_m:
            is_cutoff = True
            cutoff_status = "EXCEEDED_LOS_CUTOFF" if has_los else "EXCEEDED_MAX_RANGE"

        # 6. Packet Loss Sigmoid
        snr_margin = rssi_dbm - self.rx_sensitivity_dbm

        if is_cutoff or snr_margin <= -10.0:
            loss_rate = 1.0
        elif snr_margin >= 20.0:
            loss_rate = 0.005
        else:
            loss_rate = 1.0 / (1.0 + math.exp(0.3 * (snr_margin - 5.0)))

        loss_rate = max(0.0, min(1.0, loss_rate))

        # 7. Connectivity Decision
        is_connected = (loss_rate < 0.90) and (rssi_dbm >= self.rx_sensitivity_dbm) and not is_cutoff

        # 8. Latency and Bandwidth Shaping
        if is_connected:
            jitter = random.uniform(0.0, self.max_jitter_ms)
            latency_ms = self.base_latency_ms + (path_dist * 0.15) + (corner_count * 15.0) + jitter
            effective_bandwidth_kbps = round(self.bandwidth_limit_kbps * (1.0 - loss_rate), 1)
        else:
            latency_ms = float("inf")
            effective_bandwidth_kbps = 0.0

        status = "CONNECTED" if is_connected else (cutoff_status or "DISCONNECTED")

        return {
            "distance_m": round(euclid_dist, 2),
            "path_distance_m": round(path_dist, 2),
            "has_line_of_sight": has_los,
            "corner_count": corner_count,
            "rssi_dbm": round(rssi_dbm, 1),
            "packet_loss_rate": round(loss_rate, 4),
            "latency_ms": round(latency_ms, 2) if is_connected else float("inf"),
            "effective_bandwidth_kbps": effective_bandwidth_kbps,
            "is_connected": is_connected,
            "status": status,
            "classification_reason": reason,
        }
