from django.test import TestCase
from django.shortcuts import resolve_url as r

from sysimibio.imibio_occurrences.models import ImibioOccurrence


class OccurrenceDetailGet(TestCase):
    def setUp(self):
        self.obj = ImibioOccurrence.objects.create(
            basisOfRecord="Observation",
            institutionCode=1,
            collectionCode=1,
            catalogNumber=2,
            scientificName="Panthera Onca",
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
        self.resp = self.client.get(r("imibio_occurrences:detail", self.obj.pk))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "occurrences/occurrence_detail.html")

    def test_context(self):
        occurrence = self.resp.context["occurrence"]
        self.assertIsInstance(occurrence, ImibioOccurrence)

    def test_html(self):
        content = [
            "Observation",
            1,
            1,
            2,
            "Panthera Onca",
            "reino",
            "filo",
            "clase",
            "orden",
            "familia",
            "genero",
            "epiteto especifico",
            "ranking de la taxonomia",
            "infra espiteto",
            "calificacion de identificacion",
            "Argentina",
            "Misiones",
            "Posadas",
            "Felipe",
            1,
            -56,
            -60,
        ]
        with self.subTest():
            for expected in content:
                self.assertContains(self.resp, expected)


class OccurrenceDetailNotFound(TestCase):
    def setUp(self):
        self.resp = self.client.get(r("imibio_occurrences:detail", 0))

    def test_not_found(self):
        self.assertEqual(404, self.resp.status_code)
