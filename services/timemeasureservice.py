import subprocess
import sys
import time
from dataclasses import asdict
from typing import List

from constants import TimeMeasures
from representations import TimeMeasure
from services.directoriesmanagementservice import DirectoriesManagementService


class TimeMeasureService:
    def __init__(self, circuit_file_service=None):
        self.directories_management_service = DirectoriesManagementService(circuit_file_service=circuit_file_service)

        self.start_time = None
        self.command_line = None
        self.circuit_file_path = self.directories_management_service.get_circuit_file_path()
        self.simulation_result_file_path = self.directories_management_service.get_export_simulation_file_path()
        self.simulation_log_path = self.directories_management_service.get_simulation_log_file_path()
        self.execute_command = ''
        self.time_measure = TimeMeasure()

    def execute_with_time_measure(self) -> TimeMeasure:
        if self._is_os_linux():
            self.execute_command = f'time ngspice {self.circuit_file_path} 2>&1'
            self.start_time = self.init_python_execution_time_measure()
            simulation_log, linux_time_output = subprocess.Popen(
                ['bash', '-c', self.execute_command, '_'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ).communicate()

            self.write_python_time_measure_into_csv()
            self.write_linux_time_measure_into_csv(linux_time_output)

        else:
            self.execute_command = f'ngspice {self.circuit_file_path} 2>&1'
            self.start_time = self.init_python_execution_time_measure()

            simulation_log = subprocess.Popen(
                ['bash', '-c', self.execute_command, '_'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ).communicate()

            self.write_python_time_measure_into_csv()

        self.write_simulation_log(simulation_log=simulation_log.decode(), time_measure=self.time_measure)
        self.print_time_measure(self.time_measure)

        return self.time_measure

    @staticmethod
    def init_python_execution_time_measure() -> float:
        return time.time()

    @staticmethod
    def end_python_execution_time_measure(start_time) -> float:
        return time.time() - start_time

    def _format_linux_time_output(self, decoded_linux_time_output: str) -> None:
        decoded_real_time = decoded_linux_time_output.split('\n')[1]
        decoded_user_time = decoded_linux_time_output.split('\n')[2]
        decoded_sys_time = decoded_linux_time_output.split('\n')[3]

        real_time_minutes = float(decoded_real_time.split('\t')[1].split('m')[0])
        real_time_seconds = float(decoded_real_time.split('\t')[1].split('m')[1].split('s')[0])
        real_time_ms = (real_time_minutes * 60 + real_time_seconds) * 1000

        user_time_minutes = float(decoded_user_time.split('\t')[1].split('m')[0])
        user_time_seconds = float(decoded_user_time.split('\t')[1].split('m')[1].split('s')[0])
        user_time_ms = (user_time_minutes * 60 + user_time_seconds) * 1000

        sys_time_minutes = float(decoded_sys_time.split('\t')[1].split('m')[0])
        sys_time_seconds = float(decoded_sys_time.split('\t')[1].split('m')[1].split('s')[0])
        sys_time_ms = (sys_time_minutes * 60 + sys_time_seconds) * 1000

        self.time_measure.linux_real_execution_time = real_time_ms
        self.time_measure.linux_user_execution_time = user_time_ms
        self.time_measure.linux_sys_execution_time = sys_time_ms

        return

    def compute_time_average(self, time_measure: List[TimeMeasure], amount_iterations: int):
        raise NotImplementedError

    def write_python_time_measure_into_csv(self) -> None:
        python_time_measure_ms = (self.end_python_execution_time_measure(self.start_time)) * 1000
        self.time_measure.python_execution_time = python_time_measure_ms

        with open(self.simulation_result_file_path, "a") as f:
            f.write(f'\n# {TimeMeasures.PYTHON_EXECUTION_TIME.value} = {python_time_measure_ms} ms')

    def write_linux_time_measure_into_csv(self, linux_time_output: bytes) -> None:
        self._format_linux_time_output(linux_time_output.decode())

        with open(self.simulation_result_file_path, "a") as f:
            f.write(
                f'\n# {TimeMeasures.LINUX_REAL_EXECUTION_TIME.value} = '
                f'{self.time_measure.linux_real_execution_time} ms'
            )
            f.write(
                f'\n# {TimeMeasures.LINUX_USER_EXECUTION_TIME.value} = '
                f'{self.time_measure.linux_user_execution_time} ms'
            )
            f.write(
                f'\n# {TimeMeasures.LINUX_SYS_EXECUTION_TIME.value} = '
                f'{self.time_measure.linux_sys_execution_time} ms'
            )

    @staticmethod
    def print_time_measure(time_measure: TimeMeasure):
        for k, v in asdict(time_measure).items():
            if v is not None:
                print(f'# {k} = {str(v)} ms\n')

    def write_simulation_log(self, simulation_log: str = None, time_measure: TimeMeasure = None) -> None:
        with open(f'{self.simulation_log_path}', "a+") as f:
            if simulation_log:
                f.write(f'{"#" * 60}\n{simulation_log}\n\n')

            if time_measure:
                for k, v in asdict(time_measure).items():
                    if v is not None:
                        f.write(f'# {k} = {str(v)} ms\n')
                f.write('\n\n')

    @staticmethod
    def _is_os_linux() -> bool:
        return sys.platform == "linux" or sys.platform == "linux2"