from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from sysimibio.imibio_tree_ecological_data.models import (
    FieldWork,
    Tree,
    PermanentParcel,
    TreeMeasurement,
)


class TreeMeasurementTest(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.staff = User.objects.create_user(
            "Francisco", "fran@imibio.com", "fanpassword"
        )
        self.parcel1 = PermanentParcel.objects.create(
            name="Nombre test",
            coordinator=self.coordinator,
            province="Misiones",
            municipality="Puerto Iguazu",
            locality="600 ha",
            cadastral_parcel=1668002000000000012,
            plot_type="Publico",
            obs="Observacion",
            latitude=-26,
            longitude=-56,
            geom="",
        )
        self.field = FieldWork.objects.create(
            date="2020-12-30",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator,
            parcel_id=self.parcel1,
        )
        self.field.staff.add(self.staff)

        self.tree = Tree.objects.create(
            field=self.field,
            subplot="A1",
            tree_number=3,
            specie="Solanaceae",
            latitude=-26,
            longitude=-54,
            obs="Teste 1",
        )

        self.valid_measurement = TreeMeasurement(
            tree=self.tree,
            dap=11,
            dab=20,
            tree_height=3,
            phytosanitary_status=1,
            sociological_classification=3,
        )

    def test_tree_measurement_exists(self):
        self.valid_measurement.save()
        self.assertTrue(TreeMeasurement.objects.exists())

    def test_sociologicalclassification_Inferior_suprimido(self):
        self.valid_measurement.sociological_classification = 1
        self.assertEqual(None, self.valid_measurement.clean_fields())

    def test_sociologicalclassification_Dominante(self):
        self.valid_measurement.sociological_classification = 2
        self.assertEqual(None, self.valid_measurement.clean_fields())

    def test_sociologicalclassification_Codominante(self):
        self.valid_measurement.sociological_classification = 3
        self.assertEqual(None, self.valid_measurement.clean_fields())

    def test_sociologicalclassification_Intermedia(self):
        self.valid_measurement.sociological_classification = 4
        self.assertEqual(None, self.valid_measurement.clean_fields())

    def test_sociologicalclassification_Inferior_sumergido(self):
        self.valid_measurement.sociological_classification = 5
        self.assertEqual(None, self.valid_measurement.clean_fields())

    def test_phytosanitary_Regular(self):
        self.valid_measurement.phytosanitary_status = 1
        self.assertEqual(None, self.valid_measurement.clean_fields())

    def test_phytosanitary_Malo(self):
        self.valid_measurement.phytosanitary_status = 2
        self.assertEqual(None, self.valid_measurement.clean_fields())

    def test_phytosanitary_Muerto(self):
        self.valid_measurement.phytosanitary_status = 3
        self.assertEqual(None, self.valid_measurement.clean_fields())

    def test_min_tree_height(self):
        self.valid_measurement.tree_height = 1.29
        msg = "Altura del árbol no puede ser menor a 1.3 metros"
        with self.assertRaisesMessage(ValidationError, msg):
            self.valid_measurement.full_clean()

    def test_min_tree_dap(self):
        self.valid_measurement.dap = 9
        msg = "DAP del árbol debe ser mayor a 10 cm"
        with self.assertRaisesMessage(ValidationError, msg):
            self.valid_measurement.full_clean()

    def test_str(self):
        """measurement string must be tree_id + field work date"""
        self.assertEqual("NTA103; 2020-12-30", str(self.valid_measurement))
