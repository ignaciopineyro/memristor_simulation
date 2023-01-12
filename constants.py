import os
from enum import Enum


PATH = os.path.dirname(__file__)
MODELS_DIR = f'{PATH}/models'
SIMULATIONS_DIR = f'{PATH}/simulation_results'


class ModelsSimulationFolders(Enum):
    PERSHIN_SIMULATIONS = 'pershin_simulations'
    PERSHIN_VOURKAS_SIMULATIONS = 'pershin_vourkas_simulations'
    BIOLEK_SIMULATIONS = 'biolek_simulations'


class MemristorModels(Enum):
    PERSHIN = 'pershin.sub'
    PERSHIN_VOURKAS = 'pershin_vourkas.sub'
    BIOLEK = 'biolek.sub'


class SimulationFileNames(Enum):
    PERSHIN = 'pershin_simulation.cir'
    PERSHIN_VOURKAS = 'pershin_vourkas_simulation.cir'
    BIOLEK = 'biolek_simulation.cir'


class WaveForms(Enum):
    SIN = 'sin'


class AnalysisType(Enum):
    TRAN = '.tran'


class SpiceDevices(Enum):
    DIODE = 'D'


class SpiceModel(Enum):
    DIODE = 'd'


class TimeMeasures(Enum):
    PYTHON_EXECUTION_TIME = 'PYTHON_EXECUTION_TIME'
    LINUX_REAL_EXECUTION_TIME = 'LINUX_REAL_EXECUTION_TIME'
    LINUX_USER_EXECUTION_TIME = 'LINUX_USER_EXECUTION_TIME'
    LINUX_SYS_EXECUTION_TIME = 'LINUX_SYS_EXECUTION_TIME'
    PYTHON_AVERAGE_EXECUTION_TIME = 'PYTHON_AVERAGE_EXECUTION_TIME'
    LINUX_AVERAGE_REAL_EXECUTION_TIME = 'LINUX_AVERAGE_REAL_EXECUTION_TIME'
    LINUX_AVERAGE_USER_EXECUTION_TIME = 'LINUX_AVERAGE_USER_EXECUTION_TIME'
    LINUX_AVERAGE_SYS_EXECUTION_TIME = 'LINUX_AVERAGE_SYS_EXECUTION_TIME'
