import os
import platform
import time

from constants import SIMULATIONS_DIR, MemristorModels
from services.circuitfileservice import CircuitFileService


class TimeMeasure:
    def __init__(self):
        self.start_time = None

    def __enter__(self):
        self.start_time = self.init_python_execution_time_measure()
        if platform.system() == 'Linux':
            self.measure_linux_execution_time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.end_python_execution_time_measure(self.start_time)

    @staticmethod
    def measure_linux_execution_time():
        print('\n\nMEASURING TIME IN LINUX\n\n')
        # os.system(f'time ')

    @staticmethod
    def init_python_execution_time_measure():
        print('\n\nMEASURING TIME IN PYTHON\n\n')
        return time.time()

    @staticmethod
    def end_python_execution_time_measure(start_time):
        return time.time() - start_time


class NGSpiceService:
    def __init__(self, circuit_file_service: CircuitFileService, model: MemristorModels):
        self.circuit_file_service = circuit_file_service
        self.model = model
        self.circuit_file_path = (
            f'{SIMULATIONS_DIR}/{self.circuit_file_service.get_simulation_file_name(self.model)}'
        )

    def run_simulation(self):
        with TimeMeasure():
            os.system(f'ngspice {self.circuit_file_path}')
            # os.system('}')
