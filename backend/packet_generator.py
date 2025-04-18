import numpy as np


class PacketGenerator:
    """Generates packets for network simulation"""

    def __init__(self):
        self.packet_positions = []
        self.packet_source = []
        self.packet_target = []
        self.packet_size = []
        self.active_ratio = 0.3  # % of UEs that are active

    def generate_packets(self, network):
        """Generate packets between UEs and their serving UPFs through gNBs"""
        # Clear existing packets
        self.packet_positions = []
        self.packet_source = []
        self.packet_target = []
        self.packet_size = []

        # Generate new packets - default 30% of UEs send packets
        active_ues = np.random.choice(
            range(network.num_ues),
            size=max(1, int(self.active_ratio * network.num_ues)),
            replace=False,
        )

        for ue_id in active_ues:
            gnb_id = network.ue_to_gnb[ue_id]
            upf_id = network.gnb_to_upf[gnb_id]

            # Position along the UE-gNB path
            progress_to_gnb = np.random.uniform(0, 1)
            x = network.ue_positions[ue_id, 0] + progress_to_gnb * (
                network.gnb_positions[gnb_id, 0] - network.ue_positions[ue_id, 0]
            )
            y = network.ue_positions[ue_id, 1] + progress_to_gnb * (
                network.gnb_positions[gnb_id, 1] - network.ue_positions[ue_id, 1]
            )
            self.packet_positions.append([x, y])
            self.packet_source.append(("UE", ue_id))
            self.packet_target.append(("gNB", gnb_id))
            self.packet_size.append(np.random.choice([5, 8, 12]))  # Size in pixels

            # Position along the gNB-UPF path
            progress_to_upf = np.random.uniform(0, 1)
            x = network.gnb_positions[gnb_id, 0] + progress_to_upf * (
                network.upf_positions[upf_id, 0] - network.gnb_positions[gnb_id, 0]
            )
            y = network.gnb_positions[gnb_id, 1] + progress_to_upf * (
                network.upf_positions[upf_id, 1] - network.gnb_positions[gnb_id, 1]
            )
            self.packet_positions.append([x, y])
            self.packet_source.append(("gNB", gnb_id))
            self.packet_target.append(("UPF", upf_id))
            self.packet_size.append(np.random.choice([5, 8, 12]))  # Size in pixels

        return {
            "positions": self.packet_positions,
            "source": self.packet_source,
            "target": self.packet_target,
            "size": self.packet_size,
        }

    def set_active_ratio(self, ratio):
        """Set the ratio of active UEs"""
        self.active_ratio = max(0.01, min(1.0, ratio))  # Ensure between 1% and 100%
