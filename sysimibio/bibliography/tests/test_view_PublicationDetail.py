from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from sysimibio.bibliography.models import Publication


class PublicationDetail(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")
        self.publication1 = Publication.objects.create(
            ISBN="9780300206111", imibio=False, created_by=self.user
        )
        self.resp = self.client.get(
            r("bibliography:publication_detail", self.publication1.pk), follow=True
        )

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "bibliography/publication_detail.html")

    # def test_html(self):
    #     content = [
    #         'Thomas E. Lovejoy',
    #         '2019',
    #         False,
    #         2,
    #     ]
    #     with self.subTest():
    #         for expected in content:
    #             self.assertContains(self.resp, expected)


class PublicationDetailNotFound(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")
        self.resp = self.client.get(r("bibliography:publication_detail", 0))

    def test_not_found(self):
        self.assertEqual(404, self.resp.status_code)
