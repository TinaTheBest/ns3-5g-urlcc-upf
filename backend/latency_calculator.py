import numpy as np


class LatencyCalculator:
    """Calculates end-to-end latencies in the network"""

    def __init__(self):
        # Speed of radio waves in air: ~300,000 km/s
        # Speed in fiber: ~200,000 km/s
        self.speed_radio = 300000  # km/s
        self.speed_fiber = 200000  # km/s
        self.air_base_delay = 0.05  # ms
        self.fronthaul_base_delay = 0.02  # ms
        self.base_processing_delay = 0.03  # ms

    def calculate_latencies(self, network, ue_gnb_dist, gnb_upf_dist):
        """Calculate end-to-end latencies for all UEs"""
        latencies = []

        for ue_id in range(network.num_ues):
            gnb_id = network.ue_to_gnb[ue_id]
            upf_id = network.gnb_to_upf[gnb_id]

            # Air interface latency (ms) - distance/speed + base delay
            air_distance = ue_gnb_dist[ue_id, gnb_id]
            air_prop_delay = (air_distance / self.speed_radio) * 1000  # convert to ms
            air_delay = air_prop_delay + self.air_base_delay

            # Fronthaul latency (ms) - distance/speed + base delay
            fronthaul_distance = gnb_upf_dist[gnb_id, upf_id]
            fronthaul_prop_delay = (
                fronthaul_distance / self.speed_fiber
            ) * 1000  # convert to ms
            fronthaul_delay = fronthaul_prop_delay + self.fronthaul_base_delay

            # Processing delay at nodes (variable based on load)
            # Simulate load variation based on number of UEs connected to the same gNB
            ues_per_gnb = np.sum(network.ue_to_gnb == gnb_id)
            load_factor = (
                1 + (ues_per_gnb / network.num_ues) * 0.5
            )  # 1.0 to 1.5x based on load
            processing_delay = self.base_processing_delay * load_factor  # ms

            total_latency = air_delay + fronthaul_delay + processing_delay
            latencies.append(total_latency)

        return np.array(latencies)

    def get_latency_stats(self, latencies):
        """Calculate statistics for the latencies"""
        return {
            "average": np.mean(latencies),
            "minimum": np.min(latencies),
            "maximum": np.max(latencies),
            "urllc_target_achieved": np.mean(latencies) < 1.0,  # URLLC target is 1ms
        }
