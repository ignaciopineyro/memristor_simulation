from constants import MemristorModels


class SingleDeviceSimulation:
    def __init__(self, model: MemristorModels, parameters: dict, directory: str):
        self.model = model
        self.parameters = parameters
        self.directory = directory

    def create_netlist(self):
        raise NotImplemented()

    def export_data(self):
        raise NotImplemented()