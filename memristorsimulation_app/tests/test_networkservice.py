import networkx as nx
from unittest.mock import patch
from memristorsimulation_app.constants import NetworkType, NetworkTypeNotImplemented
from memristorsimulation_app.representations import NetworkParameters, DeviceParameters
from memristorsimulation_app.services.networkservice import NetworkService
from memristorsimulation_app.tests.basetestcase import BaseTestCase


class NetworkServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_init_grid_2d_graph_basic(self):
        service = self.create_grid_network_service(n=3, m=3)

        self.assertEqual(service.network_type, NetworkType.GRID_2D_GRAPH)
        self.assertEqual(service.network_parameters.n, 3)
        self.assertEqual(service.network_parameters.m, 3)
        self.assertEqual(service.vin_plus, (0, 0))
        self.assertEqual(service.vin_minus, (2, 0))
        self.assertEqual(service.removal_probability, 0)
        self.assertIsInstance(service.network, nx.Graph)
        self.assertEqual(len(service.network.nodes), 9)

    def test_init_grid_2d_graph_with_custom_vin_nodes(self):
        network_parameters = NetworkParameters(n=4, m=4)
        service = NetworkService(
            network_type=NetworkType.GRID_2D_GRAPH,
            network_parameters=network_parameters,
            vin_plus=(0, 1),
            vin_minus=(3, 2),
            removal_probability=0,
        )

        self.assertEqual(service.vin_plus, (0, 1))
        self.assertEqual(service.vin_minus, (3, 2))

    def test_init_random_regular_graph_basic(self):
        service = self.create_random_regular_network_service(
            amount_nodes=10, amount_connections=4
        )

        self.assertEqual(service.network_type, NetworkType.RANDOM_REGULAR_GRAPH)
        self.assertEqual(service.network_parameters.amount_nodes, 10)
        self.assertEqual(service.network_parameters.amount_connections, 4)
        self.assertEqual(service.vin_plus, 0)
        self.assertEqual(service.vin_minus, 5)
        self.assertIsInstance(service.network, nx.Graph)
        self.assertEqual(len(service.network.nodes), 10)

    def test_init_watts_strogatz_graph_basic(self):
        service = self.create_watts_strogatz_network_service()

        self.assertEqual(service.network_type, NetworkType.WATTS_STROGATZ_GRAPH)
        self.assertEqual(service.network_parameters.amount_nodes, 10)
        self.assertEqual(service.network_parameters.amount_connections, 4)
        self.assertEqual(service.network_parameters.shortcut_probability, 0.3)
        self.assertEqual(service.vin_plus, 0)
        self.assertEqual(service.vin_minus, 5)
        self.assertIsInstance(service.network, nx.Graph)
        self.assertEqual(len(service.network.nodes), 10)

    def test_init_with_removal_probability(self):
        service = self.create_grid_network_service(n=3, m=3, removal_probability=0.5)

        self.assertEqual(service.removal_probability, 0.5)

        original_edges = 3 * 2 + 2 * 3
        self.assertLessEqual(len(service.network.edges), original_edges)

    def test_init_invalid_removal_probability(self):
        network_parameters = NetworkParameters(n=3, m=3)

        with self.assertRaises(ValueError) as context:
            NetworkService(
                network_type=NetworkType.GRID_2D_GRAPH,
                network_parameters=network_parameters,
                removal_probability=1.5,
            )
        self.assertIn(
            "removal_probability should be None or a float between 0 and 1",
            str(context.exception),
        )

        with self.assertRaises(ValueError) as context:
            NetworkService(
                network_type=NetworkType.GRID_2D_GRAPH,
                network_parameters=network_parameters,
                removal_probability=-0.1,
            )
        self.assertIn(
            "removal_probability should be None or a float between 0 and 1",
            str(context.exception),
        )

    def test_init_invalid_vin_types_for_grid(self):
        network_parameters = NetworkParameters(n=3, m=3)

        with self.assertRaises(ValueError) as context:
            NetworkService(
                network_type=NetworkType.GRID_2D_GRAPH,
                network_parameters=network_parameters,
                vin_plus=0,
                vin_minus=(2, 0),
            )
        self.assertIn(
            "vin_plus and vin_minus must be None or a tuple of integers",
            str(context.exception),
        )

    def test_init_invalid_vin_types_for_random_regular(self):
        network_parameters = NetworkParameters(amount_nodes=10, amount_connections=4)

        with self.assertRaises(ValueError) as context:
            NetworkService(
                network_type=NetworkType.RANDOM_REGULAR_GRAPH,
                network_parameters=network_parameters,
                vin_plus=(0, 0),
                vin_minus=5,
            )
        self.assertIn(
            "vin_plus and vin_minus must be None or integers", str(context.exception)
        )

    def test_init_missing_parameters_for_grid(self):
        with self.assertRaises(ValueError) as context:
            NetworkParameters(n=None, m=3)
            NetworkService(
                network_type=NetworkType.GRID_2D_GRAPH,
                network_parameters=NetworkParameters(n=None, m=3),
            )

    def test_init_missing_parameters_for_random_regular(self):
        with self.assertRaises(ValueError) as context:
            NetworkService(
                network_type=NetworkType.RANDOM_REGULAR_GRAPH,
                network_parameters=NetworkParameters(
                    amount_nodes=None, amount_connections=4
                ),
            )

    def test_init_missing_parameters_for_watts_strogatz(self):
        with self.assertRaises(ValueError) as context:
            NetworkService(
                network_type=NetworkType.WATTS_STROGATZ_GRAPH,
                network_parameters=NetworkParameters(
                    amount_nodes=10, amount_connections=4, shortcut_probability=None
                ),
            )

    def test_generate_network_not_implemented(self):
        with patch.object(
            NetworkType, "__iter__", return_value=iter([NetworkType.GRID_2D_GRAPH])
        ):
            network_parameters = NetworkParameters(n=3, m=3)
            service = NetworkService.__new__(NetworkService)
            service.network_type = "INVALID_TYPE"
            service.network_parameters = network_parameters
            service.removal_probability = 0

            with self.assertRaises(NetworkTypeNotImplemented) as context:
                service.generate_network()
            self.assertIn("Network type not implemented", str(context.exception))

    def test_generate_device_parameters_grid(self):

        service = self.create_grid_network_service(n=2, m=2)

        device_params = service.generate_device_parameters("xmem", "memristor")

        self.assertIsInstance(device_params, list)
        self.assertGreater(len(device_params), 0)

        for i, param in enumerate(device_params):
            self.assertIsInstance(param, DeviceParameters)
            self.assertEqual(param.device_name, "xmem")
            self.assertEqual(param.device_number, i)
            self.assertEqual(param.subcircuit, "memristor")
            self.assertEqual(len(param.nodes), 3)
            self.assertTrue(param.nodes[2].startswith("l"))

    def test_generate_device_parameters_random_regular(self):
        service = self.create_random_regular_network_service(
            amount_nodes=6, amount_connections=2
        )

        device_params = service.generate_device_parameters("xmem", "memristor")

        self.assertIsInstance(device_params, list)
        self.assertGreater(len(device_params), 0)

        for i, param in enumerate(device_params):
            self.assertIsInstance(param, DeviceParameters)
            self.assertEqual(param.device_name, "xmem")
            self.assertEqual(param.device_number, i)
            self.assertEqual(param.subcircuit, "memristor")
            self.assertEqual(len(param.nodes), 3)

    def test_generate_device_parameters_watts_strogatz(self):
        service = self.create_watts_strogatz_network_service(
            amount_nodes=6, amount_connections=2
        )

        device_params = service.generate_device_parameters("xmem", "memristor")

        self.assertIsInstance(device_params, list)
        self.assertGreater(len(device_params), 0)

        for i, param in enumerate(device_params):
            self.assertIsInstance(param, DeviceParameters)
            self.assertEqual(param.device_name, "xmem")
            self.assertEqual(param.device_number, i)
            self.assertEqual(param.subcircuit, "memristor")
            self.assertEqual(len(param.nodes), 3)

    def test_generate_device_parameters_custom_names(self):
        service = self.create_grid_network_service(n=2, m=2)

        custom_device_name = self.get_random_string()
        custom_subcircuit = self.get_random_string()

        device_params = service.generate_device_parameters(
            custom_device_name, custom_subcircuit
        )

        for param in device_params:
            self.assertEqual(param.device_name, custom_device_name)
            self.assertEqual(param.subcircuit, custom_subcircuit)

    def test_connections_property_populated_after_generate_device_parameters(self):
        service = self.create_grid_network_service(n=2, m=2)

        self.assertEqual(len(service.connections), 0)

        device_params = service.generate_device_parameters("xmem", "memristor")

        self.assertGreater(len(service.connections), 0)
        self.assertEqual(len(service.connections), len(device_params))

    def test_state_nodes_initialized(self):
        service = self.create_grid_network_service()

        self.assertIsInstance(service.state_nodes, list)
        self.assertEqual(len(service.state_nodes), 0)

    def test_network_properties_after_init(self):
        service = self.create_grid_network_service(n=3, m=4)

        self.assertEqual(len(service.network.nodes), 12)
        self.assertIsInstance(service.network, nx.Graph)

        for node in service.network.nodes:
            self.assertIsInstance(node, tuple)
            self.assertEqual(len(node), 2)
            self.assertIsInstance(node[0], int)
            self.assertIsInstance(node[1], int)

    @patch("random.uniform")
    def test_edge_removal_with_mocked_random(self, mock_random):
        mock_random.return_value = 0.1

        service = self.create_grid_network_service(n=2, m=2, removal_probability=0.5)

        original_max_edges = 2 * 1 + 1 * 2
        self.assertLessEqual(len(service.network.edges), original_max_edges)
        mock_random.assert_called()

    def test_multiple_service_instances_independent(self):
        service1 = self.create_grid_network_service(n=2, m=2)
        service2 = self.create_random_regular_network_service(
            amount_nodes=6, amount_connections=2
        )

        params1 = service1.generate_device_parameters("xmem1", "memristor1")
        params2 = service2.generate_device_parameters("xmem2", "memristor2")

        self.assertNotEqual(len(params1), len(params2))
        self.assertNotEqual(service1.network_type, service2.network_type)
        self.assertNotEqual(len(service1.connections), len(service2.connections))

    def test_should_ignore_states(self):
        small_grid_network_service = self.create_grid_network_service(n=3, m=3)
        large_grid_network_service = self.create_grid_network_service(n=6, m=6)
        self.assertFalse(small_grid_network_service.should_ignore_states())
        self.assertTrue(large_grid_network_service.should_ignore_states())

        small_rr_network_service = self.create_random_regular_network_service(
            amount_nodes=4, amount_connections=3
        )
        large_rr_network_service = self.create_random_regular_network_service(
            amount_nodes=50, amount_connections=3
        )
        self.assertFalse(small_rr_network_service.should_ignore_states())
        self.assertTrue(large_rr_network_service.should_ignore_states())

        small_ws_network_service = self.create_watts_strogatz_network_service(
            amount_nodes=4, amount_connections=3
        )
        large_ws_network_service = self.create_watts_strogatz_network_service(
            amount_nodes=50, amount_connections=3
        )
        self.assertFalse(small_ws_network_service.should_ignore_states())
        self.assertTrue(large_ws_network_service.should_ignore_states())
