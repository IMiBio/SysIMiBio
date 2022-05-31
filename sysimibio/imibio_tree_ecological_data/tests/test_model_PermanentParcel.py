from django.contrib.auth.models import User
from django.test import TestCase
from geojson import Polygon

from sysimibio.imibio_tree_ecological_data.models import PermanentParcel


class PermanentParcelModelTest(TestCase):
    def setUp(self):
        coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.pp1 = PermanentParcel.objects.create(
            name="Reserva Yrya Pu",
            coordinator=coordinator,
            province="Misiones",
            municipality="Puerto Iguazú",
            locality="reserva 600 ha",
            cadastral_parcel=1668002000000000012,
            plot_type="Publico",
            obs="Prueba de registro",
            latitude=-26,
            longitude=-54,
            geom=Polygon(
                [[(-54.6, -27.0), (-54.0, -27.07), (-54.07, -26.62), (-54.6, -27.0)]]
            ),
        )

    def test_permanentparcel_model(self):
        self.assertTrue(PermanentParcel.objects.exists())

    def test_str(self):
        self.assertEqual(str(self.pp1), "Reserva Yrya Pu, Puerto Iguazú - Florencia")

    def test_property_geom_point(self):
        self.assertEqual(
            self.pp1.geom_point, {"coordinates": [-54, -26], "type": "Point"}
        )

    def test_property_geom_point_Valid(self):
        self.assertTrue(self.pp1.geom_point.is_valid)

    def test_geom_polygon(self):
        self.assertEqual(
            self.pp1.geom,
            {
                "coordinates": [
                    [[-54.6, -27.0], [-54.0, -27.07], [-54.07, -26.62], [-54.6, -27.0]]
                ],
                "type": "Polygon",
            },
        )

    def test_geom_point_is_valid(self):
        self.assertTrue(self.pp1.geom_point.is_valid)

    def test_entry_saved_data(self):
        self.assertEqual(self.pp1.plot_type, "Publico")


# TODO FALTA TESTAR PROPIEDADES EN MODELS
