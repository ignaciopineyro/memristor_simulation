from typing import List

from constants import MemristorModels, WaveForms, AnalysisType, ModelsSimulationFolders, SpiceDevices, SpiceModel, \
    SimulationTemplate, InvalidSimulationTemplate, SIMULATIONS_DIR, PlotType
from representations import Subcircuit, Source, Component, SimulationParameters, InputParameters, ModelParameters, \
    DeviceParameters, ExportParameters, ModelDependence
from services.circuitfileservice import CircuitFileService
from services.ngspiceservice import NGSpiceService
from services.plotterservice import PlotterService
from services.subcircuitfileservice import SubcircuitFileService


def _create_pershin_default_components() -> List[Component]:
    capacitor = Component(name='Cx', n_plus='x', n_minus='0', value=1, extra_data='IC={Rinit}')
    resistor = Component(name='R0', n_plus='pl', n_minus='mn', value=1e12)
    rmem = Component(name='Rmem', n_plus='pl', n_minus='mn', extra_data='r={V(x)}')

    return [capacitor, resistor, rmem]


def _create_pershin_vourkas_default_components() -> List[Component]:
    capacitor = Component(name='Cx', n_plus='x', n_minus='0', value=1, extra_data='IC={Rinit}')
    rmem = Component(name='Rmem', n_plus='pl', n_minus='mn', extra_data='r={V(x)}')
    diode_1 = Component(name='d1', n_plus='aux1', n_minus='x', model=SpiceDevices.DIODE)
    diode_2 = Component(name='d2', n_plus='x', n_minus='aux2', model=SpiceDevices.DIODE)
    v_1 = Component(name='v1', n_plus='aux1', n_minus='0', extra_data='{Ron}')
    v_2 = Component(name='v2', n_plus='aux2', n_minus='0', extra_data='{Roff}')
    raux = Component(name='Raux', n_plus='pl', n_minus='mn', value=1e12)

    return [capacitor, rmem, diode_1, diode_2, v_1, v_2, raux]


def create_di_francesco_variable_amplitude_circuit_file_service(model: MemristorModels) -> List[CircuitFileService]:
    circuit_file_service = []
    for amplitude in [0.7, 1, 2, 4]:
        input_params = InputParameters(1, 'vin', 'gnd', WaveForms.SIN, 0, amplitude, 1)
        device_params = DeviceParameters('xmem', 0, ['vin', 'gnd', 'l0'], 'memristor')
        simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)
        export_folder_name = 'di_francesco_vin_amplitude'
        export_file_name = f'vin_{amplitude}'
        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(model), export_folder_name, export_file_name,
            ['vin', 'i(v1)', 'l0']
        )

        circuit_file_service.append(
            CircuitFileService(model, input_params, device_params, simulation_params, export_params)
        )

    return circuit_file_service


def create_di_francesco_subcircuit_file_service(
        model: MemristorModels, model_parameters: ModelParameters
) -> List[SubcircuitFileService]:
    pershin_subckt = Subcircuit('memristor', ['pl', 'mn', 'x'], model_parameters)
    source_bx = Source(
        name='Bx', n_plus='0', n_minus='x', behaviour_function="I=\'(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: "
                                                               "(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}\'"
    )

    model_dependencies = None
    default_components = None

    if model == MemristorModels.PERSHIN:
        default_components = _create_pershin_default_components()

    elif model == MemristorModels.PERSHIN_VOURKAS:
        default_components = _create_pershin_vourkas_default_components()
        model_dependencies = [ModelDependence(name=SpiceDevices.DIODE, model=SpiceModel.DIODE)]

    control_cmd = '.func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}'

    return [
        SubcircuitFileService(
            model=MemristorModels.PERSHIN, subcircuits=[pershin_subckt], sources=[source_bx],
            model_dependencies=model_dependencies, components=default_components, control_commands=[control_cmd],
        )
    ]


