from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase

from sysimibio.bibliography.forms import PublicationForm
from sysimibio.bibliography.models import Publication


class PublicationRegisterForm(TestCase):
    def setUp(self):
        self.resp = self.client.get(r("bibliography:publication_new"))
        user = User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")
        self.publication_form = PublicationForm()
        self.p1 = Publication.objects.create(
            title="Jorge el curioso",
            publication_year="1940",
            author="juan",
            crossref=False,
            created_by=user,
        )

    def test_empty_form(self):
        self.assertIn("publication_year", self.publication_form.fields)
        self.assertIn("title", self.publication_form.fields)
        self.assertIn("author", self.publication_form.fields)
        self.assertIn("DOI", self.publication_form.fields)
        self.assertIn("ISBN", self.publication_form.fields)
        self.assertIn("subject", self.publication_form.fields)
        self.assertIn("ORCID", self.publication_form.fields)
        self.assertIn("observations", self.publication_form.fields)
        self.assertIn("imibio", self.publication_form.fields)
        self.assertIn("crossref", self.publication_form.fields)

    def test_publicationform_has_fields(self):
        self.assertSequenceEqual(
            [
                "publication_year",
                "title",
                "author",
                "DOI",
                "ISBN",
                "subject",
                "ORCID",
                "URL",
                "observations",
                "imibio",
                "crossref",
            ],
            list(self.publication_form.fields),
        )

    def make_publicationform_validated(self, **kwargs):
        user = User.objects.get(pk=1)
        valid = dict(ISBN="9780618884117", crossref=True, created_by=user)
        data = dict(valid, **kwargs)
        form = PublicationForm(data)
        form.is_valid()
        return form

    def make_publicationform_not_validated(self, **kwargs):
        user = User.objects.get(pk=1)
        invalid = dict(ISBN="2", crossref=True, created_by=user)
        data = dict(invalid, **kwargs)
        form = PublicationForm(data)
        form.is_valid()
        return form

    def test_form_is_valid(self):
        form = self.make_publicationform_validated()  # Le paso data valida
        form = form.is_valid()
        self.assertTrue(form)

    def test_form_is_not_valid(self):
        form = self.make_publicationform_not_validated()  # le paso data invalida
        form = form.is_valid()
        self.assertFalse(form)

    def test_field_doi_isbn_blank(self):
        """doi and isbn must be filled when crossref is true"""
        form = self.make_publicationform_validated(DOI="", ISBN="", crossref=True)
        self.assertListEqual(["__all__"], list(form.errors))

    def test_wrong_isbn(self):
        form = PublicationForm(data={"ISBN": "123"})  # testeo un isbn de 3 digitos

        self.assertEqual(
            form.errors["ISBN"], ["Ingrese un ISBN con 10 o 13 caracteres"]
        )

    def test_wrong_doi(self):
        form = PublicationForm(
            data={"DOI": "20.3544/4232"}
        )  # testeo un doi que no comienza con "10."

        self.assertEqual(form.errors["DOI"], ["Doi tiene que comenzar con 10."])

    def test_form_error_one(
        self,
    ):  # testeo cuando el formulario esta mal cargado, si crossref esta desactivado hay que cargar title, publication_year, author
        form = PublicationForm(
            data={"crossref": False, "title": "", "publication_year": "", "author": ""}
        )

        self.assertEqual(
            form.errors["__all__"],
            [
                "Si la publicacion no posee DOI ni ISBN, cargar Titulo, autor y año de publicacion"
            ],
        )

    def test_form_error_two(
        self,
    ):  # testeo cuando el formulario posee error de doi y isbn vacio
        form = PublicationForm(data={"DOI": "", "ISBN": "", "crossref": True})

        self.assertEqual(
            form.errors["__all__"],
            [
                "Ingresar DOI o ISBN. Si la publicacion no posee ninguno de los dos deshabilitar checkbox"
            ],
        )
