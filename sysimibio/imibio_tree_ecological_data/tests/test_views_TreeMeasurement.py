from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import resolve_url as r
from django.test import TestCase, override_settings

from sysimibio.imibio_tree_ecological_data.forms import TreeMeasurementForm
from sysimibio.imibio_tree_ecological_data.models import (
    Tree,
    PermanentParcel,
    FieldWork,
    TreeMeasurement,
    Pictures,
)

TINY_GIF = (
    b"GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;"
)


@override_settings(DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage")
class TreeMeasurementCreateView(TestCase):
    def setUp(self):
        self.tempPicture = Pictures.objects.create(
            picture=SimpleUploadedFile("tiny.gif", TINY_GIF)
        )
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
            specie="spp1",
            latitude=-26,
            longitude=-54.5,
        )
        self.resp = self.client.get(
            r("imibio_tree_ecological_data:tree_measurement_create")
        )

    def test_get(self):
        """GET /tree_measurement_create must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """must use imibio_tree_ecological_data/treemeasurement_form.html"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/treemeasurement_form.html"
        )

    #
    #     # def test_html(self):
    #     #     """HTML must contais input tags"""
    #     #     tags = (  # todo confirmar las tags a seren testadas
    #     #         ('<form'),
    #     #         ('<input'),
    #     #         ('type="text"'),
    #     #         ('type="submit"')
    #     #     )
    #     #     # for text in tags:
    #     #     #     with self.subTest():
    #     #     #         self.assertContains(self.resp, text)

    def test_csrf(self):
        """html must contains CSRF"""
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        """ "Context must have tree measurement create form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, TreeMeasurementForm)

    def test_valid_post(self):
        valid_data = {
            "tree": self.tree1.pk,
            "dap": 30,
            "dab": 50,
            "tree_height": 3,
            "picture": self.tempPicture,
            "phytosanitary_status": 1,
            "sociological_classification": 1,
            "liana_cover": 1,
            "obs": "Observación",
        }
        post_response = self.client.post(
            r("imibio_tree_ecological_data:tree_measurement_create"), valid_data
        )
        self.assertTrue(TreeMeasurement.objects.exists())
        self.assertRedirects(
            post_response, r("imibio_tree_ecological_data:tree_measurement_detail", 1)
        )

    def test_invalid_post(self):
        invalid_data = {
            "tree": self.tree1.pk,
            "dap": -30,
            "dab": -50,
            "tree_height": -3,
            "phytosanitary_status": "",
            "sociological_classification": "",
            "obs": "",
        }
        post_response = self.client.post(
            r("imibio_tree_ecological_data:tree_measurement_create"), invalid_data
        )
        self.assertFalse(TreeMeasurement.objects.exists())
        self.assertTrue(post_response.status_code, 200)


@override_settings(DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage")
class TreeEditView(TestCase):
    def setUp(self):
        self.tempPicture = Pictures.objects.create(
            picture=SimpleUploadedFile("tiny.gif", TINY_GIF)
        )
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
        self.measurement1 = TreeMeasurement.objects.create(
            tree=self.tree1,
            dap=30,
            dab=50,
            tree_height=3,
            # picture=self.tempPicture,
            phytosanitary_status=2,
            sociological_classification=2,
            liana_cover=1,
            obs="Observación",
        )

        self.resp = self.client.get(
            r("imibio_tree_ecological_data:tree_measurement_edit", self.measurement1.pk)
        )

    def test_get(self):
        """GET tree_measurement_edit must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """must use imibio_tree_ecological_data/treemeasurement_form.html"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/treemeasurement_form.html"
        )

    #     #     #     def test_html(self):
    #     #     #         """HTML must contais input tags"""
    #     #     #         tags = (  # todo confirmar las tags a seren testadas
    #     #     #             ('<form'),
    #     #     #             ('<input'),
    #     #     #             ('type="text"'),
    #     #     #             ('type="submit"')
    #     #     #         )
    #     #     #         # for text in tags:
    #     #     #         #     with self.subTest():
    #     #     #         #         self.assertContains(self.resp, text)
    #     #     #
    #     #     #     def test_csrf(self):
    #     #     #         """html must contains CSRF"""
    #     #     #         self.assertContains(self.resp, 'csrfmiddlewaretoken')
    #
    def test_has_form(self):
        """ "Context must have tree measurement create form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, TreeMeasurementForm)

    def test_update(self):  # todo fix problem with image upload
        valid_update = {
            "tree": self.tree1.pk,
            "dap": 60,
            "dab": 80,
            "tree_height": 6,
            "picture": self.tempPicture,
            "phytosanitary_status": 1,
            "sociological_classification": 1,
            "liana_cover": 1,
            "obs": "Observación Update",
        }

        post_response = self.client.post(
            r(
                "imibio_tree_ecological_data:tree_measurement_edit",
                self.measurement1.pk,
            ),
            valid_update,
        )
        self.assertRedirects(
            post_response,
            r(
                "imibio_tree_ecological_data:tree_measurement_detail",
                self.measurement1.pk,
            ),
        )

        self.measurement1.refresh_from_db()
        self.assertEqual(self.measurement1.dap, 60)


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
            specie="species two",
            latitude=-26.53,
            longitude=-55.53,
            obs="observación 3",
            geom='{"coordinates": [[-55.5, -26.5]]], "type": "Point"}',
        )

        self.measurement1 = TreeMeasurement.objects.create(
            tree=self.tree1,
            dap=30,
            dab=50,
            tree_height=3,
            # picture=self.tempPicture,
            phytosanitary_status=1,
            sociological_classification=1,
            liana_cover=1,
            obs="Observación1",
        )

        self.measurement2 = TreeMeasurement.objects.create(
            tree=self.tree2,
            dap=60,
            dab=100,
            tree_height=6,
            # picture=self.tempPicture,
            phytosanitary_status=2,
            sociological_classification=2,
            liana_cover=2,
            obs="Observación2",
        )

        self.measurement3 = TreeMeasurement.objects.create(
            tree=self.tree3,
            dap=30,
            dab=80,
            tree_height=4,
            # picture=self.tempPicture,
            phytosanitary_status=3,
            sociological_classification=3,
            liana_cover=3,
            obs="Observación3",
        )

        self.resp = self.client.get(
            r("imibio_tree_ecological_data:tree_measurement_list")
        )

    def test_get(self):
        """GET /tree_measurement_list/ must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_use_template(self):
        """GET /tree_measurement_list/ must use treemeasurement_list.html template"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/treemeasurement_list.html"
        )

    def test_list(self):
        """GET /tree_measurement_list/ must have the same queryset from database"""
        all_entries = TreeMeasurement.objects.all().order_by("-created_at")
        self.assertQuerysetEqual(self.resp.context["treemeasurement_list"], all_entries)


