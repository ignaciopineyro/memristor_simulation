from memristorsimulation_app.services.simulationservice import SimulationService
from memristorsimulation_app.tests.basetestcase import BaseTestCase


class TestSimulationService(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.request_parameters = {
            "model": "pershin.sub",
            "model_parameters": {
                "alpha": self.get_random_float(),
                "beta": self.get_random_float(),
                "rinit": self.get_random_float(),
                "roff": self.get_random_float(),
                "ron": self.get_random_float(),
                "vt": self.get_random_float(),
            },
            "magnitudes": [self.get_random_string() for _ in range(3)],
            "input_parameters": {
                "source_number": self.get_random_int(),
                "n_plus": self.get_random_string(),
                "n_minus": self.get_random_string(),
                "wave_form": {
                    "type": "sin",
                    "parameters": {
                        "vo": self.get_random_float(),
                        "amplitude": self.get_random_float(),
                        "frequency": self.get_random_float(),
                        "td": self.get_random_float(),
                        "theta": self.get_random_float(),
                        "phase": self.get_random_float(),
                    },
                },
            },
            "simulation_parameters": {
                "analysis_type": ".tran",
                "tstep": 1e-9,
                "tstop": 1e-6,
                "tstart": 0,
                "tmax": 1e-6,
                "uic": True,
            },
            "export_parameters": {
                "model_simulation_folder_name": "pershin_simulations",  # TODO: Use other enums
                "folder_name": self.get_random_string(),
                "file_name": self.get_random_string(),
                "magnitudes": [self.get_random_string() for _ in range(3)],
            },
            "network_type": "SINGLE_DEVICE",  # TODO: Use other enums
            "amount_iterations": 1,
            "network_parameters": {},  # TODO: Use network parameters
            "plot_types": ["IV", "IV_LOG"],
        }

        self.simulation_service = SimulationService(self.request_parameters)

    def test_parse_request_parameters(self):
        simulation_inputs = self.simulation_service.parse_request_parameters()

        self.assertEqual(
            simulation_inputs.model.value, self.request_parameters["model"]
        )
        self.assertEqual(
            simulation_inputs.model_parameters.alpha,
            self.request_parameters["model_parameters"]["alpha"],
        )
        self.assertEqual(
            simulation_inputs.input_parameters.source_number,
            self.request_parameters["input_parameters"]["source_number"],
        )
        self.assertEqual(
            simulation_inputs.simulation_parameters.tstep,
            self.request_parameters["simulation_parameters"]["tstep"],
        )
        self.assertEqual(
            simulation_inputs.export_parameters.folder_name,
            self.request_parameters["export_parameters"]["folder_name"],
        )
        self.assertEqual(
            simulation_inputs.network_type.value,
            self.request_parameters["network_type"],
        )
        self.assertEqual(
            simulation_inputs.amount_iterations,
            self.request_parameters["amount_iterations"],
        )
        self.assertEqual(
            simulation_inputs.network_parameters,
            None,
        )

    def test_create_subcircuit_file_service_from_request(): ...

    def test_create_circuit_file_service_from_request(): ...

    def test_simulate(): ...

    def test_build_and_write(): ...
