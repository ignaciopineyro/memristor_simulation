from memristorsimulation_app.constants import (
    AnalysisType,
    MemristorModels,
    ModelsSimulationFolders,
    NetworkType,
    WaveForms,
)
from memristorsimulation_app.representations import (
    BehaviouralSource,
    ExportParameters,
    InputParameters,
    ModelParameters,
    NetworkParameters,
    SimulationParameters,
    Subcircuit,
)
from memristorsimulation_app.serializers.simulation import (
    SimulationInputsSerializer,
    ModelParametersSerializer,
    ModelSerializer,
)
from memristorsimulation_app.services.circuitfileservice import CircuitFileService
from memristorsimulation_app.services.directoriesmanagementservice import (
    DirectoriesManagementService,
)
from memristorsimulation_app.services.networkservice import NetworkService
from memristorsimulation_app.services.ngspiceservice import NGSpiceService
from memristorsimulation_app.services.subcircuitfileservice import SubcircuitFileService
from memristorsimulation_app.simulation_templates.basetemplate import BaseTemplate


class SimulationService(BaseTemplate):
    def __init__(self, input_parameters: SimulationInputsSerializer):
        self.input_parameters = input_parameters

        self.model = MemristorModels(self.input_parameters.model)
        magnitudes = self.input_parameters.model.magnitudes
        export_folder_name = self.input_parameters.export_folder_name
        export_file_name = self.input_parameters.export_file_name
        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(self.model),
            export_folder_name=export_folder_name,
            export_file_name=export_file_name,
            magnitudes=magnitudes,
        )
        self.directories_management_service = (
            self.create_directories_management_service(self.model, export_params)
        )

    def create_directories_management_service(
        self, model: MemristorModels, export_params: ExportParameters
    ) -> DirectoriesManagementService:
        return DirectoriesManagementService(model, export_params)

    def create_subcircuit_file_service_from_request(
        self, model, model_parameters, export_folder_name, export_file_name
    ) -> SubcircuitFileService:
        model_parameters = ModelParameters(**model_parameters)
        subcircuit = Subcircuit(model_parameters)
        # Sources, components, dependencies and control_cmd are created by default due to its complexity and impact in the subcircuit
        default_sources = self.create_default_behavioural_source()
        default_components, model_dependencies = (
            self.create_default_components_and_dependencies_from_model(model)
        )
        default_control_cmd = self.create_default_control_cmd()

        return SubcircuitFileService(
            model=model,
            subcircuit=subcircuit,
            sources=default_sources,
            directories_management_service=self.directories_management_service,
            model_dependencies=model_dependencies,
            components=default_components,
            control_commands=[default_control_cmd],
        )

    def create_circuit_file_service_from_request(
        self,
        subcircuit_file_services: SubcircuitFileService,
        analysis_parameters,
        wave_form_type,
        wave_params,
    ) -> CircuitFileService:
        wave_form = self.create_wave_form(WaveForms(wave_form_type), wave_params)
        # Input params and simulation params are created by default due to its complexity and impact in the subcircuit
        input_params = self.create_default_input_parameters(wave_form)
        simulation_params = self.create_default_simulation_parameters(
            analysis_parameters
        )
        network_type = NetworkType(self.input_parameters.network_type)
        if network_type in [
            NetworkType.GRID_2D_GRAPH,
            NetworkType.RANDOM_REGULAR_GRAPH,
            NetworkType.WATTS_STROGATZ_GRAPH,
        ]:
            network_parameters = self.input_parameters.network_parameters
            network_service = NetworkService(
                network_type,
                NetworkParameters(**network_parameters),
            )
        else:
            network_service = None
        device_params = self.create_device_parameters(
            network_type, network_service=network_service
        )

        return CircuitFileService(
            subcircuit_file_services,
            input_params,
            device_params,
            simulation_params,
            self.directories_management_service,
        )

    def build_from_request(self): ...

    def simulate_from_request(self): ...

    def simulate(self):
        subcircuit_file_service = self.create_subcircuit_file_service_from_request()
        circuit_file_service = self.create_circuit_file_service(subcircuit_file_service)
        circuit_file_service.subcircuit_file_service.write_subcircuit_file()
        circuit_file_service.write_circuit_file()
        ngspice_service = NGSpiceService(self.directories_management_service)
        ngspice_service.run_single_circuit_simulation(self.AMOUNT_ITERATIONS)
        self.plot(
            export_parameters=self.export_params,
            model_parameters=circuit_file_service.subcircuit_file_service.subcircuit.parameters,
            input_parameters=circuit_file_service.input_parameters,
            plot_types=self.PLOT_TYPES,
        )
