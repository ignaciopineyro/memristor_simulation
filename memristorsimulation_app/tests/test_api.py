from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from io import BytesIO
import zipfile
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

        # Mock de todo el proceso de simulación para evitar ejecución real
        with patch(
            "memristorsimulation_app.services.simulationservice.SimulationService.simulate_and_create_results_zip"
        ) as mock_simulate:
            # Crear un ZIP mock de respuesta
            mock_zip_buffer = BytesIO()
            with zipfile.ZipFile(
                mock_zip_buffer, "w", zipfile.ZIP_DEFLATED
            ) as zip_file:
                zip_file.writestr("test_file.txt", "contenido de prueba")
            mock_zip_buffer.seek(0)

            mock_simulate.return_value = mock_zip_buffer

            # Ejecutar la request
            response = self.client.post(url, data, format="json")

            # Verificaciones
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Verificar headers de la respuesta
            self.assertEqual(response["Content-Type"], "application/zip")
            self.assertIn("attachment", response["Content-Disposition"])
            self.assertIn(
                "simulation_test_simulation.zip", response["Content-Disposition"]
            )

            # Verificar que el contenido es un ZIP válido
            zip_content = BytesIO(response.content)
            with zipfile.ZipFile(zip_content, "r") as zip_file:
                file_list = zip_file.namelist()
                self.assertIn("test_file.txt", file_list)

            # Verificar que se llamó al método de simulación
            mock_simulate.assert_called_once()

    def test_simulation_view_invalid_json(self):
        """Test que verifica manejo de JSON inválido."""
        url = "/simulation/"

        # Enviar JSON malformado
        response = self.client.post(
            url, "invalid json content", content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid JSON", response.content.decode())

    def test_simulation_view_validation_errors(self):
        """Test que verifica manejo de errores de validación."""
        url = "/simulation/"

        # Data con campos faltantes
        invalid_data = {
            "model": "pershin.sub",
            # Faltan campos requeridos
        }

        response = self.client.post(url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verificar que la respuesta contiene errores de validación
        self.assertIn("subcircuit", response.data.keys() or response.content.decode())

    def test_simulation_view_with_simulation_error(self):
        """Test que verifica manejo de errores durante la simulación."""
        url = "/simulation/"

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

        # Mock que simula error durante la simulación
        with patch(
            "memristorsimulation_app.services.simulationservice.SimulationService.simulate_and_create_results_zip"
        ) as mock_simulate:
            mock_simulate.side_effect = Exception("Error de simulación")

            response = self.client.post(url, data, format="json")

            # Debería devolver error 500 o manejar la excepción apropiadamente
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def test_simulation_view_get_method(self):
        """Test que verifica el método GET devuelve el formulario."""
        url = "/simulation/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response, "form"
        )  # Verificar que contiene el formulario HTML

    def test_simulation_view_content_length_header(self):
        """Test que verifica que se establece correctamente el Content-Length."""
        url = "/simulation/"

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
            # Crear ZIP con contenido conocido
            mock_zip_buffer = BytesIO()
            test_content = "contenido de prueba para verificar tamaño"
            with zipfile.ZipFile(
                mock_zip_buffer, "w", zipfile.ZIP_DEFLATED
            ) as zip_file:
                zip_file.writestr("test_file.txt", test_content)
            mock_zip_buffer.seek(0)

            mock_simulate.return_value = mock_zip_buffer

            response = self.client.post(url, data, format="json")

            # Verificar que Content-Length coincide con el tamaño real del contenido
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(int(response["Content-Length"]), len(response.content))

            # Verificar que el contenido no está vacío
            self.assertGreater(len(response.content), 0)
