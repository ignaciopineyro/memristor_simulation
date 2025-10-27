import os

from pyparsing import Optional
from memristorsimulation_app.constants import (
    SIMULATIONS_DIR,
    MemristorModels,
    ModelsSimulationFolders,
)
from memristorsimulation_app.representations import ExportParameters
from memristorsimulation_app.services.directoriesmanagementservice import (
    DirectoriesManagementService,
)
from memristorsimulation_app.tests.basetestcase import BaseTestCase


class DirectoriesManagementServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def _create_export_parameters(
        self, model_simulation_folder: ModelsSimulationFolders
    ) -> ExportParameters:
        return ExportParameters(
            model_simulation_folder=model_simulation_folder,
            folder_name=self.get_random_string(),
            file_name=self.get_random_string(),
            magnitudes=[],
        )

    def test_create_simulation_results_for_model_folder_if_not_exists(self):
        for model in MemristorModels:
            model_folder_name = ModelsSimulationFolders.get_simulation_folder_by_model(
                model
            ).value
            expected_dir = f"{SIMULATIONS_DIR}/{model_folder_name}"

            self.assertFalse(os.path.exists(expected_dir))

            DirectoriesManagementService.create_simulation_results_for_model_folder_if_not_exists(
                model
            )

            self.assertTrue(os.path.exists(expected_dir))
            self.assertTrue(os.path.isdir(expected_dir))

            DirectoriesManagementService.create_simulation_results_for_model_folder_if_not_exists(
                model
            )
            self.assertTrue(os.path.exists(expected_dir))

    def test_create_simulation_parameter_folder_if_not_exist(self):
        for model, model_sim_folder in zip(MemristorModels, ModelsSimulationFolders):
            export_params = self._create_export_parameters(
                model_simulation_folder=model_sim_folder
            )
            model_folder_name = ModelsSimulationFolders.get_simulation_folder_by_model(
                model
            ).value
            expected_dir = (
                f"{SIMULATIONS_DIR}/{model_folder_name}/{export_params.folder_name}"
            )

            self.assertFalse(os.path.exists(expected_dir))
            dms = DirectoriesManagementService(
                model=model,
                export_parameters=export_params,
            )
            dms.create_simulation_parameter_folder_if_not_exist(
                export_params.model_simulation_folder
            )

            self.assertTrue(os.path.exists(expected_dir))
            self.assertTrue(os.path.isdir(expected_dir))

    def test_create_figures_directory(self):
        model_sim_folder = ModelsSimulationFolders.PERSHIN_SIMULATIONS
        export_params = self._create_export_parameters(
            model_simulation_folder=model_sim_folder
        )
        dms = DirectoriesManagementService(
            export_parameters=export_params,
        )

        expected_dir = f"{SIMULATIONS_DIR}/{export_params.model_simulation_folder.value}/{export_params.folder_name}/figures"
        self.assertFalse(os.path.exists(expected_dir))

        figs_dir = dms.get_or_create_figures_directory()

        self.assertEqual(figs_dir, expected_dir)
        self.assertTrue(os.path.exists(expected_dir))
        self.assertTrue(os.path.isdir(expected_dir))

    def test_get_circuit_file_path(self):
        for model, model_sim_folder in zip(MemristorModels, ModelsSimulationFolders):
            export_params = self._create_export_parameters(
                model_simulation_folder=model_sim_folder
            )
            model_name = model.name.lower()
            expected_path = (
                f"{SIMULATIONS_DIR}/{model_sim_folder.value}/{export_params.folder_name}/"
                f"{model_name}_circuit_file.cir"
            )
            dsm = DirectoriesManagementService(
                model=model, export_parameters=export_params
            )
            circuit_file_path = dsm.get_circuit_file_path()

            self.assertEqual(circuit_file_path, expected_path)

    def test_get_subcircuit_file_path(self):
        for model, model_sim_folder in zip(MemristorModels, ModelsSimulationFolders):
            export_params = self._create_export_parameters(
                model_simulation_folder=model_sim_folder
            )
            expected_path = (
                f"{SIMULATIONS_DIR}/{model_sim_folder.value}/{export_params.folder_name}/"
                f"{model.value}"
            )
            dsm = DirectoriesManagementService(
                model=model, export_parameters=export_params
            )
            subcircuit_file_path = dsm.get_subcircuit_file_path()

            self.assertEqual(subcircuit_file_path, expected_path)

    def test_get_export_simulation_file_path(self):
        for model, model_sim_folder in zip(MemristorModels, ModelsSimulationFolders):
            export_params = self._create_export_parameters(
                model_simulation_folder=model_sim_folder
            )
            expected_path = (
                f"{SIMULATIONS_DIR}/{model_sim_folder.value}/{export_params.folder_name}/"
                f"{export_params.file_name}_results.csv"
            )
            dsm = DirectoriesManagementService(
                model=model, export_parameters=export_params
            )
            export_file_path = dsm.get_export_simulation_file_path()

            self.assertEqual(export_file_path, expected_path)
            self.assertTrue(os.path.exists(os.path.dirname(export_file_path)))

    def test_get_simulation_log_file_path(self):
        for model, model_sim_folder in zip(MemristorModels, ModelsSimulationFolders):
            export_params = self._create_export_parameters(
                model_simulation_folder=model_sim_folder
            )
            expected_path = (
                f"{SIMULATIONS_DIR}/{model_sim_folder.value}/{export_params.folder_name}/"
                f"{export_params.folder_name}.log"
            )
            dsm = DirectoriesManagementService(
                model=model, export_parameters=export_params
            )
            log_file_path = dsm.get_simulation_log_file_path()

            self.assertEqual(log_file_path, expected_path)

    def test_get_circuit_dir_and_file_name(self):
        for model, model_sim_folder in zip(MemristorModels, ModelsSimulationFolders):
            export_params = self._create_export_parameters(
                model_simulation_folder=model_sim_folder
            )
            model_name = model.name.lower()
            expected_path = (
                f"{model_sim_folder.value}/{export_params.folder_name}/"
                f"{model_name}_circuit_file.cir"
            )
            dsm = DirectoriesManagementService(
                model=model, export_parameters=export_params
            )
            dir_and_file = dsm.get_circuit_dir_and_file_name()

            self.assertEqual(dir_and_file, expected_path)

    def test_get_subcircuit_dir_and_file_name(self):
        for model, model_sim_folder in zip(MemristorModels, ModelsSimulationFolders):
            export_params = self._create_export_parameters(
                model_simulation_folder=model_sim_folder
            )
            expected_path = (
                f"{model_sim_folder.value}/{export_params.folder_name}/"
                f"{model.value}"
            )
            dsm = DirectoriesManagementService(
                model=model, export_parameters=export_params
            )
            dir_and_file = dsm.get_subcircuit_dir_and_file_name()

            self.assertEqual(dir_and_file, expected_path)
