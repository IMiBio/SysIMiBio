from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from sysimibio.bibliography.models import Publication, SpeciesList, OccurrenceList
from sysimibio.imibio_tree_ecological_data.validators import validate_lat, validate_lon


class PublicationModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.p1 = Publication.objects.create(
            crossref=False,
            title="Jorge el curioso",
            publication_year="2001",
            author="juan",
            created_by=user,
            URL="http://bibliotecadigital.ilce.edu.mx/Colecciones/ObrasClasicas/_docs/TeoriaEvolucion-Darwin.pdf",
            ORCID="https://orcid.org/0000-0002-1825-0097",
        )
        self.p2 = Publication.objects.create(
            DOI="10.1038/s41467-021-22702-2",
            title="hdad",
            author="felipe",
            crossref=True,
            publication_year=1240,
            created_by=user,
        )
        self.p3 = Publication.objects.create(
            ISBN="9780300206111",
            title="ha",
            publication_year="2001",
            author="Juan",
            crossref=True,
            created_by=user,
        )
        self.species_list = SpeciesList.objects.create(
            scientific_name="Cercopithecidae",  # Monkey
            publication=self.p1,
            other_fields_json={
                "kingdom": "animalia",
                "identificador": {0: "algun identificador"},
                "herbario": {"herbario_name": "JBRJ"},
                "Estatus  de conservacion": "amenazada",
            },
        )

        self.occurrence_list = OccurrenceList.objects.create(
            scientific_name="Sus scrofa",  # PIG
            publication=self.p2,
            latitude=-26,
            longitude=-55,
            other_fields_json="{}",
        )

    def test_check_object(self):
        self.assertTrue(Publication.objects.exists())
        self.assertTrue(SpeciesList.objects.exists())
        self.assertTrue(OccurrenceList.objects.exists())

    def test_count_created_objects(self):  # must be 3 //
        self.assertEqual(Publication.objects.count(), 3)
        self.assertEqual(SpeciesList.objects.count(), 1)
        self.assertEqual(OccurrenceList.objects.count(), 1)

    def test_object_content(self):
        p1 = Publication.objects.get(title="Jorge el curioso")
        spp_list = SpeciesList.objects.get(scientific_name="Cercopithecidae")
        occ_list = OccurrenceList.objects.get(scientific_name="Sus scrofa")
        self.assertEqual(occ_list.latitude, -26)
        self.assertEqual(occ_list.longitude, -55)
        self.assertEqual(spp_list.publication.title, "Jorge el curioso")
        self.assertEqual(p1.title, "Jorge el curioso")
        self.assertEqual(p1.author, "juan")
        self.assertEqual(p1.publication_year, "2001")
        self.assertEqual(p1.observations, "")
        self.assertEqual(p1.subject, "")
        self.assertEqual(p1.ORCID, "https://orcid.org/0000-0002-1825-0097")
        self.assertEqual(
            p1.URL,
            "http://bibliotecadigital.ilce.edu.mx/Colecciones/ObrasClasicas/_docs/TeoriaEvolucion-Darwin.pdf",
        )

    def test_check_object_is_article(self):
        self.assertTrue(self.p2.DOI)

    def test_check_object_is_book(self):
        self.assertTrue(self.p3.ISBN)

    def test_check_object_is_not_registered_publication(self):
        self.assertFalse(self.p1.DOI)
        self.assertFalse(self.p1.ISBN)
        self.assertTrue(self.p1.title)
        self.assertTrue(self.p1.publication_year)
        self.assertTrue(self.p1.author)
        self.assertFalse(self.p1.crossref)

    def test_str_publication(self):
        """Publication str must be author, publication_year - title"""
        self.assertEqual("juan, 2001 - Jorge el curioso", str(self.p1))

    def test_str_occurrence_list(self):
        self.assertEqual("Sus scrofa", str(self.occurrence_list))

    def test_str_species_list(self):
        self.assertEqual("Cercopithecidae", str(self.species_list))

    def test_created_at(self):
        """Publication  must have an auto created_at attr."""
        self.assertIsInstance(self.p1.created_at, datetime)

    def test_last_modification(self):
        self.assertIsInstance(self.p1.last_modification_at, datetime)

    def test_created_by(self):
        self.assertIsInstance(self.p1.created_by, User)

    def test_crossref_boolean(self):
        self.assertTrue(self.p2.crossref)

    def test_imibio_default_boolean(self):
        self.assertFalse(self.p2.imibio)

    def test_Url_field(self):
        self.assertEqual(
            self.p1.URL,
            "http://bibliotecadigital.ilce.edu.mx/Colecciones/ObrasClasicas/_docs/TeoriaEvolucion-Darwin.pdf",
        )

    def test_ORCID_field(self):
        self.assertEqual(self.p1.ORCID, "https://orcid.org/0000-0002-1825-0097")

    def test_validate_latitude(self):
        self.assertRaises(ValidationError, validate_lat, -29)

    def test_validate_longitude(self):
        self.assertRaises(ValidationError, validate_lon, -57)

    def test_validators(self):
        self.occurrence_list.latitude = -29
        self.occurrence_list.longitude = -57
        self.occurrence_list.save()
        self.assertRaises(ValidationError, self.occurrence_list.full_clean)

    def test_json_field(self):
        self.assertTrue(self.species_list.other_fields_json)
        self.assertTrue(self.species_list.other_fields_json.keys())
        self.assertEqual(
            self.species_list.other_fields_json,
            {
                "kingdom": "animalia",
                "identificador": {0: "algun identificador"},
                "herbario": {"herbario_name": "JBRJ"},
                "Estatus  de conservacion": "amenazada",
            },
        )

        self.assertIn("kingdom", self.species_list.other_fields_json)
        self.assertIn("identificador", self.species_list.other_fields_json)

    def test_occurrence_list_geojson_field(self):
        self.occurrence_list.latitude = -26
        self.occurrence_list.longitude = -55
        self.occurrence_list.save()
        self.assertTrue(self.occurrence_list.geom.is_valid)

    def test_occurrence_list_popup(self):
        self.assertEqual(
            self.occurrence_list.popup_content,
            "<p><strong><span>Nombre científico: </span>Sus scrofa</strong></p><span><a href=/bibliography/detail/2/>Detalles de la publicación</a></strong><br>",
        )