def create_test_pershin_circuit_file_service() -> List[CircuitFileService]:
    input_params = InputParameters(1, 'vin', 'gnd', WaveForms.SIN, 0, 5, 1)
    device_params = DeviceParameters('xmem', 0, ['vin', 'gnd', 'l0'], 'memristor')
    simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)
    export_folder_name = 'test_parameter'
    export_file_name = 'testSimulation'
    export_params = ExportParameters(
        ModelsSimulationFolders.PERSHIN_SIMULATIONS, export_folder_name, export_file_name, ['vin', 'i(v1)', 'l0']
    )

    return [
        CircuitFileService(MemristorModels.PERSHIN, input_params, device_params, simulation_params, export_params)
    ]


def create_test_pershin_subcircuit_file_service() -> List[SubcircuitFileService]:
    pershin_params = ModelParameters(0, 5e5, 5e3, 10e3, 1e3, 4.6)
    pershin_subckt = Subcircuit('memristor', ['pl', 'mn', 'x'], pershin_params)
    source_bx = Source(
        name='Bx', n_plus='0', n_minus='x', behaviour_function='I=\'(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: '
                                                               '(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}\''
    )
    capacitor = Component(name='Cx', n_plus='x', n_minus='0', value=1, extra_data='IC={Rinit}')
    resistor = Component(name='R0', n_plus='pl', n_minus='mn', value=1e12)
    rmem = Component(name='Rmem', n_plus='pl', n_minus='mn', extra_data='r={V(x)}')
    control_cmd = '.func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}'

    return [
        SubcircuitFileService(
            model=MemristorModels.PERSHIN, subcircuits=[pershin_subckt], sources=[source_bx],
            components=[capacitor, resistor, rmem], control_commands=[control_cmd]
        )
    ]


def simulate(simulation_template: SimulationTemplate = SimulationTemplate.DEFAULT, plot_types: List[PlotType] = None):
    if simulation_template == SimulationTemplate.DEFAULT:
        subcircuit_file_service = create_test_pershin_subcircuit_file_service()
        circuit_file_service = create_test_pershin_circuit_file_service()

    elif simulation_template == SimulationTemplate.DI_FRANCESCO_VARIABLE_AMPLITUDE:
        model_parameters = ModelParameters(0, 5e5, 200e3, 200e3, 2e3, 0.6)
        subcircuit_file_service = create_di_francesco_subcircuit_file_service(MemristorModels.PERSHIN, model_parameters)
        circuit_file_service = create_di_francesco_variable_amplitude_circuit_file_service(MemristorModels.PERSHIN)

    elif simulation_template == SimulationTemplate.DI_FRANCESCO_VARIABLE_BETA:
        pass

    else:
        raise InvalidSimulationTemplate()

    for cfs in circuit_file_service:
        for sfs in subcircuit_file_service:
            sfs.write_subcircuit_file()
            cfs.write_circuit_file()

            ngspice_service = NGSpiceService(cfs)
            ngspice_service.run_single_circuit_simulation()

            for subcircuit in sfs.subcircuits:
                plot(
                    export_parameters=cfs.export_parameters, subcircuit_parameters=subcircuit.parameters,
                    input_parameters=cfs.input_parameters, plot_types=plot_types
                )


def plot(
        export_parameters: ExportParameters, subcircuit_parameters: ModelParameters = None,
        input_parameters: InputParameters = None, plot_types: List[PlotType] = None
):
    plotter_service = PlotterService(
        simulation_results_directory_path=SIMULATIONS_DIR, export_parameters=export_parameters,
        model_parameters=subcircuit_parameters, input_parameters=input_parameters
    )
    data_loader = plotter_service.load_data()

    for df, csv_file_name_no_extension in zip(data_loader.dataframes, data_loader.csv_files_names_no_extension):
        plotter_service.plot_iv(df, csv_file_name_no_extension, 'titulo') if PlotType.IV in plot_types else None


if __name__ == "__main__":
    simulate(simulation_template=SimulationTemplate.DI_FRANCESCO_VARIABLE_AMPLITUDE, plot_types=[PlotType.IV])

if __name__ == "__main__":
    plot()
