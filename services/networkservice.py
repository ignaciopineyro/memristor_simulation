import networkx as nx
import random

from typing import Tuple, List
from constants import NetworkType, NetworkTypeNotImplemented
from representations import NetworkParameters, DeviceParameters


class NetworkService:
    def __init__(
            self, network_type: NetworkType, network_parameters: NetworkParameters, gnd_node: Tuple[int, int] = None,
            vin_node: Tuple[int, int] = None, removal_probability: float = None
    ):
        self.network_parameters = network_parameters
        self.network_type = network_type
        self.removal_probability = removal_probability or 0
        self._run_network_checks()

        if self.network_type == NetworkType.GRID_2D_GRAPH:
            if (isinstance(vin_node, tuple) or vin_node is None) and (isinstance(gnd_node, tuple) or gnd_node is None):
                self.vin_node = vin_node or (0, 0)
                self.gnd_node = gnd_node or (self.network_parameters.N - 1, 0)
            else:
                raise ValueError(
                    f'NetworkService vin_node and gnd_node must be None or a tuple of integers for '
                    f'NetworkType.GRID_2D_GRAPH vin_node={vin_node} and gnd_node={gnd_node} were received instead'
                )
        else:
            if (isinstance(vin_node, int) or vin_node is None) and (isinstance(gnd_node, int) or gnd_node is None):
                self.vin_node = vin_node or 0
                self.gnd_node = gnd_node or round(self.network_parameters.amount_nodes / 2)
            else:
                raise ValueError(
                    f'NetworkService vin_node and gnd_node must be None or integers but vin_node={vin_node} and '
                    f'gnd_node={gnd_node} were received instead'
                )

        self.network = self.generate_network()
        self.state_nodes = []
        self.connections = []

    def _run_network_checks(self):
        if self.removal_probability > 1 or self.removal_probability < 0:
            raise ValueError(
                f'NetworkService removal_probability should be None or a float between 0 and 1 but '
                f'removal_probability={self.removal_probability} was received instead'
            )

        if self.network_type == NetworkType.GRID_2D_GRAPH:
            if self.network_parameters.N is None or self.network_parameters.N is None:
                raise ValueError(
                    f'NetworkService parameters "N" and "M" need to be an int > 0 for NetworkType.GRID_2D_GRAPH but '
                    f'N={self.network_parameters.N} M={self.network_parameters.M} were received instead'
                )

        if self.network_type == NetworkType.RANDOM_REGULAR_GRAPH:
            if self.network_parameters.amount_connections is None or self.network_parameters.amount_nodes is None:
                raise ValueError(
                    'NetworkService parameters "amount_connections" and "amount_nodes" cannot be None for '
                    'NetworkType.RANDOM_REGULAR_GRAPH'
                )

        if self.network_type == NetworkType.WATTS_STROGATZ_GRAPH:
            if (
                self.network_parameters.amount_connections is None or
                self.network_parameters.amount_nodes is None or
                self.network_parameters.shortcut_probability is None
            ):
                raise ValueError(
                    'NetworkService parameters "amount_connections", "amount_nodes" and "shortcut_probability" cannot be None for '
                    'NetworkType.RANDOM_REGULAR_GRAPH'
                )

    def generate_network(self) -> nx.Graph:
        if self.network_type == NetworkType.GRID_2D_GRAPH:
            network = nx.grid_2d_graph(self.network_parameters.N, self.network_parameters.M)
        elif self.network_type == NetworkType.RANDOM_REGULAR_GRAPH:
            network = nx.random_regular_graph(
                self.network_parameters.amount_connections, self.network_parameters.amount_nodes
            )
        elif self.network_type == NetworkType.WATTS_STROGATZ_GRAPH:
            network = nx.watts_strogatz_graph(
                self.network_parameters.amount_nodes, self.network_parameters.amount_connections,
                self.network_parameters.shortcut_probability
            )
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

            if self.network_type == NetworkType.GRID_2D_GRAPH:
                n1 = f"n{node1[0]}{node1[1]}"
                n2 = f"n{node2[0]}{node2[1]}"

            else:
                n1 = f"n{node1}"
                n2 = f"n{node2}"

            if node1 == self.vin_node:
                n1 = "vin"

            elif node1 == self.gnd_node:
                n1 = "gnd"

            if node2 == self.vin_node:
                n2 = "vin"

            elif node2 == self.gnd_node:
                n2 = "gnd"

            self.connections.append((n1, n2))

    def generate_device_parameters(self, device_name: str, subcircuit: str) -> List[DeviceParameters]:
        self._generate_netlist()

        return [
            DeviceParameters(
                device_name, index, list(connection) + [f'l{index}'], subcircuit
            ) for index, connection in enumerate(self.connections)
        ]
