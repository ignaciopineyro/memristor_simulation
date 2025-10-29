import os
import zipfile

from io import BytesIO
from memristorsimulation_app.constants import (
    MemristorModels,
    NetworkType,
)
from memristorsimulation_app.representations import (
    ExportParameters,
    InputParameters,
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
        export_params = ExportParameters.from_dict(
            request_parameters["export_parameters"], model
        )
        input_params = InputParameters.from_dict(request_parameters["input_parameters"])
        simulation_params = SimulationParameters.from_dict(
            request_parameters["simulation_parameters"]
        )
        subcircuit = Subcircuit.from_dict(request_parameters["subcircuit"])
        network_type = NetworkType(request_parameters["network_type"])
        network_params = NetworkParameters(**request_parameters["network_parameters"])
        plot_types = request_parameters["plot_types"]

        return SimulationInputs(
            model=model,
            subcircuit=subcircuit,
            input_parameters=input_params,
            simulation_parameters=simulation_params,
            export_parameters=export_params,
            network_type=network_type,
            network_parameters=network_params,
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
        network_service, ignore_states = None, None
        if self.simulation_inputs.network_type != NetworkType.SINGLE_DEVICE:
            network_service = NetworkService(
                self.simulation_inputs.network_type,
                self.simulation_inputs.network_parameters,
            )
            ignore_states = network_service.should_ignore_states()
        device_params = self.create_device_parameters(
            self.simulation_inputs.network_type, network_service=network_service
        )

        return CircuitFileService(
            subcircuit_file_services,
            self.simulation_inputs.input_parameters,
            device_params,
            self.simulation_inputs.simulation_parameters,
            self.directories_management_service,
            ignore_states=ignore_states,
        )

    def _build_from_request_and_write(self) -> CircuitFileService:
        subcircuit_file_service = self.create_subcircuit_file_service_from_request()
        circuit_file_service = self.create_circuit_file_service_from_request(
            subcircuit_file_service
        )
        subcircuit_file_service.write_subcircuit_file()
        circuit_file_service.write_circuit_file()

        return circuit_file_service

    def simulate(self) -> None:
        circuit_file_service = self._build_from_request_and_write()
        ngspice_service = NGSpiceService(self.directories_management_service)
        ngspice_service.run_single_circuit_simulation(
            self.simulation_inputs.amount_iterations
        )
        self.plot(
            export_parameters=self.simulation_inputs.export_parameters,
            model_parameters=circuit_file_service.subcircuit_file_service.subcircuit.model_parameters,
            input_parameters=circuit_file_service.input_parameters,
            plot_types=self.simulation_inputs.plot_types,
        )

    def create_results_zip(self) -> BytesIO:
        zip_buffer = BytesIO()

        file_paths = self.directories_management_service.get_all_simulation_files()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_path, archive_name in file_paths:
                if os.path.exists(file_path):
                    zip_file.write(file_path, archive_name)

        zip_buffer.seek(0)

        return zip_buffer

    def simulate_and_create_results_zip(self) -> BytesIO:
        self.simulate()

        return self.create_results_zip()
