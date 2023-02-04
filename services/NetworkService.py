import networkx as nx

from representations import NetworkDimensions


class NetworkService:
    def __init__(self, network_dimensions: NetworkDimensions):
        self.network_dimensions = network_dimensions
        self.network = nx.grid_2d_graph(self.network_dimensions.N, self.network_dimensions.M)

    def generate_netlist(self):
        for edge in self.network.edges:
            node1 = edge[0]
            node2 = edge[1]
            gnd_node = self._get_gnd_node(network, params.network_dimention)
            voltage_input_node = list(network.nodes)[0]

            n1 = f"n{node1[0]}{node1[1]}"
            n2 = f"n{node2[0]}{node2[1]}"

            if node1 == voltage_input_node:
                n1 = "vin"

            if node1 == gnd_node:
                n1 = "gnd"

            if node2 == gnd_node:
                n2 = "gnd"

            self.state_nodes.append(f"L({node1[0]};{node1[1]})({node2[0]};{node2[1]})")
            self.connections.append((n1, n2))

    def _get_gnd_node(self, network, N):
        last_row_nodes = []
        for node in network.nodes:
            if str(N-1) in str(node[0]):
                last_row_nodes.append(node)
        return last_row_nodes[0]