import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.network_manager import NetworkManager
from frontend.dashboard_app import Dashboard
from backend.latency_calculator import LatencyCalculator
from backend.reliability_analyzer import ReliabilityAnalyzer
from backend.upf_optimizer import UPFOptimizer
from backend.packet_generator import PacketGenerator
from frontend.visualizer import NetworkVisualizer


def main():
    """Entry point for the 5G URLLC Network Optimization application"""
    # Initialize the network manager (backend components)
    network_manager = NetworkManager(num_ues=15, num_gnbs=5, num_upfs=3)

    # Create all required components
    latency_calculator = LatencyCalculator()
    reliability_analyzer = ReliabilityAnalyzer()
    upf_optimizer = UPFOptimizer()
    packet_generator = PacketGenerator()
    visualizer = NetworkVisualizer()

    # Initialize the dashboard (frontend components)
    dashboard = Dashboard(
        network=network_manager.topology,  # Assuming the network manager has a topology property
        latency_calculator=latency_calculator,
        reliability_analyzer=reliability_analyzer,
        upf_optimizer=upf_optimizer,
        packet_generator=packet_generator,
        visualizer=visualizer,
    )

    # Run the dashboard
    print("Starting 5G URLLC Network Optimization Dashboard...")
    print("Open your browser at http://127.0.0.1:8050 to view the application")
    dashboard.run(debug=True, port=8050)


if __name__ == "__main__":
    main()
