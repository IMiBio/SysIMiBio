from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from sysimibio.bibliography.models import Publication


class PublicationList(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "Florencia", "flor@imibio.com", "florpassword"
        )
        self.client.login(username="Florencia", password="florpassword")
        self.publication1 = Publication.objects.create(
            ISBN="9780300206111", imibio=False, created_by=self.user
        )
        self.publication2 = Publication.objects.create(
            DOI="10.1038/s41467-021-22702-2", imibio=False, created_by=self.user
        )
        self.publication3 = Publication.objects.create(
            title="Viejo",
            author="Juan Vinuesa",
            publication_year="1945",
            imibio=False,
            created_by=self.user,
        )

    def test_view_url_exists(self):
        resp = self.client.get(r("bibliography:publication_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "bibliography/publication_list.html")

    def test_list_equal(self):
        resp = self.client.get(r("bibliography:publication_list"))
        all_entries = Publication.objects.all().order_by("-publication_year")
        self.assertQuerysetEqual(
            resp.context["object_list"], all_entries, ordered=False
        )
