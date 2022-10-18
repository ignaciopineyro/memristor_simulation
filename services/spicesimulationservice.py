from constants import MemristorModels, SIMULATIONS_DIR, WaveForms, AnalysisType, ModelsSimulationFolders
from representations import InputParameters, ModelParameters, SimulationParameters, DeviceParameters, ExportParameters


class NetlistSimulation:
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

    def create_netlist(self):
        simulation_file_path = f'{SIMULATIONS_DIR}/{self._get_simulation_file_name(self.model)}'
        with open(simulation_file_path, "w+") as f:
            f.write(f'MEMRISTOR SIMULATION - MODEL {self.model.value}')
            f.write("\n\n* DEPENDENCIES:\n")
            f.write(f".include {self.model_dir}")
            f.write("\n\n* COMPONENTS:\n")
            f.write(self.input_parameters.get_voltage_source(self.input_parameters))
            f.write(self.device_parameters.get_device(self.device_parameters))
            f.write("\n\n* ANALYSIS COMMANDS:\n")
            f.write(self.simulation_parameters.get_analysis(self.simulation_parameters))
            f.write("\n\n* CONTROL COMMANDS:\n")
            f.write('.control\n')
            f.write('run\n')
            f.write('set wr_vecnames\n')
            f.write('set wr_singlescale\n')
            f.write(self.export_parameters.get_export_parameters(self.export_parameters))
            # TODO: AGREGAR TIEMPO DE SIMULACION
            f.write('\n.endc\n')
            f.write('.end\n')

    def write_single_device_simulation(self):
        raise NotImplemented()

    def export_data(self):
        raise NotImplemented()


class InvalidMemristorModel(Exception):
    pass


input_params = InputParameters(1, 'vin', 'gnd', WaveForms.SIN, 0, 5, 1)
model_params = ModelParameters(1e3, 10e3, 5e3, 0, 1e5, 4.6)
device_params = DeviceParameters('xmem', 0, ['vin', 'gnd', 'l0'], 'memristor')
simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)
export_params = ExportParameters(
    ModelsSimulationFolders.PERSHIN_SIMULATIONS, 'TestFolderName', 'TestFileName', ['vin', 'i(v1)', 'l0']
)
netlist_simulation = NetlistSimulation(
    MemristorModels.PERSHIN, input_params, model_params, device_params, simulation_params, export_params
)

netlist_simulation.create_netlist()
