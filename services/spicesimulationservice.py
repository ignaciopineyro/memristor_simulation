from constants import MemristorModels, MODELS_DIR, SIMULATIONS_DIR


class NetlistSimulation:
    def __init__(self, model: MemristorModels, parameters: dict, export_directory: str):
        self.model = model
        self.model_dir = f'{MODELS_DIR}/{model}'
        self.parameters = parameters
        self.export_directory = export_directory

    @staticmethod
    def _get_simulation_file_name(model: MemristorModels) -> str:
        if model == MemristorModels.PERSHIN:
            return 'pershin_simulations/pershin_simulation.cir'
        elif model == MemristorModels.PERSHIN_VOURKAS:
            return 'pershin_vourkas_simulations/pershin_vourkas_simulation.cir'
        elif model == MemristorModels.BIOLEK:
            return 'biolek_simulations/biolek_simulation.cir'
        else:
            raise InvalidMemristorModel(f'The model {model} is not valid')

    def create_netlist(self):
        simulation_file_path = f'{SIMULATIONS_DIR}/{self._get_simulation_file_name(self.model)}'
        with open(simulation_file_path, "w+") as f:
            f.write(f'MEMRISTOR SIMULATION - MODEL {self.model}\n')
            f.write(f".include {self.model_dir}\n")

    def write_single_device_simulation(self):
        raise NotImplemented()

    def export_data(self):
        raise NotImplemented()


class InvalidMemristorModel(Exception):
    pass


netlist_simulation = NetlistSimulation(MemristorModels.PERSHIN, {}, '')
netlist_simulation.create_netlist()
