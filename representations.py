from dataclasses import fields
import os
from dataclasses import dataclass
from typing import List

from constants import WaveForms, AnalysisType, SIMULATIONS_DIR, ModelsSimulationFolders, SpiceDevices, SpiceModel


@dataclass()
class InputParameters:
    source_number: int
    n_plus: str
    n_minus: str
    wave_form: WaveForms
    vo: float
    amplitude: float
    frequency: float
    td: float = None
    theta: float = None
    phase: float = None

    @classmethod
    def get_voltage_source(cls, params) -> str:
        return(
            f"V{params.source_number} {params.n_plus} {params.n_minus} {params.wave_form.value} {params.vo}"
            f" {params.amplitude} {params.frequency} {params.td if params.td else ''}"
            f" {params.theta if params.theta else ''} {params.phase if params.phase else ''}\n"
        )


@dataclass()
class DeviceParameters:
    device_name: str
    device_number: int
    nodes: List[str]
    subcircuit: str

    @classmethod
    def get_device(cls, params) -> str:
        nodes = ' '.join(params.nodes)
        return(
            f"{params.device_name}{params.device_number} {nodes} {params.subcircuit}"
        )


@dataclass()
class ModelParameters:
    alpha: float
    beta: float
    rinit: float
    roff: float
    ron: float
    vt: float


@dataclass()
class SimulationParameters:
    analysis_type: AnalysisType
    tstep: float
    tstop: float
    tstart: float = None
    tmax: float = None
    uic: bool = None

    @classmethod
    def get_analysis(cls, params) -> str:
        return(
            f"{params.analysis_type.value} {params.tstep} {params.tstop} {params.tstart if params.tstart else ''}"
            f" {params.tmax if params.tmax else ''} {'uic' if params.uic else ''}"
        )


@dataclass()
class ExportParameters:
    model_simulation_folder_name: ModelsSimulationFolders
    folder_name: str
    file_name: str
    magnitudes: List[str]

    @staticmethod
    def create_folder_if_not_exist(model_simulation_folder_name: ModelsSimulationFolders, folder_name: str) -> None:
        folder_directory = f'{SIMULATIONS_DIR}/{model_simulation_folder_name.value}/{folder_name}'
        if not os.path.exists(folder_directory):
            os.makedirs(folder_directory)

    def get_export_simulation_file_path(self) -> str:
        self.create_folder_if_not_exist(self.model_simulation_folder_name, self.folder_name)
        return (
            f"./simulation_results/{self.model_simulation_folder_name.value}/{self.folder_name}/"
            f"{self.file_name}.csv"
        )

    def get_export_magnitudes(self) -> str:
        return ' '.join(self.magnitudes)


@dataclass()
class Subcircuit:
    name: str
    nodes: List[str]
    parameters: dict

    @classmethod
    def get_subcircuit_nodes(cls, subcircuit) -> str:
        nodes = ''
        for node in subcircuit.nodes:
            nodes += f'{node} '

        return nodes

    @classmethod
    def get_subcircuit_parameters(cls, subcircuit) -> str:
        params = ''
        for key, value in subcircuit.parameters.items():
            params += f'{key}={value} '

        return params


@dataclass()
class ModelDependence:
    name: SpiceDevices
    model: SpiceModel


@dataclass()
class Source:
    name: str
    n_plus: str
    n_minus: str
    behaviour_function: str

    @classmethod
    def get_source_nodes(cls, source) -> str:
        return ' '.join(source.nodes)


@dataclass()
class Component:
    name: str
    n_plus: str
    n_minus: str
    value: float = None
    extra_data: str = None
    model: str = None

    def get_attributes_as_string(self):
        attr_str = ''
        for field in fields(self):
            if getattr(self, field.name) is not None:
                attr_str += f'{getattr(self, field.name) } '

        return attr_str
