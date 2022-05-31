import csv

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from sysimibio.bibliography.models import Publication, SpeciesList


class SpeciesListUpdateTest(TestCase):
    def generate_file(self):
        try:
            myfile = open("test.csv", "w")
            wr = csv.writer(myfile)
            wr.writerow(
                (
                    "scientific_name",
                    "herbarium",
                    "kingdom",
                    "conservation_status",
                    "autor",
                )
            )
            wr.writerow(("1", "herbarium1", "kingdom1", "status1", "felipe"))
            wr.writerow(("2", "herbarium2", "kingdom2", "status2", "juan"))
            wr.writerow(("3", "herbarium3", "kingdom3", "status3", "francisco"))
        finally:
            myfile.close()

        return myfile

    def test_update_specieslist(self):
        user = User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")
        self.p1 = Publication.objects.create(
            title="Test de species list",
            publication_year="1940",
            author="juan",
            created_by=user,
        )
        myfile = self.generate_file()
        file_path = myfile.name
        f = open(file_path, "rb")
        self.species_list = SpeciesList.objects.create(
            publication=self.p1,
            scientific_name="h1",
            other_fields_json={"kingdom": "flora"},
        )
        response = self.client.post(
            reverse("bibliography:specieslist_edit", kwargs={"pk": self.p1.pk}),
            {"species_list_spreadsheet": f, "publication": self.p1.pk},
        )
        self.species_list.refresh_from_db()
        self.assertEqual(response.status_code, 302)
