from memristorsimulation_app.services.directoriesmanagementservice import (
    DirectoriesManagementService,
)
from memristorsimulation_app.services.timemeasureservice import TimeMeasureService


class NGSpiceService:
    def __init__(self, directories_management_service: DirectoriesManagementService):
        self.time_measure_service = TimeMeasureService(directories_management_service)

    def run_single_circuit_simulation(self, amount_iterations: int = 1) -> None:
        enable_print_time_measure = True if amount_iterations == 1 else False
        time_measures = []

        for _ in range(amount_iterations):
            time_measures.append(
                self.time_measure_service.execute_with_time_measure(
                    enable_print_time_measure
                )
            )

        if amount_iterations > 1:
            average_time_measure = self.time_measure_service.compute_time_average(
                time_measures, amount_iterations
            )
            self.time_measure_service.write_simulation_log(
                average_time_measure=average_time_measure
            )
            self.time_measure_service.print_average_time_measure(average_time_measure)
