from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from geojson import Polygon

from sysimibio.imibio_tree_ecological_data.forms import TreeMeasurementForm
from sysimibio.imibio_tree_ecological_data.models import (
    PermanentParcel,
    Tree,
    FieldWork,
    Pictures,
)

TINY_GIF = (
    b"GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;"
)


@override_settings(DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage")
class TreeMeasurementFormTest(TestCase):
    def setUp(self):
        self.coordinator1 = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )

        self.tempPicture = Pictures.objects.create(
            picture=SimpleUploadedFile("tiny.gif", TINY_GIF)
        )

        self.permanent_plot1 = PermanentParcel.objects.create(
            name="Reserva Yriapu",
            coordinator=self.coordinator1,
            province="Misiones",
            municipality="Puerto Iguazú",
            locality="600Ha",
            cadastral_parcel=1668002000000000012,
            plot_type="Publico",
            obs="Parcela de prueba",
            latitude=-26,
            longitude=-54,
            geom=Polygon(
                [[(-54.6, -27.0), (-54.0, -27.07), (-54.07, -26.62), (-54.6, -27.0)]]
            ),
        )

        self.field1 = FieldWork.objects.create(
            date="2020-12-30",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator1,
            parcel_id=self.permanent_plot1,
        )

        self.tree = Tree.objects.create(
            field=self.field1,
            subplot="A1",
            tree_number=1,
            specie="Solanaceae",
            latitude=-26,
            longitude=-54,
            obs="Teste 1",
        )

        self.tree_measurement_form = TreeMeasurementForm()

    def create_TreeMeasurementForm(self, **kwargs):
        valid_form = dict(
            field=self.field1,
            tree=self.tree,
            dap=11,
            dab=20,
            tree_height=10,
            picture=self.tempPicture,
            phytosanitary_status=1,
            sociological_classification=4,
            liana_cover=1,
        )
        valid_form.update(**kwargs)
        form = TreeMeasurementForm(valid_form)
        return form

    def test_tree_measurement_has_fields(self):
        """Tree Measurement form must have models fields"""
        self.assertSequenceEqual(
            [
                "tree",
                "dap",
                "dab",
                "tree_height",
                "phytosanitary_status",
                "sociological_classification",
                "liana_cover",
                "obs",
            ],
            list(self.tree_measurement_form.fields),
        )

    def test_form_is_valid(self):
        form = self.create_TreeMeasurementForm()
        self.assertTrue(form.is_valid())
