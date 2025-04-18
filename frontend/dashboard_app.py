import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import numpy as np


class Dashboard:
    def __init__(
        self,
        network,
        latency_calculator,
        reliability_analyzer,
        upf_optimizer,
        packet_generator,
        visualizer,
    ):
        self.network = network
        self.latency_calculator = latency_calculator
        self.reliability_analyzer = reliability_analyzer
        self.upf_optimizer = upf_optimizer
        self.packet_generator = packet_generator
        self.visualizer = visualizer

        # Initial state
        self.selected_upf = -1
        self.latencies = None
        self.reliabilities = None
        self.packet_data = None

        # Calculate initial metrics
        self.update_metrics()

        # Create Dash app
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.setup_layout()
        self.setup_callbacks()

    def update_metrics(self):
        """Update all network metrics"""
        ue_gnb_dist, gnb_upf_dist = self.network.update_associations()
        self.latencies = self.latency_calculator.calculate_latencies(
            self.network, ue_gnb_dist, gnb_upf_dist
        )
        self.reliabilities = self.reliability_analyzer.calculate_reliability(
            self.network, ue_gnb_dist, gnb_upf_dist
        )
        self.packet_data = self.packet_generator.generate_packets(self.network)

    def setup_layout(self):
        """Set up the Dash layout"""
        self.app.layout = html.Div(
            [
                # Header section
                html.Div(
                    [
                        html.H1(
                            "5G URLLC Network Optimization",
                            style={"margin-bottom": "5px", "text-align": "center"},
                        ),
                        # Latency and reliability stats
                        html.Div(
                            [
                                html.Div(id="latency-stats", style={"flex": "1"}),
                                html.Div(id="reliability-stats", style={"flex": "1"}),
                            ],
                            style={
                                "display": "flex",
                                "margin": "10px 0",
                                "gap": "20px",
                            },
                        ),
                        # Instructions for the user
                        html.Div(
                            [
                                html.H4("Mode d'emploi:"),
                                html.Ul(
                                    [
                                        html.Li(
                                            "1. Cliquez sur un UPF (carré bleu) pour le sélectionner"
                                        ),
                                        html.Li(
                                            "2. Cliquez à un nouvel emplacement pour y déplacer l'UPF"
                                        ),
                                        html.Li(
                                            "3. Utilisez le bouton 'Optimize UPF Placement' pour placer automatiquement les UPFs"
                                        ),
                                    ]
                                ),
                                html.P(
                                    "Note: Désactivez le mode zoom pour faciliter la sélection",
                                    style={"font-weight": "bold", "color": "red"},
                                ),
                            ],
                            style={
                                "margin": "10px 0",
                                "padding": "10px",
                                "background-color": "#e8f5e9",
                                "border-radius": "5px",
                            },
                        ),
                        # Control buttons
                        html.Div(
                            [
                                html.Button(
                                    "Optimize UPF Placement",
                                    id="optimize-btn",
                                    n_clicks=0,
                                    style={
                                        "margin": "5px",
                                        "padding": "10px",
                                        "background-color": "#4CAF50",
                                        "color": "white",
                                        "border": "none",
                                        "border-radius": "4px",
                                    },
                                ),
                                html.Button(
                                    "Randomize UPF Positions",
                                    id="randomize-btn",
                                    n_clicks=0,
                                    style={
                                        "margin": "5px",
                                        "padding": "10px",
                                        "background-color": "#2196F3",
                                        "color": "white",
                                        "border": "none",
                                        "border-radius": "4px",
                                    },
                                ),
                                html.Button(
                                    "Generate New Packets",
                                    id="packets-btn",
                                    n_clicks=0,
                                    style={
                                        "margin": "5px",
                                        "padding": "10px",
                                        "background-color": "#ff9800",
                                        "color": "white",
                                        "border": "none",
                                        "border-radius": "4px",
                                    },
                                ),
                            ],
                            style={"text-align": "center", "margin": "10px 0"},
                        ),
                    ]
                ),
                # Graph section
                html.Div(
                    [
                        dcc.Graph(
                            id="network-graph",
                            figure=self.visualizer.create_figure(
                                self.network, self.packet_data, self.latencies
                            ),
                            config={
                                "displayModeBar": True,
                                "scrollZoom": False,
                                "modeBarButtonsToRemove": [
                                    "zoomIn",
                                    "zoomOut",
                                    "resetScale",
                                ],
                            },
                            style={"height": "700px"},
                        ),
                    ],
                    style={"margin": "10px 0"},
                ),
                # Hidden divs for state management
                html.Div(id="selected-upf", style={"display": "none"}, children="-1"),
                dcc.Store(id="upf-positions", data=self.network.upf_positions.tolist()),
                dcc.Interval(
                    id="interval-component",
                    interval=1000,  # ms
                    n_intervals=0,
                    disabled=False,
                ),
            ],
            style={"max-width": "1200px", "margin": "0 auto", "padding": "20px"},
        )

    def setup_callbacks(self):
        """Set up all Dash callbacks"""

        @self.app.callback(
            Output("latency-stats", "children"), [Input("network-graph", "figure")]
        )
        def update_latency_stats(figure):
            stats = self.latency_calculator.get_latency_stats(self.latencies)

            return html.Div(
                [
                    html.H3(
                        "Latency Statistics",
                        style={"margin": "0", "text-align": "center"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong("Average: "),
                                    html.Span(
                                        f"{stats['average']:.3f} ms",
                                        style={"color": "blue", "font-weight": "bold"},
                                    ),
                                ],
                                style={"display": "inline-block", "margin": "0 20px"},
                            ),
                            html.Div(
                                [
                                    html.Strong("Minimum: "),
                                    html.Span(
                                        f"{stats['minimum']:.3f} ms",
                                        style={"color": "green", "font-weight": "bold"},
                                    ),
                                ],
                                style={"display": "inline-block", "margin": "0 20px"},
                            ),
                            html.Div(
                                [
                                    html.Strong("Maximum: "),
                                    html.Span(
                                        f"{stats['maximum']:.3f} ms",
                                        style={"color": "red", "font-weight": "bold"},
                                    ),
                                ],
                                style={"display": "inline-block", "margin": "0 20px"},
                            ),
                        ],
                        style={"text-align": "center", "margin-top": "5px"},
                    ),
                    html.Progress(
                        value=stats["average"],
                        max="1",  # 1ms as maximum acceptable latency
                        style={"width": "100%", "height": "10px", "margin-top": "10px"},
                    ),
                    html.Div(
                        f"URLLC Target (1ms): {'Achieved' if stats['urllc_target_achieved'] else 'Not Achieved'}",
                        style={
                            "text-align": "center",
                            "margin-top": "5px",
                            "color": "green"
                            if stats["urllc_target_achieved"]
                            else "red",
                            "font-weight": "bold",
                        },
                    ),
                ],
                style={
                    "background-color": "#f1f8e9",
                    "padding": "10px",
                    "border-radius": "5px",
                    "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                },
            )

        @self.app.callback(
            Output("reliability-stats", "children"), [Input("network-graph", "figure")]
        )
        def update_reliability_stats(figure):
            stats = self.reliability_analyzer.get_reliability_stats(self.reliabilities)

            return html.Div(
                [
                    html.H3(
                        "Reliability Statistics",
                        style={"margin": "0", "text-align": "center"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong("Average: "),
                                    html.Span(
                                        f"{stats['average']:.6f}",
                                        style={"color": "blue", "font-weight": "bold"},
                                    ),
                                ],
                                style={"display": "inline-block", "margin": "0 20px"},
                            ),
                            html.Div(
                                [
                                    html.Strong("Minimum: "),
                                    html.Span(
                                        f"{stats['minimum']:.6f}",
                                        style={"color": "green", "font-weight": "bold"},
                                    ),
                                ],
                                style={"display": "inline-block", "margin": "0 20px"},
                            ),
                            html.Div(
                                [
                                    html.Strong("Maximum: "),
                                    html.Span(
                                        f"{stats['maximum']:.6f}",
                                        style={"color": "red", "font-weight": "bold"},
                                    ),
                                ],
                                style={"display": "inline-block", "margin": "0 20px"},
                            ),
                        ],
                        style={"text-align": "center", "margin-top": "5px"},
                    ),
                    html.Progress(
                        value=min(
                            stats["minimum"] * 100000, 100
                        ),  # Scale up for visibility
                        max="100",
                        style={"width": "100%", "height": "10px", "margin-top": "10px"},
                    ),
                    html.Div(
                        f"URLLC Target (99.999%): {'Achieved' if stats['urllc_target_achieved'] else 'Not Achieved'}",
                        style={
                            "text-align": "center",
                            "margin-top": "5px",
                            "color": "green"
                            if stats["urllc_target_achieved"]
                            else "red",
                            "font-weight": "bold",
                        },
                    ),
                ],
                style={
                    "background-color": "#e3f2fd",
                    "padding": "10px",
                    "border-radius": "5px",
                    "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
                },
            )

        @self.app.callback(
            [
                Output("network-graph", "figure"),
                Output("selected-upf", "children"),
                Output("upf-positions", "data"),
            ],
            [
                Input("network-graph", "clickData"),
                Input("optimize-btn", "n_clicks"),
                Input("randomize-btn", "n_clicks"),
                Input("packets-btn", "n_clicks"),
                Input("interval-component", "n_intervals"),
            ],
            [
                State("selected-upf", "children"),
                State("upf-positions", "data"),
            ],
        )
        def update_graph(
            clickData,
            optimize_clicks,
            randomize_clicks,
            packets_clicks,
            n_intervals,
            selected_upf,
            stored_positions,
        ):
            ctx = dash.callback_context

            # Load stored UPF positions if available
            if stored_positions:
                self.network.upf_positions = np.array(stored_positions)

            if not ctx.triggered:
                return (
                    self.visualizer.create_figure(
                        self.network, self.packet_data, self.latencies
                    ),
                    "-1",
                    self.network.upf_positions.tolist(),
                )

            # Identify which input triggered the callback
            triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if triggered_id == "optimize-btn":
                # Run optimization algorithm
                self.upf_optimizer.optimize(self.network)
                self.update_metrics()
                selected_upf = "-1"  # Reset selection after optimization

            elif triggered_id == "randomize-btn":
                # Randomize UPF positions
                self.network.randomize_upf_positions()
                self.update_metrics()
                selected_upf = "-1"  # Reset selection after randomization

            elif triggered_id == "packets-btn":
                # Generate new packet data
                self.packet_data = self.packet_generator.generate_packets(self.network)

            elif triggered_id == "interval-component":
                # Update packets for animation
                if (
                    n_intervals % 2 == 0
                ):  # Only update every other interval to reduce load
                    self.packet_data = self.packet_generator.generate_packets(
                        self.network
                    )

            elif triggered_id == "network-graph" and clickData:
                curr_selected = int(selected_upf)

                # Check what was clicked
                if "points" not in clickData:
                    return (
                        self.visualizer.create_figure(
                            self.network,
                            self.packet_data,
                            self.latencies,
                            selected_upf=curr_selected if curr_selected >= 0 else -1,
                        ),
                        selected_upf,
                        self.network.upf_positions.tolist(),
                    )

                point = clickData["points"][0]

                if "curveNumber" not in point:
                    return (
                        self.visualizer.create_figure(
                            self.network,
                            self.packet_data,
                            self.latencies,
                            selected_upf=curr_selected if curr_selected >= 0 else -1,
                        ),
                        selected_upf,
                        self.network.upf_positions.tolist(),
                    )

                curve_number = point["curveNumber"]

                # If a UPF was clicked (UPF is trace index 2)
                if curve_number == 2 and "pointIndex" in point:
                    # Select this UPF
                    new_selected = point["pointIndex"]
                    return (
                        self.visualizer.create_figure(
                            self.network,
                            self.packet_data,
                            self.latencies,
                            selected_upf=new_selected,
                        ),
                        str(new_selected),
                        self.network.upf_positions.tolist(),
                    )

                # If something else was clicked while a UPF is selected
                elif curr_selected >= 0:
                    # Move the selected UPF to the clicked location
                    if "x" in point and "y" in point:
                        x, y = point["x"], point["y"]
                        self.network.upf_positions[curr_selected] = [x, y]
                        self.update_metrics()
                        selected_upf = "-1"  # Deselect after moving

            # Create the figure with potentially updated data
            fig = self.visualizer.create_figure(
                self.network,
                self.packet_data,
                self.latencies,
                selected_upf=int(selected_upf) if selected_upf != "-1" else -1,
            )

            return (
                fig,
                selected_upf,
                self.network.upf_positions.tolist(),
            )

    def run(self, debug=True, port=8050):
        """Run the Dash application"""
        self.app.run(debug=debug, port=port)
