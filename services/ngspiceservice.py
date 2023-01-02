from services.circuitfileservice import CircuitFileService
from services.timemeasureservice import TimeMeasureService


class NGSpiceService:
    def __init__(self, circuit_file_service: CircuitFileService):
        self.circuit_file_service = circuit_file_service
        self.time_measure_service = TimeMeasureService(self.circuit_file_service)

    def run_single_simulation(self, amount_iterations: int = 1) -> None:
        time_measures = []
        for iteration in range(amount_iterations):
            time_measures.append(self.time_measure_service.execute_with_time_measure())

        if amount_iterations > 1:
            self.time_measure_service.compute_time_average(time_measures, amount_iterations)

    def run_batch_simulations(self) -> None:
        # TODO: Correr simulaciones con listas de argumentos
        raise NotImplementedError
