from typing import List

from memristorsimulation_app.constants import (
    MemristorModels,
    AnalysisType,
    ModelsSimulationFolders,
    SpiceDevices,
    SpiceModel,
    SimulationTemplate,
    InvalidSimulationTemplate,
    SIMULATIONS_DIR,
    PlotType,
    NetworkType,
)
from representations import (
    Subcircuit,
    BehaviouralSource,
    Component,
    SimulationParameters,
    InputParameters,
    ModelParameters,
    DeviceParameters,
    ExportParameters,
    ModelDependence,
    NetworkParameters,
    SinWaveForm,
    PulseWaveForm,
)
from services.networkservice import NetworkService
from services.circuitfileservice import CircuitFileService
from services.ngspiceservice import NGSpiceService
from services.plotterservice import PlotterService
from services.subcircuitfileservice import SubcircuitFileService


def _create_pershin_default_components() -> List[Component]:
    capacitor = Component(
        name="Cx", n_plus="x", n_minus="0", value=1, extra_data="IC={Rinit}"
    )
    resistor = Component(name="R0", n_plus="pl", n_minus="mn", value=1e12)
    rmem = Component(name="Rmem", n_plus="pl", n_minus="mn", extra_data="r={V(x)}")

    return [capacitor, resistor, rmem]


def _create_vourkas_default_components() -> List[Component]:
    capacitor = Component(
        name="Cx", n_plus="x", n_minus="0", value=1, extra_data="IC={Rinit}"
    )
    rmem = Component(name="Rmem", n_plus="pl", n_minus="mn", extra_data="r={V(x)}")
    diode_1 = Component(
        name="d1", n_plus="aux1", n_minus="x", model=SpiceDevices.DIODE.value
    )
    diode_2 = Component(
        name="d2", n_plus="x", n_minus="aux2", model=SpiceDevices.DIODE.value
    )
    v_1 = Component(name="v1", n_plus="aux1", n_minus="0", extra_data="{Ron}")
    v_2 = Component(name="v2", n_plus="aux2", n_minus="0", extra_data="{Roff}")
    raux = Component(name="Raux", n_plus="pl", n_minus="mn", value=1e12)

    return [capacitor, rmem, diode_1, diode_2, v_1, v_2, raux]


def create_di_francesco_variable_beta_circuit_file_service(
    subcircuit_file_services: List[SubcircuitFileService],
) -> List[CircuitFileService]:
    circuit_file_service = []
    input_params = InputParameters(1, "vin", "gnd", SinWaveForm(0, 2, 1))
    device_params = [DeviceParameters("xmem", 0, ["vin", "gnd", "l0"], "memristor")]
    simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)
    export_folder_name = "di_francesco_beta"

    for subcircuit_file_service in subcircuit_file_services:
        export_file_name = f"beta_{subcircuit_file_service.subcircuit.parameters.beta}"
        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(
                subcircuit_file_service.model
            ),
            export_folder_name,
            export_file_name,
            ["vin", "i(v1)", "l0"],
        )

        circuit_file_service.append(
            CircuitFileService(
                subcircuit_file_service,
                input_params,
                device_params,
                simulation_params,
                export_params,
            )
        )

    return circuit_file_service


def create_di_francesco_variable_beta_subcircuit_file_service(
    model: MemristorModels, model_parameters: List[ModelParameters]
) -> List[SubcircuitFileService]:
    subcircuit = [
        Subcircuit("memristor", ["pl", "mn", "x"], model_parameter)
        for model_parameter in model_parameters
    ]
    source_bx = BehaviouralSource(
        name="Bx",
        n_plus="0",
        n_minus="x",
        behaviour_function="I='(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: "
        "(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}'",
    )

    model_dependencies = None
    default_components = None

    if model == MemristorModels.PERSHIN:
        default_components = _create_pershin_default_components()

    elif model == MemristorModels.VOURKAS:
        default_components = _create_vourkas_default_components()
        model_dependencies = [
            ModelDependence(name=SpiceDevices.DIODE, model=SpiceModel.DIODE)
        ]

    control_cmd = ".func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}"

    return [
        SubcircuitFileService(
            model=model,
            subcircuit=subcircuit,
            sources=[source_bx],
            model_dependencies=model_dependencies,
            components=default_components,
            control_commands=[control_cmd],
        )
        for subcircuit in subcircuit
    ]


