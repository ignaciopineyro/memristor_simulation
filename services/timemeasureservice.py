import subprocess
import sys
import time
from typing import Dict

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

    @staticmethod
    def _is_os_linux() -> bool:
        return sys.platform == "linux" or sys.platform == "linux2"

    def execute_with_time_measure(self, amount_iterations: int = None) -> None:
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

        self.write_simulation_log(str(simulation_log))

    @staticmethod
    def init_python_execution_time_measure() -> float:
        return time.time()

    @staticmethod
    def end_python_execution_time_measure(start_time) -> float:
        return time.time() - start_time

    @staticmethod
    def _format_linux_time_output(decoded_linux_time_output: str):
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

        return {
            'LINUX_REAL_EXECUTION_TIME': real_time_ms, 'LINUX_USER_EXECUTION_TIME': user_time_ms,
            'LINUX_SYS_EXECUTION_TIME': sys_time_ms
        }

    def write_python_time_measure_into_csv(self) -> None:
        python_time_measure_ms = (self.end_python_execution_time_measure(self.start_time)) * 1000
        with open(self.simulation_result_file_path, "a") as f:
            f.write(f'\n# PYTHON EXECUTION TIME = {python_time_measure_ms} ms')

        self.write_simulation_log(python_time_measure=str(python_time_measure_ms))

        print(f'\n# PYTHON EXECUTION TIME = {python_time_measure_ms} ms')

    def write_linux_time_measure_into_csv(self, linux_time_output: bytes) -> None:
        linux_execution_time = self._format_linux_time_output(linux_time_output.decode())

        with open(self.simulation_result_file_path, "a") as f:
            f.write(f'\n# LINUX REAL EXECUTION TIME = {linux_execution_time.get("LINUX_REAL_EXECUTION_TIME")}')
            f.write(f'\n# LINUX USER EXECUTION TIME = {linux_execution_time.get("LINUX_USER_EXECUTION_TIME")}')
            f.write(f'\n# LINUX SYS EXECUTION TIME = {linux_execution_time.get("LINUX_SYS_EXECUTION_TIME")}')

        self.write_simulation_log(linux_time_measure=linux_execution_time)

        print(f'\n# LINUX REAL EXECUTION TIME = {linux_execution_time.get("LINUX_REAL_EXECUTION_TIME")}')
        print(f'# LINUX USER EXECUTION TIME = {linux_execution_time.get("LINUX_USER_EXECUTION_TIME")}')
        print(f'# LINUX SYS EXECUTION TIME = {linux_execution_time.get("LINUX_SYS_EXECUTION_TIME")}\n')

    def write_simulation_log(self, simulation_log: str = None, python_time_measure: str = None,
                             linux_time_measure: Dict = None) -> None:
        with open(f'{self.simulation_log_path}', "w+") as f:
            if simulation_log:
                f.write(simulation_log)

            if python_time_measure:
                f.write(f'\n# PYTHON EXECUTION TIME = {str(python_time_measure)} ms')

            if linux_time_measure:
                f.write('\n')
                for k, v in linux_time_measure.items():
                    f.write(f'#{k} = {v} ms')
