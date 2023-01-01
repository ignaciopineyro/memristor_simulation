from services.circuitfileservice import CircuitFileService
from services.timemeasureservice import TimeMeasureService


class NGSpiceService:
    def __init__(self, circuit_file_service: CircuitFileService):
        self.circuit_file_service = circuit_file_service
        self.time_measure_service = TimeMeasureService(self.circuit_file_service)

    def run_single_simulation(self) -> None:
        # TODO: Agregar argumento para correr reiterativamente la simulacion para obtener valor medio de tiempos de sim
        self.time_measure_service.execute_with_time_measure()

    def run_batch_simulations(self) -> None:
        # TODO: Correr simulaciones con listas de argumentos
        raise NotImplementedError
