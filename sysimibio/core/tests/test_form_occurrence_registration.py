from unittest import TestCase
from sysimibio.imibio_occurrences.forms import OccurrencesRegistrationForm


class OccurrenceRegistrationFormTest(TestCase):
    def setUp(self):
        self.form = OccurrencesRegistrationForm()

    def test_form_has_fields(self):
        """Form must have 19 fields"""
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
