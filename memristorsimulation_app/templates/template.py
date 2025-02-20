from abc import ABC
from typing import List, Union
from memristorsimulation_app.constants import SpiceDevices, PlotType, SIMULATIONS_DIR
from memristorsimulation_app.representations import (
    Component,
    ExportParameters,
    ModelParameters,
    InputParameters,
    Graph,
)
from memristorsimulation_app.services.circuitfileservice import CircuitFileService
from memristorsimulation_app.services.plotterservice import PlotterService
from memristorsimulation_app.services.subcircuitfileservice import SubcircuitFileService


class Template(ABC):
    @staticmethod
    def _create_pershin_default_components() -> List[Component]:
        capacitor = Component(
            name="Cx", n_plus="x", n_minus="0", value=1, extra_data="IC={Rinit}"
        )
        resistor = Component(name="R0", n_plus="pl", n_minus="mn", value=1e12)
        rmem = Component(name="Rmem", n_plus="pl", n_minus="mn", extra_data="r={V(x)}")

        return [capacitor, resistor, rmem]

    @staticmethod
    def _create_vourkas_default_components() -> List[Component]:
        capacitor = Component(
            name="Cx", n_plus="x", n_minus="0", value=1, extra_data="IC={Rinit}"
        )
        rmem = Component(name="Rmem", n_plus="pl", n_minus="mn", extra_data="r={V(x)}")
        diode_1 = Component(
            name="d1", n_plus="aux1", n_minus="x", model=SpiceDevices.DIODE.value
        )
        diode_2 = Component(
            name="d2", n_plus="x", n_minus="aux2", model=SpiceDevices.DIODE.value
        )
        v_1 = Component(name="v1", n_plus="aux1", n_minus="0", extra_data="{Ron}")
        v_2 = Component(name="v2", n_plus="aux2", n_minus="0", extra_data="{Roff}")
        raux = Component(name="Raux", n_plus="pl", n_minus="mn", value=1e12)

        return [capacitor, rmem, diode_1, diode_2, v_1, v_2, raux]

    @staticmethod
    def plot(
        export_parameters: ExportParameters,
        model_parameters: ModelParameters = None,
        input_parameters: InputParameters = None,
        plot_types: List[PlotType] = None,
        graph: Graph = None,
    ):
        if plot_types is not None:
            plotter_service = PlotterService(
                simulation_results_directory_path=SIMULATIONS_DIR,
                export_parameters=export_parameters,
                model_parameters=model_parameters,
                input_parameters=input_parameters,
                graph=graph,
            )
            data_loaders = plotter_service.load_data_from_csv()

            for data_loader in data_loaders:
                if PlotType.IV in plot_types:
                    plotter_service.plot_iv(
                        data_loader.dataframe, data_loader.csv_file_name_no_extension
                    )
                if PlotType.IV_OVERLAPPED in plot_types:
                    plotter_service.plot_iv_overlapped(data_loader.dataframe)
                if PlotType.IV_LOG in plot_types:
                    plotter_service.plot_iv_log(
                        data_loader.dataframe, data_loader.csv_file_name_no_extension
                    )
                if PlotType.IV_LOG_OVERLAPPED in plot_types:
                    plotter_service.plot_iv_log_overlapped(data_loader.dataframe)
                if PlotType.CURRENT_AND_VIN_VS_TIME in plot_types:
                    plotter_service.plot_current_and_vin_vs_time(
                        data_loader.dataframe, data_loader.csv_file_name_no_extension
                    )
                if PlotType.STATE_AND_VIN_VS_TIME in plot_types:
                    plotter_service.plot_state_and_vin_vs_time(
                        data_loader.dataframe, data_loader.csv_file_name_no_extension
                    )
                if PlotType.MEMRISTIVE_STATES_OVERLAPPED in plot_types:
                    plotter_service.plot_states_overlapped(data_loader.dataframe)

            if PlotType.GRAPH in plot_types and graph is not None:
                plotter_service.plot_networkx_graph()

    def create_subcircuit_file_service(
        self,
    ) -> Union[SubcircuitFileService, List[SubcircuitFileService]]:
        pass

    def create_circuit_file_service(
        self,
        subcircuit_file_service: Union[
            SubcircuitFileService, List[SubcircuitFileService]
        ],
    ) -> Union[CircuitFileService, List[CircuitFileService]]:
        pass

    def simulate(self):
        pass
