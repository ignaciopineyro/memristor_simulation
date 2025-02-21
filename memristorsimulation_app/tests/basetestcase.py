import os
import random
import shutil
import string
import pandas as pd

from typing import Dict, Optional, Set
from unittest import TestCase
from memristorsimulation_app.constants import (
    SIMULATIONS_DIR,
    MemristorModels,
    ModelsSimulationFolders,
)


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.test_simulation_path = None

    def tearDown(self) -> None:
        self._delete_test_simulation_folder()

    def _delete_test_simulation_folder(self):
        if self.test_simulation_path and os.path.exists(self.test_simulation_path):
            shutil.rmtree(self.test_simulation_path)

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
