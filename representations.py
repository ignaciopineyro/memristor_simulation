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

    def get_voltage_source(self) -> str:
        return(
            f"V{self.source_number} {self.n_plus} {self.n_minus} {self.wave_form.value} {self.vo}"
            f" {self.amplitude} {self.frequency} {self.td if self.td else ''}"
            f" {self.theta if self.theta else ''} {self.phase if self.phase else ''}\n"
        )


@dataclass()
class DeviceParameters:
    device_name: str
    device_number: int
    nodes: List[str]
    subcircuit: str

    def get_device(self) -> str:
        return(
            f"{self.device_name}{self.device_number} {' '.join(self.nodes)} {self.subcircuit}"
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

    def get_analysis(self) -> str:
        return(
            f"{self.analysis_type.value} {self.tstep} {self.tstop} {self.tstart if self.tstart else ''}"
            f" {self.tmax if self.tmax else ''} {'uic' if self.uic else ''}"
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

    def get_subcircuit_nodes(self) -> str:
        return ' '.join(self.nodes)

    def get_subcircuit_parameters(self) -> str:
        params = ''
        for key, value in self.parameters.items():
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

    @staticmethod
    def get_source_nodes(source) -> str:
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
