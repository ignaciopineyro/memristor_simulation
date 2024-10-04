import numpy as np
import pandas as pd
import os

from matplotlib import pyplot as plt

path = os.path.dirname(__file__)

dataframes = []

models = ['pershin_simulations', 'vourkas_simulations']
pershin_params = {'Alpha': '0', 'Beta': '1E5', 'Rinit': '5K', 'Roff': '10K', 'Ron': '1K', 'Vt': '4.6'}
vourkas_params = {'Alpha': '0', 'Beta': '1E5', 'Rinit': '5K', 'Roff': '10K', 'Ron': '1K', 'Vt': '4.6'}
pershin_values = {
    'Alpha': [0, 1, 10, 100, 1e3, 1e5, 1e7, 1e9],
    'Beta': [0, 1, 1e3, 1e5, 1e10, 1e13, 1e20, 1e30],
    'Rinit': [value * 1e3 for value in [0.2, 0.5, 1, 2.5, 5, 10, 100, 1000]],
    'Roff': [value * 1e3 for value in [0.2, 0.5, 1, 2.5, 5, 10, 100, 1000]],
    'Ron': [value * 1e3 for value in [0.2, 0.5, 1, 2.5, 5, 10, 100, 1000]],
    'Vt': [0, 1.5, 3, 3.8, 4.2, 4.6, 5, 6]
}
vourkas_values = {
    'Alpha': [0, 1, 10, 100, 1e3, 1e5, 1e7, 1e9],
    'Beta': [0, 1, 1e3, 1e5, 1e10, 1e13, 1e20, 1e30],
    'Rinit': [value * 1e3 for value in [0.2, 0.5, 1, 2.5, 5, 10, 100, 1000]],
    'Roff': [value * 1e3 for value in [0.2, 0.5, 1, 2.5, 5, 10, 100, 1000]],
    'Ron': [value * 1e3 for value in [0.2, 0.5, 1, 2.5, 5, 10, 100, 1000]],
    'Vt': [0, 1.5, 3, 3.8, 4.2, 4.6, 5, 6]
}

for variable_param in list(pershin_params):
    csv_files_in_directory = []
    csv_files_path_in_directory = []

    model = models[0]
    simulations_path = f'simulation_results/{models[0]}/{variable_param}/'
    files_in_directory = os.listdir(simulations_path)
    for file_in_directory in files_in_directory:
        if len(file_in_directory.split('.csv')) > 1:
            csv_files_in_directory.append(file_in_directory.replace('.csv', ''))
            csv_file_path = os.path.join(path, simulations_path+file_in_directory)
            csv_files_path_in_directory.append(csv_file_path)
    csv_files_in_directory.sort()
    csv_files_path_in_directory.sort()

    for file_count, filepath in enumerate(csv_files_path_in_directory, 1):
        df = pd.DataFrame(
            np.concatenate([pd.read_csv(filepath, sep=r"\s+")[1:len(pd.read_csv(filepath, sep=r"\s+"))+1]]),
            columns=pd.read_csv(filepath, sep=r"\s+").columns
        )

        plt.figure(0, figsize=(15, 10))
        plt.plot(df['vin'], -df['i(v1)'], label=f'{variable_param} = {pershin_values[variable_param][file_count-1]}')
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'I-V {model} - {variable_param} = {pershin_values[variable_param]}', fontsize=18)
        plt.legend()
        plt.savefig(f'{path}/{simulations_path}/{variable_param}_comparison.jpg')

        plt.figure(1, figsize=(20, 16))
        plt.subplot(3, 3, file_count)
        plt.plot(df['vin'], -df['i(v1)'])
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'{variable_param} = {pershin_values[variable_param][file_count - 1]}', fontsize=18)
        plt.suptitle(f'I-V {model} {pershin_params}', fontsize=25)
        plt.savefig(f'{path}/{simulations_path}/iv_subplot.jpg')

        plt.figure(2 * file_count, figsize=(15, 10))
        plt.plot(df['vin'], -df['i(v1)'])
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'I-V {model} - {variable_param} = {pershin_values[variable_param][file_count - 1]}', fontsize=16)
        plt.savefig(f'{path}/{simulations_path}/{csv_files_in_directory[file_count - 1]}.jpg')

        plt.figure(2 * file_count + 1, figsize=(15, 10))
        plt.subplot(2, 1, 1)
        plt.plot(df['time'], df['vin'])
        plt.hlines(0, 0, max(df['time']), color='black', linewidth=0.5)
        plt.xlabel('Time [s]')
        plt.ylabel('Vin [V]')
        plt.title(f'{variable_param} = {pershin_values[variable_param][file_count - 1]}', fontsize=14)
        plt.subplot(2, 1, 2)
        plt.plot(df['time'], df['l0'])
        # TODO: La hline me saca los valores del eje Y
        plt.hlines(
            pershin_params['Rinit'], 0, max(df['time']), color='black', linestyle='dashed', linewidth=0.5,
            label='Rinit = {}'.format(pershin_params['Rinit'])
        )
        plt.xlabel('Time [s]')
        plt.ylabel('l0 [ohm]')
        plt.title(f'{variable_param} = {pershin_values[variable_param][file_count - 1]}', fontsize=14)
        plt.suptitle(f'Input voltage and State vs Time {model} {pershin_params}', fontsize=16)
        plt.legend()
        plt.savefig(f'{path}/{simulations_path}/{csv_files_in_directory[file_count - 1]}_states.jpg')

    plt.close('all')
