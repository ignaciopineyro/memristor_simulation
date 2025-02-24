import os

from memristorsimulation_app.constants import (
    SIMULATIONS_DIR,
    ModelsSimulationFolders,
    MemristorModels,
)
from memristorsimulation_app.representations import ExportParameters


class DirectoriesManagementService:
    def __init__(
        self,
        model: MemristorModels = None,
        export_parameters: ExportParameters = None,
    ):
        self.model = model
        self.export_parameters = export_parameters

    @staticmethod
    def create_simulation_results_for_model_folder_if_not_exists(
        model: MemristorModels,
    ):
        if not os.path.exists(
            f"{SIMULATIONS_DIR}/{ModelsSimulationFolders.get_simulation_folder_by_model(model).value}"
        ):
            os.makedirs(
                f"{SIMULATIONS_DIR}/{ModelsSimulationFolders.get_simulation_folder_by_model(model).value}"
            )

    def create_simulation_parameter_folder_if_not_exist(
        self, model_simulation_folder_name: ModelsSimulationFolders
    ) -> None:
        folder_directory = f"{SIMULATIONS_DIR}/{model_simulation_folder_name.value}/{self.export_parameters.folder_name}"
        if not os.path.exists(folder_directory):
            os.makedirs(folder_directory)

    @staticmethod
    def create_figures_directory(simulations_directory_path):
        if not os.path.exists(f"{simulations_directory_path}/figures"):
            os.makedirs(f"{simulations_directory_path}/figures")

    def get_circuit_file_path(self) -> str:
        return f"{SIMULATIONS_DIR}/{self.get_circuit_dir_and_file_name()}"

    def get_subcircuit_file_path(self) -> str:
        return f"{SIMULATIONS_DIR}/{self.get_subcircuit_dir_and_file_name()}"

    def get_export_simulation_file_path(self) -> str:
        self.create_simulation_parameter_folder_if_not_exist(
            self.export_parameters.model_simulation_folder_name
        )
        export_simulation_file_path = (
            f"{SIMULATIONS_DIR}/{self.export_parameters.model_simulation_folder_name.value}/"
            f"{self.export_parameters.folder_name}/{self.export_parameters.file_name}_results.csv"
        )

        return export_simulation_file_path

    def get_simulation_log_file_path(self) -> str:
        return (
            f"{SIMULATIONS_DIR}/{self.export_parameters.model_simulation_folder_name.value}/"
            f"{self.export_parameters.folder_name}/{self.export_parameters.folder_name}.log"
        )

    def get_circuit_dir_and_file_name(self) -> str:
        if self.model == MemristorModels.PERSHIN:
            return (
                f"{ModelsSimulationFolders.PERSHIN_SIMULATIONS.value}/{self.export_parameters.folder_name}/"
                f"pershin_circuit_file.cir"
            )
        elif self.model == MemristorModels.VOURKAS:
            return (
                f"{ModelsSimulationFolders.VOURKAS_SIMULATIONS.value}/{self.export_parameters.folder_name}/"
                f"vourkas_circuit_file.cir"
            )
        elif self.model == MemristorModels.BIOLEK:
            return (
                f"{ModelsSimulationFolders.BIOLEK_SIMULATIONS.value}/{self.export_parameters.folder_name}/"
                f"biolek_circuit_file.cir"
            )
        else:
            raise InvalidMemristorModel(f"The model {self.model} is not valid")

    def get_subcircuit_dir_and_file_name(self) -> str:
        if self.model == MemristorModels.PERSHIN:
            return (
                f"{ModelsSimulationFolders.PERSHIN_SIMULATIONS.value}/{self.export_parameters.folder_name}/"
                f"{self.model.value}"
            )
        elif self.model == MemristorModels.VOURKAS:
            return (
                f"{ModelsSimulationFolders.VOURKAS_SIMULATIONS.value}/{self.export_parameters.folder_name}/"
                f"{self.model.value}"
            )
        elif self.model == MemristorModels.BIOLEK:
            return (
                f"{ModelsSimulationFolders.BIOLEK_SIMULATIONS.value}/{self.export_parameters.folder_name}/"
                f"{self.model.value}"
            )
        else:
            raise InvalidMemristorModel(f"The model {self.model} is not valid")


class InvalidMemristorModel(Exception):
    pass
