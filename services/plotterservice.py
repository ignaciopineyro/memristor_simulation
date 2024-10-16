import networkx as nx
import pandas as pd
import os

from matplotlib import pyplot as plt
from matplotlib import animation as anime
from typing import List, Tuple
from constants import MeasuredMagnitude
from representations import DataLoader, ModelParameters, InputParameters, ExportParameters
from services.directoriesmanagementservice import DirectoriesManagementService


class PlotterService:
    def __init__(
            self, simulation_results_directory_path: str, export_parameters: List[ExportParameters],
            model_parameters: ModelParameters = None, input_parameters: InputParameters = None, graph: nx.Graph = None
    ):
        self.directories_management_service = DirectoriesManagementService()

        self.simulation_results_directory_path = simulation_results_directory_path
        self.export_parameters = export_parameters
        self.model_simulations_directory_path = (
            f'{self.simulation_results_directory_path}/{self.export_parameters[0].model_simulation_folder_name.value}'
        )
        self.simulations_directory_path = (
            f'{self.model_simulations_directory_path}/{self.export_parameters[0].folder_name}'
        )
        self.figures_directory_path = f'{self.simulations_directory_path}/figures'
        self.directories_management_service.create_figures_directory(self.simulations_directory_path)

        self.model_parameters = model_parameters
        self.input_parameters = input_parameters
        self.graph = graph


    @staticmethod
    def _get_csv_measured_magnitude(csv_file_name_no_extension: str):
        if csv_file_name_no_extension.endswith('_iv'):
            return MeasuredMagnitude.IV
        elif csv_file_name_no_extension.endswith('_states'):
            return MeasuredMagnitude.STATES
        else:
            return MeasuredMagnitude.OTHER

    def load_data(self) -> List[DataLoader]:
        data_loaders = []
        files_in_model_simulations_directory = os.listdir(self.simulations_directory_path)
        for file_in_simulations_directory in sorted(files_in_model_simulations_directory):
            if file_in_simulations_directory.split('.csv')[0] in [
                export_parameter.file_name for export_parameter in self.export_parameters
            ]:
                csv_file_name_no_extension = file_in_simulations_directory.replace('.csv', '')
                csv_file_path = os.path.join(self.simulations_directory_path, file_in_simulations_directory)
                dataframe = pd.DataFrame(
                        pd.read_csv(csv_file_path, sep=r"\s+", engine='python', skipfooter=4)
                    )
                measured_magnitude = self._get_csv_measured_magnitude(csv_file_name_no_extension)

                data_loaders.append(
                    DataLoader(
                        file_in_simulations_directory, csv_file_name_no_extension, csv_file_path, measured_magnitude,
                        dataframe
                    )
                )

        return data_loaders

    def plot_iv(self, df: pd.DataFrame, csv_file_name: str, title: str = None) -> None:
        plt.figure(figsize=(12, 8))
        plt.plot(
            df['vin'], -df['i(v1)'],
            label=(
                f'{self.model_parameters.get_parameters_as_string()}'
                f'\n{self.input_parameters.get_input_parameters_for_plot_as_string()}'
            )
        )
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'I-V {csv_file_name} {title if title is not None else ""}', fontsize=22)
        plt.autoscale()
        plt.legend(loc='lower right', fontsize=12)
        plt.savefig(f'{self.figures_directory_path}/{csv_file_name}.jpg')
        plt.close()

    def plot_iv_overlapped(self, df: pd.DataFrame, title: str = None, label: str = None) -> None:
        plt.figure(0, figsize=(12, 8))
        plt.plot(
            df['vin'], -df['i(v1)'],
            label=label if label is not None else (
                f'{self.model_parameters.get_parameters_as_string()}'
                f'\n{self.input_parameters.get_input_parameters_for_plot_as_string()}'
            )
        )
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'I-V {title if title is not None else ""}', fontsize=22)
        plt.autoscale()
        plt.legend(loc='lower right', fontsize=12)
        plt.savefig(f'{self.figures_directory_path}/iv_overlapped.jpg')

    def plot_iv_log(self, df: pd.DataFrame, csv_file_name: str, title: str = None) -> None:
        plt.figure(figsize=(12, 8))
        plt.plot(
            df['vin'], abs(-df['i(v1)']),
            label=(
                f'{self.model_parameters.get_parameters_as_string()}'
                f'\n{self.input_parameters.get_input_parameters_for_plot_as_string()}'
            )
        )
        plt.yscale(value='log')
        plt.xlabel('Vin [V]')
        plt.ylabel('log(i(v1)) [A]')
        plt.title(f'log(I)-V {csv_file_name} {title if title is not None else ""}', fontsize=22)
        plt.autoscale()
        plt.legend(loc='lower right', fontsize=12)
        plt.savefig(f'{self.figures_directory_path}/{csv_file_name}_log.jpg')
        plt.close()

    def plot_iv_log_overlapped(self, df: pd.DataFrame, title: str = None, label: str = None):
        plt.figure(1, figsize=(12, 8))
        plt.plot(
            df['vin'], abs(-df['i(v1)']),
            label=label if label is not None else (
                f'{self.model_parameters.get_parameters_as_string()}'
                f'\n{self.input_parameters.get_input_parameters_for_plot_as_string()}'
            )
        )
        plt.yscale(value='log')
        plt.xlabel('Vin [V]')
        plt.ylabel('log(i(v1)) [A]')
        plt.title(f'log(I)-V {title if title is not None else ""}', fontsize=22)
        plt.autoscale()
        plt.legend(loc='lower right', fontsize=12)
        plt.savefig(f'{self.figures_directory_path}/iv_log_overlapped.jpg')

    def plot_states(self, df: pd.DataFrame, csv_file_name: str, title: dict = None) -> None:
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 1, 1)
        plt.plot(df['time'], df['vin'])
        plt.xticks([])
        plt.ylabel('Vin [V]')
        plt.subplot(2, 1, 2)
        plt.plot(
            df['time'], df['l0'],
            label=(
                f'{self.model_parameters.get_parameters_as_string()}'
                f'\n{self.input_parameters.get_input_parameters_for_plot_as_string()}'
            )
        )
        plt.xlabel('Time [s]')
        plt.ylabel(f'l0 [ohm]')
        plt.suptitle(
            f'Input voltage and State vs Time - {csv_file_name} {title if title is not None else ""}', fontsize=22
        )
        plt.legend(loc='center', bbox_to_anchor=(0.5, 1.1))
        plt.savefig(f'{self.figures_directory_path}/{csv_file_name}.jpg')
        plt.close()

    def plot_states_overlapped(self, df: pd.DataFrame, title: str = None, label: str = None) -> None:
        plt.figure(2, figsize=(12, 8))
        plt.plot(
            df['vin'], df['l0'],
            label=label if label is not None else (
                f'{self.model_parameters.get_parameters_as_string()}'
                f'\n{self.input_parameters.get_input_parameters_for_plot_as_string()}'
            )
        )
        plt.xlabel('Vin [V]')
        plt.ylabel('l0 [ohm]')
        plt.title(f'Memristive states vs Input Voltage {title if title is not None else ""}', fontsize=22)
        plt.autoscale()
        plt.legend(loc='center')
        plt.savefig(f'{self.figures_directory_path}/states_overlapped.jpg')

    def plot_iv_animated(
            self, df: pd.DataFrame, csv_file_name: str, title: dict = None
    ) -> None:
        fig = plt.figure(figsize=(12, 8))
        l, = plt.plot([], [], 'k-')
        p1, = plt.plot([], [], 'ko')
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'I-V {csv_file_name} - {title}', fontsize=10)

        plt.xlim(min(df['vin']) * 1.1, max(df['vin']) * 1.1)
        plt.ylim(min(df['i(v1)']) * 1.1, max(df['i(v1)']) * 1.1)

        metadata = dict(title="animation", artist="ignaciopineyro")
        writer = anime.PillowWriter(fps=15, metadata=metadata)

        xlist = []
        ylist = []

        with writer.saving(fig, f"{self.figures_directory_path}/{csv_file_name}_animation.gif", 100):
            for xval, yval in zip(df['vin'], -df['i(v1)']):
                xlist.append(xval)
                ylist.append(yval)

                l.set_data(xlist, ylist)
                p1.set_data(xval, yval)
                writer.grab_frame()

        plt.close()

    def plot_networkx_graph(self, gnd_node: Tuple[int, int], vin_node: Tuple[int, int]):
        color_map = []
        labels = {}
        for node in self.graph:
            if node == gnd_node:
                color_map.append('#f07b07')
                labels[node] = f'V- {node}'
            elif node == vin_node:
                color_map.append('#f07b07')
                labels[node] = f'V+ {node}'
            else:
                color_map.append('#93d9f5')
                labels[node] = node

        fig = plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph)
        nx.draw(
            self.graph, pos=pos, ax=fig.add_subplot(), with_labels=False, node_color=color_map, edge_color='#545454'
        )
        nx.draw_networkx_labels(
            self.graph, pos, labels, font_color='black', font_size=12, font_weight='bold'
        )
        fig.savefig(f'{self.figures_directory_path}/graph.jpg')
        plt.close()
