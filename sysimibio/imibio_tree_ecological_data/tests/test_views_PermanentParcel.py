import json

from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase
from django.urls import reverse
from geojson import Polygon

from sysimibio.imibio_tree_ecological_data.forms import PermanentParcelForm
from sysimibio.imibio_tree_ecological_data.models import PermanentParcel


class PermanentParcelListView(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.pp1 = PermanentParcel.objects.create(
            name="Reserva Yrya Pu",
            coordinator=self.coordinator,
            province="Misiones",
            municipality="Puerto Iguazú",
            locality="reserva 600 ha",
            cadastral_parcel="1668002000000000012",
            plot_type="Fiscal",
            obs="Prueba de registro",
            latitude=-26,
            longitude=-54,
            geom=Polygon(
                [[(-54.6, -27.0), (-54.0, -27.07), (-54.07, -26.62), (-54.6, -27.0)]]
            ),
        )
        self.pp2 = PermanentParcel.objects.create(
            name="Campoo San Juan",
            coordinator=self.coordinator,
            province="Misiones",
            municipality="Posadas",
            locality="Campo San Juan",
            cadastral_parcel="1668002000000000012",
            plot_type="Fiscal",
            obs="Prueba de registro 2",
            latitude=-26.002,
            longitude=-56,
            geom=Polygon(
                [[(-56, -27.0), (-54.0, -27.07), (-54.07, -26.62), (-56, -27.0)]]
            ),
        )

        self.resp = self.client.get(r("imibio_tree_ecological_data:plot_list"))

    def test_get(self):
        """GET /plot_list/ must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_use_template(self):
        """GET /plot_list/ must use permanentparcel_list.html template"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/permanentparcel_list.html"
        )

    def test_list(self):
        """GET /plot_list/ must have the same queryset from database"""
        all_entries = PermanentParcel.objects.all()
        self.assertQuerysetEqual(
            self.resp.context["permanentparcel_list"], all_entries, ordered=False
        )


