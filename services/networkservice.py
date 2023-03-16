from typing import Tuple

import networkx as nx

from representations import NetworkDimensions, DeviceParameters


class NetworkService:
    def __init__(
            self, network_dimensions: NetworkDimensions, gnd_node: Tuple[int, int] = None,
            vin_node: Tuple[int, int] = None
    ):
        self.network_dimensions = network_dimensions
        self.network = nx.grid_2d_graph(self.network_dimensions.N, self.network_dimensions.M)
        self.gnd_node = gnd_node or (self.network_dimensions.N - 1, 0)
        self.vin_node = vin_node or (0, 0)

        self.state_nodes = []
        self.connections = []

    def _generate_netlist(self):
        for edge in self.network.edges:
            node1 = edge[0]
            node2 = edge[1]

            n1 = f"n{node1[0]}{node1[1]}"
            n2 = f"n{node2[0]}{node2[1]}"

            if node1 == self.vin_node:
                n1 = "vin"

            elif node1 == self.gnd_node:
                n1 = "gnd"

            if node2 == self.gnd_node:
                n2 = "gnd"

            self.state_nodes.append(f"L({node1[0]};{node1[1]})({node2[0]};{node2[1]})")
            self.connections.append((n1, n2))

    def generate_device_parameters(self, device_name: str, subcircuit: str):
        self._generate_netlist()

        return [
            DeviceParameters(
                device_name, index, list(connection) + [f'l{index}'], subcircuit
            ) for index, connection in enumerate(self.connections)
        ]
