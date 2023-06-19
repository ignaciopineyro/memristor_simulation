import networkx as nx
import random

from typing import Tuple, List

from constants import NetworkType, NetworkTypeNotImplemented
from representations import NetworkDimensions, DeviceParameters


class NetworkService:
    def __init__(
            self, network_dimensions: NetworkDimensions, gnd_node: Tuple[int, int] = None,
            vin_node: Tuple[int, int] = None, removal_probability: float = None, network_type: NetworkType = None
    ):
        self.network_dimensions = network_dimensions
        self.network_type = network_type or NetworkType.GRID_2D_GRAPH
        self.gnd_node = gnd_node or (self.network_dimensions.N - 1, 0)
        self.vin_node = vin_node or (0, 0)
        if removal_probability is not None and (removal_probability > 1 or removal_probability < 0):
            raise ValueError('The removal probability should be a float between 0 and 1')
        else:
            self.removal_probability = removal_probability or 0
        self.network = self.generate_network()

        self.state_nodes = []
        self.connections = []

    def generate_network(self) -> nx.Graph:
        if self.network_type == NetworkType.GRID_2D_GRAPH:
            network = nx.grid_2d_graph(self.network_dimensions.N, self.network_dimensions.M)
        else:
            raise NetworkTypeNotImplemented(
                f'Network type not implemented. Valid networks are {[network_type for network_type in NetworkType]}'
            )

        if self.removal_probability > 0:
            # EDGES_TO_REMOVE = [[(3, 0), (3, 1)], [(3, 1), (3, 2)], [(3, 2), (3, 3)]]
            for edge in list(network.edges):
                network = self._remove_network_edges_by_neighbor_nodes(network, edge)

        return network

    def _remove_network_edges_by_neighbor_nodes(self, network: nx.Graph, edge: List[Tuple[int, int]]) -> nx.Graph:
        if random.uniform(0, 1) < self.removal_probability:
            network.remove_edge(edge[0], edge[1])

        return network

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
