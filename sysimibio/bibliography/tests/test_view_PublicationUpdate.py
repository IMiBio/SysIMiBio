from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from sysimibio.bibliography.models import Publication


class PublicationUpdateTest(TestCase):
    def test_update_publication(self):
        user = User.objects.create_user(
            username="myusername", password="password", email="abc@testmail.com"
        )
        self.client.login(username="myusername", password="password")
        p1 = Publication.objects.create(
            title="The Catcher in the Rye",
            publication_year="1940",
            author="juan",
            created_by=user,
        )
        response = self.client.post(
            reverse("bibliography:publication_edit", kwargs={"pk": p1.id}),
            {
                "title": "The Catcher in the Rye",
                "author": "Juan vinuesa",
                "publication_year": "1940",
                "created_by": "user",
            },
        )

        self.assertEqual(response.status_code, 302)

        p1.refresh_from_db()
        self.assertEqual(p1.author, "Juan vinuesa")
