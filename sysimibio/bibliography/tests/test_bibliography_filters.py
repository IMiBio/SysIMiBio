from django.contrib.auth.models import User
from django.test import TestCase

from sysimibio.bibliography.filters import (
    PublicationFilters,
    SpeciesListFilters,
    OccurrenceListFilters,
)
from sysimibio.bibliography.models import Publication, SpeciesList, OccurrenceList


class PublicationFilterTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")

        self.p1 = Publication.objects.create(
            title="Poor article",
            author="eric",
            publication_year="2010",
            DOI="10.1038/s41467-021-22702-2",
            imibio=False,
            crossref=True,
            subject="One,",
            observations="article",
            created_by=user,
        )
        self.p2 = Publication.objects.create(
            title="people report",
            publication_year="2011",
            author="juan",
            ISBN="9780300206111",
            imibio=False,
            crossref=True,
            subject="Two,",
            observations="book",
            created_by=user,
        )
        self.p3 = Publication.objects.create(
            title="world health",
            author="Felipe",
            publication_year="2012",
            imibio=False,
            crossref=True,
            subject="Three,",
            ORCID=" https://orcid.org/0000-0002-7014-3707",
            observations="c",
            created_by=user,
        )

    def test_title_filter(self):
        qs = Publication.objects.all()
        f = PublicationFilters()
        result = f.my_custom_filter(qs, "title", "people report")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, self.p2.title)

    def test_author_filter(self):
        qs = Publication.objects.all()
        f = PublicationFilters()
        result = f.my_custom_filter(qs, "author", "eric")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].author, self.p1.author)

    def test_observation_filter(self):
        qs = Publication.objects.all()
        f = PublicationFilters()
        result = f.my_custom_filter(qs, "observations", "article")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].observations, self.p1.observations)

    def test_DOI_filter(self):
        qs = Publication.objects.all()
        f = PublicationFilters()
        result = f.my_custom_filter(qs, "DOI", "10.1038/s41467-021-22702-2")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].DOI, self.p1.DOI)

    def test_DOI_filter(self):
        qs = Publication.objects.all()
        f = PublicationFilters()
        result = f.my_custom_filter(qs, "ISBN", "9780300206111")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ISBN, self.p2.ISBN)

    def test_subject_filter(self):
        qs = Publication.objects.all()
        f = PublicationFilters()
        result = f.my_custom_filter(qs, "subject", "One")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].subject, self.p1.subject)

    def test_ORCID_filter(self):
        qs = Publication.objects.all()
        f = PublicationFilters()
        result = f.my_custom_filter(qs, "ORCID", "0000-0002-7014-3707")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].ORCID, self.p3.ORCID)


class SpeciesListFilterTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")
        self.p1 = Publication.objects.create(
            title="Poor article",
            author="eric",
            publication_year="2010",
            DOI="10.1038/s41467-021-22702-2",
            imibio=False,
            crossref=True,
            subject="One,",
            observations="article",
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
        self.species_list2 = SpeciesList.objects.create(
            scientific_name="Cyclopedidae",  # OSO HORMIGUERO
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
            publication=self.p1,
            latitude=-26,
            longitude=-55,
            other_fields_json="{}",
        )
        self.occurrence_list2 = OccurrenceList.objects.create(
            scientific_name="Caiman latirostris",  # PIG
            publication=self.p1,
            latitude=-25.5,
            longitude=-54.5,
            other_fields_json="{}",
        )

    def test_specieslist_ScientificName_filter(self):
        qs = SpeciesList.objects.all()
        f = SpeciesListFilters(data={"scientific_name": "Cercopithecidae"}, queryset=qs)
        result = f.qs
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].scientific_name, self.species_list.scientific_name)

    def test_occurrencelist_ScientificName_filter(self):
        qs = OccurrenceList.objects.all()
        f = OccurrenceListFilters(data={"scientific_name": "Sus scrofa"}, queryset=qs)
        result = f.qs
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0].scientific_name, self.occurrence_list.scientific_name
        )
