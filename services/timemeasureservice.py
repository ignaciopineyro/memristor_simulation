import subprocess
import sys
import time

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

    def execute_with_time_measure(self) -> None:
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

            # subprocess.call(self.generic_os_execute_command)
            simulation_log = subprocess.Popen(
                ['bash', '-c', self.execute_command, '_'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ).communicate()

            self.write_python_time_measure_into_csv()

        self.write_simulation_log(simulation_log)

    @staticmethod
    def init_python_execution_time_measure() -> float:
        return time.time()

    @staticmethod
    def end_python_execution_time_measure(start_time) -> float:
        return time.time() - start_time

    def write_python_time_measure_into_csv(self) -> None:
        with open(self.simulation_result_file_path, "a") as f:
            f.write(
                f'\n# PYTHON EXECUTION TIME = {(self.end_python_execution_time_measure(self.start_time)) * 1000} ms'
            )

        print(f'\n# PYTHON EXECUTION TIME = {(self.end_python_execution_time_measure(self.start_time)) * 1000} ms')

    def write_linux_time_measure_into_csv(self, linux_time_output) -> None:
        decoded_linux_time_output = linux_time_output.decode().split('\n')
        real_time = decoded_linux_time_output[1]
        user_time = decoded_linux_time_output[2]
        sys_time = decoded_linux_time_output[3]

        with open(self.simulation_result_file_path, "a") as f:
            f.write(f'\n# LINUX EXECUTION TIME = {real_time}; {user_time}; {sys_time};')

        print(f'\n# LINUX EXECUTION TIME = {real_time}; {user_time}; {sys_time};')

    def write_simulation_log(self, simulation_log, time_measure_statistics=None) -> None:
        with open(f'{self.simulation_log_path}', "w+") as f:
            f.write(simulation_log.decode())

            if time_measure_statistics:
                f.write(time_measure_statistics)
