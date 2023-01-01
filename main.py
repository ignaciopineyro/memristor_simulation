from constants import MemristorModels, WaveForms, AnalysisType, ModelsSimulationFolders
from representations import Subcircuit, Source, Component, SimulationParameters, InputParameters, ModelParameters, \
    DeviceParameters, ExportParameters
from services.circuitfileservice import CircuitFileService
from services.ngspiceservice import NGSpiceService
from services.subcircuitfileservice import SubcircuitFileService


def create_circuits():
    input_params = InputParameters(1, 'vin', 'gnd', WaveForms.SIN, 0, 5, 1)
    model_params = ModelParameters(1e3, 10e3, 5e3, 0, 1e5, 4.6)
    device_params = DeviceParameters('xmem', 0, ['vin', 'gnd', 'l0'], 'memristor')
    simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)
    export_folder_name = 'Alpha'
    export_file_name = 'secondTest'
    export_params = ExportParameters(
        ModelsSimulationFolders.PERSHIN_SIMULATIONS, export_folder_name, export_file_name, ['vin', 'i(v1)', 'l0']
    )

    circuit_file_service = CircuitFileService(
        MemristorModels.PERSHIN, input_params, model_params, device_params, simulation_params, export_params
    )

    return circuit_file_service


def create_subcircuits():
    pershin_params = {'Ron': 1e3, 'Roff': 10e3, 'Rinit': 5e3, 'alpha': 0, 'beta': 1E5, 'Vt': 4.6}
    pershin_subckt = Subcircuit('memristor', ['pl', 'mn', 'x'], pershin_params)
    source_bx = Source(
        name='Bx', n_plus='0', n_minus='x', behaviour_function='I=\'(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: '
                                                               '(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}\''
    )
    capacitor = Component(name='Cx', n_plus='x', n_minus='0', value=1, extra_data='IC={Rinit}')
    resistor = Component(name='R0', n_plus='pl', n_minus='mn', value=1e12)
    rmem = Component(name='Rmem', n_plus='pl', n_minus='mn', extra_data='r={V(x)}')
    control_cmd = '.func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}'

    subcircuit_service = SubcircuitFileService(
        model=MemristorModels.PERSHIN, subcircuits=[pershin_subckt], sources=[source_bx],
        components=[capacitor, resistor, rmem], control_commands=[control_cmd]
    )

    return subcircuit_service


def main():
    subcircuit = create_subcircuits()
    circuit = create_circuits()

    subcircuit.write_model_subcircuit()
    circuit.write_circuit_file()

    ngspice_service = NGSpiceService(circuit)
    ngspice_service.run_single_simulation()


if __name__ == "__main__":
    main()
