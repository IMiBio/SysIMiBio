from django.test import TestCase
from django.shortcuts import resolve_url as r
from sysimibio.imibio_occurrences.forms import OccurrencesRegistrationForm


class TestOccurrenceFormTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r("imibio_occurrences:new"))
        self.form = OccurrencesRegistrationForm()

    def test_form_has_fields(self):
        """form must have fields"""
        self.assertSequenceEqual(
            [
                "basisOfRecord",
                "institutionCode",
                "collectionCode",
                "catalogNumber",
                "scientificName",
                "kingdom",
                "phylum",
                "clase",
                "order",
                "family",
                "genus",
                "specificEpithet",
                "taxonRank",
                "infraspecificEpithet",
                "identificationQualifier",
                "county",
                "stateProvince",
                "locality",
                "recordedBy",
                "recordNumber",
                "decimalLatitude",
                "decimalLongitude",
            ],
            list(self.form.fields),
        )
