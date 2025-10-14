import os

from enum import Enum
from djangoproject.settings import CURRENT_ENVIRONMENT, Environments


PATH = (
    f"{os.path.dirname(__file__)}/temp"
    if Environments.is_testing(CURRENT_ENVIRONMENT)
    else f"{os.path.dirname(__file__)}"
)
MODELS_DIR = f"{PATH}/models"
SIMULATIONS_DIR = f"{PATH}/simulation_results"


class MemristorModels(Enum):
    PERSHIN = "pershin.sub"
    VOURKAS = "vourkas.sub"
    BIOLEK = "biolek.sub"


class ModelsSimulationFolders(Enum):
    PERSHIN_SIMULATIONS = "pershin_simulations"
    VOURKAS_SIMULATIONS = "vourkas_simulations"
    BIOLEK_SIMULATIONS = "biolek_simulations"

    @classmethod
    def get_simulation_folder_by_model(cls, model: MemristorModels):
        if model == MemristorModels.PERSHIN:
            return cls.PERSHIN_SIMULATIONS

        elif model == MemristorModels.VOURKAS:
            return cls.VOURKAS_SIMULATIONS

        elif model == MemristorModels.BIOLEK:
            return cls.BIOLEK_SIMULATIONS

        else:
            raise InvalidMemristorModel()


class SimulationFileNames(Enum):
    PERSHIN = "pershin_simulation.cir"
    VOURKAS = "vourkas_simulation.cir"
    BIOLEK = "biolek_simulation.cir"


class WaveForms(Enum):
    SIN = "sin"
    PULSE = "pulse"
    PWL = "pwl"


class AnalysisType(Enum):
    TRAN = ".tran"


class SpiceDevices(Enum):
    DIODE = "D"


class SpiceModel(Enum):
    DIODE = "d"


class TimeMeasures(Enum):
    PYTHON_EXECUTION_TIME = "PYTHON_EXECUTION_TIME"
    LINUX_REAL_EXECUTION_TIME = "LINUX_REAL_EXECUTION_TIME"
    LINUX_USER_EXECUTION_TIME = "LINUX_USER_EXECUTION_TIME"
    LINUX_SYS_EXECUTION_TIME = "LINUX_SYS_EXECUTION_TIME"
    PYTHON_AVERAGE_EXECUTION_TIME = "PYTHON_AVERAGE_EXECUTION_TIME"
    LINUX_AVERAGE_REAL_EXECUTION_TIME = "LINUX_AVERAGE_REAL_EXECUTION_TIME"
    LINUX_AVERAGE_USER_EXECUTION_TIME = "LINUX_AVERAGE_USER_EXECUTION_TIME"
    LINUX_AVERAGE_SYS_EXECUTION_TIME = "LINUX_AVERAGE_SYS_EXECUTION_TIME"


class PlotType(Enum):
    IV = "IV"
    IV_OVERLAPPED = "IV_OVERLAPPED"
    IV_LOG = "IV_LOG"
    IV_LOG_OVERLAPPED = "IV_LOG_OVERLAPPED"
    IV_ANIMATED = "IV_ANIMATED"
    CURRENT_AND_VIN_VS_TIME = "CURRENT_AND_VIN_VS_TIME"
    STATE_AND_VIN_VS_TIME = "STATE_AND_VIN_VS_TIME"
    MEMRISTIVE_STATES_OVERLAPPED = "MEMRISTIVE_STATES_OVERLAPPED"
    GRAPH = "GRAPH"


class MeasuredMagnitude(Enum):
    IV = "IV"
    STATES = "STATES"
    OTHER = "OTHER"


class NetworkType(Enum):
    GRID_2D_GRAPH = "GRID_2D_GRAPH"
    RANDOM_REGULAR_GRAPH = "RANDOM_REGULAR_GRAPH"
    WATTS_STROGATZ_GRAPH = "WATTS_STROGATZ_GRAPH"


class InvalidMemristorModel(Exception):
    pass


class InvalidSimulationTemplate(Exception):
    pass


class NetworkTypeNotImplemented(Exception):
    pass
