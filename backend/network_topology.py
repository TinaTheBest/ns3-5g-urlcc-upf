import numpy as np


class NetworkTopology:
    """Handles network element positions and their associations"""

    def __init__(self, num_ues=15, num_gnbs=5, num_upfs=3, scale_factor=10):
        self.num_ues = num_ues
        self.num_gnbs = num_gnbs
        self.num_upfs = num_upfs
        self.scale_factor = scale_factor  # 10km area
        np.random.seed(42)

        # Initial positions - scale in km (0-10km)
        self.ue_positions = np.random.rand(num_ues, 2) * self.scale_factor
        self.gnb_positions = np.random.rand(num_gnbs, 2) * self.scale_factor
        self.upf_positions = np.random.rand(num_upfs, 2) * self.scale_factor

        # Association maps
        self.ue_to_gnb = None
        self.gnb_to_upf = None

        # Initialize associations
        self.update_associations()

    def update_associations(self):
        """Update the associations between UEs, gNBs, and UPFs based on proximity"""
        # Calculate distances between UEs and gNBs
        ue_gnb_dist = np.linalg.norm(
            self.ue_positions[:, None] - self.gnb_positions, axis=2
        )
        # Assign each UE to nearest gNB
        self.ue_to_gnb = np.argmin(ue_gnb_dist, axis=1)

        # Calculate distances between gNBs and UPFs
        gnb_upf_dist = np.zeros((self.num_gnbs, self.num_upfs))
        for gnb_id in range(self.num_gnbs):
            for upf_id in range(self.num_upfs):
                gnb_upf_dist[gnb_id, upf_id] = np.linalg.norm(
                    self.gnb_positions[gnb_id] - self.upf_positions[upf_id]
                )
        # Assign each gNB to nearest UPF
        self.gnb_to_upf = np.argmin(gnb_upf_dist, axis=1)

        return ue_gnb_dist, gnb_upf_dist

    def randomize_upf_positions(self):
        """Randomize positions of UPFs"""
        self.upf_positions = np.random.rand(self.num_upfs, 2) * self.scale_factor
        return self.update_associations()

    def move_upf(self, upf_id, new_position):
        """Move a UPF to a new position"""
        # Ensure within bounds
        x = max(0, min(self.scale_factor, new_position[0]))
        y = max(0, min(self.scale_factor, new_position[1]))
        self.upf_positions[upf_id] = [x, y]
        return self.update_associations()
