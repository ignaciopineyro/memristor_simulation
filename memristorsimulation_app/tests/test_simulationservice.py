from io import BytesIO
from unittest.mock import Mock, patch
import zipfile
from memristorsimulation_app.constants import AnalysisType
from memristorsimulation_app.representations import SinWaveForm
from memristorsimulation_app.services.networkservice import NetworkService
from memristorsimulation_app.services.simulationservice import SimulationService
from memristorsimulation_app.services.ngspiceservice import NGSpiceService
from memristorsimulation_app.simulation_templates.basetemplate import BaseTemplate
from memristorsimulation_app.tests.basetestcase import BaseTestCase


class TestSimulationService(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.request_parameters = {
            "model": "pershin.sub",
            "subcircuit": {
                "model_parameters": {
                    "alpha": self.get_random_float(),
                    "beta": self.get_random_float(),
                    "rinit": self.get_random_float(),
                    "roff": self.get_random_float(),
                    "ron": self.get_random_float(),
                    "vt": self.get_random_float(),
                },
                "name": "memristor",
                "nodes": [self.get_random_string() for _ in range(3)],
            },
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
                "model_simulation_folder": "pershin_simulations",
                "folder_name": self.get_random_string(),
                "file_name": self.get_random_string(),
                "magnitudes": [self.get_random_string() for _ in range(3)],
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

        self.simulation_service = SimulationService(self.request_parameters)

    def test_parse_request_parameters(self):
        simulation_inputs = self.simulation_service.parse_request_parameters(
            self.request_parameters
        )

        # Model
        self.assertEqual(
            simulation_inputs.model.value, self.request_parameters["model"]
        )

        # Subcircuit
        self.assertEqual(
            simulation_inputs.subcircuit.model_parameters.alpha,
            self.request_parameters["subcircuit"]["model_parameters"]["alpha"],
        )
        self.assertEqual(
            simulation_inputs.subcircuit.model_parameters.beta,
            self.request_parameters["subcircuit"]["model_parameters"]["beta"],
        )
        self.assertEqual(
            simulation_inputs.subcircuit.model_parameters.rinit,
            self.request_parameters["subcircuit"]["model_parameters"]["rinit"],
        )
        self.assertEqual(
            simulation_inputs.subcircuit.model_parameters.roff,
            self.request_parameters["subcircuit"]["model_parameters"]["roff"],
        )
        self.assertEqual(
            simulation_inputs.subcircuit.model_parameters.ron,
            self.request_parameters["subcircuit"]["model_parameters"]["ron"],
        )
        self.assertEqual(
            simulation_inputs.subcircuit.model_parameters.vt,
            self.request_parameters["subcircuit"]["model_parameters"]["vt"],
        )
        self.assertEqual(
            simulation_inputs.subcircuit.name,
            self.request_parameters["subcircuit"]["name"],
        )
        self.assertEqual(
            simulation_inputs.subcircuit.nodes,
            self.request_parameters["subcircuit"]["nodes"],
        )

        # Input parameters
        self.assertEqual(
            simulation_inputs.input_parameters.source_number,
            self.request_parameters["input_parameters"]["source_number"],
        )
        self.assertEqual(
            simulation_inputs.input_parameters.n_plus,
            self.request_parameters["input_parameters"]["n_plus"],
        )
        self.assertEqual(
            simulation_inputs.input_parameters.n_minus,
            self.request_parameters["input_parameters"]["n_minus"],
        )
        wave_form = SinWaveForm(
            **self.request_parameters["input_parameters"]["wave_form"]["parameters"]
        )
        self.assertEqual(
            simulation_inputs.input_parameters.wave_form,
            wave_form,
        )

        # Simulation parameters
        analysis_type = AnalysisType(
            self.request_parameters["simulation_parameters"]["analysis_type"]
        )
        self.assertEqual(
            simulation_inputs.simulation_parameters.analysis_type,
            analysis_type,
        )
        self.assertEqual(
            simulation_inputs.simulation_parameters.tstep,
            self.request_parameters["simulation_parameters"]["tstep"],
        )
        self.assertEqual(
            simulation_inputs.simulation_parameters.tstop,
            self.request_parameters["simulation_parameters"]["tstop"],
        )
        self.assertEqual(
            simulation_inputs.simulation_parameters.tstart,
            self.request_parameters["simulation_parameters"]["tstart"],
        )
        self.assertEqual(
            simulation_inputs.simulation_parameters.tmax,
            self.request_parameters["simulation_parameters"]["tmax"],
        )
        self.assertEqual(
            simulation_inputs.simulation_parameters.uic,
            self.request_parameters["simulation_parameters"]["uic"],
        )

        # Export parameters
        self.assertEqual(
            simulation_inputs.export_parameters.model_simulation_folder.value,
            self.request_parameters["export_parameters"]["model_simulation_folder"],
        )
        self.assertEqual(
            simulation_inputs.export_parameters.folder_name.split("_")[
                0
            ],  # Folder name has timestamp appended
            self.request_parameters["export_parameters"]["folder_name"],
        )
        self.assertEqual(
            simulation_inputs.export_parameters.file_name,
            self.request_parameters["export_parameters"]["file_name"],
        )
        self.assertEqual(
            simulation_inputs.export_parameters.magnitudes,
            self.request_parameters["export_parameters"]["magnitudes"],
        )

        # Network type
        self.assertEqual(
            simulation_inputs.network_type.value,
            self.request_parameters["network_type"],
        )

        # Network parameters
        self.assertEqual(
            simulation_inputs.network_parameters.n,
            self.request_parameters["network_parameters"]["n"],
        )
        self.assertEqual(
            simulation_inputs.network_parameters.m,
            self.request_parameters["network_parameters"]["m"],
        )
        self.assertEqual(
            simulation_inputs.network_parameters.amount_connections,
            self.request_parameters["network_parameters"]["amount_connections"],
        )
        self.assertEqual(
            simulation_inputs.network_parameters.amount_nodes,
            self.request_parameters["network_parameters"]["amount_nodes"],
        )
        self.assertEqual(
            simulation_inputs.network_parameters.shortcut_probability,
            self.request_parameters["network_parameters"]["shortcut_probability"],
        )
        self.assertEqual(
            simulation_inputs.network_parameters.seed,
            self.request_parameters["network_parameters"]["seed"],
        )

        # Amount iterations
        self.assertEqual(
            simulation_inputs.amount_iterations,
            self.request_parameters["amount_iterations"],
        )

        # Plot types
        self.assertEqual(
            simulation_inputs.plot_types,
            self.request_parameters["plot_types"],
        )

    def test_create_subcircuit_file_service_from_request(self):
        sfs = self.simulation_service.create_subcircuit_file_service_from_request()

        self.assertEqual(sfs.model, self.simulation_service.simulation_inputs.model)
        self.assertEqual(
            sfs.subcircuit, self.simulation_service.simulation_inputs.subcircuit
        )
        self.assertEqual(
            sfs.sources, BaseTemplate().create_default_behavioural_source()
        )
        self.assertEqual(
            sfs.components,
            BaseTemplate().create_default_components_and_dependencies_from_model(
                self.simulation_service.simulation_inputs.model
            )[0],
        )
        self.assertEqual(
            sfs.model_dependencies,
            BaseTemplate().create_default_components_and_dependencies_from_model(
                self.simulation_service.simulation_inputs.model
            )[1],
        )
        self.assertEqual(
            sfs.directories_management_service,
            self.simulation_service.directories_management_service,
        )
        self.assertEqual(
            sfs.control_commands, [BaseTemplate().create_default_control_cmd()]
        )

    def test_create_circuit_file_service_from_request(self):
        sfs = self.simulation_service.create_subcircuit_file_service_from_request()
        cfs = self.simulation_service.create_circuit_file_service_from_request(sfs)
        network_service = NetworkService(
            self.simulation_service.simulation_inputs.network_type,
            self.simulation_service.simulation_inputs.network_parameters,
        )

        self.assertEqual(
            cfs.input_parameters,
            self.simulation_service.simulation_inputs.input_parameters,
        )
        self.assertEqual(
            cfs.device_parameters,
            BaseTemplate().create_device_parameters(
                self.simulation_service.simulation_inputs.network_type,
                network_service=network_service,
            ),
        )
        self.assertEqual(
            cfs.simulation_parameters,
            self.simulation_service.simulation_inputs.simulation_parameters,
        )
        self.assertFalse(cfs.ignore_states)
        self.assertEqual(cfs.subcircuit_file_service, sfs)
        self.assertEqual(
            cfs.directories_management_service,
            self.simulation_service.directories_management_service,
        )

    def test_simulate(self):
        mock_circuit_file_service = Mock()
        mock_subcircuit_file_service = Mock()
        mock_subcircuit = Mock()
        mock_model_parameters = Mock()
        mock_input_parameters = Mock()

        mock_circuit_file_service.subcircuit_file_service = mock_subcircuit_file_service
        mock_subcircuit_file_service.subcircuit = mock_subcircuit
        mock_subcircuit.model_parameters = mock_model_parameters
        mock_circuit_file_service.input_parameters = mock_input_parameters

        mock_ngspice_service = Mock(spec=NGSpiceService)

        with patch.object(
            self.simulation_service,
            "_build_from_request_and_write",
            return_value=mock_circuit_file_service,
        ) as mock_build:
            with patch(
                "memristorsimulation_app.services.simulationservice.NGSpiceService",
                return_value=mock_ngspice_service,
            ) as mock_ngspice_class:
                with patch.object(self.simulation_service, "plot") as mock_plot:
                    self.simulation_service.simulate()
                    mock_build.assert_called_once()
                    mock_ngspice_class.assert_called_once_with(
                        self.simulation_service.directories_management_service
                    )

                    mock_ngspice_service.run_single_circuit_simulation.assert_called_once_with(
                        self.simulation_service.simulation_inputs.amount_iterations
                    )

                    mock_plot.assert_called_once_with(
                        export_parameters=self.simulation_service.simulation_inputs.export_parameters,
                        model_parameters=mock_model_parameters,
                        input_parameters=mock_input_parameters,
                        plot_types=self.simulation_service.simulation_inputs.plot_types,
                    )

    def test_create_results_zip(self):
        mock_file_paths = [
            ("/path/to/subcircuit.sub", "subcircuit.sub"),
            ("/path/to/circuit.cir", "circuit.cir"),
            ("/path/to/results.csv", "results.csv"),
            ("/path/to/simulation.log", "simulation.log"),
            ("/path/to/figures/plot1.png", "figures/plot1.png"),
            ("/path/to/figures/plot2.png", "figures/plot2.png"),
        ]

        def mock_exists(path):
            return any(path == file_path for file_path, _ in mock_file_paths)

        with patch.object(
            self.simulation_service.directories_management_service,
            "get_all_simulation_files",
            return_value=mock_file_paths,
        ) as mock_get_files:
            with patch("os.path.exists", side_effect=mock_exists) as mock_exists_patch:
                with patch("zipfile.ZipFile") as mock_zipfile:
                    mock_zip_context = Mock()
                    mock_zipfile.return_value.__enter__.return_value = mock_zip_context
                    mock_zipfile.return_value.__exit__.return_value = None

                    result = self.simulation_service.create_results_zip()

                    mock_get_files.assert_called_once()

                    self.assertEqual(mock_exists_patch.call_count, len(mock_file_paths))
                    for file_path, _ in mock_file_paths:
                        mock_exists_patch.assert_any_call(file_path)

                    mock_zipfile.assert_called_once()
                    args, kwargs = mock_zipfile.call_args
                    self.assertEqual(
                        kwargs.get("mode", args[1] if len(args) > 1 else None), "w"
                    )
                    self.assertEqual(
                        kwargs.get("compression", args[2] if len(args) > 2 else None),
                        zipfile.ZIP_DEFLATED,
                    )

                    self.assertEqual(
                        mock_zip_context.write.call_count, len(mock_file_paths)
                    )
                    for file_path, archive_name in mock_file_paths:
                        mock_zip_context.write.assert_any_call(file_path, archive_name)

                    self.assertIsInstance(result, BytesIO)

                    self.assertEqual(result.tell(), 0)

    def test_create_results_zip_with_non_existent_files(self):
        mock_file_paths = [
            ("/path/to/existing.sub", "existing.sub"),
            ("/path/to/non_existent.cir", "non_existent.cir"),
            ("/path/to/another_existing.csv", "another_existing.csv"),
        ]

        def mock_exists(path):
            existing_files = ["/path/to/existing.sub", "/path/to/another_existing.csv"]
            return path in existing_files

        with patch.object(
            self.simulation_service.directories_management_service,
            "get_all_simulation_files",
            return_value=mock_file_paths,
        ):
            with patch("os.path.exists", side_effect=mock_exists):
                with patch("zipfile.ZipFile") as mock_zipfile:
                    mock_zip_context = Mock()
                    mock_zipfile.return_value.__enter__.return_value = mock_zip_context
                    mock_zipfile.return_value.__exit__.return_value = None

                    result = self.simulation_service.create_results_zip()

                    self.assertEqual(mock_zip_context.write.call_count, 2)
                    mock_zip_context.write.assert_any_call(
                        "/path/to/existing.sub", "existing.sub"
                    )
                    mock_zip_context.write.assert_any_call(
                        "/path/to/another_existing.csv", "another_existing.csv"
                    )

                    with self.assertRaises(AssertionError):
                        mock_zip_context.write.assert_any_call(
                            "/path/to/non_existent.cir", "non_existent.cir"
                        )

                    self.assertIsInstance(result, BytesIO)

    def test_create_results_zip_empty_file_list(self):
        with patch.object(
            self.simulation_service.directories_management_service,
            "get_all_simulation_files",
            return_value=[],
        ):
            with patch("zipfile.ZipFile") as mock_zipfile:
                mock_zip_context = Mock()
                mock_zipfile.return_value.__enter__.return_value = mock_zip_context
                mock_zipfile.return_value.__exit__.return_value = None

                result = self.simulation_service.create_results_zip()

                mock_zipfile.assert_called_once()
                mock_zip_context.write.assert_not_called()

                self.assertIsInstance(result, BytesIO)
