from django.shortcuts import resolve_url as r
from django.test import TestCase

from sysimibio.imibio_occurrences.forms import OccurrencesRegistrationForm
from sysimibio.imibio_occurrences.models import ImibioOccurrence


class RegistrationGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r("imibio_occurrences:new"))

    def test_get(self):
        """get /registro_ocurrencias/ must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """must use imibio_occurrences/occurrences_registration_form.html"""
        self.assertTemplateUsed(
            self.resp, "occurrences/occurrences_registration_form.html"
        )

    def test_html(self):
        """HTML must contais input tags"""
        tags = (("<form"), ("<input"), ('type="text"'), ('type="submit"'))
        for text in tags:
            with self.subTest():
                self.assertContains(self.resp, text)

    def test_csrf(self):
        """html must contains CSRF"""
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        """ "Context must have occurrence registration form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, OccurrencesRegistrationForm)


class RegistrationPostValid(TestCase):
    def setUp(self):
        data = dict(
            basisOfRecord="Observation",
            institutionCode=1,
            collectionCode=1,
            catalogNumber=2,
            scientificName="Pathera Onca",
            kingdom="reino",
            phylum="filo",
            clase="clase",
            order="orden",
            family="familia",
            genus="genero",
            specificEpithet="epiteto especifico",
            taxonRank="ranking de la taxonomia",
            infraspecificEpithet="infra espiteto",
            identificationQualifier="calificacion de identificacion",
            county="Argentina",
            stateProvince="Misiones",
            locality="Posadas",
            recordedBy="Felipe",
            recordNumber=1,
            decimalLatitude=-56,
            decimalLongitude=-60,
        )
        self.resp = self.client.post(r("imibio_occurrences:new"), data)

    def test_post(self):
        """Valid POST should redirect to /registro_ocurrencias/1/"""
        # self.assertEqual(302, self.resp.status_code)
        self.assertRedirects(self.resp, r("imibio_occurrences:detail", 1))

    def test_save_occurrence_registration(self):
        self.assertTrue(ImibioOccurrence.objects.exists())


class RegistrationPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r("imibio_occurrences:new"), {})

    def test_post(self):
        """Invalid POST should not redirect to /registro_ocurrencias/"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.resp, "occurrences/occurrences_registration_form.html"
        )

    def test_has_form(self):
        form = self.resp.context["form"]
        self.assertIsInstance(form, OccurrencesRegistrationForm)

    def test_has_errors(self):
        form = self.resp.context["form"]
        self.assertTrue(form.errors)

    def test_dont_save_occurrence_registration(self):
        self.assertFalse(ImibioOccurrence.objects.exists())
