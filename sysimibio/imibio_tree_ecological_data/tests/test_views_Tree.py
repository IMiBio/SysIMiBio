from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from sysimibio.imibio_tree_ecological_data.forms import TreeForm
from sysimibio.imibio_tree_ecological_data.models import (
    Tree,
    PermanentParcel,
    FieldWork,
)


class TreeCreateView(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.staff1 = User.objects.create_user(
            "Feli", "feli@imibio.com", "felipassword"
        )
        self.staff2 = User.objects.create_user(
            "Fran", "Fran@imibio.com", "Franpassword"
        )
        self.permanent_parcel = PermanentParcel.objects.create(
            name="Reserva Yrya Pu",
            coordinator=self.coordinator,
            province="Misiones",
            municipality="Puerto Iguazú",
            locality="reserva 600 ha",
            cadastral_parcel=1668002000000000012,
            plot_type="Publico",
            obs="Prueba de registro",
            latitude=-26,
            longitude=-56,
            geom='{"coordinates": [[[-54.6, -27.0], [-54.0, -27.07], [-54.07, -26.62], [-54.6, -27.0]]], "type": "Polygon"}',
        )
        self.field = FieldWork(
            date="2020-12-30",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator,
            parcel_id=self.permanent_parcel,
        )

        self.field.save()
        self.field.staff.add(self.staff1)
        self.field.staff.add(self.staff2)

        self.resp = self.client.get(r("imibio_tree_ecological_data:tree_create"))

    def test_get(self):
        """GET /tree_create must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """must use imibio_tree_ecological_data/tree_form.html"""
        self.assertTemplateUsed(self.resp, "imibio_tree_ecological_data/tree_form.html")

    # def test_html(self):
    #     """HTML must contais input tags"""
    #     tags = (  # todo confirmar las tags a seren testadas
    #         ('<form'),
    #         ('<input'),
    #         ('type="text"'),
    #         ('type="submit"')
    #     )
    #     # for text in tags:
    #     #     with self.subTest():
    #     #         self.assertContains(self.resp, text)

    def test_csrf(self):
        """html must contains CSRF"""
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        """ "Context must have tree create form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, TreeForm)

    def test_valid_post(self):
        data = {
            "field": self.field.pk,
            "subplot": "A1",
            "tree_number": 1,
            "specie": "spp1",
            "latitude": 5,
            "longitude": 9,
            "has_herbarium": True,
            "herbarium_info": "",
        }
        post_response = self.client.post(
            r("imibio_tree_ecological_data:tree_create"), data
        )
        self.assertTrue(Tree.objects.exists())
        self.assertRedirects(
            post_response, r("imibio_tree_ecological_data:tree_detail", 1)
        )

    def test_invalid_post(self):
        data = {
            "field": self.field.pk,
            "subplot": "",
            "tree_number": 1,
            "specie": "",
            "latitude": 0,
            "longitude": 0,
            "geom": '{"coordinates": [[0, 0]], "type": "Point"}',
        }
        post_response = self.client.post(
            r("imibio_tree_ecological_data:tree_create"), data
        )
        self.assertFalse(Tree.objects.exists())
        self.assertTrue(post_response.status_code, 200)


class TreeEditView(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.staff1 = User.objects.create_user(
            "Feli", "feli@imibio.com", "felipassword"
        )
        self.staff2 = User.objects.create_user(
            "Fran", "Fran@imibio.com", "Franpassword"
        )
        self.permanent_parcel = PermanentParcel.objects.create(
            name="Reserva Yrya Pu",
            coordinator=self.coordinator,
            province="Misiones",
            municipality="Puerto Iguazú",
            locality="reserva 600 ha",
            cadastral_parcel=1668002000000000012,
            plot_type="Publico",
            obs="Prueba de registro",
            latitude=-26,
            longitude=-56,
            geom='{"coordinates": [[[-54.6, -27.0], [-54.0, -27.07], [-54.07, -26.62], [-54.6, -27.0]]], "type": "Polygon"}',
        )
        self.field = FieldWork(
            date="2020-12-30",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator,
            parcel_id=self.permanent_parcel,
        )

        self.field.save()
        self.field.staff.add(self.staff1)
        self.field.staff.add(self.staff2)

        self.tree1 = Tree.objects.create(
            field=self.field,
            subplot="A1",
            tree_number=1,
            specie="species one",
            latitude=5,
            longitude=9,
            obs="observación",
            geom='{"coordinates": [[-54.5, -26.0]]], "type": "Point"}',
            has_herbarium=True,
            herbarium_info="",
        )  # todo buscar una forma de generar la latitud a partir de la distancia
        self.resp = self.client.get(
            r("imibio_tree_ecological_data:tree_edit", self.tree1.pk)
        )

    def test_get(self):
        """GET tree/edit must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """must use imibio_tree_ecological_data/tree_form.html"""
        self.assertTemplateUsed(self.resp, "imibio_tree_ecological_data/tree_form.html")

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
    #     def test_csrf(self):
    #         """html must contains CSRF"""
    #         self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ "Context must have tree create form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, TreeForm)

    def test_update(self):
        update = {
            "field": self.tree1.field.pk,
            "subplot": "A3",
            "tree_number": 2,
            "specie": "species update",
            "latitude": 6,
            "longitude": 6,
            "obs": "observación update",
            "has_herbarium": False,
            "herbarium_info": "teste",
        }

        post_response = self.client.post(
            r("imibio_tree_ecological_data:tree_edit", self.tree1.pk), update
        )

        self.assertRedirects(
            post_response, r("imibio_tree_ecological_data:tree_detail", self.tree1.pk)
        )

        self.tree1.refresh_from_db()
        self.assertEqual(self.tree1.tree_number, 2)


class TreeListView(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.staff1 = User.objects.create_user(
            "Feli", "feli@imibio.com", "felipassword"
        )
        self.staff2 = User.objects.create_user(
            "Fran", "Fran@imibio.com", "Franpassword"
        )
        self.permanent_parcel = PermanentParcel.objects.create(
            name="Reserva Yrya Pu",
            coordinator=self.coordinator,
            province="Misiones",
            municipality="Puerto Iguazú",
            locality="reserva 600 ha",
            cadastral_parcel=1668002000000000012,
            plot_type="Publico",
            obs="Prueba de registro",
            latitude=-26,
            longitude=-56,
            geom='{"coordinates": [[[-54.6, -27.0], [-54.0, -27.07], [-54.07, -26.62], [-54.6, -27.0]]], "type": "Polygon"}',
        )
        self.field = FieldWork(
            date="2020-12-30",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator,
            parcel_id=self.permanent_parcel,
        )

        self.field.save()
        self.field.staff.add(self.staff1)
        self.field.staff.add(self.staff2)

        self.tree1 = Tree.objects.create(
            field=self.field,
            subplot="A1",
            tree_number=1,
            specie="species one",
            latitude=-26,
            longitude=-54.5,
            obs="observación",
            geom='{"coordinates": [[-54.5, -26.0]]], "type": "Point"}',
        )
        self.tree2 = Tree.objects.create(
            field=self.field,
            subplot="A2",
            tree_number=2,
            specie="species two",
            latitude=-26.5,
            longitude=-55.5,
            obs="observación 2",
            geom='{"coordinates": [[-55.5, -26.5]]], "type": "Point"}',
        )
        self.tree3 = Tree.objects.create(
            field=self.field,
            subplot="A3",
            tree_number=3,
            specie="species three",
            latitude=-26.56,
            longitude=-55.56,
            obs="observación 3",
            geom='{"coordinates": [[-55.56, -26.56]]], "type": "Point"}',
        )

        self.resp = self.client.get(r("imibio_tree_ecological_data:tree_list"))

    def test_get(self):
        """GET /tree_list/ must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_use_template(self):
        """GET /tree_list/ must use tree_list.html template"""
        self.assertTemplateUsed(self.resp, "imibio_tree_ecological_data/tree_list.html")

    def test_list(self):
        """GET /tree_list/ must have the same queryset from database"""
        all_entries = Tree.objects.all()
        self.assertQuerysetEqual(
            self.resp.context["tree_list"], all_entries, ordered=False
        )


class TreeDetailView(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.staff1 = User.objects.create_user(
            "Feli", "feli@imibio.com", "felipassword"
        )
        self.staff2 = User.objects.create_user(
            "Fran", "Fran@imibio.com", "Franpassword"
        )
        self.permanent_parcel = PermanentParcel.objects.create(
            name="Reserva Yrya Pu",
            coordinator=self.coordinator,
            province="Misiones",
            municipality="Puerto Iguazú",
            locality="reserva 600 ha",
            cadastral_parcel=1668002000000000012,
            plot_type="Publico",
            obs="Prueba de registro",
            latitude=-26,
            longitude=-56,
            geom='{"coordinates": [[[-54.6, -27.0], [-54.0, -27.07], [-54.07, -26.62], [-54.6, -27.0]]], "type": "Polygon"}',
        )
        self.field = FieldWork(
            date="2020-12-30",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator,
            parcel_id=self.permanent_parcel,
        )

        self.field.save()
        self.field.staff.add(self.staff1)
        self.field.staff.add(self.staff2)

        self.Tree1 = Tree.objects.create(
            field=self.field,
            subplot="A1",
            tree_number=1,
            specie="species one",
            latitude=-26,
            longitude=-54.5,
            obs="observación",
            geom='{"coordinates": [[-54.5, -26.0]]], "type": "Point"}',
        )

        self.resp = self.client.get(
            r("imibio_tree_ecological_data:tree_detail", self.Tree1.pk)
        )

    def test_get(self):
        """GET /tree_detail/1 must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_detail_use_template(self):
        """GET /tree_detail/1 must use tree_detail.html template"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/tree_detail.html"
        )


#     def test_detail_html(self):  # todo testar mapa
#         content = [
#             "Reserva Yrya Pu",
#             "Reserva Yrya Pu",
#             "Florencia",
#             "Misiones",
#             "Puerto Iguazú",
#             'reserva 600 ha',
#             "Prueba de registro"]
#         with self.subTest():
#             for expected in content:
#                 self.assertContains(self.resp, expected)


class TreeDetailNotFound(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.resp = self.client.get(r("imibio_tree_ecological_data:tree_detail", 0))

    def test_not_found(self):
        self.assertEqual(404, self.resp.status_code)
