import time
import pandas as pd

from abc import ABC, abstractmethod
from dataclasses import fields, dataclass, asdict
from typing import List
from constants import (
    WaveForms,
    AnalysisType,
    ModelsSimulationFolders,
    SpiceDevices,
    SpiceModel,
)


class WaveForm(ABC):
    @abstractmethod
    def to_string(self) -> str:
        pass


@dataclass
class SinWaveForm(WaveForm):
    vo: float
    amplitude: float
    frequency: float
    td: float = 0.0
    theta: float = 0.0
    phase: float = 0.0

    def to_string(self) -> str:
        return (
            f"{WaveForms.SIN.value} {self.vo} {self.amplitude} {self.frequency} {self.td if self.td else ''} "
            f"{self.theta if self.theta else ''} {self.phase if self.phase else ''}\n"
        )


@dataclass
class PulseWaveForm(WaveForm):
    v1: float
    v2: float
    td: float = 0.0
    tr: float = 0.0
    tf: float = 0.0
    pw: float = 0.5
    per: float = 1
    np: int = 0

    def to_string(self) -> str:
        return (
            f"{WaveForms.PULSE.value} {self.v1} {self.v2} {self.td} {self.tr} {self.tf} {self.pw} {self.per} "
            f"{self.np}\n"
        )


@dataclass()
class InputParameters:
    source_number: int
    n_plus: str
    n_minus: str
    wave_form: WaveForm

    def get_voltage_source_as_string(self) -> str:
        return f"V{self.source_number} {self.n_plus} {self.n_minus} {self.wave_form.to_string()}"

    def get_input_parameters_for_plot_as_string(self):
        input_params = ""
        for k, v in asdict(self).items():
            if k not in ["source_number", "n_plus", "n_minus"] and v is not None:
                input_params += f"{k}={v} "

        return input_params


@dataclass()
class DeviceParameters:
    device_name: str
    device_number: int
    nodes: List[str]
    subcircuit: str

    def get_device(self) -> str:
        return f"{self.device_name}{self.device_number} {' '.join(self.nodes)} {self.subcircuit}"


@dataclass()
class ModelParameters:
    alpha: float
    beta: float
    Rinit: float
    Roff: float
    Ron: float
    Vt: float

    def get_parameters_as_string(self):
        params = ""
        for k, v in asdict(self).items():
            params += f"{k}={v} "

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
        return (
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
        return " ".join(self.magnitudes)

    def __post_init__(self):
        timestamp = int(time.time())
        self.folder_name = self.folder_name + "_" + str(timestamp)


@dataclass()
class Subcircuit:
    name: str
    nodes: List[str]
    parameters: ModelParameters

    def get_nodes_as_string(self) -> str:
        return " ".join(self.nodes)


@dataclass()
class ModelDependence:
    name: SpiceDevices
    model: SpiceModel


@dataclass()
class SinSource:
    vo: float
    amplitude: float
    frequency: float
    td: float = None
    theta: float = None
    phase: float = None


@dataclass()
class BehaviouralSource:
    name: str
    n_plus: str
    n_minus: str
    behaviour_function: str

    @staticmethod
    def get_source_nodes(source) -> str:
        return " ".join(source.nodes)


@dataclass()
class Component:
    name: str
    n_plus: str
    n_minus: str
    value: float = None
    extra_data: str = None
    model: SpiceDevices = None

    def get_attributes_as_string(self):
        attr_str = ""
        for field in fields(self):
            if getattr(self, field.name) is not None:
                attr_str += f"{getattr(self, field.name) } "

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
    dataframe: pd.DataFrame
    csv_file_name_no_extension: str


@dataclass()
class NetworkParameters:
    N: int = None  # N dimension of a 2D NxM grid
    M: int = None  # M dimension of a 2D NxM grid
    amount_connections: int = None  # Amount of connections per node in the network
    amount_nodes: int = None  # Amount of nodes in the network
    shortcut_probability: float = (
        None  # Shortcut probability of a WATTS_STROGATZ_GRAPH (between 0 and 1)
    )
