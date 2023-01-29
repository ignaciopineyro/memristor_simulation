from typing import TextIO

from representations import InputParameters, SimulationParameters, DeviceParameters, ExportParameters
from services.directoriesmanagementservice import DirectoriesManagementService
from services.subcircuitfileservice import SubcircuitFileService


class CircuitFileService:
    def __init__(
            self, subcircuit_file_service: SubcircuitFileService, input_parameters: InputParameters,
            device_parameters: DeviceParameters, simulation_parameters: SimulationParameters,
            export_parameters: ExportParameters,
    ):
        self.input_parameters = input_parameters
        self.device_parameters = device_parameters
        self.simulation_parameters = simulation_parameters
        self.export_parameters = export_parameters

        self.subcircuit_file_service = subcircuit_file_service
        self.directories_management_service = DirectoriesManagementService(circuit_file_service=self)

    def _write_dependencies(self, f: TextIO) -> None:
        f.write("\n\n* DEPENDENCIES:\n")
        f.write(f".include {self.directories_management_service.get_model_dir()}")

    def _write_components(self, file: TextIO) -> None:
        file.write("\n\n* COMPONENTS:\n")
        file.write(self.input_parameters.get_voltage_source_as_string())
        file.write(self.device_parameters.get_device())

    def _write_analysis_commands(self, file: TextIO) -> None:
        file.write("\n\n* ANALYSIS COMMANDS:\n")
        file.write(self.simulation_parameters.get_analysis())

    def _write_control_commands(self, file: TextIO) -> None:
        file.write("\n\n* CONTROL COMMANDS:\n")
        file.write('.control\n')
        file.write('run\n')
        file.write('set wr_vecnames\n')
        file.write('set wr_singlescale\n')
        file.write(
            f'wrdata {self.directories_management_service.get_export_simulation_file_path()} '
            f'{self.export_parameters.get_export_magnitudes()}'
        )
        # TODO: ADD NGSPICE SIMULATION TIME COMMAND IF EXISTS

    def write_circuit_file(self) -> None:
        """
        Writes the .cir circuit file to execute in Spice. The file is saved in simulation_results/model-name_simulations
        :return: None
        """
        self.directories_management_service.create_simulation_model_folder_if_not_exists(
            self.subcircuit_file_service.model
        )
        with open(self.directories_management_service.get_circuit_file_path(), "w+") as f:
            f.write(f'* MEMRISTOR CIRCUIT - MODEL {self.subcircuit_file_service.model.value}')
            self._write_dependencies(f)
            self._write_components(f)
            self._write_analysis_commands(f)
            self._write_control_commands(f)
            f.write('\nquit\n')
            f.write('\n.endc\n')
            f.write('.end\n')