@override_settings(DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage")
class TreeDetailView(TestCase):
    def setUp(self):
        self.tempPicture = Pictures.objects.create(
            picture=SimpleUploadedFile("tiny.gif", TINY_GIF)
        )
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

        self.measurement1 = TreeMeasurement.objects.create(
            tree=self.tree1,
            dap=30,
            dab=50,
            tree_height=3,
            picture=self.tempPicture,
            phytosanitary_status=1,
            sociological_classification=1,
            obs="Observación",
        )

        self.resp = self.client.get(
            r(
                "imibio_tree_ecological_data:tree_measurement_detail",
                self.measurement1.pk,
            )
        )

    def test_get(self):
        """GET /tree_measurement_detail/1 must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_detail_use_template(self):
        """GET /tree_measurement_detail/1 must use treemeasurement_detail.html template"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/treemeasurement_detail.html"
        )


# #     def test_detail_html(self):  # todo testar mapa
# #         content = [
# #             "Reserva Yrya Pu",
# #             "Reserva Yrya Pu",
# #             "Florencia",
# #             "Misiones",
# #             "Puerto Iguazú",
# #             'reserva 600 ha',
# #             "Prueba de registro"]
# #         with self.subTest():
# #             for expected in content:
# #                 self.assertContains(self.resp, expected)


class PermanentParcelDetailNotFound(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.resp = self.client.get(
            r("imibio_tree_ecological_data:tree_measurement_detail", 0)
        )

    def test_not_found(self):
        self.assertEqual(404, self.resp.status_code)
