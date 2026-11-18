"""
Subterranean Radio-Frequency (RF) Attenuation & Communication Model
Milestone M1: Underground Mine Simulation (TASK-M1-005)

Simulates distance-dependent signal degradation, tunnel wall line-of-sight (LOS)
obstruction, tunnel corner diffraction loss, configurable packet loss and latency,
and explicit forced communication blackout for fault-injection testing.

Note: This is a documented, simplified subterranean waveguide propagation model
calibrated for underground mine drifts, not a full 3D Maxwell electromagnetic solver.
"""

import math
import random
from typing import Dict, List, Optional, Tuple


class SubterraneanRFModel:
    """
    Subterranean RF propagation model for underground tunnels.
    Computes RSSI, packet drop rate, and latency between coordinate pairs
    based on distance, line-of-sight rock obstructions, and tunnel corner counts.
    """

    def __init__(
        self,
        tx_power_dbm: float = 20.0,
        rx_sensitivity_dbm: float = -95.0,
        path_loss_exponent: float = 2.4,
        reference_distance_m: float = 1.0,
        reference_loss_db: float = 40.0,
        corner_attenuation_db: float = 18.0,
        base_latency_ms: float = 8.0,
        max_jitter_ms: float = 12.0,
        random_seed: Optional[int] = 42,
    ):
        self.tx_power_dbm = tx_power_dbm
        self.rx_sensitivity_dbm = rx_sensitivity_dbm
        self.path_loss_exponent = path_loss_exponent
        self.reference_distance_m = reference_distance_m
        self.reference_loss_db = reference_loss_db
        self.corner_attenuation_db = corner_attenuation_db
        self.base_latency_ms = base_latency_ms
        self.max_jitter_ms = max_jitter_ms
        self.forced_blackout = False

        if random_seed is not None:
            random.seed(random_seed)

    def set_forced_blackout(self, enabled: bool):
        """Forces total communication blackout between all nodes for fault injection."""
        self.forced_blackout = enabled

    def calculate_distance(
        self, pos_a: Tuple[float, float, float], pos_b: Tuple[float, float, float]
    ) -> float:
        """Euclidean 3D distance between two positions."""
        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]
        dz = pos_a[2] - pos_b[2]
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def check_line_of_sight(
        self,
        pos_a: Tuple[float, float, float],
        pos_b: Tuple[float, float, float],
        tunnel_width: float = 3.5,
    ) -> Tuple[bool, int]:
        """
        Evaluates line-of-sight and estimates corner count between positions
        within the canonical mine drift network.
        Returns:
            (has_los: bool, corner_count: int)
        """
        # In mine_world.sdf:
        # Main haulage drift: y approx 0, x in [0, 68]
        # Crosscut drift: x approx 30, y in [0, 24]
        # East drift extension: y approx 23, x in [30, 46]

        x1, y1, _ = pos_a
        x2, y2, _ = pos_b

        # If both are in main drift (y within tunnel width/2)
        half_w = tunnel_width / 2.0
        in_main_1 = abs(y1) <= half_w
        in_main_2 = abs(y2) <= half_w

        if in_main_1 and in_main_2:
            return True, 0

        # If both are in north crosscut drift (x within tunnel width/2 of x=30)
        in_cross_1 = abs(x1 - 30.0) <= half_w and y1 > half_w
        in_cross_2 = abs(x2 - 30.0) <= half_w and y2 > half_w

        if in_cross_1 and in_cross_2:
            return True, 0

        # One in main drift, one in crosscut drift: 1 corner (at junction x=30, y=0)
        if (in_main_1 and in_cross_2) or (in_cross_1 and in_main_2):
            return False, 1

        # One in east drift (y > 20, x > 32) and one in main drift: 2 corners
        in_east_1 = y1 > 20.0 and x1 > 32.0
        in_east_2 = y2 > 20.0 and x2 > 32.0

        if (in_main_1 and in_east_2) or (in_east_1 and in_main_2):
            return False, 2

        if (in_cross_1 and in_east_2) or (in_east_1 and in_cross_2):
            return False, 1

        # Default estimation based on coordinate variation
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        if dx > half_w and dy > half_w:
            return False, 1
        return True, 0

    def evaluate_link(
        self,
        pos_a: Tuple[float, float, float],
        pos_b: Tuple[float, float, float],
    ) -> Dict[str, float]:
        """
        Evaluates communication link parameters between two robot positions.
        Returns dictionary containing distance, RSSI, packet loss probability,
        latency, and link availability status.
        """
        dist = max(self.calculate_distance(pos_a, pos_b), 0.1)
        has_los, corner_count = self.check_line_of_sight(pos_a, pos_b)

        if self.forced_blackout:
            return {
                "distance_m": dist,
                "has_line_of_sight": False,
                "corner_count": corner_count,
                "rssi_dbm": -120.0,
                "packet_loss_rate": 1.0,
                "latency_ms": float("inf"),
                "is_connected": False,
                "status": "FORCED_BLACKOUT",
            }

        # Log-distance path loss
        path_loss_db = self.reference_loss_db + 10.0 * self.path_loss_exponent * math.log10(
            dist / self.reference_distance_m
        )
        total_attenuation = path_loss_db + (corner_count * self.corner_attenuation_db)
        rssi_dbm = self.tx_power_dbm - total_attenuation

        # Packet loss estimation via sigmoid curve centered near receiver sensitivity
        snr_margin = rssi_dbm - self.rx_sensitivity_dbm
        if snr_margin >= 20.0:
            loss_rate = 0.005  # baseline negligible packet drop
        elif snr_margin <= -10.0:
            loss_rate = 1.0    # complete link cutoff
        else:
            # Sigmoid transition
            loss_rate = 1.0 / (1.0 + math.exp(0.3 * (snr_margin - 5.0)))

        # Bounded packet loss rate
        loss_rate = max(0.0, min(1.0, loss_rate))

        # Latency calculation
        jitter = random.uniform(0.0, self.max_jitter_ms) if loss_rate < 1.0 else 0.0
        latency_ms = self.base_latency_ms + (dist * 0.15) + (corner_count * 15.0) + jitter
        if loss_rate >= 1.0:
            latency_ms = float("inf")

        is_connected = (loss_rate < 0.95) and (rssi_dbm >= self.rx_sensitivity_dbm)

        return {
            "distance_m": round(dist, 2),
            "has_line_of_sight": has_los,
            "corner_count": corner_count,
            "rssi_dbm": round(rssi_dbm, 1),
            "packet_loss_rate": round(loss_rate, 4),
            "latency_ms": round(latency_ms, 2) if is_connected else float("inf"),
            "is_connected": is_connected,
            "status": "CONNECTED" if is_connected else "DISCONNECTED",
        }
