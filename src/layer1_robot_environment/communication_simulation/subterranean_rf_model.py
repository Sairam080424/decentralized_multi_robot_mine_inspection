"""
Subterranean Radio-Frequency (RF) Attenuation & Communication Model
Milestone M1: Underground Mine Simulation (TASK-M1-005)

Approach A: Geometry-Based Analytical Subterranean RF Model.
Simulates distance-dependent signal degradation, physical tunnel wall
line-of-sight (LOS) ray-casting, obstacle shadowing (rock piles, timber supports),
waveguide bend diffraction loss, configurable packet loss and latency,
effective bandwidth shaping, and explicit forced communication blackout.

All parameters can be loaded dynamically from config/simulation/rf_attenuation_config.yaml.
"""

import math
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import yaml


class SubterraneanRFModel:
    """
    Geometry-aware subterranean RF propagation model for underground mine drifts.
    Performs 2D/3D ray-casting against mine tunnel walls and physical obstacles,
    determines waveguide paths around corners, and computes RSSI, packet loss,
    jittered latency, and effective bandwidth.
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
    ):
        self.tx_power_dbm = tx_power_dbm
        self.rx_sensitivity_dbm = rx_sensitivity_dbm
        self.path_loss_exponent = path_loss_exponent
        self.reference_distance_m = reference_distance_m
        self.reference_loss_db = reference_loss_db
        self.corner_diffraction_loss_db = (
            corner_attenuation_db if corner_attenuation_db is not None else corner_diffraction_loss_db
        )
        self.corner_attenuation_db = self.corner_diffraction_loss_db  # alias for backward compatibility
        self.obstacle_shadow_loss_db = obstacle_shadow_loss_db
        self.los_cutoff_distance_m = los_cutoff_distance_m
        self.nlos_corner_limit = nlos_corner_limit
        self.base_latency_ms = base_latency_ms
        self.max_jitter_ms = max_jitter_ms
        self.bandwidth_limit_kbps = bandwidth_limit_kbps
        self.forced_blackout = forced_blackout

        if random_seed is not None:
            random.seed(random_seed)

        # Build geometric representation of mine tunnel walls and obstacles
        self._init_mine_geometry()

    @classmethod
    def from_yaml(cls, yaml_path: Union[str, Path], random_seed: Optional[int] = 42) -> "SubterraneanRFModel":
        """Construct model by loading parameters from a YAML configuration file."""
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
        )

    def _init_mine_geometry(self):
        """
        Defines the 2D bounding line segments for rock walls and bounding boxes
        for physical obstacles in the canonical mine_world layout.
        Tunnel width is nominally 3.5m (clearance y in [-1.75, +1.75]).
        T-Junction Alpha centered at (30.0, 0.0), branch opening at x in [28.25, 31.75].
        """
        # Wall segments: ((x1, y1), (x2, y2))
        self.wall_segments: List[Tuple[Tuple[float, float], Tuple[float, float]]] = [
            # Main drift south/right wall (continuous from portal x=-6 to upper dead-end x=68.2)
            ((-6.0, -1.75), (68.2, -1.75)),
            # Main drift north/left wall (portal to west corner of T-junction)
            ((-6.0, 1.75), (28.25, 1.75)),
            # Main drift north/left wall (east corner of T-junction to upper dead-end)
            ((31.75, 1.75), (68.2, 1.75)),
            # Upper drift dead-end rock face
            ((68.2, -1.75), (68.2, 1.75)),
            # Crosscut west wall (from T-junction corner north to 90-degree turn)
            ((28.25, 1.75), (28.25, 24.75)),
            # Crosscut east wall (from T-junction corner north to south corner of east drift)
            ((31.75, 1.75), (31.75, 21.25)),
            # East drift south wall (from crosscut east corner to east dead-end)
            ((31.75, 21.25), (56.0, 21.25)),
            # East drift north wall (from crosscut west corner extended to east dead-end)
            ((28.25, 24.75), (56.0, 24.75)),
            # East drift dead-end rock face
            ((56.0, 21.25), (56.0, 24.75)),
        ]

        # Physical obstacles with 2D bounding boxes and vertical heights
        # (name, (min_x, max_x, min_y, max_y), max_z)
        self.obstacles: List[Tuple[str, Tuple[float, float, float, float], float]] = [
            # Fallen rock pile on north flank of T-junction: pose (28.5, 0.8), size 2.5 x 1.2 x 0.85
            ("fallen_rock_pile", (27.25, 29.75, 0.25, 1.45), 0.85),
            # Timber roof support portal: pose (5.0, 0.0), posts at y=+/-1.6, crossbeam height 2.9
            ("timber_roof_support", (4.8, 5.2, -1.75, 1.75), 2.9),
            # Mine debris in east drift: pose (42.0, 24.8), size 2.0 x 1.2 x 0.55
            ("mine_debris", (41.0, 43.0, 24.0, 25.4), 0.55),
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
        q1: Tuple[float, float], q2: Tuple[float, float]
    ) -> bool:
        """Check if 2D line segment p1-p2 strictly intersects segment q1-q2."""
        def ccw(a, b, c):
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

        return (
            ccw(p1, q1, q2) != ccw(p2, q1, q2)
            and ccw(p1, p2, q1) != ccw(p1, p2, q2)
        )

    def is_in_mine(self, pos: Tuple[float, float, float]) -> bool:
        """Verify whether a coordinate lies within navigable underground mine corridors."""
        x, y, z = pos

        # Main haulage drift and ramp: x in [-6.0, 68.2], y in [-1.85, 1.85]
        # Elevation: z in [-0.5, 4.0] for lower drift, up to 7.0 for upper drift
        if -6.0 <= x <= 68.2 and -1.85 <= y <= 1.85:
            if x <= 42.0 and -0.5 <= z <= 3.5:
                return True
            if x > 42.0 and -0.5 <= z <= 7.0:
                return True

        # North crosscut drift: x in [28.1, 31.9], y in [1.7, 24.9], z in [-0.5, 3.5]
        if 28.1 <= x <= 31.9 and 1.7 <= y <= 24.9 and -0.5 <= z <= 3.5:
            return True

        # East drift extension: x in [31.5, 56.2], y in [21.1, 24.9], z in [-0.5, 3.5]
        if 31.5 <= x <= 56.2 and 21.1 <= y <= 24.9 and -0.5 <= z <= 3.5:
            return True

        return False

    def check_line_of_sight(
        self,
        pos_a: Tuple[float, float, float],
        pos_b: Tuple[float, float, float],
    ) -> Tuple[bool, int, str]:
        """
        Evaluates geometric line-of-sight using 2D/3D ray-casting against rock walls
        and physical obstacles.
        Returns:
            (has_los: bool, corner_count: int, reason: str)
        """
        # 1. Bounds verification
        if not self.is_in_mine(pos_a) or not self.is_in_mine(pos_b):
            return False, 99, "OUTSIDE_MINE_BOUNDS"

        p1 = (pos_a[0], pos_a[1])
        p2 = (pos_b[0], pos_b[1])

        # 2. Geometric Ray-Casting against Rock Walls
        wall_intersections = 0
        for seg_start, seg_end in self.wall_segments:
            if self._segments_intersect(p1, p2, seg_start, seg_end):
                wall_intersections += 1

        # 3. Waveguide Path & Corner / Bend Count Determination
        x1, y1, _ = pos_a
        x2, y2, _ = pos_b

        in_main_1 = -1.85 <= y1 <= 1.85
        in_main_2 = -1.85 <= y2 <= 1.85
        in_cross_1 = 28.1 <= x1 <= 31.9 and y1 > 1.85
        in_cross_2 = 28.1 <= x2 <= 31.9 and y2 > 1.85
        in_east_1 = x1 > 31.9 and y1 > 20.0
        in_east_2 = x2 > 31.9 and y2 > 20.0

        if in_main_1 and in_main_2:
            corner_count = 0
        elif (in_main_1 and in_cross_2) or (in_cross_1 and in_main_2):
            corner_count = 1
        elif (in_main_1 and in_east_2) or (in_east_1 and in_main_2):
            corner_count = 2
        elif (in_cross_1 and in_east_2) or (in_east_1 and in_cross_2):
            corner_count = 1
        elif in_cross_1 and in_cross_2:
            corner_count = 0
        elif in_east_1 and in_east_2:
            corner_count = 0
        else:
            corner_count = 1 if wall_intersections > 0 else 0

        # If direct ray does NOT intersect any rock wall, direct optical LOS exists!
        # This handles cases where robots are near intersection boundaries with clear sightlines.
        if wall_intersections == 0:
            # Check if an opaque physical obstacle blocks the ray (e.g. fallen_rock_pile)
            obstacle_hit = self._check_obstacle_intersection(pos_a, pos_b)
            if obstacle_hit:
                return False, 0, f"BLOCKED_BY_OBSTACLE_{obstacle_hit.upper()}"
            return True, 0, "CLEAR_LINE_OF_SIGHT"

        # Direct ray is blocked by solid rock tunnel walls
        return False, corner_count, f"BLOCKED_BY_ROCK_WALLS_{wall_intersections}_INTERSECTIONS"

    def _check_obstacle_intersection(
        self, pos_a: Tuple[float, float, float], pos_b: Tuple[float, float, float]
    ) -> Optional[str]:
        """Check if 3D segment pos_a - pos_b intersects any opaque obstacle volume."""
        p1 = (pos_a[0], pos_a[1])
        p2 = (pos_b[0], pos_b[1])
        avg_z = (pos_a[2] + pos_b[2]) / 2.0

        for name, (min_x, max_x, min_y, max_y), max_z in self.obstacles:
            if avg_z > max_z:
                continue  # Ray passes cleanly over obstacle
            # Test 4 bounding segments of the box
            box_segs = [
                ((min_x, min_y), (max_x, min_y)),
                ((max_x, min_y), (max_x, max_y)),
                ((max_x, max_y), (min_x, max_y)),
                ((min_x, max_y), (min_x, min_y)),
            ]
            for s1, s2 in box_segs:
                if self._segments_intersect(p1, p2, s1, s2):
                    return name

            # Also check if either endpoint is inside the obstacle box
            for pt in [p1, p2]:
                if min_x <= pt[0] <= max_x and min_y <= pt[1] <= max_y:
                    return name

        return None

    def evaluate_link(
        self,
        pos_a: Tuple[float, float, float],
        pos_b: Tuple[float, float, float],
    ) -> Dict[str, Union[float, bool, int, str]]:
        """
        Evaluates communication link parameters between two robot positions.
        Returns dictionary containing distance, LOS classification, corner count,
        RSSI, packet loss probability, latency, effective bandwidth, and status.
        """
        dist = max(self.calculate_distance(pos_a, pos_b), 0.1)
        has_los, corner_count, reason = self.check_line_of_sight(pos_a, pos_b)

        # 1. Forced Blackout Test Mode
        if self.forced_blackout:
            return {
                "distance_m": round(dist, 2),
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

        # 2. Outside Known Mine Bounds
        if reason == "OUTSIDE_MINE_BOUNDS":
            return {
                "distance_m": round(dist, 2),
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

        # 3. Path Loss and Attenuation Calculation
        # Log-distance path loss based on Euclidean distance
        path_loss_db = self.reference_loss_db + 10.0 * self.path_loss_exponent * math.log10(
            dist / self.reference_distance_m
        )

        total_attenuation = path_loss_db

        # Apply specific LOS vs NLOS attenuation penalties
        if has_los:
            # Clear line of sight
            pass
        elif "BLOCKED_BY_OBSTACLE" in reason:
            # Same corridor, blocked by physical obstacle (e.g. fallen rock pile)
            total_attenuation += self.obstacle_shadow_loss_db
        else:
            # Blocked by solid rock tunnel walls around bends
            total_attenuation += corner_count * self.corner_diffraction_loss_db

        rssi_dbm = self.tx_power_dbm - total_attenuation

        # 4. Check Disconnection Thresholds (Distance Cutoff & Corner Limit)
        is_cutoff = False
        cutoff_status = ""

        if dist > self.los_cutoff_distance_m:
            is_cutoff = True
            cutoff_status = "EXCEEDED_LOS_CUTOFF" if has_los else "EXCEEDED_MAX_RANGE"
        elif corner_count >= self.nlos_corner_limit:
            # Exceeding corner limit (e.g. 2 corners) severely degrades or breaks link
            is_cutoff = True
            cutoff_status = "EXCEEDED_CORNER_LIMIT"

        # 5. Packet Loss Estimation via Sigmoid Function
        snr_margin = rssi_dbm - self.rx_sensitivity_dbm

        if is_cutoff or snr_margin <= -10.0:
            loss_rate = 1.0
        elif snr_margin >= 20.0:
            loss_rate = 0.005  # baseline negligible packet drop
        else:
            # Sigmoid transition centered at margin = 5 dB
            loss_rate = 1.0 / (1.0 + math.exp(0.3 * (snr_margin - 5.0)))

        loss_rate = max(0.0, min(1.0, loss_rate))

        # 6. Connectivity Decision
        is_connected = (loss_rate < 0.90) and (rssi_dbm >= self.rx_sensitivity_dbm) and not is_cutoff

        # 7. Latency Calculation (ms)
        if is_connected:
            jitter = random.uniform(0.0, self.max_jitter_ms)
            latency_ms = self.base_latency_ms + (dist * 0.15) + (corner_count * 15.0) + jitter
        else:
            latency_ms = float("inf")

        # 8. Effective Bandwidth (kbps)
        if is_connected:
            effective_bandwidth_kbps = round(self.bandwidth_limit_kbps * (1.0 - loss_rate), 1)
        else:
            effective_bandwidth_kbps = 0.0

        status = "CONNECTED" if is_connected else (cutoff_status or "DISCONNECTED")

        return {
            "distance_m": round(dist, 2),
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
