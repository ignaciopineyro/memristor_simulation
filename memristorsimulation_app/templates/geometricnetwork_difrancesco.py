from memristorsimulation_app.constants import (
    MemristorModels,
    SpiceDevices,
    SpiceModel,
    AnalysisType,
    ModelsSimulationFolders,
    PlotType,
    NetworkType,
)
from memristorsimulation_app.representations import (
    ModelParameters,
    Subcircuit,
    BehaviouralSource,
    ModelDependence,
    InputParameters,
    SinWaveForm,
    SimulationParameters,
    ExportParameters,
    NetworkParameters,
    Graph,
)
from memristorsimulation_app.services.circuitfileservice import CircuitFileService
from memristorsimulation_app.services.networkservice import NetworkService
from memristorsimulation_app.services.ngspiceservice import NGSpiceService
from memristorsimulation_app.services.subcircuitfileservice import SubcircuitFileService
from memristorsimulation_app.templates.template import Template


class GeometricNetworkDiFrancesco(Template):
    N = 4
    M = 4
    REMOVAL_PROBABILITY = 0

    ALPHA = 0
    BETA = 500e3
    RINIT = 200e3
    ROFF = 200e3
    RON = 2e3
    VT = 0.6

    VO = 0
    AMPLITUDE = 12
    FREQUENCY = 1
    PHASE = 180
    WAVE_FORM = SinWaveForm

    T_STEP = 2e-3
    T_STOP = 10

    EXPORT_FOLDER_NAME = f"geometric_network_difrancesco_{N}x{M}"
    EXPORT_FILE_NAME = f"geometric_network_difrancesco_{N}x{M}_simulation"
    AMOUNT_ITERATIONS = 1

    PLOT_TYPES = [
        PlotType.IV,
        PlotType.IV_LOG,
        PlotType.CURRENT_AND_VIN_VS_TIME,
        PlotType.GRAPH,
    ]

    def __init__(self, model: MemristorModels):
        self.model = model
        self.network_service = NetworkService(
            NetworkType.GRID_2D_GRAPH,
            NetworkParameters(N=self.N, M=self.M),
            removal_probability=self.REMOVAL_PROBABILITY,
        )
        self.graph = Graph(
            self.network_service.network,
            self.network_service.vin_minus,
            self.network_service.vin_plus,
        )

    def create_subcircuit_file_service(
        self,
    ) -> SubcircuitFileService:
        model_parameters = ModelParameters(
            self.ALPHA, self.BETA, self.RINIT, self.ROFF, self.RON, self.VT
        )
        subcircuit = Subcircuit("memristor", ["pl", "mn", "x"], model_parameters)
        source_bx = BehaviouralSource(
            name="Bx",
            n_plus="0",
            n_minus="x",
            behaviour_function="I='(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: "
            "(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}'",
        )

        model_dependencies = None
        default_components = None

        if self.model == MemristorModels.PERSHIN:
            default_components = self._create_pershin_default_components()

        elif self.model == MemristorModels.VOURKAS:
            default_components = self._create_vourkas_default_components()
            model_dependencies = [
                ModelDependence(name=SpiceDevices.DIODE, model=SpiceModel.DIODE)
            ]

        control_cmd = ".func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}"

        return SubcircuitFileService(
            model=self.model,
            subcircuit=subcircuit,
            sources=[source_bx],
            model_dependencies=model_dependencies,
            components=default_components,
            control_commands=[control_cmd],
        )

    def create_circuit_file_service(
        self, subcircuit_file_services: SubcircuitFileService
    ) -> CircuitFileService:
        input_params = InputParameters(
            1,
            "vin",
            "gnd",
            self.WAVE_FORM(self.VO, self.AMPLITUDE, self.FREQUENCY, phase=self.PHASE),
        )

        device_params = self.network_service.generate_device_parameters(
            "xmem", "memristor"
        )
        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(
                subcircuit_file_services.model
            ),
            self.EXPORT_FOLDER_NAME,
            self.EXPORT_FILE_NAME,
            ["vin", "i(v1)"]
            + [device_param.nodes[2] for device_param in device_params],
        )

        simulation_params = SimulationParameters(
            AnalysisType.TRAN, self.T_STEP, self.T_STOP, 1e-9, uic=True
        )

        return CircuitFileService(
            subcircuit_file_services,
            input_params,
            device_params,
            simulation_params,
            export_params,
        )

    def simulate(self):
        subcircuit_file_service = self.create_subcircuit_file_service()
        circuit_file_service = self.create_circuit_file_service(subcircuit_file_service)
        circuit_file_service.subcircuit_file_service.write_subcircuit_file()
        circuit_file_service.write_circuit_file()
        ngspice_service = NGSpiceService(circuit_file_service)
        ngspice_service.run_single_circuit_simulation(self.AMOUNT_ITERATIONS)
        self.plot(
            export_parameters=circuit_file_service.export_parameters,
            model_parameters=circuit_file_service.subcircuit_file_service.subcircuit.parameters,
            input_parameters=circuit_file_service.input_parameters,
            plot_types=self.PLOT_TYPES,
            graph=self.graph,
        )


if __name__ == "__main__":
    GeometricNetworkDiFrancesco(MemristorModels.VOURKAS).simulate()