def create_di_francesco_variable_amplitude_circuit_file_service(
    subcircuit_file_service: SubcircuitFileService,
) -> List[CircuitFileService]:
    circuit_file_service = []
    for amplitude in [0.7, 1, 2, 4]:
        input_params = InputParameters(1, "vin", "gnd", SinWaveForm(0, amplitude, 1))
        device_params = [DeviceParameters("xmem", 0, ["vin", "gnd", "l0"], "memristor")]
        simulation_params = SimulationParameters(
            AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True
        )
        export_folder_name = "di_francesco_vin_amplitude"
        export_file_name = f"vin_{amplitude}"
        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(
                subcircuit_file_service.model
            ),
            export_folder_name,
            export_file_name,
            ["vin", "i(v1)", "l0"],
        )

        circuit_file_service.append(
            CircuitFileService(
                subcircuit_file_service,
                input_params,
                device_params,
                simulation_params,
                export_params,
            )
        )

    return circuit_file_service


def create_di_francesco_variable_amplitude_subcircuit_file_service(
    model: MemristorModels, model_parameters: ModelParameters
) -> List[SubcircuitFileService]:
    subcircuit = Subcircuit("memristor", ["pl", "mn", "x"], model_parameters)
    source_bx = BehaviouralSource(
        name="Bx",
        n_plus="0",
        n_minus="x",
        behaviour_function="I='(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: "
        "(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}'",
    )

    model_dependencies = None
    default_components = None

    if model == MemristorModels.PERSHIN:
        default_components = _create_pershin_default_components()

    elif model == MemristorModels.VOURKAS:
        default_components = _create_vourkas_default_components()
        model_dependencies = [
            ModelDependence(name=SpiceDevices.DIODE, model=SpiceModel.DIODE)
        ]

    control_cmd = ".func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}"

    return [
        SubcircuitFileService(
            model=model,
            subcircuit=subcircuit,
            sources=[source_bx],
            model_dependencies=model_dependencies,
            components=default_components,
            control_commands=[control_cmd],
        )
    ]


def create_default_test_circuit_file_service(
    subcircuit_file_service: SubcircuitFileService,
    network_service: NetworkService = None,
) -> List[CircuitFileService]:
    input_params = InputParameters(1, "vin", "gnd", SinWaveForm(0, 10, 1))

    if network_service:
        device_params = network_service.generate_device_parameters("xmem", "memristor")

        if network_service.removal_probability == 0:
            export_folder_name = (
                f"default_network_{network_service.network_parameters.N}x"
                f"{network_service.network_parameters.M}"
            )
            export_file_name = (
                f"default_network_simulation_{network_service.network_parameters.N}x"
                f"{network_service.network_parameters.M}"
            )

        else:
            export_folder_name = (
                f"default_network_with_edge_removal_{network_service.network_parameters.N}x"
                f"{network_service.network_parameters.M}"
            )
            export_file_name = (
                f"default_network_simulation_with_edge_removal_{network_service.network_parameters.N}x"
                f"{network_service.network_parameters.M}"
            )

        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(
                subcircuit_file_service.model
            ),
            export_folder_name,
            export_file_name,
            ["vin", "i(v1)"]
            + [device_param.nodes[2] for device_param in device_params],
        )

    else:
        device_params = [DeviceParameters("xmem", 0, ["vin", "gnd", "l0"], "memristor")]
        export_folder_name = "default_test"
        export_file_name = "default_test_simulation"
        export_params = ExportParameters(
            ModelsSimulationFolders.get_simulation_folder_by_model(
                subcircuit_file_service.model
            ),
            export_folder_name,
            export_file_name,
            ["vin", "i(v1)", "l0"],
        )

    simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)

    return [
        CircuitFileService(
            subcircuit_file_service,
            input_params,
            device_params,
            simulation_params,
            export_params,
        )
    ]


