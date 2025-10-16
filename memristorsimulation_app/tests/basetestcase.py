import os
import random
import shutil
import string
import pandas as pd

from pathlib import Path
from typing import Dict, List, Optional, Set, Union
from unittest import TestCase
from memristorsimulation_app.constants import (
    SIMULATIONS_DIR,
    AnalysisType,
    MemristorModels,
    ModelsSimulationFolders,
    NetworkType,
    SpiceDevices,
    SpiceModel,
    WaveForms,
)
from memristorsimulation_app.representations import (
    BehaviouralSource,
    Component,
    DeviceParameters,
    ExportParameters,
    InputParameters,
    ModelDependence,
    ModelParameters,
    NetworkParameters,
    PulseWaveForm,
    SimulationParameters,
    Subcircuit,
)
from memristorsimulation_app.services.circuitfileservice import CircuitFileService
from memristorsimulation_app.services.directoriesmanagementservice import (
    DirectoriesManagementService,
)
from memristorsimulation_app.services.networkservice import NetworkService
from memristorsimulation_app.services.subcircuitfileservice import SubcircuitFileService


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self._delete_test_simulation_folder()

    def tearDown(self) -> None:
        self._delete_test_simulation_folder()

    def _delete_test_simulation_folder(self):
        if os.path.exists(SIMULATIONS_DIR):
            shutil.rmtree(SIMULATIONS_DIR)

    @staticmethod
    def get_random_string(length=10, use_numbers=True, use_letters=True) -> str:
        chars = ""
        if use_numbers:
            chars = chars + string.digits
        if use_letters:
            chars = chars + string.ascii_uppercase
        return "".join(random.choices(chars, k=length))

    @staticmethod
    def get_random_int() -> int:
        return random.randint(0, 2**16)

    @staticmethod
    def get_random_float() -> float:
        return random.uniform(0, 1)

    def get_simulation_folder_path(
        self, model: MemristorModels, folder_name: str
    ) -> str:
        model_simulations_folder = (
            ModelsSimulationFolders.get_simulation_folder_by_model(model)
        )
        base_path = f"{SIMULATIONS_DIR}/{model_simulations_folder.value}"

        try:
            folders_match = [
                os.path.join(base_path, d)
                for d in os.listdir(base_path)
                if d.startswith(folder_name)
                and os.path.isdir(os.path.join(base_path, d))
            ]

            if not folders_match:
                RuntimeError(
                    f"No folders file in directory {base_path} starting with name {folder_name}"
                )

            elif len(folders_match) > 1:
                RuntimeError(
                    f"More than one folder found in directory {base_path} starting with name {folder_name}"
                )

            self.test_simulation_path = folders_match[0]
            return folders_match[0]

        except FileNotFoundError:
            raise RuntimeError(f"Invalid directory {base_path}")

    def list_files_in_simulation_directory(
        self, model: MemristorModels, folder_name: str
    ) -> Dict[str, int]:
        simulation_folder = self.get_simulation_folder_path(model, folder_name)
        files_size = {}
        for dirpath, _, filenames in os.walk(simulation_folder):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                files_size[filename] = os.path.getsize(file_path)

        return files_size

    def load_dataframe_from_csv(
        self, model: MemristorModels, folder_name: str
    ) -> pd.DataFrame:
        simulation_folder = self.get_simulation_folder_path(model, folder_name)
        csv_files = [f for f in os.listdir(simulation_folder) if f.endswith(".csv")]
        if not csv_files:
            RuntimeError(f"No csv file in directory {simulation_folder}")

        elif len(csv_files) > 1:
            RuntimeError(
                f"More than one csv file found in directory {simulation_folder}"
            )

        csv_file_path = f"{simulation_folder}/{csv_files[0]}"

        return pd.DataFrame(
            pd.read_csv(csv_file_path, sep=r"\s+", engine="python", skipfooter=4)
        )

    @staticmethod
    def check_file_size(
        file_extension: str,
        files: Dict[str, int],
        min_size_bytes: int,
        amount_coincidences: Optional[int] = 1,
    ):
        return (
            sum(
                [
                    filename.endswith(file_extension) and size >= min_size_bytes
                    for filename, size in files.items()
                ]
            )
            == amount_coincidences
        )

    @staticmethod
    def check_csv_content(
        dataframe: pd.DataFrame, columns: Set["str"], min_amount_rows: int
    ):
        has_columns = columns.issubset(set(dataframe.columns))
        has_min_amount_rows = len(dataframe) >= min_amount_rows

        return has_columns and has_min_amount_rows

    def open_file(self, file_path: Path) -> str:
        self.assertTrue(os.path.exists(file_path))
        self.assertGreater(os.path.getsize(file_path), 300)

        with open(file_path, "r") as f:
            content = f.read()

        return content

    def create_directories_management_service(
        self, memristor_model: MemristorModels
    ) -> DirectoriesManagementService:
        export_file_name = self.get_random_string()
        export_folder_name = self.get_random_string()
        magnitudes = [
            self.get_random_string(),
            self.get_random_string(),
            self.get_random_string(),
        ]
        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(memristor_model),
            export_folder_name,
            export_file_name,
            magnitudes,
        )

        return DirectoriesManagementService(memristor_model, export_params)

    def create_subcircuit_file_service(
        self, memristor_model: MemristorModels = MemristorModels.PERSHIN
    ) -> SubcircuitFileService:
        model_parameters = ModelParameters(
            self.get_random_int(),
            self.get_random_int(),
            self.get_random_int(),
            self.get_random_int(),
            self.get_random_int(),
            self.get_random_int(),
        )
        subcircuit = Subcircuit(
            model_parameters,
            self.get_random_string(),
            [
                self.get_random_string(),
                self.get_random_string(),
                self.get_random_string(),
            ],
        )
        behavioural_sources = [
            BehaviouralSource(
                name=self.get_random_string(),
                n_plus=self.get_random_string(),
                n_minus=self.get_random_string(),
                behaviour_function=self.get_random_string(),
            )
        ]
        components = [
            Component(
                name=self.get_random_string(),
                n_plus=self.get_random_string(),
                n_minus=self.get_random_string(),
                value=self.get_random_int(),
            )
        ]
        model_dependencies = [
            ModelDependence(name=SpiceDevices.DIODE, model=SpiceModel.DIODE)
        ]
        control_cmd = [self.get_random_string()]

        directories_management_service = self.create_directories_management_service(
            memristor_model
        )
        return SubcircuitFileService(
            model=memristor_model,
            subcircuit=subcircuit,
            sources=behavioural_sources,
            directories_management_service=directories_management_service,
            model_dependencies=model_dependencies,
            components=components,
            control_commands=control_cmd,
        )

    def create_circuit_file_service(
        self, subcircuit_file_service: SubcircuitFileService
    ) -> CircuitFileService:
        input_parameters = InputParameters(
            source_number=self.get_random_int(),
            n_plus=self.get_random_string(),
            n_minus=self.get_random_string(),
            wave_form=PulseWaveForm(
                v1=self.get_random_int(),
                v2=self.get_random_int(),
                td=self.get_random_int(),
                tr=self.get_random_int(),
                tf=self.get_random_int(),
                pw=self.get_random_int(),
                per=self.get_random_int(),
            ),
        )
        device_parameters = [
            DeviceParameters(
                device_name=self.get_random_string(),
                device_number=self.get_random_int(),
                nodes=[
                    self.get_random_string(),
                    self.get_random_string(),
                    self.get_random_string(),
                ],
                subcircuit=self.get_random_string(),
            )
        ]
        simulation_parameters = SimulationParameters(
            analysis_type=AnalysisType.TRAN,
            tstep=self.get_random_int(),
            tstop=self.get_random_int(),
        )
        directories_management_service = self.create_directories_management_service(
            MemristorModels.PERSHIN
        )

        return CircuitFileService(
            subcircuit_file_service,
            input_parameters,
            device_parameters,
            simulation_parameters,
            directories_management_service,
        )

    def create_grid_network_service(self, n=3, m=3, removal_probability=0):
        network_parameters = NetworkParameters(n=n, m=m)
        return NetworkService(
            network_type=NetworkType.GRID_2D_GRAPH,
            network_parameters=network_parameters,
            vin_plus=(0, 0),
            vin_minus=(n - 1, 0),
            removal_probability=removal_probability,
        )

    def create_random_regular_network_service(
        self, amount_nodes=10, amount_connections=4, removal_probability=0
    ):
        network_parameters = NetworkParameters(
            amount_nodes=amount_nodes,
            amount_connections=amount_connections,
            seed=42,
        )
        return NetworkService(
            network_type=NetworkType.RANDOM_REGULAR_GRAPH,
            network_parameters=network_parameters,
            vin_plus=0,
            vin_minus=amount_nodes // 2,
            removal_probability=removal_probability,
        )

    def create_watts_strogatz_network_service(
        self,
        amount_nodes=10,
        amount_connections=4,
        shortcut_probability=0.3,
        removal_probability=0,
    ):
        network_parameters = NetworkParameters(
            amount_nodes=amount_nodes,
            amount_connections=amount_connections,
            shortcut_probability=shortcut_probability,
            seed=42,
        )
        return NetworkService(
            network_type=NetworkType.WATTS_STROGATZ_GRAPH,
            network_parameters=network_parameters,
            vin_plus=0,
            vin_minus=amount_nodes // 2,
            removal_probability=removal_probability,
        )
