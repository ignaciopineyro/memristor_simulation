import numpy as np
import pandas as pd
import os

from matplotlib import pyplot as plt
from matplotlib import animation as anime

from representations import DataLoader, ModelParameters, InputParameters, ExportParameters


class PlotterService:
    def __init__(
            self, simulation_results_directory_path: str, export_parameters: ExportParameters,
            simulation_path: str = None, model_parameters: ModelParameters = None,
            input_parameters: InputParameters = None
    ):
        self.simulation_results_directory_path = simulation_results_directory_path
        self.export_parameters = export_parameters
        self.model_simulations_directory_path = (
            f'{self.simulation_results_directory_path}/{self.export_parameters.model_simulation_folder_name.value}'
        )
        self.simulations_directory_path = (
            f'{self.model_simulations_directory_path}/{self.export_parameters.folder_name}'
        )

        self.simulation_path = simulation_path  # TODO: Agregar posibilidad de simular 1 solo file
        self.model_parameters = model_parameters
        self.input_parameters = input_parameters

    def load_data(self) -> DataLoader:
        files_in_model_simulations_directory = os.listdir(self.simulations_directory_path)
        csv_files_names, csv_files_names_no_extension, csv_files_path = [], [], []
        for file_in_simulations_directory in sorted(files_in_model_simulations_directory):
            if len(file_in_simulations_directory.split('.csv')) > 1:
                csv_files_names.append(file_in_simulations_directory)
                csv_files_names_no_extension.append(file_in_simulations_directory.replace('.csv', ''))
                csv_files_path.append(
                    os.path.join(self.simulations_directory_path, file_in_simulations_directory)
                )

        # Depracted way to read csv
        # dataframes = [
        #     pd.DataFrame(
        #         np.concatenate(
        #             [
        #                 pd.read_csv(
        #                     csv_file_path, sep=r"\s+", engine='python', skipfooter=4
        #                 )[1:len(pd.read_csv(csv_file_path, sep=r"\s+", engine='python', skipfooter=4)) + 1]
        #             ]
        #         ), columns=pd.read_csv(csv_file_path, sep=r"\s+", engine='python', skipfooter=4).columns
        #     ) for csv_file_path in csv_files_path
        # ]

        dataframes = [
            pd.DataFrame(
                pd.read_csv(csv_file_path, sep=r"\s+", engine='python', skipfooter=4)
            ) for csv_file_path in csv_files_path
        ]

        return DataLoader(csv_files_names, csv_files_names_no_extension, csv_files_path, dataframes)

    def plot_iv(
            self, df: pd.DataFrame, csv_file_name: str, title: str = None
    ) -> None:
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
        plt.savefig(f'{self.simulations_directory_path}/{csv_file_name}.jpg')
        plt.close()

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
        plt.savefig(f'{self.simulations_directory_path}/{csv_file_name}_states.jpg')

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

        with writer.saving(fig, f"{self.simulations_directory_path}/{csv_file_name}_animation.gif", 100):
            for xval, yval in zip(df['vin'], -df['i(v1)']):
                xlist.append(xval)
                ylist.append(yval)

                l.set_data(xlist, ylist)
                p1.set_data(xval, yval)
                writer.grab_frame()

        plt.close()

    def plot_heaviside_terms(self):
        raise NotImplementedError
