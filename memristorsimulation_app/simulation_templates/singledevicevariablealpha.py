from typing import List, Tuple
from memristorsimulation_app.constants import (
    MemristorModels,
    SpiceDevices,
    SpiceModel,
    AnalysisType,
    ModelsSimulationFolders,
    PlotType,
)
from memristorsimulation_app.representations import (
    ModelParameters,
    Subcircuit,
    BehaviouralSource,
    ModelDependence,
    InputParameters,
    SinWaveForm,
    DeviceParameters,
    SimulationParameters,
    ExportParameters,
)
from memristorsimulation_app.services.circuitfileservice import CircuitFileService
from memristorsimulation_app.services.directoriesmanagementservice import (
    DirectoriesManagementService,
)
from memristorsimulation_app.services.ngspiceservice import NGSpiceService
from memristorsimulation_app.services.subcircuitfileservice import SubcircuitFileService
from memristorsimulation_app.simulation_templates.basetemplate import BaseTemplate


class SingleDeviceVariableAlpha(BaseTemplate):
    ALPHA = [10e3, 100e3, 1e6, 10e6]
    BETA = 500e3
    RINIT = 200e3
    ROFF = 200e3
    RON = 2e3
    VT = 0.6

    VO = 0
    AMPLITUDE = 4
    FREQUENCY = 1
    PHASE = 0
    WAVE_FORM = SinWaveForm

    T_STEP = 2e-3
    T_STOP = 2

    EXPORT_FOLDER_NAME = "single_device_variable_alpha"
    AMOUNT_ITERATIONS = 100

    PLOT_TYPES = [
        PlotType.IV,
        PlotType.IV_OVERLAPPED,
        PlotType.IV_LOG,
        PlotType.IV_LOG_OVERLAPPED,
        PlotType.CURRENT_AND_VIN_VS_TIME,
        PlotType.STATE_AND_VIN_VS_TIME,
        PlotType.MEMRISTIVE_STATES_OVERLAPPED,
    ]

    def __init__(self, model: MemristorModels):
        self.model = model

    def create_subcircuit_file_service(
        self,
    ) -> List[SubcircuitFileService]:
        model_parameters = [
            ModelParameters(alpha, self.BETA, self.RINIT, self.ROFF, self.RON, self.VT)
            for alpha in self.ALPHA
        ]
        subcircuit = [
            Subcircuit(model_parameter) for model_parameter in model_parameters
        ]
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

        export_file_name = "alpha_variable"
        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(self.model),
            self.EXPORT_FOLDER_NAME,
            export_file_name,
            ["vin", "i(v1)", "l0"],
        )
        subcircuit_directories_management_service = DirectoriesManagementService(
            self.model, export_params
        )

        return [
            SubcircuitFileService(
                model=self.model,
                subcircuit=subcircuit,
                sources=[source_bx],
                directories_management_service=subcircuit_directories_management_service,
                model_dependencies=model_dependencies,
                components=default_components,
                control_commands=[control_cmd],
            )
            for subcircuit in subcircuit
        ]

    def create_circuit_file_service(
        self, subcircuit_file_services: List[SubcircuitFileService]
    ) -> Tuple[List[CircuitFileService], List[DirectoriesManagementService]]:
        circuit_file_services, circuit_directories_management_services = [], []
        input_params = InputParameters(
            1,
            "vin",
            "gnd",
            self.WAVE_FORM(self.VO, self.AMPLITUDE, self.FREQUENCY, phase=self.PHASE),
        )
        device_params = [DeviceParameters("xmem", 0, ["vin", "gnd", "l0"], "memristor")]
        simulation_params = SimulationParameters(
            AnalysisType.TRAN, self.T_STEP, self.T_STOP, 1e-9, uic=True
        )
        for subcircuit_file_service in subcircuit_file_services:
            export_file_name = (
                f"alpha_{subcircuit_file_service.subcircuit.model_parameters.alpha}"
            )
            export_params = ExportParameters(
                ModelsSimulationFolders.get_simulation_folder_by_model(
                    subcircuit_file_service.model
                ),
                self.EXPORT_FOLDER_NAME,
                export_file_name,
                ["vin", "i(v1)", "l0"],
            )
            circuit_directories_management_service = DirectoriesManagementService(
                self.model, export_params
            )

            circuit_file_services.append(
                CircuitFileService(
                    subcircuit_file_service,
                    input_params,
                    device_params,
                    simulation_params,
                    circuit_directories_management_service,
                )
            )
            circuit_directories_management_services.append(
                circuit_directories_management_service
            )

        return circuit_file_services, circuit_directories_management_services

    def simulate(self):
        subcircuit_file_service = self.create_subcircuit_file_service()
        circuit_file_services, directories_management_services = (
            self.create_circuit_file_service(subcircuit_file_service)
        )

        for cfs, dms in zip(circuit_file_services, directories_management_services):
            cfs.subcircuit_file_service.write_subcircuit_file()
            cfs.write_circuit_file()

            ngspice_service = NGSpiceService(dms)
            ngspice_service.run_single_circuit_simulation(self.AMOUNT_ITERATIONS)

        for cfs, dms in zip(circuit_file_services, directories_management_services):
            self.plot(
                export_parameters=dms.export_parameters,
                model_parameters=cfs.subcircuit_file_service.subcircuit.model_parameters,
                input_parameters=cfs.input_parameters,
                plot_types=self.PLOT_TYPES,
            )


if __name__ == "__main__":
    SingleDeviceVariableAlpha(MemristorModels.PERSHIN).simulate()