class PermanentParcelDetailView(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.pp1 = PermanentParcel.objects.create(
            name="Reserva Yrya Pu",
            coordinator=self.coordinator,
            province="Misiones",
            municipality="Puerto Iguazú",
            locality="reserva 600 ha",
            cadastral_parcel="1668002000000000012",
            plot_type='{"Fiscal":"Fiscal"}',  # todo revisar con felipe si esto esta bien cargado
            obs="Prueba de registro",
            latitude=-26,
            longitude=-54,
            geom=Polygon(
                [[(-54.6, -27.0), (-54.0, -27.07), (-54.07, -26.62), (-54.6, -27.0)]]
            ),
        )
        self.resp = self.client.get(r("imibio_tree_ecological_data:plot_detail", 1))

    def test_get(self):
        """GET /plot_detail/1 must get status code 200"""
        self.assertEqual(
            200, self.resp.status_code
        )  # todo averiguar como testar la view que usa una propieda

    def test_detail_use_template(self):
        """GET /plot_detail/1 must use permanentparcel_detail.html template"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/permanentparcel_detail.html"
        )


#     def test_detail_html(self):  # todo testar mapa
#         content = [
#             "Reserva Yrya Pu",
#             "Reserva Yrya Pu",
#             "Florencia",
#             "Misiones",
#             "Puerto Iguazú",
#             'reserva 600 ha',
#             '1668002000000000012',
#             'Fiscal',
#             "Prueba de registro"]
#         with self.subTest():
#             for expected in content:
#                 self.assertContains(self.resp, expected)
#
#
class PermanentParcelDetailNotFound(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.resp = self.client.get(r("imibio_tree_ecological_data:plot_detail", 0))

    def test_not_found(self):
        self.assertEqual(404, self.resp.status_code)


class PermanentParcelCreateView(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.resp = self.client.get(r("imibio_tree_ecological_data:plot_create"))

    def test_get(self):
        """GET /plot_create must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """must use imibio_tree_ecological_data/permanentparcel_form.html"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/permanentparcel_form.html"
        )

    def test_html(self):
        """HTML must contais input tags"""
        tags = (  # todo confirmar las tags a seren testadas
            ("<form"),
            ("<input"),
            ('type="text"'),
            ('type="submit"'),
        )
        for text in tags:
            with self.subTest():
                self.assertContains(self.resp, text)

    def test_csrf(self):
        """html must contains CSRF"""
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        """ "Context must have permanentparcel create form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, PermanentParcelForm)

    def test_valid_post(self):
        data = {
            "name": "Reserva Yrya Pu",
            "coordinator": self.coordinator.pk,
            "province": "Misiones",
            "municipality": "Puerto Iguazú",
            "locality": "reserva 600 ha",
            "cadastral_parcel": "1668002000000000012",
            "plot_choices": "Fiscal",
            "obs": "Prueba de registro",
            "latitude": -26,
            "longitude": -56,
            "geom": '{"coordinates": [[[-54.6, -27.0], [-54.0, -27.07], [-54.07, -26.62], [-54.6, -27.0]]], "type": "Polygon"}',
        }
        post_response = self.client.post(
            r("imibio_tree_ecological_data:plot_create"), data
        )
        self.assertTrue(PermanentParcel.objects.exists())
        self.assertRedirects(
            post_response, r("imibio_tree_ecological_data:plot_detail", 1)
        )

    def test_invalid_post(self):
        data = {
            "name": "",
            "coordinator": 1,
            "province": "",
            "municipality": "",
            "locality": "",
            "cadastral_parcel": "1668002000000000012",
            "plot_choices": "Fiscal",
            "obs": "Prueba de registro",
            "latitude": "",
            "longitude": "",
            "geom": "",
        }
        post_response = self.client.post(
            r("imibio_tree_ecological_data:plot_create"), data
        )
        self.assertFalse(PermanentParcel.objects.exists())
        self.assertTrue(post_response.status_code, 200)


class PermanentParcelEditView(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.pp1 = PermanentParcel.objects.create(
            name="Reserva Yrya Pu",
            coordinator=self.coordinator,
            province="Misiones",
            municipality="Puerto Iguazú",
            locality="reserva 600 ha",
            cadastral_parcel="1668002000000000012",
            plot_type="",  #'{"Fiscal":"Fiscal"}', #Todo fijarse si esta bien cargado
            obs="Prueba de registro",
            latitude=-26,
            longitude=-54,
            geom=Polygon(
                [[(-54.6, -27.0), (-54.0, -27.07), (-54.07, -26.62), (-54.6, -27.0)]]
            ),
        )
        self.resp = self.client.get(
            r("imibio_tree_ecological_data:plot_edit", self.pp1.pk)
        )

    def test_get(self):
        """GET plot/create must get status code 200"""
        self.assertEqual(200, self.resp.status_code)
        self.assertTrue(PermanentParcel.objects.exists())

    def test_template(self):
        """must use imibio_tree_ecological_data/permanentparcel_form.html"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/permanentparcel_form.html"
        )

    #     def test_html(self):
    #         """HTML must contais input tags"""
    #         tags = (  # todo confirmar las tags a seren testadas
    #             ('<form'),
    #             ('<input'),
    #             ('type="text"'),
    #             ('type="submit"')
    #         )
    #         # for text in tags:
    #         #     with self.subTest():
    #         #         self.assertContains(self.resp, text)
    #
    def test_csrf(self):
        """html must contains CSRF"""
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        """ "Context must have permanentparcel create form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, PermanentParcelForm)

    def test_update(self):
        update = {
            "name": "Campo San Juan",
            "coordinator": self.coordinator.pk,
            "province": "Misiones",
            "municipality": "Posadas",
            "locality": "reserva 600 ha",
            "cadastral_parcel": "1668002000000000012",
            "plot_choices": {"Privado"},
            "obs": "Prueba de registro",
            "latitude": -26,
            "longitude": -56,
            "geom": '{"coordinates": [[[-54.6, -27.0], [-54.0, -27.07], [-54.07, -26.62], [-54.6, -27.0]]], "type": "Polygon"}',
        }
        # PermanentParcel.objects.filter(pk=self.pp1.pk).update(name='Campo San Juan', municipality='Posadas')

        post_response = self.client.post(
            r("imibio_tree_ecological_data:plot_edit", self.pp1.pk), update
        )
        #     post_response = self.client.post(reverse('imibio_tree_ecological_data:plot_edit', kwargs={'pk': self.pp1.pk}),
        #         {
        #         'name': "Campo San Juan",
        #         'coordinator': self.coordinator.pk,
        #         'province': "Misiones",
        #         'municipality': "Puerto Iguazú",
        #         'locality': "reserva 600 ha",
        #         'cadastral_parcel': '1668002000000000012',
        #         'plot_choices': 'Fiscal',
        #         'obs': "Prueba de registro",
        #         'latitude': -26,
        #         'longitude': -56,
        #         'geom': '{"coordinates": [[[-54.6, -27.0], [-54.0, -27.07], [-54.07, -26.62], [-54.6, -27.0]]], "type": "Polygon"}',
        #         'created_at': '',
        #         }
        #

        self.pp1.refresh_from_db()
        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(self.pp1.name, "Campo San Juan")
        self.assertEqual(self.pp1.municipality, "Posadas")
