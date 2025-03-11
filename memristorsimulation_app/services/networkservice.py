import networkx as nx
import random

from typing import Tuple, List, Union
from memristorsimulation_app.constants import NetworkType, NetworkTypeNotImplemented
from memristorsimulation_app.representations import NetworkParameters, DeviceParameters


class NetworkService:
    def __init__(
        self,
        network_type: NetworkType,
        network_parameters: NetworkParameters,
        vin_minus: Union[int, Tuple[int, int]] = None,
        vin_plus: Union[int, Tuple[int, int]] = None,
        removal_probability: float = None,
    ):
        self.network_parameters = network_parameters
        self.network_type = network_type
        self.removal_probability = removal_probability or 0
        self._run_network_checks()

        if self.network_type == NetworkType.GRID_2D_GRAPH:
            if (isinstance(vin_plus, tuple) or vin_plus is None) and (
                isinstance(vin_minus, tuple) or vin_minus is None
            ):
                self.vin_plus = vin_plus or (0, 0)
                self.vin_minus = vin_minus or (self.network_parameters.n - 1, 0)
            else:
                raise ValueError(
                    f"NetworkService vin_plus and vin_minus must be None or a tuple of integers for "
                    f"NetworkType.GRID_2D_GRAPH vin_plus={vin_plus} and vin_minus={vin_minus} were received instead"
                )
        else:
            if (isinstance(vin_plus, int) or vin_plus is None) and (
                isinstance(vin_minus, int) or vin_minus is None
            ):
                self.vin_plus = vin_plus or 0
                self.vin_minus = vin_minus or round(
                    self.network_parameters.amount_nodes / 2
                )
            else:
                raise ValueError(
                    f"NetworkService vin_plus and vin_minus must be None or integers but vin_plus={vin_plus} and "
                    f"vin_minus={vin_minus} were received instead"
                )

        self.network = self.generate_network()
        self.state_nodes = []
        self.connections = []

    def _run_network_checks(self):
        if self.removal_probability > 1 or self.removal_probability < 0:
            raise ValueError(
                f"NetworkService removal_probability should be None or a float between 0 and 1 but "
                f"removal_probability={self.removal_probability} was received instead"
            )

        if self.network_type == NetworkType.GRID_2D_GRAPH:
            if self.network_parameters.n is None or self.network_parameters.m is None:
                raise ValueError(
                    f'NetworkService parameters "N" and "M" need to be an int > 0 for NetworkType.GRID_2D_GRAPH but '
                    f"N={self.network_parameters.n} M={self.network_parameters.m} were received instead"
                )

        if self.network_type == NetworkType.RANDOM_REGULAR_GRAPH:
            if (
                self.network_parameters.amount_connections is None
                or self.network_parameters.amount_nodes is None
            ):
                raise ValueError(
                    'NetworkService parameters "amount_connections" and "amount_nodes" cannot be None for '
                    "NetworkType.RANDOM_REGULAR_GRAPH"
                )

        if self.network_type == NetworkType.WATTS_STROGATZ_GRAPH:
            if (
                self.network_parameters.amount_connections is None
                or self.network_parameters.amount_nodes is None
                or self.network_parameters.shortcut_probability is None
            ):
                raise ValueError(
                    'NetworkService parameters "amount_connections", "amount_nodes" and "shortcut_probability" cannot '
                    "be None for NetworkType.RANDOM_REGULAR_GRAPH"
                )

    def generate_network(self) -> nx.Graph:
        if self.network_type == NetworkType.GRID_2D_GRAPH:
            network = nx.grid_2d_graph(
                self.network_parameters.n, self.network_parameters.m
            )
        elif self.network_type == NetworkType.RANDOM_REGULAR_GRAPH:
            network = nx.random_regular_graph(
                self.network_parameters.amount_connections,
                self.network_parameters.amount_nodes,
                seed=self.network_parameters.seed,
            )
        elif self.network_type == NetworkType.WATTS_STROGATZ_GRAPH:
            network = nx.watts_strogatz_graph(
                self.network_parameters.amount_nodes,
                self.network_parameters.amount_connections,
                self.network_parameters.shortcut_probability,
                seed=self.network_parameters.seed,
            )
        else:
            raise NetworkTypeNotImplemented(
                f"Network type not implemented. Valid networks are {[network_type for network_type in NetworkType]}"
            )

        if self.removal_probability > 0:
            for edge in list(network.edges):
                network = self._remove_network_edges_by_neighbor_nodes(network, edge)

        return network

    def _remove_network_edges_by_neighbor_nodes(
        self, network: nx.Graph, edge: List[Tuple[int, int]]
    ) -> nx.Graph:
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

            if node1 == self.vin_plus:
                n1 = "vin"

            elif node1 == self.vin_minus:
                n1 = "gnd"

            if node2 == self.vin_plus:
                n2 = "vin"

            elif node2 == self.vin_minus:
                n2 = "gnd"

            self.connections.append((n1, n2))

    def generate_device_parameters(
        self, device_name: str, subcircuit: str
    ) -> List[DeviceParameters]:
        self._generate_netlist()

        return [
            DeviceParameters(
                device_name, index, list(connection) + [f"l{index}"], subcircuit
            )
            for index, connection in enumerate(self.connections)
        ]
