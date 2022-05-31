from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from sysimibio.bibliography.forms import PublicationForm
from sysimibio.bibliography.models import Publication


class PublicationViewNewGet(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")
        self.resp = self.client.get(r("bibliography:publication_new"))

    def test_get(self):
        """GET /new/ must get status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_use_template(self):
        """must use publication_form.html template"""
        self.assertTemplateUsed(self.resp, "bibliography/publication_form.html")

    def test_html(self):
        """HTML must contain input tags"""
        tags = (("<form", 2), ("<input", 12), ('type="submit"', 2))
        for text, amount in tags:
            with self.subTest():
                self.assertContains(self.resp, text, amount)

    def test_csrf(self):
        """html must contains CSRF"""
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        """context must have publication form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, PublicationForm)


class PublicationViewNewPostInvalid(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")
        self.resp = self.client.post(r("bibliography:publication_new"), {})
        self.form = self.resp.context["form"]

    def test_Post(self):
        """Invalid post must not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "bibliography/publication_form.html")

    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)

    def test_form_error_all_blank(self):
        self.assertFalse(self.form.is_valid())
        self.assertEqual(
            self.form.errors["__all__"][0],
            "Si la publicacion no posee DOI ni ISBN, cargar Titulo, autor y año de publicacion",
        )  # Primero por la validacion del metodo clean

    def test_form_error_crossref_doi_isbn_blank(self):
        resp = self.client.post(r("bibliography:publication_new"), {"crossref": True})

        self.assertFalse(resp.context["form"].is_valid())
        self.assertEqual(
            resp.context["form"].errors["__all__"][0],
            "Ingresar DOI o ISBN. Si la publicacion no posee ninguno de los dos deshabilitar checkbox",
        )  # Primero por la validacion del metodo clean

    def test_dont_save_publication(self):
        self.assertFalse(Publication.objects.exists())


class PublicationNewValid(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")

        # Named data_doi for entrys with doi
        self.data_doi = dict(
            DOI="10.1038/s41467-021-22702-2", imibio=False, crossref=True
        )
        self.resp_doi = self.client.post(
            r("bibliography:publication_new"), self.data_doi, follow=True
        )

        # Named data_isbn for entrys with isbn
        self.data_isbn = dict(ISBN="9780300206111", imibio=False, crossref=True)
        self.resp_isbn = self.client.post(
            r("bibliography:publication_new"), self.data_isbn, follow=True
        )

        # Named data_manual for entrys without doi or isbn
        self.data_manual = dict(
            title="Jorge el curioso",
            author="Juan",
            publication_year="1940",
            imibio=False,
            crossref=False,
        )
        self.resp_manual = self.client.post(
            r("bibliography:publication_new"), self.data_manual, follow=True
        )

    def test_post_doi(self):
        self.assertEqual(200, self.resp_doi.status_code)

    def test_template_doi(self):
        self.assertTemplateUsed(self.resp_doi, "bibliography/publication_detail.html")

    def test_exists_doi(self):
        self.assertTrue(Publication.objects.exists())

    def test_post_isbn(self):
        self.assertEqual(200, self.resp_isbn.status_code)

    def test_template_isbn(self):
        self.assertTemplateUsed(self.resp_isbn, "bibliography/publication_detail.html")

    def test_exists_isbn(self):
        self.assertTrue(Publication.objects.exists())

    def test_post_manual(self):
        self.assertEqual(200, self.resp_manual.status_code)

    def test_template_manual(self):
        self.assertTemplateUsed(
            self.resp_manual, "bibliography/publication_detail.html"
        )

    def test_exists_manual(self):
        self.assertTrue(Publication.objects.exists())
