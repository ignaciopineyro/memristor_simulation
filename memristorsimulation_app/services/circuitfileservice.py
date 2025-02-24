from typing import TextIO, List

from memristorsimulation_app.representations import (
    InputParameters,
    SimulationParameters,
    DeviceParameters,
)
from memristorsimulation_app.services.directoriesmanagementservice import (
    DirectoriesManagementService,
)
from memristorsimulation_app.services.subcircuitfileservice import SubcircuitFileService


class CircuitFileService:
    def __init__(
        self,
        subcircuit_file_service: SubcircuitFileService,
        input_parameters: InputParameters,
        device_parameters: List[DeviceParameters],
        simulation_parameters: SimulationParameters,
        directories_management_service: DirectoriesManagementService,
    ):
        self.input_parameters = input_parameters
        self.device_parameters = device_parameters
        self.simulation_parameters = simulation_parameters

        self.subcircuit_file_service = subcircuit_file_service
        self.directories_management_service = directories_management_service

    def _write_dependencies(self, f: TextIO) -> None:
        f.write("\n\n* DEPENDENCIES:\n")
        f.write(
            f".include {self.directories_management_service.get_subcircuit_file_path()}"
        )

    def _write_components(self, file: TextIO) -> None:
        file.write("\n\n* COMPONENTS:\n")
        file.write(self.input_parameters.get_voltage_source_as_string())
        for device_parameter in self.device_parameters:
            file.write(f"{device_parameter.get_device()}\n")

    def _write_analysis_commands(self, file: TextIO) -> None:
        file.write("\n\n* ANALYSIS COMMANDS:\n")
        file.write(self.simulation_parameters.get_analysis())

    def _write_control_commands(self, file: TextIO) -> None:
        file.write("\n\n* CONTROL COMMANDS:\n")
        file.write(".control\n")
        file.write("run\n")
        file.write("set wr_vecnames\n")
        file.write("set wr_singlescale\n")
        file.write(
            f"wrdata {self.directories_management_service.get_export_simulation_file_path()} "
            f"{self.directories_management_service.export_parameters.get_export_magnitudes()}\n"
        )

    def write_circuit_file(self) -> None:
        """
        Writes the .cir circuit file to execute in Spice. The file is saved in simulation_results/model-name_simulations
        :return: None
        """
        self.directories_management_service.get_export_simulation_file_path()
        self.directories_management_service.create_simulation_results_for_model_folder_if_not_exists(
            self.subcircuit_file_service.model
        )

        with open(
            self.directories_management_service.get_circuit_file_path(), "w+"
        ) as f:
            f.write(
                f"* MEMRISTOR CIRCUIT - MODEL {self.subcircuit_file_service.model.value}"
            )
            self._write_dependencies(f)
            self._write_components(f)
            self._write_analysis_commands(f)
            self._write_control_commands(f)
            f.write("\nquit\n")
            f.write("\n.endc\n")
            f.write(".end\n")
