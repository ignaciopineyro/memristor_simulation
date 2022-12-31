import subprocess
import sys
import time


class TimeMeasureService:
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
        if self._is_os_linux():
            self.start_time = self.init_python_execution_time_measure()
            _, linux_time_output = subprocess.Popen(
                ['bash', '-c', f'time ngspice {self.circuit_file_path} 2>&1', '_'], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).communicate()

            self.write_python_time_measure_into_csv()
            self.write_linux_time_measure_into_csv(linux_time_output)

        else:
            self.start_time = self.init_python_execution_time_measure()

            subprocess.call(self.generic_os_execute_command)

            self.write_python_time_measure_into_csv()

    @staticmethod
    def init_python_execution_time_measure():
        return time.time()

    @staticmethod
    def end_python_execution_time_measure(start_time):
        return time.time() - start_time

    def write_python_time_measure_into_csv(self):
        with open(self.simulation_result_file_path, "a") as f:
            f.write(
                f'\n# PYTHON EXECUTION TIME = {(self.end_python_execution_time_measure(self.start_time)) * 1000} ms'
            )

        print(f'\n# PYTHON EXECUTION TIME = {(self.end_python_execution_time_measure(self.start_time)) * 1000} ms')

    def write_linux_time_measure_into_csv(self, linux_time_output):
        decoded_linux_time_output = linux_time_output.decode().split('\n')
        real_time = decoded_linux_time_output[1]
        user_time = decoded_linux_time_output[2]
        sys_time = decoded_linux_time_output[3]

        with open(self.simulation_result_file_path, "a") as f:
            f.write(f'\n# LINUX EXECUTION TIME = {real_time}; {user_time}; {sys_time};')

        print(f'\n# LINUX EXECUTION TIME = {real_time}; {user_time}; {sys_time};')
