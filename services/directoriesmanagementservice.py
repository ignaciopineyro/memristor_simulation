import os

from constants import SIMULATIONS_DIR, MODELS_DIR, ModelsSimulationFolders, MemristorModels


class DirectoriesManagementService:
    def __init__(self, model: MemristorModels = None, circuit_file_service=None):
        self.model = model

        if circuit_file_service:
            self.circuit_file_service = circuit_file_service
            self.export_parameters = self.circuit_file_service.export_parameters
            self.model = circuit_file_service.model

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
    def create_figures_directory( figures_directory_path):
        if not os.path.exists(figures_directory_path):
            os.makedirs(figures_directory_path)

    def get_circuit_file_path(self) -> str:
        return f'{SIMULATIONS_DIR}/{self.get_circuit_dir_and_file_name()}'

    def get_export_simulation_file_path(self) -> str:
        self.create_simulation_parameter_folder_if_not_exist(
            self.export_parameters.model_simulation_folder_name, self.export_parameters.folder_name
        )
        return (
            f"{SIMULATIONS_DIR}/{self.export_parameters.model_simulation_folder_name.value}/"
            f"{self.export_parameters.folder_name}/{self.export_parameters.file_name}.csv"
        )

    def get_simulation_log_file_path(self) -> str:
        return (
            f"./simulation_results/{self.export_parameters.model_simulation_folder_name.value}/"
            f"{self.export_parameters.folder_name}/logs/{self.export_parameters.file_name}.log"
        )

    def get_circuit_dir_and_file_name(self) -> str:
        if self.model == MemristorModels.PERSHIN:
            return f'{ModelsSimulationFolders.PERSHIN_SIMULATIONS.value}/pershin_simulation.cir'
        elif self.model == MemristorModels.PERSHIN_VOURKAS:
            return f'{ModelsSimulationFolders.PERSHIN_VOURKAS_SIMULATIONS.value}/pershin_vourkas_simulation.cir'
        elif self.model == MemristorModels.BIOLEK:
            return f'{ModelsSimulationFolders.BIOLEK_SIMULATIONS.value}/biolek_simulation.cir'
        else:
            raise InvalidMemristorModel(f'The model {self.model} is not valid')

    def get_model_dir(self) -> str:
        return f'{MODELS_DIR}/{self.model.value}'


class InvalidMemristorModel(Exception):
    pass
