from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
from django.test import TestCase
from sysimibio.bibliography.models import Publication, SpeciesList
from sysimibio.bibliography.forms import  UploadSpeciesListForm
from django.core.files.uploadedfile import SimpleUploadedFile
import csv

class SpeciesListViewNewGet(TestCase):

    def setUp(self):
        User.objects.create_user(username="myusername", password="password", email="abc@testmail.com")
        self.client.login(username='myusername', password='password')
        self.resp = self.client.get(r('bibliography:species_new'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_use_template(self):
        """must use specieslist_form.html template"""
        self.assertTemplateUsed(self.resp, 'bibliography/specieslist_form.html')

    def test_csrf(self):
        """html must contains CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """context must have uploadSpeciesList form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, UploadSpeciesListForm)


class SpeciesListViewNewPost(TestCase):
    def generate_file(self):
        try:
            myfile = open('test.csv', 'w')
            wr = csv.writer(myfile)
            wr.writerow(('scientific_name', 'herbarium', 'kingdom', 'conservation_status', 'autor'))
            wr.writerow(('1', 'herbarium1', 'kingdom1', 'status1', 'felipe'))
            wr.writerow(('2', 'herbarium2', 'kingdom2', 'status2', 'juan'))
            wr.writerow(('3', 'herbarium3', 'kingdom3', 'status3', 'francisco'))
        finally:
            myfile.close()

        return myfile
    def setUp(self):
        self.user = User.objects.create_user('Florencia', 'flor@imibio.com', 'florpassword')
        self.client.login(username='Florencia', password='florpassword')
        self.publication1 = Publication.objects.create(
            ISBN='9780300206111',
            imibio=False,
            created_by=self.user
        )
        # f = open("species_list.csv", "rb") #todo fijarse como generar el archivo en el propio test
        myfile = self.generate_file()
        file_path = myfile.name
        f = open(file_path, "r")
        self.resp = self.client.post(r('bibliography:species_new'), {'species_list_spreadsheet': f, 'bibliography': self.publication1.pk})

    def test_post(self):
        self.assertEqual(302, self.resp.status_code)

    def test_redirect(self):
        self.assertRedirects(self.resp, r('bibliography:publication_detail', 1))

    # def test_use_template(self):
    #     """must use publication_detail.html template"""
    #     self.assertTemplateUsed(self.resp, 'bibliography/detail')

    def test_exist_species_list(self):
        self.assertTrue(SpeciesList.objects.exists())


class SpeciesListViewNewPostInvalid(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Florencia', 'flor@imibio.com', 'florpassword')
        self.client.login(username='Florencia', password='florpassword')
        self.publication1 = Publication.objects.create(
            ISBN='9780300206111',
            imibio=False,
            created_by=self.user
        )
        data = SimpleUploadedFile("species_list.csv", b"file_content", content_type="text/csv")
        data_manual = {'file': data,
                       'scientific_name':'juan',
                        'bibliography': self.publication1} #Esto carga el archivo vacio
        self.resp = self.client.post(r('bibliography:species_new'), {'species_list_spreadsheet': data_manual, 'bibliography': self.publication1.pk})

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'bibliography/specieslist_form.html')

    def test_dont_save_publication(self):
        self.assertFalse(SpeciesList.objects.exists())