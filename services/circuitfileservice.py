from typing import TextIO

from constants import MemristorModels
from representations import InputParameters, ModelParameters, SimulationParameters, DeviceParameters, ExportParameters
from services.filemanagementservice import FileManagementService


class CircuitFileService:
    def __init__(self, model: MemristorModels, input_parameters: InputParameters, model_parameters: ModelParameters,
                 device_parameters: DeviceParameters, simulation_parameters: SimulationParameters,
                 export_parameters: ExportParameters):

        self.model = model
        self.input_parameters = input_parameters
        self.model_parameters = model_parameters
        self.device_parameters = device_parameters
        self.simulation_parameters = simulation_parameters
        self.export_parameters = export_parameters

        self.file_management_service = FileManagementService(circuit_file_service=self)
        self.circuit_file_path = self.file_management_service.get_circuit_file_path()
        self.model_dir = self.file_management_service.get_model_dir()
        self.export_simulation_file_path = self.file_management_service.get_export_simulation_file_path()

    def _write_dependencies(self, f: TextIO) -> None:
        f.write("\n\n* DEPENDENCIES:\n")
        f.write(f".include {self.model_dir}")

    def _write_components(self, file: TextIO) -> None:
        file.write("\n\n* COMPONENTS:\n")
        file.write(self.input_parameters.get_voltage_source())
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
            f'wrdata {self.export_simulation_file_path} {self.export_parameters.get_export_magnitudes()}'
        )
        # TODO: ADD NGSPICE SIMULATION TIME COMMAND IF EXISTS

    def write_circuit_file(self) -> None:
        """
        Writes the .cir circuit file to execute in Spice. The file is saved in simulation_results/model-name_simulations
        :return: None
        """
        with open(self.circuit_file_path, "w+") as f:
            f.write(f'* MEMRISTOR CIRCUIT - MODEL {self.model.value}')
            self._write_dependencies(f)
            self._write_components(f)
            self._write_analysis_commands(f)
            self._write_control_commands(f)
            f.write('\nquit\n')
            f.write('\n.endc\n')
            f.write('.end\n')
