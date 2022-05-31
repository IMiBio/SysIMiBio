from django.test import TestCase
from datetime import datetime

from dateutil.tz import tzoffset


from sysimibio.bioblitz.models import BioblitzProjects


class BioblitzProjectTest(TestCase):
    def setUp(self):
        self.bioblitz = BioblitzProjects.objects.create(
            iconURL="https://static.inaturalist.org/projects/69644-icon-span2.jpg?1584740458",
            description="Este proyecto tiene como ",
            created_at=datetime.datetime(
                2020, 3, 20, 18, 40, 59, tzinfo=tzoffset(None, -10800)
            ),
            title="Biodiversidad de Misiones",
            project_id=69644,
            slug="biodiversidad-de-misiones",
            place_id=10422,
            project_type="collection",
            manager_id=1626810,
            manager_login="institutomisionerodebiodiversidad",
            manager_name="IMiBio",
        )
        # self.bioblitz.save()

    def test_create(self):
        self.assertTrue(BioblitzProjects.objects.exists())
