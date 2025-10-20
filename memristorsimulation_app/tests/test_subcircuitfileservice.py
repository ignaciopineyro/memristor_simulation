from memristorsimulation_app.constants import (
    MemristorModels,
)
from memristorsimulation_app.tests.basetestcase import BaseTestCase


class SubcircuitFileServiceTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

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

        # Subcircuits
        self.assertIn("* SUBCIRCUITS:", content)
        self.assertIn(
            f".subckt {subcircuit_file_service.subcircuit.name} {subcircuit_file_service.subcircuit.get_nodes_as_string()}",
            content,
        )
        self.assertIn(
            f"PARAMS: {subcircuit_file_service.subcircuit.model_parameters.get_parameters_as_string()}",
            content,
        )

        # Spice dependencies
        self.assertIn("* SPICE DEPENDENCIES:", content)
        model_dependence = subcircuit_file_service.model_dependencies[0]
        self.assertIn(
            f".model {model_dependence.name.value} {model_dependence.model.value}",
            content,
        )

        # Sources
        self.assertIn("* SOURCES:", content)
        source = subcircuit_file_service.sources[0]
        self.assertIn(
            f"{source.name} {source.n_plus} {source.n_minus} {source.behaviour_function}",
            content,
        )

        # Components
        self.assertIn("* COMPONENTS:", content)
        component = subcircuit_file_service.components[0]
        self.assertIn(
            f"{component.name} {component.n_plus} {component.n_minus} {component.value}",
            content,
        )

        # Control commands
        control_command = subcircuit_file_service.control_commands[0]
        self.assertIn("* CONTROL COMMANDS:", content)
        self.assertIn(f"{control_command}", content)

        self.assertIn(".ends", content)
