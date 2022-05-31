from datetime import datetime

from django.test import TestCase
from sysimibio.imibio_occurrences.models import ImibioOccurrence


class OcurrenceModelTest(TestCase):
    def setUp(self):
        self.obj = ImibioOccurrence(
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
            geom={"type": "Point", "coordinates": [-60, -56]},
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(ImibioOccurrence.objects.exists())

    def test_created_at(self):
        """Registration must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual("Panthera Onca", str(self.obj))


class OccurrenceModelGeomTest(TestCase):
    def setUp(self):
        self.obj = ImibioOccurrence(
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
            # geom={'type': 'Point', 'coordinates': [-60, -56]} #created on seave method
        )
        self.obj.save()

    def test_exists(self):
        self.assertTrue(ImibioOccurrence.objects.exists())

    def test_geom_is_Point(self):
        self.assertEqual(self.obj.geom.get("type"), "Point")

    def test_geom_lon_Equals_lon_field(self):
        self.assertEqual(self.obj.geom.get("coordinates")[0], self.obj.decimalLongitude)

    def test_geom_lon_Equals_lat_field(self):
        self.assertEqual(self.obj.geom.get("coordinates")[1], self.obj.decimalLatitude)
