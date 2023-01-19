import numpy as np
import pandas as pd
import os

from matplotlib import pyplot as plt
from matplotlib import animation as anime

from representations import DataLoader, ModelParameters, InputParameters


class PlotterService:
    def __init__(
            self, simulations_directory_path: str, simulation_path: str = None,
            model_parameters: ModelParameters = None, input_parameters: InputParameters = None
    ):
        self.simulations_directory_path = simulations_directory_path
        self.simulation_path = simulation_path  # TODO: Agregar posibilidad de simular 1 solo file
        self.model_parameters = model_parameters
        self.input_parameters = input_parameters

    def _load_data(self) -> DataLoader:
        files_in_simulations_directory = os.listdir(self.simulations_directory_path)
        csv_files_names, csv_files_names_no_extension, csv_files_path = [], [], []
        for file_in_simulations_directory in sorted(files_in_simulations_directory):
            if len(file_in_simulations_directory.split('.csv')) > 1:
                csv_files_names.append(file_in_simulations_directory)
                csv_files_names_no_extension.append(file_in_simulations_directory.replace('.csv', ''))
                csv_files_path.append(os.path.join(self.simulations_directory_path, file_in_simulations_directory))

        dataframes = [
            pd.DataFrame(
                np.concatenate(
                    [pd.read_csv(csv_file_path, sep=r"\s+")[1:len(pd.read_csv(csv_file_path, sep=r"\s+")) + 1]]),
                columns=pd.read_csv(csv_file_path, sep=r"\s+").columns
            ) for csv_file_path in csv_files_path
        ]

        return DataLoader(csv_files_names, csv_files_names_no_extension, csv_files_path, dataframes)


       """
        # Parameters
        parameters = [
            {'Alpha': 0, 'Beta': np.float64(1e13), 'Rinit': np.float64(5e3), 'Roff': np.float64(10e3), 'Ron': np.float64(1e3), 'Vt': 4.6},
            {'Alpha': 0, 'Beta': np.float64(1e13), 'Rinit': np.float64(5e3), 'Roff': np.float64(10e3), 'Ron': np.float64(1e3), 'Vt': 4.6},
            {'Alpha': 0, 'Beta': np.float64(1e5), 'Rinit': np.float64(5e3), 'Roff': np.float64(10e3), 'Ron': np.float64(1e3), 'Vt': 4.6},
            {'Alpha': np.float64(10e3), 'Beta': np.float64(1e5), 'Rinit': np.float64(5e3), 'Roff': np.float64(10e3), 'Ron': np.float64(1e3), 'Vt': 4.6},
            {'Alpha': np.float64(10e3), 'Beta': np.float64(1e5), 'Rinit': np.float64(5e3), 'Roff': np.float64(10e3), 'Ron': np.float64(1e3), 'Vt': 4.6},
        ]
        """

    def plot_iv(self, fig_number: int, df: pd.DataFrame, csv_file_name: str, title: dict) -> None:
        plt.figure(fig_number, figsize=(10, 6))
        plt.plot(df['vin'], -df['i(v1)'])
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'I-V {csv_file_name} - {title}', fontsize=16)
        plt.savefig(f'{self.simulations_directory_path}/{csv_file_name}.jpg')
        plt.show()

    def plot_states(self, fig_number: int, df: pd.DataFrame, csv_file_name: str, title: dict) -> None:
        plt.figure(fig_number, figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.plot(df['time'], df['vin'])
        plt.hlines(0, 0, max(df['time']), color='black', linewidth=0.5)
        plt.xlabel('Time [s]')
        plt.ylabel('Vin [V]')
        plt.subplot(2, 1, 2)
        plt.plot(df['time'], df['l0'])
        plt.xlabel('Time [s]')
        plt.ylabel('l0 [ohm]')
        plt.suptitle(f'Input voltage and State vs Time - {csv_file_name} - {title}', fontsize=16)
        plt.savefig(f'{simulations_directory_path}/{csv_file_name}_states.jpg')
        plt.show()

    def plot_iv_animated(self, fig_number: int, df: pd.DataFrame, csv_file_name: str, title: dict,
                         plot: bool = False) -> None:
        if plot:
            fig = plt.figure(fig_number, figsize=(12, 8))
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

            with writer.saving(fig, f"{simulations_directory_path}/{csv_file_name}_animation.gif", 100):
                for xval, yval in zip(df['vin'], -df['i(v1)']):
                    xlist.append(xval)
                    ylist.append(yval)

                    l.set_data(xlist, ylist)
                    p1.set_data(xval, yval)
                    writer.grab_frame()

            plt.close()

    def plot_heaviside_terms(self):
        raise NotImplementedError
