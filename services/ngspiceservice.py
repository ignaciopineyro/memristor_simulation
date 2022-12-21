import os
import platform
import time

from constants import SIMULATIONS_DIR, MemristorModels
from services.circuitfileservice import CircuitFileService


class TimeMeasure:
    def __init__(self, circuit_file_path):
        self.start_time = None
        self.command_line = None
        self.circuit_file_path = circuit_file_path

    def execute_with_time_measure(self):
        self.start_time = self.init_python_execution_time_measure()

        # TODO: Linux time measure unresolved issue
        """
        if platform.system() == 'Linux':
            self.command_line = self.start_measure_linux_execution_time()
        """

        self.command_line = f'ngspice {self.circuit_file_path}'
        print(f'{self.command_line=}')

        # TODO: Linux time measure unresolved issue
        """
        self.command_line = self.command_line + f'ngspice {self.circuit_file_path}'
        
        if platform.system() == 'Linux':
            self.command_line = self.command_line #+ self.end_measure_linux_execution_time()
        """

        os.system(self.command_line)
        #os.system('exit')

        print(f'PYTHON TIME = {(self.end_python_execution_time_measure(self.start_time)) * 1000} ms')

    @staticmethod
    def start_measure_linux_execution_time():
        return 'time -o simulation.log '

    @staticmethod
    def end_measure_linux_execution_time():
        return ' | exit'

    @staticmethod
    def init_python_execution_time_measure():
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

        self.time_measure = TimeMeasure(self.circuit_file_path)

    def run_simulation(self):
        self.time_measure.execute_with_time_measure()