def create_quinteros_experiments_subcircuit_file_service(
    model: MemristorModels,
) -> List[SubcircuitFileService]:

    model_parameters = [
        ModelParameters(alpha=0, beta=5e5, Rinit=2e5, Roff=2e5, Ron=2e3, Vt=0.6),
        ModelParameters(alpha=0, beta=5e5, Rinit=2e3, Roff=2e5, Ron=2e3, Vt=0.6),
        ModelParameters(alpha=0, beta=5e5, Rinit=2e5, Roff=2e5, Ron=2e3, Vt=0.6),
        ModelParameters(alpha=0, beta=5e5, Rinit=2e3, Roff=2e5, Ron=2e3, Vt=0.6),
    ]
    subcircuits = [
        Subcircuit("memristor", ["pl", "mn", "x"], model_parameter)
        for model_parameter in model_parameters
    ]
    source_bx = BehaviouralSource(
        name="Bx",
        n_plus="0",
        n_minus="x",
        behaviour_function="I='(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: "
        "(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}'",
    )

    model_dependencies = None
    default_components = None

    if model == MemristorModels.PERSHIN:
        default_components = _create_pershin_default_components()

    elif model == MemristorModels.VOURKAS:
        default_components = _create_vourkas_default_components()
        model_dependencies = [
            ModelDependence(name=SpiceDevices.DIODE, model=SpiceModel.DIODE)
        ]

    control_cmd = ".func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}"

    return [
        SubcircuitFileService(
            model=model,
            subcircuit=subcircuit,
            sources=[source_bx],
            model_dependencies=model_dependencies,
            components=default_components,
            control_commands=[control_cmd],
        )
        for subcircuit in subcircuits
    ]


def create_quinteros_experiments_circuit_file_service(
    subcircuit_file_service: SubcircuitFileService,
    network_service: NetworkService,
    experiment_number: int,
) -> CircuitFileService:
    input_params = InputParameters(1, "vin", "gnd", SinWaveForm(0, 10, 1))
    device_params = network_service.generate_device_parameters("xmem", "memristor")

    export_folder_name = (
        f"quinteros_experiment_{experiment_number}_{network_service.network_parameters.N}x"
        f"{network_service.network_parameters.M}"
    )

    export_file_name = (
        f"quinteros_experiments_simulation_{experiment_number}_{network_service.network_parameters.N}x"
        f"{network_service.network_parameters.M}"
    )

    export_params = ExportParameters(
        ModelsSimulationFolders.get_simulation_folder_by_model(
            subcircuit_file_service.model
        ),
        export_folder_name,
        export_file_name,
        ["vin", "i(v1)"] + [device_param.nodes[2] for device_param in device_params],
    )

    simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)

    return CircuitFileService(
        subcircuit_file_service,
        input_params,
        device_params,
        simulation_params,
        export_params,
    )


