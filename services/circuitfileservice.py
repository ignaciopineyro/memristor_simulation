from typing import TextIO

from constants import MemristorModels, SIMULATIONS_DIR, WaveForms, AnalysisType, ModelsSimulationFolders
from representations import InputParameters, ModelParameters, SimulationParameters, DeviceParameters, ExportParameters


class CircuitFileService:
    def __init__(self, model: MemristorModels, input_parameters: InputParameters, model_parameters: ModelParameters,
                 device_parameters: DeviceParameters, simulation_parameters: SimulationParameters,
                 export_parameters: ExportParameters):
        self.model = model
        self.model_dir = f'../../models/{model.value}'
        self.input_parameters = input_parameters
        self.model_parameters = model_parameters
        self.device_parameters = device_parameters
        self.simulation_parameters = simulation_parameters
        self.export_parameters = export_parameters

    @staticmethod
    def _get_simulation_file_name(model: MemristorModels) -> str:
        if model == MemristorModels.PERSHIN:
            return f'{ModelsSimulationFolders.PERSHIN_SIMULATIONS.value}/pershin_simulation.cir'
        elif model == MemristorModels.PERSHIN_VOURKAS:
            return f'{ModelsSimulationFolders.PERSHIN_VOURKAS_SIMULATIONS.value}/pershin_vourkas_simulation.cir'
        elif model == MemristorModels.BIOLEK:
            return f'{ModelsSimulationFolders.BIOLEK_SIMULATIONS.value}/biolek_simulation.cir'
        else:
            raise InvalidMemristorModel(f'The model {model} is not valid')

    def _write_dependencies(self, f: TextIO):
        f.write("\n\n* DEPENDENCIES:\n")
        f.write(f".include {self.model_dir}")

    def _write_components(self, file: TextIO):
        file.write("\n\n* COMPONENTS:\n")
        file.write(self.input_parameters.get_voltage_source(self.input_parameters))
        file.write(self.device_parameters.get_device(self.device_parameters))

    def _write_analysis_commands(self, file: TextIO):
        file.write("\n\n* ANALYSIS COMMANDS:\n")
        file.write(self.simulation_parameters.get_analysis(self.simulation_parameters))

    def _write_control_commands(self, file: TextIO):
        file.write("\n\n* CONTROL COMMANDS:\n")
        file.write('.control\n')
        file.write('run\n')
        file.write('set wr_vecnames\n')
        file.write('set wr_singlescale\n')
        file.write(self.export_parameters.get_export_parameters(self.export_parameters))
        # TODO: AGREGAR TIEMPO DE SIMULACION EN SPICE

    def write_circuit_file(self) -> None:
        """
        Writes the .cir circuit file to execute in Spice. The file is saved in simulation_results/model-name_simulations
        :return: None
        """
        simulation_file_path = f'{SIMULATIONS_DIR}/{self._get_simulation_file_name(self.model)}'
        with open(simulation_file_path, "w+") as f:
            f.write(f'MEMRISTOR CIRCUIT - MODEL {self.model.value}')
            self._write_dependencies(f)
            self._write_components(f)
            self._write_analysis_commands(f)
            self._write_control_commands(f)
            f.write('\n.endc\n')
            f.write('.end\n')


class InvalidMemristorModel(Exception):
    pass


input_params = InputParameters(1, 'vin', 'gnd', WaveForms.SIN, 0, 5, 1)
model_params = ModelParameters(1e3, 10e3, 5e3, 0, 1e5, 4.6)
device_params = DeviceParameters('xmem', 0, ['vin', 'gnd', 'l0'], 'memristor')
simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)
export_params = ExportParameters(
    ModelsSimulationFolders.PERSHIN_SIMULATIONS, 'TestFolderName', 'TestFileName', ['vin', 'i(v1)', 'l0']
)
netlist_simulation = CircuitFileService(
    MemristorModels.PERSHIN, input_params, model_params, device_params, simulation_params, export_params
)

netlist_simulation.write_circuit_file()
