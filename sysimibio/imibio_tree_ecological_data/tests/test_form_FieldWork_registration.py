from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from sysimibio.imibio_tree_ecological_data.forms import FieldForm
from sysimibio.imibio_tree_ecological_data.models import FieldWork, PermanentParcel


class FieldRegistrationFormTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r("imibio_tree_ecological_data:field_create"))
        self.Fieldform = FieldForm()
        self.coordinator1 = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.parcel1 = PermanentParcel.objects.create(
            name="Nombre test",
            coordinator=self.coordinator1,
            province="Misiones",
            municipality="Puerto Iguazu",
            cadastral_parcel=1668002000000000012,
            plot_type="Fiscal",
            locality="600 ha",
            obs="Observacion",
            latitude=-26,
            longitude=-56,
            geom="",
        )
        self.staff1 = User.objects.create_user(
            "Felipe", "feli@imibio.com", "felipassword"
        )
        self.field1 = FieldWork.objects.create(
            date="2020-12-30",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator1,
            parcel_id=self.parcel1,
        )

    def test_Fieldform_has_fields(self):
        """Field form must have models fields"""
        self.assertSequenceEqual(
            [
                "date",
                "start_time",
                "end_time",
                "temperature",
                "humidity",
                "coordinator",
                "staff",
                "parcel_id",
            ],
            list(self.Fieldform.fields),
        )

    def make_FieldForm_validated(self, **kwargs):
        valid = dict(
            date="2020-12-01",
            start_time="0:0",
            end_time="0:30",
            temperature=35.9,
            humidity=80,
            coordinator=self.coordinator1,
            staff=[self.staff1],
            parcel_id=self.parcel1,
        )

        data = dict(valid, **kwargs)
        form = FieldForm(data)
        form.is_valid()
        return form

    def assertFormCode(self, form, field, code):
        error = form.errors.as_data()
        error_list = error[field]
        exception = error_list[0]
        self.assertEqual(code, exception.code)

    def test_field_start_time_not_bigger_than_end_time(self):
        """Start time must be lower then end time"""
        form = self.make_FieldForm_validated(start_time="10:40", end_time="9:00")
        self.assertListEqual(["__all__"], list(form.errors))

    def test_field_date_not_bigger_then_today(self):
        form = self.make_FieldForm_validated(date="2050-12-31")
        self.assertFormCode(form, "date", "Date in the future")

    def test_field_temp_not_bigger_45(self):
        form = self.make_FieldForm_validated(temperature="56")
        self.assertFormCode(form, "temperature", "Temperature out of the range")

    def test_field_temp_not_lower_minus5(self):
        form = self.make_FieldForm_validated(temperature="-6")
        self.assertFormCode(form, "temperature", "Temperature out of the range")

    def test_field_humedad_not_bigger_100(self):
        form = self.make_FieldForm_validated(humidity="101")
        self.assertFormCode(form, "humidity", "Humidity out of the range")

    def test_field_humedad_not_lower_0(self):
        form = self.make_FieldForm_validated(humidity="-1")
        self.assertFormCode(form, "humidity", "Humidity out of the range")
