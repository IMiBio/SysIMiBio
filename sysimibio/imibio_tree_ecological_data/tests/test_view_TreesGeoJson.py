from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from sysimibio.imibio_tree_ecological_data.forms import TreeForm
from sysimibio.imibio_tree_ecological_data.models import (
    FieldWork,
    Tree,
    PermanentParcel,
)


class TreesGeoJsonView(TestCase):
    def setUp(self):
        coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.parcel1 = PermanentParcel.objects.create(
            name="Nombre test",
            province="Misiones",
            coordinator=coordinator,
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
            coordinator=coordinator,
            parcel_id=self.parcel1,
        )

        self.tree = TreeForm(
            {
                "field": self.field,
                "subplot": "A1",
                "tree_number": 1,
                "specie": "Solanaceae",
                "dap": 40.0,
                "dab": 60.0,
                "tree_height": 60.0,
                "latitude": 5,
                "longitude": 9,
                "obs": "Teste 1",
                "has_herbarium ": True,
                "herbarium_info": "",
            }
        )
        self.tree.save()
        self.occurrence = Tree.objects.all()[0]
        self.resp = self.client.get(r("imibio_tree_ecological_data:data"))

    def test_get(self):
        """GET /geojson/ must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_keys(self):
        self.assertListEqual(["type", "features", "crs"], list(self.resp.json().keys()))

    def test_type(self):
        self.assertEqual("FeatureCollection", self.resp.json().get("type"))

    def test_crs(self):
        self.assertEqual(
            "EPSG:4326", self.resp.json().get("crs").get("properties").get("name")
        )

    def test_properties(self):
        popup = (
            self.resp.json().get("features")[0].get("properties").get("popup_content")
        )
        self.assertEqual(popup, self.occurrence.popup_content)
