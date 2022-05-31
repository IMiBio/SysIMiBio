from django.contrib.auth.models import User
from django.test import TestCase
from geojson import Polygon, Point

from sysimibio.imibio_tree_ecological_data.forms import PermanentParcelForm


class PermanentParcelFormTest(TestCase):
    def setUp(self):
        self.pp = PermanentParcelForm()
        self.coordinator1 = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )

    def create_PermanentParcelForm(self, **kwargs):
        valid_form = dict(
            name="YryaPu",
            coordinator=self.coordinator1,
            province="Misiones",
            municipality="Capital",
            locality="600Ha",
            cadastral_parcel="1668002000000000012",
            plot_choices=[
                "Fiscal",
            ],
            obs="Parcela de prueba",
            latitude=-26,  # Plot_choices una lista con un elemento para sacar el len()
            longitude=-54,
            geom=Polygon(
                [[(-54.6, -27.0), (-54.0, -27.07), (-54.07, -26.62), (-54.6, -27.0)]]
            ),
        )
        valid_form.update(**kwargs)
        form = PermanentParcelForm(valid_form)
        return form

    def test_empty_form(self):
        self.assertIn("name", self.pp.fields)
        self.assertIn("coordinator", self.pp.fields)
        self.assertIn("province", self.pp.fields)
        self.assertIn("municipality", self.pp.fields)
        self.assertIn("locality", self.pp.fields)
        self.assertIn("cadastral_parcel", self.pp.fields)
        self.assertIn("obs", self.pp.fields)
        self.assertIn("latitude", self.pp.fields)
        self.assertIn(
            "longitude", self.pp.fields
        )  # todo como testar cuando el form tiene campo diferente al del model
        self.assertIn("plot_choices", self.pp.fields)
        self.assertIn("geom", self.pp.fields)

    #
    # def test_permanent_parcel_has_fields(self):
    #     """Permanent Parcel form must have models fields"""
    #     self.assertSequenceEqual(
    #         ['name', 'coordinator', 'province', 'municipality', 'locality',
    #          'cadastral_parcel', 'plot_type', 'obs', 'latitude', 'longitude',
    #          'geom'], list(self.pp.fields))

    def test_form_is_valid(self):
        form = self.create_PermanentParcelForm()
        self.assertTrue(form.is_valid())

    def test_province_restriction(self):
        """ "province different from Misiones must return error"""
        form = self.create_PermanentParcelForm(province="OtraProvincia")
        self.assertFalse(form.is_valid())

    def test_geom_is_invalid(self):
        """ "geom must be polygon geojson"""
        form = self.create_PermanentParcelForm(geom=Point((-54.6, -27.0)))
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors["geom"][0], "Point does not match geometry type")
