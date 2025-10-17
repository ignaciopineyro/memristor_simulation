from memristorsimulation_app.constants import (
    MemristorModels,
    ModelsSimulationFolders,
    NetworkType,
)
from memristorsimulation_app.representations import (
    ExportParameters,
    InputParameters,
    ModelParameters,
    NetworkParameters,
    SimulationInputs,
    SimulationParameters,
    Subcircuit,
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
    def __init__(self, request_parameters: dict):
        self.request_parameters = request_parameters
        self.simulation_inputs: SimulationInputs = self.parse_request_parameters(
            request_parameters
        )

        self.directories_management_service = DirectoriesManagementService(
            self.simulation_inputs.model, self.simulation_inputs.export_parameters
        )

    def parse_request_parameters(self, request_parameters: dict) -> SimulationInputs:
        model = MemristorModels(request_parameters["model"])
        magnitudes = request_parameters["magnitudes"]
        folder_name = request_parameters["folder_name"]
        file_name = request_parameters["file_name"]
        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(model),
            folder_name=folder_name,
            file_name=file_name,
            magnitudes=magnitudes,
        )
        model_params = ModelParameters(**request_parameters["model_parameters"])
        input_params = InputParameters(**request_parameters["input_parameters"])
        simulation_params = SimulationParameters(
            **request_parameters["simulation_parameters"]
        )
        model_parameters = ModelParameters(**model_parameters)
        subcircuit = Subcircuit(model_parameters)
        network_params = (
            NetworkParameters(**request_parameters["input_parameters"])
            if "network_parameters" in request_parameters["input_parameters"]
            else None
        )
        plot_types = request_parameters.get("plot_types", [])

        return SimulationInputs(
            model=model,
            model_parameters=model_params,
            subcircuit=subcircuit,
            input_parameters=input_params,
            simulation_parameters=simulation_params,
            network_parameters=network_params,
            export_parameters=export_params,
            plot_types=plot_types,
        )

    def create_subcircuit_file_service_from_request(self) -> SubcircuitFileService:
        # Sources, components, dependencies and control_cmd are created by default due to its complexity and impact in the subcircuit
        default_sources = self.create_default_behavioural_source()
        default_components, model_dependencies = (
            self.create_default_components_and_dependencies_from_model(
                self.simulation_inputs.model
            )
        )
        default_control_cmd = self.create_default_control_cmd()

        return SubcircuitFileService(
            model=self.simulation_inputs.model,
            subcircuit=self.simulation_inputs.subcircuit,
            sources=default_sources,
            directories_management_service=self.directories_management_service,
            model_dependencies=model_dependencies,
            components=default_components,
            control_commands=[default_control_cmd],
        )

    def create_circuit_file_service_from_request(
        self,
        subcircuit_file_services: SubcircuitFileService,
    ) -> CircuitFileService:
        # TODO: Borrar
        # wave_form = self.create_wave_form(self.simulation_inputs.wave)
        # Input params and simulation params are created by default due to its complexity and impact in the subcircuit
        input_params = self.create_default_input_parameters(
            self.simulation_inputs.input_parameters.wave_form
        )
        network_type = NetworkType(self.simulation_inputs.network_type)
        if network_type in [
            NetworkType.GRID_2D_GRAPH,
            NetworkType.RANDOM_REGULAR_GRAPH,
            NetworkType.WATTS_STROGATZ_GRAPH,
        ]:
            network_parameters = self.simulation_inputs.network_parameters
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
            self.simulation_inputs.simulation_parameters,
            self.directories_management_service,
        )

    def simulate(
        self,
        circuit_file_service: CircuitFileService,
    ) -> None:
        circuit_file_service = self.build_and_write()
        ngspice_service = NGSpiceService(self.directories_management_service)
        ngspice_service.run_single_circuit_simulation(
            self.simulation_inputs.amount_iterations
        )
        self.plot(
            export_parameters=self.simulation_inputs.export_parameters,
            model_parameters=circuit_file_service.subcircuit_file_service.subcircuit.parameters,
            input_parameters=circuit_file_service.input_parameters,
            plot_types=self.simulation_inputs.plot_types,
        )

    def build_and_write(self) -> CircuitFileService:
        subcircuit_file_service = self.create_subcircuit_file_service_from_request()
        circuit_file_service = self.create_circuit_file_service_from_request(
            subcircuit_file_service
        )
        circuit_file_service.subcircuit_file_service.write_subcircuit_file()
        circuit_file_service.write_circuit_file()

        return circuit_file_service