def create_default_test_subcircuit_file_service(
    model: MemristorModels,
) -> List[SubcircuitFileService]:
    model_parameters = ModelParameters(0, 5e5, 200e3, 200e3, 2e3, 0.6)
    subcircuit = Subcircuit("memristor", ["pl", "mn", "x"], model_parameters)
    source_bx = BehaviouralSource(
        name="Bx",
        n_plus="0",
        n_minus="x",
        behaviour_function="I='(f1(V(pl,mn))>0) && (V(x)<Roff) ? {f1(V(pl,mn))}: "
        "(f1(V(pl,mn))<0) && (V(x)>Ron) ? {f1(V(pl,mn))}: {0}'",
    )

    model_dependencies = None
    default_components = None

    if model == MemristorModels.PERSHIN:
        default_components = _create_pershin_default_components()

    elif model == MemristorModels.VOURKAS:
        default_components = _create_vourkas_default_components()
        model_dependencies = [
            ModelDependence(name=SpiceDevices.DIODE, model=SpiceModel.DIODE)
        ]

    control_cmd = ".func f1(y)={beta*y+0.5*(alpha-beta)*(abs(y+Vt)-abs(y-Vt))}"

    return [
        SubcircuitFileService(
            model=model,
            subcircuit=subcircuit,
            sources=[source_bx],
            model_dependencies=model_dependencies,
            components=default_components,
            control_commands=[control_cmd],
        )
    ]


def create_random_regular_circuit_file_service(
    subcircuit_file_service: SubcircuitFileService, network_service: NetworkService
):
    input_params = InputParameters(1, "vin", "gnd", SinWaveForm(0, 10, 1))
    device_params = network_service.generate_device_parameters("xmem", "memristor")

    export_folder_name = (
        f"random_regular_n{network_service.network_parameters.amount_nodes}_k"
        f"{network_service.network_parameters.amount_connections}"
    )
    export_file_name = (
        f"random_regular_n{network_service.network_parameters.amount_nodes}_k"
        f"{network_service.network_parameters.amount_connections}"
    )

    export_params = ExportParameters(
        ModelsSimulationFolders.get_simulation_folder_by_model(
            subcircuit_file_service.model
        ),
        export_folder_name,
        export_file_name,
        ["vin", "i(v1)"] + [device_param.nodes[2] for device_param in device_params],
    )

    simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)

    return [
        CircuitFileService(
            subcircuit_file_service,
            input_params,
            device_params,
            simulation_params,
            export_params,
        )
    ]


def create_watts_strogatz_circuit_file_service(
    subcircuit_file_service: SubcircuitFileService, network_service: NetworkService
):
    input_params = InputParameters(1, "vin", "gnd", SinWaveForm(0, 10, 1))
    device_params = network_service.generate_device_parameters("xmem", "memristor")

    export_folder_name = (
        f"watss_strogatz_n{network_service.network_parameters.amount_nodes}_k"
        f"{network_service.network_parameters.amount_connections}_p"
        f"{network_service.network_parameters.shortcut_probability}"
    )
    export_file_name = (
        f"watss_strogatz_n{network_service.network_parameters.amount_nodes}_k"
        f"{network_service.network_parameters.amount_connections}_p"
        f"{network_service.network_parameters.shortcut_probability}"
    )

    export_params = ExportParameters(
        ModelsSimulationFolders.get_simulation_folder_by_model(
            subcircuit_file_service.model
        ),
        export_folder_name,
        export_file_name,
        ["vin", "i(v1)"] + [device_param.nodes[2] for device_param in device_params],
    )

    simulation_params = SimulationParameters(AnalysisType.TRAN, 2e-3, 2, 1e-9, uic=True)

    return [
        CircuitFileService(
            subcircuit_file_service,
            input_params,
            device_params,
            simulation_params,
            export_params,
        )
    ]


