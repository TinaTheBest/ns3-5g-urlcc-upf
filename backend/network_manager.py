import numpy as np
from backend.network_topology import NetworkTopology
from backend.latency_calculator import LatencyCalculator
from backend.reliability_analyzer import ReliabilityAnalyzer
from backend.upf_optimizer import UPFOptimizer
from backend.packet_generator import PacketGenerator


class NetworkManager:
    """Main backend class that orchestrates all network components"""

    def __init__(self, num_ues=15, num_gnbs=5, num_upfs=3):
        # Initialize all components
        self.topology = NetworkTopology(num_ues, num_gnbs, num_upfs)
        self.latency_calculator = LatencyCalculator()
        self.reliability_analyzer = ReliabilityAnalyzer()
        self.upf_optimizer = UPFOptimizer()
        self.packet_generator = PacketGenerator()

        # Current state
        self.latencies = None
        self.reliabilities = None
        self.packet_data = None

        # Initialize metrics
        self.update_all_metrics()

    def update_all_metrics(self):
        """Update all network metrics"""
        ue_gnb_dist, gnb_upf_dist = self.topology.update_associations()
        self.latencies = self.latency_calculator.calculate_latencies(
            self.topology, ue_gnb_dist, gnb_upf_dist
        )
        self.reliabilities = self.reliability_analyzer.calculate_reliability(
            self.topology, ue_gnb_dist, gnb_upf_dist
        )
        self.packet_data = self.packet_generator.generate_packets(self.topology)

        return {
            "latency_stats": self.latency_calculator.get_latency_stats(self.latencies),
            "reliability_stats": self.reliability_analyzer.get_reliability_stats(
                self.reliabilities
            ),
        }

    def optimize_upf_placement(self):
        """Optimize UPF placement and update metrics"""
        self.upf_optimizer.optimize_placement(self.topology)
        return self.update_all_metrics()

    def randomize_upf_positions(self):
        """Randomize UPF positions and update metrics"""
        self.topology.randomize_upf_positions()
        return self.update_all_metrics()

    def move_upf(self, upf_id, new_position):
        """Move a specific UPF and update metrics"""
        self.topology.move_upf(upf_id, new_position)
        return self.update_all_metrics()

    def generate_new_packets(self):
        """Generate new packets and return data"""
        self.packet_data = self.packet_generator.generate_packets(self.topology)
        return self.packet_data

    def get_current_state(self):
        """Return the current state of the network"""
        return {
            "topology": {
                "ue_positions": self.topology.ue_positions,
                "gnb_positions": self.topology.gnb_positions,
                "upf_positions": self.topology.upf_positions,
                "ue_to_gnb": self.topology.ue_to_gnb,
                "gnb_to_upf": self.topology.gnb_to_upf,
            },
            "latencies": self.latencies,
            "reliabilities": self.reliabilities,
            "packet_data": self.packet_data,
        }
