import datetime

from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from sysimibio.imibio_tree_ecological_data.forms import FieldForm
from sysimibio.imibio_tree_ecological_data.models import FieldWork, PermanentParcel


class FieldWorkListView(TestCase):
    def setUp(self):
        self.coordinator = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
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
        self.field1 = FieldWork.objects.create(
            date="2020-12-30",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator,
            parcel_id=self.parcel1,
        )
        self.field1.save()
        self.field1.staff.add(self.coordinator)

        self.field2 = FieldWork.objects.create(
            date="2020-11-30",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator,
            parcel_id=self.parcel1,
        )

        self.resp = self.client.get(r("imibio_tree_ecological_data:field_list"))

    def test_get(self):
        """GET list/plot/ must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_use_template(self):
        """GET list/plot/ must use fieldwork_list.html template"""
        self.assertTemplateUsed(
            self.resp, "imibio_tree_ecological_data/fieldwork_list.html"
        )

    def test_list(self):
        """GET list/plot/ must have the same queryset from database"""
        all_entries = FieldWork.objects.all()
        self.assertQuerysetEqual(
            self.resp.context["fieldwork_list"], all_entries, ordered=False
        )


#
# class FieldWorkDetailView(TestCase):
#     def setUp(self):
#         self.coordinator = User.objects.create_user('Florencia',
#                                                     'flor@imibio.com',
#                                                     'florpassword')
#         self.client.login(username='Florencia', password='florpassword')
#         self.parcel1 = PermanentParcel.objects.create(name='Reserva Yrya Pu',
#                                                       coordinator=self.coordinator,
#                                                       province='Misiones',
#                                                       municipality='Puerto Iguazu',
#                                                       locality='600 ha',
#                                                       cadastral_parcel=1668002000000000012,
#                                                       plot_type='Publico',
#                                                       obs='Observacion',
#                                                       latitude=-26,
#                                                       longitude=-56,
#                                                       geom='')
#         self.field1 = FieldWork.objects.create(
#             date='2020-12-30',
#             start_time='0:0',
#             end_time='0:30',
#             temperature=35.9,
#             humidity=80,
#             coordinator=self.coordinator,
#             parcel_id=self.parcel1
#         )
#
#         self.resp = self.client.get(r('imibio_tree_ecological_data:field_detail', self.field1.pk))
#
#     def test_get(self):
#         """GET field/detail/1 must get status code 200"""
#         self.assertEqual(200, self.resp.status_code)
#
#     def test_detail_use_template(self):
#         """GET field/detail/1 must use fieldwork_detail.html template"""
#         self.assertTemplateUsed(self.resp, 'imibio_tree_ecological_data/fieldwork_detail.html')
#
#     def test_detail_html(self):  # todo testar mapa
#         content = [
#             'Reserva Yrya Pu, Puerto Iguazu - Florencia',
#             'Florencia',
#             '30 de Diciembre de 2020',
#             '0:0',
#             '0:30',
#             '35,9',
#             '80,0'
#         ]
#         with self.subTest():
#             for expected in content:
#                 self.assertContains(self.resp, expected)
#
#
# class FieldWorkDetailNotFound(TestCase):
#     def setUp(self):
#         self.coordinator = User.objects.create_user('Florencia',
#                                                     'flor@imibio.com',
#                                                     'florpassword')
#         self.client.login(username='Florencia', password='florpassword')
#         self.resp = self.client.get(r('imibio_tree_ecological_data:field_detail', 0))
#
#     def test_not_found(self):
#         self.assertEqual(404, self.resp.status_code)
#
#
# class FieldWorkCreateView(TestCase):
#     def setUp(self):
#         self.coordinator = User.objects.create_user('Florencia',
#                                                     'flor@imibio.com',
#                                                     'florpassword')
#         self.client.login(username='Florencia', password='florpassword')
#         self.parcel1 = PermanentParcel.objects.create(
#             name='Reserva Yrya Pu',
#             coordinator=self.coordinator,
#             province='Misiones',
#             municipality='Puerto Iguazu',
#             locality='600 ha',
#             cadastral_parcel=1668002000000000012,
#             plot_type='Publico',
#             obs='Observacion',
#             latitude=-26,
#             longitude=-56,
#             geom='')
#
#         # self.field1 = FieldWork.objects.create(
#         #     date='2020-12-30',
#         #     start_time='0:0',
#         #     end_time='0:30',
#         #     temperature=35.9,
#         #     humidity=80,
#         #     coordinator=self.coordinator,
#         #     parcel_id=self.parcel1
#         # )
#
#         self.resp = self.client.get(r('imibio_tree_ecological_data:field_create'))
#
#     def test_get(self):
#         """GET field/create/ must get status code 200"""
#         self.assertEqual(200, self.resp.status_code)
#
#     def test_template(self):
#         """must use imibio_tree_ecological_data/fieldwork_form.html"""
#         self.assertTemplateUsed(self.resp, 'imibio_tree_ecological_data/fieldwork_form.html')
#
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
#
#     def test_has_form(self):
#         """"Context must have fieldwork create form"""
#         form = self.resp.context['form']
#         self.assertIsInstance(form, FieldForm)
#
#     def test_valid_post(self):
#         valid_data = {
#             'date': '2020-12-30',
#             'start_time': '0:0',
#             'end_time': '0:30',
#             'temperature': 35.9,
#             'humidity': 80,
#             'coordinator': self.coordinator.pk,
#             'staff': self.coordinator.pk,
#             'parcel_id': self.parcel1.pk
#         }
#         post_response = self.client.post(r('imibio_tree_ecological_data:field_create'), valid_data)
#         self.assertTrue(FieldWork.objects.exists())
#         self.assertRedirects(post_response, r('imibio_tree_ecological_data:field_detail', 1))
#
#     def test_invalid_post(self):
#         invalid_data = {
#             'date': '',
#             'start_time': '',
#             'end_time': '',
#             'temperature': '',
#             'humidity': '',
#             'coordinator': '',
#             'staff': '',
#             'parcel_id': ''
#         }
#         post_response = self.client.post(r('imibio_tree_ecological_data:field_create'), invalid_data)
#         self.assertFalse(FieldWork.objects.exists())
#         self.assertTrue(post_response.status_code, 200)
#
#
# class FieldWorkEditView(TestCase):
#     def setUp(self):
#         self.coordinator = User.objects.create_user('Florencia',
#                                                     'flor@imibio.com',
#                                                     'florpassword')
#         self.client.login(username='Florencia', password='florpassword')
#         self.parcel1 = PermanentParcel.objects.create(name='Nombre test',
#                                                       coordinator=self.coordinator,
#                                                       province='Misiones',
#                                                       municipality='Puerto Iguazu',
#                                                       locality='600 ha',
#                                                       cadastral_parcel=1668002000000000012,
#                                                       plot_type='Publico',
#                                                       obs='Observacion',
#                                                       latitude=-26,
#                                                       longitude=-56,
#                                                       geom='')
#         self.field1 = FieldWork.objects.create(
#             date='2020-12-30',
#             start_time='0:0',
#             end_time='0:30',
#             temperature=35.9,
#             humidity=80,
#             coordinator=self.coordinator,
#             parcel_id=self.parcel1
#         )
#         self.field1.save()
#         self.field1.staff.add(self.coordinator)
#         self.resp = self.client.get(r('imibio_tree_ecological_data:field_edit', self.field1.pk))
#
#     def test_get(self):
#         """GET field/edit/ must get status code 200"""
#         self.assertEqual(200, self.resp.status_code)
#
#     def test_template(self):
#         """must use imibio_tree_ecological_data/fieldwork_form.html"""
#         self.assertTemplateUsed(self.resp, 'imibio_tree_ecological_data/fieldwork_form.html')
#
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
#
#     def test_has_form(self):
#         """"Context must have fieldwork create form"""
#         form = self.resp.context['form']
#         self.assertIsInstance(form, FieldForm)
#
#     def test_update(self):
#         valid_update = {
#             'date': '2021-01-01',
#             'start_time': '0:0',
#             'end_time': '0:30',
#             'temperature': 35.9,
#             'humidity': 80,
#             'coordinator': self.coordinator.pk,
#             'staff': self.coordinator.pk,
#             'parcel_id': self.parcel1.pk
#         }
#
#         post_response = self.client.post(r('imibio_tree_ecological_data:field_edit', self.field1.pk), valid_update)
#         self.assertRedirects(post_response, r('imibio_tree_ecological_data:field_detail', self.field1.pk))
#         self.field1.refresh_from_db()
#         self.assertEqual(self.field1.date, datetime.date(2021, 1, 1))
