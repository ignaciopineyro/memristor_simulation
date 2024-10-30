import os

from constants import (
    SIMULATIONS_DIR,
    MODELS_DIR,
    ModelsSimulationFolders,
    MemristorModels,
)


class DirectoriesManagementService:
    def __init__(self, model: MemristorModels = None, circuit_file_service=None):
        self.model = model

        if circuit_file_service:
            self.circuit_file_service = circuit_file_service
            self.export_parameters = self.circuit_file_service.export_parameters
            self.model = circuit_file_service.subcircuit_file_service.model or None

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
            f"./simulation_results/{self.export_parameters.model_simulation_folder_name.value}/"
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
                f"pershin_vourkas_circuit_file.cir"
            )
        elif self.model == MemristorModels.BIOLEK:
            return (
                f"{ModelsSimulationFolders.BIOLEK_SIMULATIONS.value}/{self.export_parameters.folder_name}/"
                f"biolek_circuit_file.cir"
            )
        else:
            raise InvalidMemristorModel(f"The model {self.model} is not valid")

    def get_model_path(self) -> str:
        if not os.path.exists(f"{MODELS_DIR}"):
            os.makedirs(f"{MODELS_DIR}")

        return f"{MODELS_DIR}/{self.model.value}"


class InvalidMemristorModel(Exception):
    pass
