from django.test import TestCase
from unittest import skip
from django.shortcuts import resolve_url as r


class HomeTest(TestCase):
    def setUp(self):
        """creating response instance atribute"""
        self.response = self.client.get(r("home"))

    def test_get(self):
        """GET must return status 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, "index.html")

    @skip("Link not availiable for now")
    def test_registro_link(self):
        expected = 'href="{}"'.format(r("imibio_occurrences:new"))
        self.assertContains(self.response, expected)
