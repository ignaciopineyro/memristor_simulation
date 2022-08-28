import numpy as np
import pandas as pd
import os

from matplotlib import pyplot as plt

path = os.path.dirname(__file__)

dataframes = []
csv_files_in_directory = []
csv_files_path_in_directory = []

models = ['pershin_simulations', 'pershin-vourkas_simulations']
pershin_params = {'Alpha': '0', 'Beta': '1E13', 'Rinit': '5K', 'Roff': '10K', 'Ron': '1K', 'Vt': '4.6'}
pershin_values = {
    'Alpha': [0, 0.01, 0.05, 0.1, 0.5, 1, 2, 10],
    'Beta': [0, 1, 1e3, 1e5, 1e10, 1e13, 1e20, 1e30],
    'Rinit': [value * 1e3 for value in [0.2, 0.5, 1, 2.5, 5, 10, 100, 1000]],
    'Roff': [value * 1e3 for value in [0.2, 0.5, 1, 2.5, 5, 10, 100, 1000]],
    'Ron': [value * 1e3 for value in [0.2, 0.5, 1, 2.5, 5, 10, 100, 1000]],
    'Vt': [0, 1.5, 3, 3.8, 4.2, 4.6, 5, 6]
}

for variable_param in list(pershin_params):
    #variable_param = list(pershin_params)[0]
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

    subplot_index = 1

    for filepath in csv_files_path_in_directory:
        df = pd.DataFrame(
            np.concatenate([pd.read_csv(filepath, sep=r"\s+")[1:len(pd.read_csv(filepath, sep=r"\s+"))+1]]),
            columns=pd.read_csv(filepath, sep=r"\s+").columns
        )

        plt.figure(0, figsize=(15, 10))
        plt.plot(df['vin'], -df['i(v1)'], label=f'{variable_param} = {pershin_values[variable_param][subplot_index-1]}')
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'I-V {model} - {variable_param} = {pershin_values[variable_param]}', fontsize=18)
        plt.legend()
        plt.savefig(f'{path}/{simulations_path}/{variable_param}_comparison.jpg')

        plt.figure(1, figsize=(20, 16))
        plt.subplot(3, 3, subplot_index)
        plt.plot(df['vin'], -df['i(v1)'])
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'{variable_param} = {pershin_values[variable_param][subplot_index - 1]}', fontsize=18)
        plt.suptitle(f'I-V {model} {pershin_params}', fontsize=25)
        plt.savefig(f'{path}/{simulations_path}/subplot.jpg')

        plt.figure(subplot_index + 1, figsize=(15, 10))
        plt.plot(df['vin'], -df['i(v1)'])
        plt.xlabel('Vin [V]')
        plt.ylabel('i(v1) [A]')
        plt.title(f'I-V {model} - {variable_param} = {pershin_values[variable_param][subplot_index - 1]}', fontsize=18)
        plt.savefig(f'{path}/{simulations_path}/{csv_files_in_directory[subplot_index - 1]}.jpg')

        subplot_index += 1