def simulate(
    simulation_template: SimulationTemplate = SimulationTemplate.DEFAULT_TEST,
    plot_types: List[PlotType] = None,
    model: MemristorModels = None,
    amount_iterations: int = 1,
):
    if simulation_template == SimulationTemplate.DEFAULT_TEST:
        subcircuit_file_service = create_default_test_subcircuit_file_service(model)
        circuit_file_service = create_default_test_circuit_file_service(
            subcircuit_file_service[0]
        )

    elif simulation_template == SimulationTemplate.DEFAULT_NETWORK:
        network_dimensions = NetworkParameters(N=4, M=4)
        network_service = NetworkService(NetworkType.GRID_2D_GRAPH, network_dimensions)
        subcircuit_file_service = create_default_test_subcircuit_file_service(model)
        circuit_file_service = create_default_test_circuit_file_service(
            subcircuit_file_service[0], network_service
        )

    elif simulation_template == SimulationTemplate.DEFAULT_NETWORK_WITH_EDGE_REMOVAL:
        network_dimensions = NetworkParameters(N=4, M=4)
        removal_probability = 1
        network_service = NetworkService(
            NetworkType.GRID_2D_GRAPH,
            network_dimensions,
            removal_probability=removal_probability,
        )
        subcircuit_file_service = create_default_test_subcircuit_file_service(model)
        circuit_file_service = create_default_test_circuit_file_service(
            subcircuit_file_service[0], network_service
        )

    elif simulation_template == SimulationTemplate.DI_FRANCESCO_VARIABLE_AMPLITUDE:
        model_parameters = ModelParameters(0, 5e5, 200e3, 200e3, 2e3, 0.6)
        subcircuit_file_service = (
            create_di_francesco_variable_amplitude_subcircuit_file_service(
                model, model_parameters
            )
        )
        circuit_file_service = (
            create_di_francesco_variable_amplitude_circuit_file_service(
                subcircuit_file_service[0]
            )
        )

    elif simulation_template == SimulationTemplate.DI_FRANCESCO_VARIABLE_BETA:
        model_parameters = [
            ModelParameters(0, 500e3, 200e3, 200e3, 2e3, 0.6),
            ModelParameters(0, 50e6, 200e3, 200e3, 2e3, 0.6),
        ]
        subcircuit_file_service = (
            create_di_francesco_variable_beta_subcircuit_file_service(
                model, model_parameters
            )
        )
        circuit_file_service = create_di_francesco_variable_beta_circuit_file_service(
            subcircuit_file_service
        )

    elif simulation_template == SimulationTemplate.QUINTEROS_EXPERIMENTS:
        network_dimensions = NetworkParameters(N=4, M=4)
        subcircuit_files_service = create_quinteros_experiments_subcircuit_file_service(
            model
        )
        circuit_file_service = []

        for experiment_number, subcircuit_index in zip(
            [1, 2, 4, 5], range(len(subcircuit_files_service))
        ):
            if experiment_number in [4, 5]:
                vin_minus = (3, 3)
            else:
                vin_minus = (3, 0)

            network_service = NetworkService(
                NetworkType.GRID_2D_GRAPH, network_dimensions, vin_minus=vin_minus
            )
            circuit_file_service.append(
                create_quinteros_experiments_circuit_file_service(
                    subcircuit_files_service[subcircuit_index],
                    network_service,
                    experiment_number,
                )
            )

    elif simulation_template == SimulationTemplate.RANDOM_REGULAR:
        network_parameters = NetworkParameters(amount_connections=5, amount_nodes=50)
        network_service = NetworkService(
            NetworkType.RANDOM_REGULAR_GRAPH, network_parameters
        )
        subcircuit_file_service = create_default_test_subcircuit_file_service(model)
        circuit_file_service = create_random_regular_circuit_file_service(
            subcircuit_file_service[0], network_service
        )

    elif simulation_template == SimulationTemplate.WATTS_STROGATZ_CIRCULAR_REGULAR:
        network_parameters = NetworkParameters(
            amount_connections=5, amount_nodes=50, shortcut_probability=0
        )
        network_service = NetworkService(
            NetworkType.WATTS_STROGATZ_GRAPH, network_parameters
        )
        subcircuit_file_service = create_default_test_subcircuit_file_service(model)
        circuit_file_service = create_watts_strogatz_circuit_file_service(
            subcircuit_file_service[0], network_service
        )

    elif simulation_template == SimulationTemplate.WATTS_STROGATZ:
        network_parameters = NetworkParameters(
            amount_connections=5, amount_nodes=50, shortcut_probability=0.1
        )
        network_service = NetworkService(
            NetworkType.WATTS_STROGATZ_GRAPH, network_parameters
        )
        subcircuit_file_service = create_default_test_subcircuit_file_service(model)
        circuit_file_service = create_watts_strogatz_circuit_file_service(
            subcircuit_file_service[0], network_service
        )

    else:
        raise InvalidSimulationTemplate()

    for cfs in circuit_file_service:
        cfs.subcircuit_file_service.write_subcircuit_file()
        cfs.write_circuit_file()

        ngspice_service = NGSpiceService(cfs)
        ngspice_service.run_single_circuit_simulation(amount_iterations)

    print("PLOT SERVICE STARTED")
    for cfs in circuit_file_service:
        plot(
            export_parameters=cfs.export_parameters,
            model_parameters=cfs.subcircuit_file_service.subcircuit.parameters,
            input_parameters=cfs.input_parameters,
            plot_types=plot_types,
        )
    print("PLOT SERVICE ENDED")


