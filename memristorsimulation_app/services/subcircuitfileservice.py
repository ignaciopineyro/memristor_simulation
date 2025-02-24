from typing import TextIO, List
from memristorsimulation_app.constants import MemristorModels
from memristorsimulation_app.representations import (
    Subcircuit,
    ModelDependence,
    BehaviouralSource,
    Component,
)
from memristorsimulation_app.services.directoriesmanagementservice import (
    DirectoriesManagementService,
)


class SubcircuitFileService:
    def __init__(
        self,
        model: MemristorModels,
        subcircuit: Subcircuit,
        sources: List[BehaviouralSource],
        directories_management_service: DirectoriesManagementService,
        model_dependencies: List[ModelDependence] = None,
        components: List[Component] = None,
        control_commands: List[str] = None,
    ):
        self.model = model
        self.subcircuit = subcircuit
        self.model_dependencies = model_dependencies
        self.sources = sources
        self.components = components
        self.control_commands = control_commands

        self.directories_management_service = directories_management_service
        self.model_file_path = (
            self.directories_management_service.get_subcircuit_file_path()
        )

    def _write_subcircuit_parameters(self, file: TextIO) -> None:
        file.write("\n\n* SUBCIRCUITS:\n")
        file.write(
            f".subckt {self.subcircuit.name} {self.subcircuit.get_nodes_as_string()} PARAMS: "
            f"{self.subcircuit.parameters.get_parameters_as_string()}\n"
        )

    def _write_model_dependencies(self, file: TextIO) -> None:
        file.write("\n\n* SPICE DEPENDENCIES:\n")
        for model_dependence in self.model_dependencies:
            file.write(
                f".model {model_dependence.name.value} {model_dependence.model.value}"
            )

    def _write_sources(self, file: TextIO) -> None:
        file.write("\n\n* SOURCES:\n")
        for source in self.sources:
            file.write(
                f"{source.name} {source.n_plus} {source.n_minus} {source.behaviour_function}\n"
            )

    def _write_components(self, file: TextIO) -> None:
        file.write("\n\n* COMPONENTS:\n")
        for component in self.components:
            file.write(f"{component.get_attributes_as_string()}\n")

    def _write_control_commands(self, file: TextIO) -> None:
        file.write("\n\n* CONTROL COMMANDS:\n")
        for control_command in self.control_commands:
            file.write(f"{control_command}\n")

    def write_subcircuit_file(self) -> None:
        """
        Writes the .sub subcircuit file to include on circuit's file. The file is saved in models/
        :return: None
        """
        self.directories_management_service.get_export_simulation_file_path()

        with open(self.model_file_path, "w+") as f:
            f.write(f"* MEMRISTOR SUBCIRCUIT - MODEL {self.model.value}")
            self._write_subcircuit_parameters(f)
            if self.model_dependencies:
                self._write_model_dependencies(f)
            self._write_sources(f)
            self._write_components(f)
            self._write_control_commands(f)
            f.write("\n.ends")
