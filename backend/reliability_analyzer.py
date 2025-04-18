import numpy as np


class ReliabilityAnalyzer:
    """Analyzes network reliability metrics"""

    def __init__(self):
        # Constants for reliability analysis
        self.reliability_threshold = 0.99999  # 5 nines reliability (URLLC target)
        self.distance_reliability_factor = 0.01  # Reliability degrades with distance
        self.base_reliability = 0.99999  # Base reliability at optimal conditions

    def calculate_reliability(self, network, ue_gnb_dist, gnb_upf_dist):
        """Calculate reliability metrics for all UEs based on distances and network conditions"""
        reliabilities = []

        for ue_id in range(network.num_ues):
            gnb_id = network.ue_to_gnb[ue_id]
            upf_id = network.gnb_to_upf[gnb_id]

            # Air interface reliability (decreases with distance)
            air_distance = ue_gnb_dist[ue_id, gnb_id]
            air_reliability = self.base_reliability * np.exp(
                -self.distance_reliability_factor * air_distance
            )

            # Fronthaul reliability (decreases with distance)
            fronthaul_distance = gnb_upf_dist[gnb_id, upf_id]
            fronthaul_reliability = self.base_reliability * np.exp(
                -self.distance_reliability_factor * fronthaul_distance * 0.5
            )

            # Load-based reliability factor
            ues_per_gnb = np.sum(network.ue_to_gnb == gnb_id)
            load_factor = max(0.99, 1 - (ues_per_gnb / network.num_ues) * 0.01)

            # Combined reliability (product of all reliability factors)
            total_reliability = air_reliability * fronthaul_reliability * load_factor
            reliabilities.append(total_reliability)

        return np.array(reliabilities)

    def get_reliability_stats(self, reliabilities):
        """Calculate statistics for the reliabilities"""
        return {
            "average": np.mean(reliabilities),
            "minimum": np.min(reliabilities),
            "maximum": np.max(reliabilities),
            "urllc_target_achieved": np.min(reliabilities)
            >= self.reliability_threshold,
        }
