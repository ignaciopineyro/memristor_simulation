from constants import SIMULATIONS_DIR, MemristorModels
from services.circuitfileservice import CircuitFileService
from services.timemeasureservice import TimeMeasureService


class NGSpiceService:
    def __init__(self, circuit_file_service: CircuitFileService, model: MemristorModels):
        self.circuit_file_service = circuit_file_service
        self.model = model
        self.circuit_file_path = (
            f'{SIMULATIONS_DIR}/{self.circuit_file_service.get_simulation_file_name(self.model)}'
        )

        self.time_measure = TimeMeasureService(
            self.circuit_file_path, self.circuit_file_service.export_parameters.get_export_simulation_file_path()
        )

    def run_simulation(self):
        self.time_measure.execute_with_time_measure()
