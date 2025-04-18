import numpy as np
from sklearn.cluster import KMeans


class UPFOptimizer:
    """Optimizes the placement of UPFs in the network"""

    def __init__(self):
        self.kmeans = None

    def optimize_placement(self, network):
        """Optimize UPF placement using K-means clustering of gNB positions"""
        self.kmeans = KMeans(n_clusters=network.num_upfs, n_init=10, random_state=42)
        self.kmeans.fit(network.gnb_positions)

        # Set UPF positions to cluster centers
        network.upf_positions = self.kmeans.cluster_centers_

        # Update network associations
        return network.update_associations()

    def find_optimal_num_upfs(self, network, min_upfs=2, max_upfs=10):
        """Find the optimal number of UPFs to minimize inertia/latency"""
        results = []

        for num_upfs in range(min_upfs, max_upfs + 1):
            kmeans = KMeans(n_clusters=num_upfs, n_init=10, random_state=42)
            kmeans.fit(network.gnb_positions)
            results.append(
                {
                    "num_upfs": num_upfs,
                    "inertia": kmeans.inertia_,  # Sum of squared distances to closest cluster center
                }
            )

        return results
