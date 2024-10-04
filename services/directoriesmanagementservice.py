import os
from typing import List

from constants import SIMULATIONS_DIR, MODELS_DIR, ModelsSimulationFolders, MemristorModels


class DirectoriesManagementService:
    def __init__(self, model: MemristorModels = None, circuit_file_service=None):
        self.model = model

        if circuit_file_service:
            self.circuit_file_service = circuit_file_service
            self.export_parameters = self.circuit_file_service.export_parameters or []
            self.model = circuit_file_service.subcircuit_file_service.model or None

    @staticmethod
    def create_simulation_results_for_model_folder_if_not_exists(model: MemristorModels):
        if not os.path.exists(
                f'{SIMULATIONS_DIR}/{ModelsSimulationFolders.get_simulation_folder_by_model(model).value}'
        ):
            os.makedirs(f'{SIMULATIONS_DIR}/{ModelsSimulationFolders.get_simulation_folder_by_model(model).value}')

    @staticmethod
    def create_simulation_parameter_folder_if_not_exist(
            model_simulation_folder_name: ModelsSimulationFolders, folder_name: str
    ) -> None:
        folder_directory = f'{SIMULATIONS_DIR}/{model_simulation_folder_name.value}/{folder_name}'
        if not os.path.exists(folder_directory):
            os.makedirs(folder_directory)
        if not os.path.exists(f'{folder_directory}/logs'):
            os.makedirs(f'{folder_directory}/logs')

    @staticmethod
    def create_figures_directory(simulations_directory_path):
        if not os.path.exists(f'{simulations_directory_path}/figures'):
            os.makedirs(f'{simulations_directory_path}/figures')

    def get_circuit_file_path(self) -> str:
        return f'{SIMULATIONS_DIR}/{self.get_circuit_dir_and_file_name()}'

    def get_export_simulation_file_paths(self) -> List[str]:
        export_simulation_file_paths = []

        for export_parameter in self.export_parameters:
            self.create_simulation_parameter_folder_if_not_exist(
                export_parameter.model_simulation_folder_name, export_parameter.folder_name
            )

            export_simulation_file_paths.append(
                f"{SIMULATIONS_DIR}/{export_parameter.model_simulation_folder_name.value}/"
                f"{export_parameter.folder_name}/{export_parameter.file_name}.csv"
            )

        return export_simulation_file_paths

    def get_simulation_log_file_path(self) -> str:
        return (
                f"./simulation_results/{self.export_parameters[0].model_simulation_folder_name.value}/"
                f"{self.export_parameters[0].folder_name}/logs/{self.export_parameters[0].folder_name}.log"
        )

    def get_circuit_dir_and_file_name(self) -> str:
        if self.model == MemristorModels.PERSHIN:
            return (
                f'{ModelsSimulationFolders.PERSHIN_SIMULATIONS.value}/{self.export_parameters[0].folder_name}/'
                f'pershin_circuit_file.cir'
            )
        elif self.model == MemristorModels.VOURKAS:
            return (
                f'{ModelsSimulationFolders.VOURKAS_SIMULATIONS.value}/{self.export_parameters[0].folder_name}/'
                f'pershin_vourkas_circuit_file.cir'
            )
        elif self.model == MemristorModels.BIOLEK:
            return (
                f'{ModelsSimulationFolders.BIOLEK_SIMULATIONS.value}/{self.export_parameters[0].folder_name}/'
                f'biolek_circuit_file.cir'
            )
        else:
            raise InvalidMemristorModel(f'The model {self.model} is not valid')

    def get_model_path(self) -> str:
        if not os.path.exists(f'{MODELS_DIR}'):
            os.makedirs(f'{MODELS_DIR}')

        return f'{MODELS_DIR}/{self.model.value}'


class InvalidMemristorModel(Exception):
    pass
