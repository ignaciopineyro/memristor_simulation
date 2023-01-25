from dataclasses import fields, dataclass, asdict
from typing import List

import pandas as pd

from constants import WaveForms, AnalysisType, ModelsSimulationFolders, SpiceDevices, SpiceModel


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

    def get_voltage_source_as_string(self) -> str:
        return(
            f"V{self.source_number} {self.n_plus} {self.n_minus} {self.wave_form.value} {self.vo}"
            f" {self.amplitude} {self.frequency} {self.td if self.td else ''}"
            f" {self.theta if self.theta else ''} {self.phase if self.phase else ''}\n"
        )

    def get_input_parameters_for_plot_as_string(self):
        input_params = ''
        for k, v in asdict(self).items():
            if k not in ['source_number', 'n_plus', 'n_minus'] and v is not None:
                input_params += f'{k}={v} '

        return input_params

    def get_input_parameters_for_plot_legend(self):
        return f'{self.wave_form} {self.amplitude} {self.frequency} {self.td} {self.theta} {self.phase} {self.vo}'


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
    Rinit: float
    Roff: float
    Ron: float
    Vt: float

    def get_parameters_as_string(self):
        params = ''
        for k, v in asdict(self).items():
            params += f'{k}={v} '

        return params


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

    def get_export_magnitudes(self) -> str:
        return ' '.join(self.magnitudes)


@dataclass()
class Subcircuit:
    name: str
    nodes: List[str]
    parameters: ModelParameters

    def get_nodes_as_string(self) -> str:
        return ' '.join(self.nodes)


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
    model: SpiceDevices = None

    def get_attributes_as_string(self):
        attr_str = ''
        for field in fields(self):
            if getattr(self, field.name) is not None:
                attr_str += f'{getattr(self, field.name) } '

        return attr_str


@dataclass()
class TimeMeasure:
    start_time: float = None
    python_execution_time: float = None
    linux_real_execution_time: float = None
    linux_user_execution_time: float = None
    linux_sys_execution_time: float = None


@dataclass()
class AverageTimeMeasure:
    amount_iterations: int = None
    average_python_execution_time: float = None
    average_linux_real_execution_time: float = None
    average_linux_user_execution_time: float = None
    average_linux_sys_execution_time: float = None


@dataclass()
class DataLoader:
    csv_files_names: List[str]
    csv_files_names_no_extension: List[str]
    csv_files_path: List[str]
    dataframes: List[pd.DataFrame]
