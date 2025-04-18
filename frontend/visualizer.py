import plotly.graph_objects as go
import numpy as np


class NetworkVisualizer:
    def __init__(self):
        pass

    def create_figure(self, network, packet_data, latencies, selected_upf=-1):
        """Create a Plotly figure visualizing the network"""
        fig = go.Figure()

        # UE nodes
        fig.add_trace(
            go.Scatter(
                x=network.ue_positions[:, 0],
                y=network.ue_positions[:, 1],
                mode="markers",
                marker=dict(color="red", size=10),
                name="UE",
                hoverinfo="text",
                text=[
                    f"UE {i}<br>Position: ({network.ue_positions[i,0]:.2f}, {network.ue_positions[i,1]:.2f}) km<br>Latency: {latencies[i]:.3f} ms"
                    for i in range(network.num_ues)
                ],
            )
        )

        # gNB nodes
        fig.add_trace(
            go.Scatter(
                x=network.gnb_positions[:, 0],
                y=network.gnb_positions[:, 1],
                mode="markers",
                marker=dict(color="green", size=15, symbol="triangle-up"),
                name="gNB",
                hoverinfo="text",
                text=[
                    f"gNB {i}<br>Position: ({network.gnb_positions[i,0]:.2f}, {network.gnb_positions[i,1]:.2f}) km"
                    for i in range(network.num_gnbs)
                ],
            )
        )

        # UPF nodes (draggable)
        fig.add_trace(
            go.Scatter(
                x=network.upf_positions[:, 0],
                y=network.upf_positions[:, 1],
                mode="markers+text",
                marker=dict(color="blue", size=20, symbol="square"),
                textposition="top center",
                name="UPF",
                hoverinfo="text",
                text=[
                    f"UPF {i}<br>Position: ({network.upf_positions[i,0]:.2f}, {network.upf_positions[i,1]:.2f}) km"
                    for i in range(network.num_upfs)
                ],
                customdata=np.arange(network.num_upfs),
            )
        )

        # Packets in transit
        if packet_data and len(packet_data["positions"]) > 0:
            # Convert to numpy for easier manipulation
            packet_positions = np.array(packet_data["positions"])
            packet_sizes = np.array(packet_data["size"])

            # Add packet trace
            fig.add_trace(
                go.Scatter(
                    x=packet_positions[:, 0],
                    y=packet_positions[:, 1],
                    mode="markers",
                    marker=dict(
                        color="yellow",
                        size=packet_sizes,
                        symbol="circle",
                        line=dict(color="orange", width=1),
                    ),
                    name="Packets",
                    hoverinfo="text",
                    text=[
                        f"Packet<br>From: {src[0]} {src[1]}<br>To: {tgt[0]} {tgt[1]}"
                        for src, tgt in zip(
                            packet_data["source"], packet_data["target"]
                        )
                    ],
                )
            )

        # Connections from UEs to gNBs
        for ue_id in range(network.num_ues):
            gnb_id = network.ue_to_gnb[ue_id]
            fig.add_trace(
                go.Scatter(
                    x=[
                        network.ue_positions[ue_id, 0],
                        network.gnb_positions[gnb_id, 0],
                    ],
                    y=[
                        network.ue_positions[ue_id, 1],
                        network.gnb_positions[gnb_id, 1],
                    ],
                    line=dict(color="rgba(255, 0, 0, 0.5)", width=1, dash="dot"),
                    showlegend=False,
                    hoverinfo="none",
                )
            )

        # Connections from gNBs to UPFs
        for gnb_id in range(network.num_gnbs):
            upf_id = network.gnb_to_upf[gnb_id]
            fig.add_trace(
                go.Scatter(
                    x=[
                        network.gnb_positions[gnb_id, 0],
                        network.upf_positions[upf_id, 0],
                    ],
                    y=[
                        network.gnb_positions[gnb_id, 1],
                        network.upf_positions[upf_id, 1],
                    ],
                    line=dict(color="rgba(0, 0, 255, 0.5)", width=1, dash="dot"),
                    showlegend=False,
                    hoverinfo="none",
                )
            )

        # Highlight selected UPF if any
        if selected_upf != -1:
            upf_id = int(selected_upf)
            fig.add_trace(
                go.Scatter(
                    x=[network.upf_positions[upf_id, 0]],
                    y=[network.upf_positions[upf_id, 1]],
                    mode="markers",
                    marker=dict(
                        color="red",
                        size=30,
                        symbol="circle-open",
                        line=dict(width=2),
                    ),
                    showlegend=False,
                    hoverinfo="none",
                )
            )

            # Add text annotation
            fig.add_annotation(
                x=network.upf_positions[upf_id, 0],
                y=network.upf_positions[upf_id, 1] + 0.2,
                text="Selected - Click to place",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                bgcolor="white",
                bordercolor="red",
                borderwidth=2,
            )

        # Update layout
        fig.update_layout(
            title="5G URLLC Network - Click and Drag UPFs to Optimize",
            xaxis=dict(
                title="X Position (km)",
                range=[0, network.scale_factor],
                gridcolor="lightgray",
            ),
            yaxis=dict(
                title="Y Position (km)",
                range=[0, network.scale_factor],
                gridcolor="lightgray",
            ),
            hovermode="closest",
            plot_bgcolor="rgba(240, 240, 245, 0.95)",
            height=700,
            margin=dict(t=50, b=50, l=50, r=50),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5
            ),
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=[
                        dict(
                            label="Play Animation",
                            method="animate",
                            args=[
                                None,
                                {
                                    "frame": {"duration": 100, "redraw": True},
                                    "fromcurrent": True,
                                },
                            ],
                        )
                    ],
                    pad={"r": 10, "t": 10},
                    showactive=False,
                    x=0.1,
                    xanchor="right",
                    y=0,
                    yanchor="top",
                ),
            ],
        )

        # Add annotation for how to interact
        fig.add_annotation(
            text="Click on a UPF node, then click at the new location to move it",
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.05,
            showarrow=False,
            font=dict(size=12),
        )

        return fig
