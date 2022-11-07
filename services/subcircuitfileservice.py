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
        model_file_path = f'{MODELS_DIR}/{self.model.value}'
        with open(model_file_path, "w+") as f:
            f.write(f'MEMRISTOR SUBCIRCUIT - MODEL {self.model.value}')
            self._write_subcircuit_parameters(f)
            if self.model_dependencies:
                self._write_model_dependencies(f)
            self._write_sources(f)
            self._write_components(f)
            self._write_control_commands(f)
            f.write('\n.ends')


pershin_params = {'Ron': 1e3, 'Roff': 10e3, 'Rinit': 5e3, 'alpha': 0, 'beta': 1E5, 'Vt': 4.6}
pershin_subckt = Subcircuit('memristor', ['pl', 'mn', 'x'], pershin_params)
source_Bx = Source(
    name='Bx', n_plus='0', n_minus='x', behaviour_function='I=\'(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: '
                                                           '(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}\''
)
capacitor = Component(name='Cx', n_plus='x', n_minus='0', value=1, extra_data='IC={Rinit}')
resistor = Component(name='R0', n_plus='pl', n_minus='mn', value=1e12)
rmem = Component(name='Rmem', n_plus='pl', n_minus='mn', extra_data='r={V(x)}')
control_cmd = '.func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}'

subcircuit_service = SubcircuitFileService(
    model=MemristorModels.PERSHIN, subcircuits=[pershin_subckt], sources=[source_Bx],
    components=[capacitor, resistor, rmem], control_commands=[control_cmd]
)

subcircuit_service.write_model_subcircuit()
