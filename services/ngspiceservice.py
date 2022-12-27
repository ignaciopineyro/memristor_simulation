import subprocess
import sys
import time

from constants import SIMULATIONS_DIR, MemristorModels
from services.circuitfileservice import CircuitFileService


class TimeMeasure:
    def __init__(self, circuit_file_path: str, simulation_result_file_path: str):
        self.start_time = None
        self.command_line = None
        self.circuit_file_path = circuit_file_path
        self.simulation_result_file_path = simulation_result_file_path
        self.generic_os_execute_command = f'ngspice {self.circuit_file_path}'

    @staticmethod
    def _is_os_linux() -> bool:
        return sys.platform == "linux" or sys.platform == "linux2"

    def execute_with_time_measure(self) -> None:
        self.start_time = self.init_python_execution_time_measure()

        if self._is_os_linux:
            _, linux_time_output = subprocess.Popen(
                ['bash', '-c', f'time ngspice {self.circuit_file_path} 2>&1', '_'], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).communicate()

            self.write_python_time_measure_into_csv()
            self.write_linux_time_measure_into_csv(linux_time_output)

        else:
            subprocess.call(self.generic_os_execute_command)

            self.write_python_time_measure_into_csv()

    @staticmethod
    def init_python_execution_time_measure():
        return time.time()

    @staticmethod
    def end_python_execution_time_measure(start_time):
        return time.time() - start_time

    def write_python_time_measure_into_csv(self):
        with open(self.simulation_file_path, "w+") as f:

        print(f'PYTHON TIME = {(self.end_python_execution_time_measure(self.start_time)) * 1000} ms')

    def write_linux_time_measure_into_csv(self, linux_time_output):
        decoded_linux_time_output = linux_time_output.decode().split('\n')
        real_time = decoded_linux_time_output[1]
        user_time = decoded_linux_time_output[2]
        sys_time = decoded_linux_time_output[3]
        print(f'LINUX TIME = {real_time} {user_time} {sys_time}')


class NGSpiceService:
    def __init__(self, circuit_file_service: CircuitFileService, model: MemristorModels):
        self.circuit_file_service = circuit_file_service
        self.model = model
        self.circuit_file_path = (
            f'{SIMULATIONS_DIR}/{self.circuit_file_service.get_simulation_file_name(self.model)}'
        )

        self.time_measure = TimeMeasure(self.circuit_file_path, self.circuit_file_service.)

    def run_simulation(self):
        self.time_measure.execute_with_time_measure()
