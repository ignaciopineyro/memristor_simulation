import zipfile

from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from io import BytesIO
from memristorsimulation_app.tests.basetestcase import BaseTestCase


class UserAPITestCase(APITestCase, BaseTestCase):
    def test_simulation_view(self):
        url = ""

        data = {
            "model": "pershin.sub",
            "subcircuit": {
                "model_parameters": {
                    "alpha": 0.0,
                    "beta": 500000.0,
                    "rinit": 200000.0,
                    "roff": 200000.0,
                    "ron": 2000.0,
                    "vt": 0.6,
                },
                "name": "memristor",
                "nodes": ["vin", "0", "x"],
            },
            "input_parameters": {
                "source_number": 1,
                "n_plus": "vin",
                "n_minus": "0",
                "wave_form": {
                    "type": "sin",
                    "parameters": {
                        "vo": 0.0,
                        "amplitude": 1.0,
                        "frequency": 1000.0,
                        "td": 0.0,
                        "theta": 0.0,
                        "phase": 0.0,
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
                "model_simulation_folder": "pershin_simulations",
                "folder_name": "test_simulation",
                "file_name": "test_results",
                "magnitudes": ["v(vin)", "i(v1)", "v(x)"],
            },
            "network_type": "GRID_2D_GRAPH",
            "network_parameters": {
                "n": 4,
                "m": 4,
                "amount_connections": 8,
                "amount_nodes": 16,
                "shortcut_probability": 0.1,
                "seed": 42,
            },
            "amount_iterations": 1,
            "plot_types": ["IV", "IV_LOG"],
        }

        with patch(
            "memristorsimulation_app.services.simulationservice.SimulationService.simulate_and_create_results_zip"
        ) as mock_simulate:
            mock_zip_buffer = BytesIO()
            with zipfile.ZipFile(
                mock_zip_buffer, "w", zipfile.ZIP_DEFLATED
            ) as zip_file:
                zip_file.writestr("test_file.txt", "contenido de prueba")
            mock_zip_buffer.seek(0)

            mock_simulate.return_value = mock_zip_buffer

            response = self.client.post(url, data, format="json")

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response["Content-Type"], "application/zip")
            self.assertIn("attachment", response["Content-Disposition"])
            self.assertIn("simulation_test_simulation", response["Content-Disposition"])
            self.assertIn(".zip", response["Content-Disposition"])

            zip_content = BytesIO(response.content)
            with zipfile.ZipFile(zip_content, "r") as zip_file:
                file_list = zip_file.namelist()
                self.assertIn("test_file.txt", file_list)

            mock_simulate.assert_called_once()

    def test_simulation_view_invalid_json(self):
        url = ""

        response = self.client.post(
            url, "invalid json content", content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid JSON", response.content.decode())

    def test_simulation_view_validation_errors(self):
        url = ""

        invalid_data = {
            "model": "pershin.sub",
        }

        response = self.client.post(url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("subcircuit", response.data.keys() or response.content.decode())

    def test_simulation_view_with_simulation_error(self):
        url = ""

        data = {
            "model": "pershin.sub",
            "subcircuit": {
                "model_parameters": {
                    "alpha": 0.0,
                    "beta": 500000.0,
                    "rinit": 200000.0,
                    "roff": 200000.0,
                    "ron": 2000.0,
                    "vt": 0.6,
                },
                "name": "memristor",
                "nodes": ["vin", "0", "x"],
            },
            "input_parameters": {
                "source_number": 1,
                "n_plus": "vin",
                "n_minus": "0",
                "wave_form": {
                    "type": "sin",
                    "parameters": {
                        "vo": 0.0,
                        "amplitude": 1.0,
                        "frequency": 1000.0,
                        "td": 0.0,
                        "theta": 0.0,
                        "phase": 0.0,
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
                "model_simulation_folder": "pershin_simulations",
                "folder_name": "test_simulation",
                "file_name": "test_results",
                "magnitudes": ["v(vin)", "i(v1)", "v(x)"],
            },
            "network_type": "GRID_2D_GRAPH",
            "network_parameters": {
                "n": 4,
                "m": 4,
                "amount_connections": 8,
                "amount_nodes": 16,
                "shortcut_probability": 0.1,
                "seed": 42,
            },
            "amount_iterations": 1,
            "plot_types": ["IV", "IV_LOG"],
        }

        with patch(
            "memristorsimulation_app.services.simulationservice.SimulationService.simulate_and_create_results_zip"
        ) as mock_simulate:
            mock_simulate.side_effect = Exception("Error de simulación")

            response = self.client.post(url, data, format="json")

            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def test_simulation_view_get_method(self):
        url = ""

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "form")

    def test_simulation_view_content_length_header(self):
        url = ""

        data = {
            "model": "pershin.sub",
            "subcircuit": {
                "model_parameters": {
                    "alpha": 0.0,
                    "beta": 500000.0,
                    "rinit": 200000.0,
                    "roff": 200000.0,
                    "ron": 2000.0,
                    "vt": 0.6,
                },
                "name": "memristor",
                "nodes": ["vin", "0", "x"],
            },
            "input_parameters": {
                "source_number": 1,
                "n_plus": "vin",
                "n_minus": "0",
                "wave_form": {
                    "type": "sin",
                    "parameters": {
                        "vo": 0.0,
                        "amplitude": 1.0,
                        "frequency": 1000.0,
                        "td": 0.0,
                        "theta": 0.0,
                        "phase": 0.0,
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
                "model_simulation_folder": "pershin_simulations",
                "folder_name": "test_simulation",
                "file_name": "test_results",
                "magnitudes": ["v(vin)", "i(v1)", "v(x)"],
            },
            "network_type": "GRID_2D_GRAPH",
            "network_parameters": {
                "n": 4,
                "m": 4,
                "amount_connections": 8,
                "amount_nodes": 16,
                "shortcut_probability": 0.1,
                "seed": 42,
            },
            "amount_iterations": 1,
            "plot_types": ["IV", "IV_LOG"],
        }

        with patch(
            "memristorsimulation_app.services.simulationservice.SimulationService.simulate_and_create_results_zip"
        ) as mock_simulate:
            mock_zip_buffer = BytesIO()
            test_content = "Test content"
            with zipfile.ZipFile(
                mock_zip_buffer, "w", zipfile.ZIP_DEFLATED
            ) as zip_file:
                zip_file.writestr("test_file.txt", test_content)
            mock_zip_buffer.seek(0)

            mock_simulate.return_value = mock_zip_buffer

            response = self.client.post(url, data, format="json")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(int(response["Content-Length"]), len(response.content))
            self.assertGreater(len(response.content), 0)
