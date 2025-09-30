from click import Path
from memristorsimulation_app.constants import (
    MemristorModels,
    ModelsSimulationFolders,
    SpiceDevices,
    SpiceModel,
)
from memristorsimulation_app.representations import (
    BehaviouralSource,
    Component,
    ExportParameters,
    ModelDependence,
    ModelParameters,
    Subcircuit,
)
from memristorsimulation_app.services.directoriesmanagementservice import (
    DirectoriesManagementService,
)
from memristorsimulation_app.services.subcircuitfileservice import SubcircuitFileService
from memristorsimulation_app.tests.basetestcase import BaseTestCase


class SubcircuitFileServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        # self.export_file_name = self.get_random_string()
        # self.export_folder_name = self.get_random_string()
        # self.magnitudes = [
        #     self.get_random_string(),
        #     self.get_random_string(),
        #     self.get_random_string(),
        # ]
        # self.model_parameters = ModelParameters(
        #     self.get_random_int(),
        #     self.get_random_int(),
        #     self.get_random_int(),
        #     self.get_random_int(),
        #     self.get_random_int(),
        #     self.get_random_int(),
        # )
        # self.subcircuit = Subcircuit(
        #     self.get_random_string(),
        #     [
        #         self.get_random_string(),
        #         self.get_random_string(),
        #         self.get_random_string(),
        #     ],
        #     self.model_parameters,
        # )
        # self.behavioural_sources = [
        #     BehaviouralSource(
        #         name=self.get_random_string(),
        #         n_plus=self.get_random_string(),
        #         n_minus=self.get_random_string(),
        #         behaviour_function=self.get_random_string(),
        #     )
        # ]
        # self.components = [
        #     Component(
        #         name=self.get_random_string(),
        #         n_plus=self.get_random_string(),
        #         n_minus=self.get_random_string(),
        #         value=self.get_random_int(),
        #     )
        # ]
        # self.model_dependencies = [
        #     ModelDependence(name=SpiceDevices.DIODE, model=SpiceModel.DIODE)
        # ]
        # self.control_cmd = [self.get_random_string()]
        # self.export_file_name = self.get_random_string()

    def test_write_pershin_subcircuit_file(self):
        subcircuit_file_service = self.create_subcircuit_file_service(
            MemristorModels.PERSHIN
        )
        subcircuit_file_service.write_subcircuit_file()

        content = self.open_file(subcircuit_file_service.model_file_path)

        self.assertIn(
            f"* MEMRISTOR SUBCIRCUIT - MODEL {MemristorModels.PERSHIN.value}",
            content,
        )
        self.assertIn("* SUBCIRCUITS:", content)
        self.assertIn("* SPICE DEPENDENCIES:", content)
        self.assertIn("* SOURCES:", content)
        self.assertIn("* COMPONENTS:", content)
        self.assertIn("* CONTROL COMMANDS:", content)
        self.assertIn(".ends", content)

        self.assertIn(
            f".subckt {subcircuit_file_service.subcircuit.name} {subcircuit_file_service.subcircuit.get_nodes_as_string()}",
            content,
        )
        self.assertIn(
            f"PARAMS: {subcircuit_file_service.subcircuit.parameters.get_parameters_as_string()}",
            content,
        )

        # Dependencias
        self.assertIn(
            f".model {self.model_dependencies[0].name.value} {self.model_dependencies[0].model.value}",
            content,
        )

        # Fuentes
        source = self.behavioural_sources[0]
        self.assertIn(
            f"{source.name} {source.n_plus} {source.n_minus} {source.behaviour_function}",
            content,
        )

        # Componentes
        component = self.components[0]
        self.assertIn(
            f"{component.name} {component.n_plus} {component.n_minus} {component.value}",
            content,
        )

        # Comandos de control
        self.assertIn(self.control_cmd[0], content)

    def test_write_vourkas_subcircuit_file(self):
        pass
