from typing import TextIO, List

from constants import MODELS_DIR, MemristorModels
from representations import Subcircuit, ModelDependence, Source


class SubcircuitFileService:
    def __init__(
            self, model: MemristorModels, subcircuits: List[Subcircuit], sources: List[Source],
            model_dependencies: List[ModelDependence] = None
    ):
        self.model = model
        self.subcircuits = subcircuits
        self.model_dependencies = model_dependencies
        self.sources = sources

    def _write_subcircuit_parameters(self, file: TextIO):
        for subcircuit in self.subcircuits:
            file.write('\n\n* SUBCIRCUITS:\n')
            file.write(
                f'.subckt {subcircuit.name} {subcircuit.get_subcircuit_nodes(subcircuit)} PARAMS: '
                f'{subcircuit.get_subcircuit_parameters}')

    def _write_model_dependencies(self, file: TextIO):
        file.write('\n\n* SPICE DEPENDENCIES:\n')
        for model_dependence in self.model_dependencies:
            file.write(f'.model {model_dependence.name} {model_dependence.model}')

    def _write_sources(self, file: TextIO):
        file.write('\n\n* SOURCES:\n')
        for source in self.sources:
            file.write(f'{source.name} {source.get_source_nodes(source)} {source.behaviour_function}')

    def _write_components(self, file: TextIO):
        file.write("\n\n* COMPONENTS:\n")
        # TODO

    def _write_control_commands(self, file: TextIO):
        file.write("\n\n* CONTROL COMMANDS:\n")
        # TODO

    def write_model_subcircuit(self):
        """
        Writes the .sub subcircuit file to include on circuit's file. The file is saved in models/
        :return: None
        """
        model_file_path = f'{MODELS_DIR}/{self.model.value}.sub'
        with open(model_file_path, "w+") as f:
            f.write(f'MEMRISTOR SUBCIRCUIT - MODEL {self.model.value}')
            self._write_subcircuit_parameters(f)
            if self.model_dependencies:
                self._write_model_dependencies(f)
            self._write_sources(f)
            self._write_components(f)
            self._write_control_commands(f)
            f.write('.ends')

# TODO: Testear clase