def plot(
    export_parameters: ExportParameters,
    model_parameters: ModelParameters = None,
    input_parameters: InputParameters = None,
    plot_types: List[PlotType] = None,
):
    if plot_types is not None:
        plotter_service = PlotterService(
            simulation_results_directory_path=SIMULATIONS_DIR,
            export_parameters=export_parameters,
            model_parameters=model_parameters,
            input_parameters=input_parameters,
        )
        data_loaders = plotter_service.load_data_from_csv()

        for data_loader in data_loaders:
            if PlotType.IV in plot_types:
                plotter_service.plot_iv(
                    data_loader.dataframe, data_loader.csv_file_name_no_extension
                )
            if PlotType.IV_OVERLAPPED in plot_types:
                plotter_service.plot_iv_overlapped(data_loader.dataframe)
            if PlotType.IV_LOG in plot_types:
                plotter_service.plot_iv_log(
                    data_loader.dataframe, data_loader.csv_file_name_no_extension
                )
            if PlotType.IV_LOG_OVERLAPPED in plot_types:
                plotter_service.plot_iv_log_overlapped(data_loader.dataframe)
            if PlotType.CURRENT_AND_VIN_VS_TIME in plot_types:
                plotter_service.plot_current_and_vin_vs_time(
                    data_loader.dataframe, data_loader.csv_file_name_no_extension
                )
            if PlotType.STATE_AND_VIN_VS_TIME in plot_types:
                plotter_service.plot_state_and_vin_vs_time(
                    data_loader.dataframe, data_loader.csv_file_name_no_extension
                )
            if PlotType.MEMRISTIVE_STATES_OVERLAPPED in plot_types:
                plotter_service.plot_states_overlapped(data_loader.dataframe)


if __name__ == "__main__":
    simulate(
        simulation_template=(
            SimulationTemplate.DEFAULT_TEST
            # SimulationTemplate.DEFAULT_NETWORK
            # SimulationTemplate.DEFAULT_NETWORK_WITH_EDGE_REMOVAL  # Not working
            # SimulationTemplate.DI_FRANCESCO_VARIABLE_AMPLITUDE
            # SimulationTemplate.DI_FRANCESCO_VARIABLE_BETA
            # SimulationTemplate.QUINTEROS_EXPERIMENTS
            # SimulationTemplate.RANDOM_REGULAR
            # SimulationTemplate.WATTS_STROGATZ_CIRCULAR_REGULAR
            # SimulationTemplate.WATTS_STROGATZ
        ),
        plot_types=[
            PlotType.IV,
            PlotType.IV_OVERLAPPED,
            PlotType.IV_LOG,
            PlotType.IV_LOG_OVERLAPPED,
            PlotType.CURRENT_AND_VIN_VS_TIME,
            PlotType.STATE_AND_VIN_VS_TIME,
            PlotType.MEMRISTIVE_STATES_OVERLAPPED,
        ],
        model=(
            MemristorModels.PERSHIN
            # MemristorModels.VOURKAS
        ),
        amount_iterations=1,
    )
