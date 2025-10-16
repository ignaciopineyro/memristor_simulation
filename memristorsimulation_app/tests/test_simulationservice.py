from typing import List
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
                "vt": self.get_random_float()
            },
            "magnitudes": [
                self.get_random_string(),
                self.get_random_string(),
                self.get_random_string(),
            ],
            "subcircuit": {
                "parameters": {},
                "name": str,
                "nodes": List[str]
            } Subcircuit,
            "input_parameters": InputParameters
            "simulation_parameters": SimulationParameters
            "export_parameters": ExportParameters
            "wave": Wave
            "network_type": NetworkType
            "amount_iterations": int = 1
            "network_parameters": NetworkParameters = None
            "plot_types": List[PlotType] = None
        }

    def test_parse_request_parameters(): ...

    def test_create_subcircuit_file_service_from_request(): ...

    def test_create_circuit_file_service_from_request(): ...

    def test_simulate(): ...

    def test_build_and_write(): ...
