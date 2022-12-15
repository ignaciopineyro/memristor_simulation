from typing import TextIO, List

from constants import MODELS_DIR, MemristorModels
from representations import Subcircuit, ModelDependence, Source, Component


class SubcircuitFileService:
    def __init__(
            self, model: MemristorModels, subcircuits: List[Subcircuit], sources: List[Source],
            model_dependencies: List[ModelDependence] = None, components: List[Component] = None,
            control_commands: List[str] = None
    ):
        self.model = model
        self.model_file_path = f'{MODELS_DIR}/{self.model.value}'
        self.subcircuits = subcircuits
        self.model_dependencies = model_dependencies
        self.sources = sources
        self.components = components
        self.control_commands = control_commands

    def _write_subcircuit_parameters(self, file: TextIO):
        for subcircuit in self.subcircuits:
            file.write('\n\n* SUBCIRCUITS:\n')
            file.write(
                f'.subckt {subcircuit.name} {subcircuit.get_subcircuit_nodes(subcircuit)}PARAMS: '
                f'{subcircuit.get_subcircuit_parameters(subcircuit)}\n')

    def _write_model_dependencies(self, file: TextIO):
        file.write('\n\n* SPICE DEPENDENCIES:\n')
        for model_dependence in self.model_dependencies:
            file.write(f'.model {model_dependence.name} {model_dependence.model}')

    def _write_sources(self, file: TextIO):
        file.write('\n\n* SOURCES:\n')
        for source in self.sources:
            file.write(f'{source.name} {source.n_plus} {source.n_minus} {source.behaviour_function}\n')

    def _write_components(self, file: TextIO):
        file.write("\n\n* COMPONENTS:\n")
        for component in self.components:
            file.write(f'{component.get_attributes_as_string()}\n')

    def _write_control_commands(self, file: TextIO):
        file.write("\n\n* CONTROL COMMANDS:\n")
        for control_command in self.control_commands:
            file.write(f'{control_command}\n')

    def write_model_subcircuit(self):
        """
        Writes the .sub subcircuit file to include on circuit's file. The file is saved in models/
        :return: None
        """
        with open(self.model_file_path, "w+") as f:
            f.write(f'* MEMRISTOR SUBCIRCUIT - MODEL {self.model.value}')
            self._write_subcircuit_parameters(f)
            if self.model_dependencies:
                self._write_model_dependencies(f)
            self._write_sources(f)
            self._write_components(f)
            self._write_control_commands(f)
            f.write('\n.ends')
