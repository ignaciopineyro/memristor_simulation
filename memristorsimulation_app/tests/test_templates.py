from memristorsimulation_app.constants import MemristorModels
from memristorsimulation_app.simulation_templates.singledevice import SingleDevice
from memristorsimulation_app.tests.basetestcase import BaseTestCase


class TemplatesTestCase(BaseTestCase):
    def test_singledevice_pershin_template(self):
        memristor_model = MemristorModels.PERSHIN
        export_folder_name = self.get_random_string()
        SingleDevice.EXPORT_FOLDER_NAME = export_folder_name
        SingleDevice.AMOUNT_ITERATIONS = 1

        SingleDevice(memristor_model).simulate()

        files_in_simulation_directory = self.list_files_in_simulation_directory(
            memristor_model, export_folder_name
        )
        dataframe = self.load_dataframe_from_csv(memristor_model, export_folder_name)

        self.assertEqual(8, len(files_in_simulation_directory))
        self.assertTrue(
            self.check_file_size(".sub", files_in_simulation_directory, 300)
        )
        self.assertTrue(
            self.check_file_size(".cir", files_in_simulation_directory, 300)
        )
        self.assertTrue(
            self.check_file_size(".log", files_in_simulation_directory, 300)
        )
        self.assertTrue(
            self.check_file_size(".csv", files_in_simulation_directory, 30000)
        )
        self.assertTrue(
            self.check_file_size(
                ".jpg", files_in_simulation_directory, 40000, amount_coincidences=4
            )
        )
        self.assertTrue(
            self.check_csv_content(dataframe, {"time", "vin", "i(v1)", "l0"}, 500)
        )
