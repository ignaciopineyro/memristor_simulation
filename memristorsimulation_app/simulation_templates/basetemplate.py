from abc import ABC
from typing import List, Union, Tuple, Optional
from memristorsimulation_app.constants import (
    InvalidNetworkType,
    MemristorModels,
    NetworkType,
    SpiceDevices,
    PlotType,
    SIMULATIONS_DIR,
    SpiceModel,
)
from memristorsimulation_app.representations import (
    BehaviouralSource,
    Component,
    DeviceParameters,
    ExportParameters,
    ModelDependence,
    ModelParameters,
    InputParameters,
    Graph,
)
from memristorsimulation_app.services.circuitfileservice import CircuitFileService
from memristorsimulation_app.services.directoriesmanagementservice import (
    InvalidMemristorModel,
)
from memristorsimulation_app.services.networkservice import NetworkService
from memristorsimulation_app.services.plotterservice import PlotterService
from memristorsimulation_app.services.subcircuitfileservice import SubcircuitFileService


class BaseTemplate(ABC):
    def create_default_behavioural_source(self) -> List[BehaviouralSource]:
        return [
            BehaviouralSource(
                name="Bx",
                n_plus="0",
                n_minus="x",
                behaviour_function="I='(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: "
                "(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}'",
            )
        ]

    def create_default_control_cmd(self) -> str:
        return ".func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}"

    def create_default_components_and_dependencies_from_model(
        self, model: MemristorModels
    ) -> Tuple[List[Component], Optional[ModelDependence]]:
        if model == MemristorModels.PERSHIN:
            default_components = self._create_pershin_default_components()
            model_dependencies = None
        elif model == MemristorModels.VOURKAS:
            default_components = self._create_vourkas_default_components()
            model_dependencies = [
                ModelDependence(name=SpiceDevices.DIODE, model=SpiceModel.DIODE)
            ]
        else:
            raise InvalidMemristorModel(f"Model {model} not implemented.")

        return default_components, model_dependencies

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

    def create_device_parameters(
        self,
        network_type: NetworkType,
        network_service: Optional[NetworkService] = None,
    ) -> List[DeviceParameters]:
        network_service = network_service if network_service is not None else None
        if network_type == NetworkType.SINGLE_DEVICE:
            return [DeviceParameters("xmem", 0, ["vin", "gnd", "l0"], "memristor")]
        elif network_type in [
            NetworkType.GRID_2D_GRAPH,
            NetworkType.RANDOM_REGULAR_GRAPH,
            NetworkType.WATTS_STROGATZ_GRAPH,
        ]:
            if network_service is None:
                raise ValueError("network_service must be provided for network types.")
            return network_service.generate_device_parameters("xmem", "memristor")
        else:
            raise InvalidNetworkType(f"Network type {network_type} not implemented.")

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
