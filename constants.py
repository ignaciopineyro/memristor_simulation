import os
from enum import Enum


PATH = os.path.dirname(__file__)
MODELS_DIR = f'{PATH}/models/'
SIMULATIONS_DIR = f'{PATH}/simulation_results/'


class MemristorModels(Enum):
    PERSHIN = 'pershin.sub'
    PERSHIN_VOURKAS = 'pershin_vourkas.sub'
    BIOLEK = 'biolek.sub'


class SimulationFileNames(Enum):
    PERSHIN = 'pershin_simulation.cir'
    PERSHIN_VOURKAS = 'pershin_vourkas_simulation.cir'
    BIOLEK = 'biolek_simulation.cir'
