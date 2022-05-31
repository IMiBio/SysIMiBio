from django.db import models
from django.urls import reverse_lazy
from djgeojson.fields import PointField

# Create your models here.


class BioblitzProject(models.Model):
    iconURL = models.URLField(verbose_name="URL del icono del proyecto", blank=True)
    description = models.TextField(verbose_name="Descripción del proyecto", blank=True)
    created_at = models.DateTimeField(verbose_name="Fecha de creacción")
    title = models.CharField(verbose_name="Título del proyecto", max_length=200)
    project_id = models.IntegerField(verbose_name="Id del proyecto", unique=True)
    project_slug = models.CharField(
        verbose_name="Nombre del proyecto",
        max_length=250,
        help_text="(Nombre sin espacio. Con guión)",
    )
    place_id = models.IntegerField(verbose_name="Id del local", unique=True)
    project_type = models.CharField(verbose_name="Tipo de proyecto", max_length=100)
    manager_id = models.IntegerField(verbose_name="Id del administrador", unique=True)
    manager_login = models.CharField(
        verbose_name="Login del administrador", max_length=200
    )
    manager_name = models.CharField(
        verbose_name="Nombre del administrador", max_length=200
    )

    def __str__(self):
        return f"{self.title} {self.manager_name} {self.project_id}"

    def get_absolute_url(self):
        return reverse_lazy("bioblitz:project_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Proyecto de BioBlitz"
        verbose_name_plural = "Proyecto de BioBlitz"


class BioblitzOccurrence(models.Model):  # todo work with sounds?
    project_id = models.ForeignKey("BioBlitzProject", on_delete=models.CASCADE)
    obs_id = models.IntegerField("ID de la observación")
    quality_grade = models.CharField("Calidad de ranking", max_length=50)
    created_at = models.DateTimeField("Fecha de la observación")
    uri = models.URLField("URL de la observación")
    # taxon
    taxon_name = models.CharField(
        "Nombre cientifico de la especie", max_length=300, blank=True, default=""
    )
    taxon_rank = models.CharField(
        "Ranking taxonomico", max_length=50, blank=True, default=""
    )
    iconic_taxon_name = models.CharField("Grupo", max_length=50, blank=True, default="")
    endemic = models.BooleanField("Especie endémica?", default=False)
    threatened = models.BooleanField("Especie amenazada?", default=False)
    introduced = models.BooleanField("Especie introducida?", default=False)
    native = models.BooleanField("Especie nativa?", default=False)
    # geo
    geom = PointField(null=True)
    # User
    user_id = models.IntegerField("ID del observador")
    user_login = models.CharField("Login del observador", max_length=50)
    user_name = models.CharField("Nombre del observador", max_length=100, null=True)

    def __str__(self):
        return f"{self.taxon_name} - {self.project_id}"

    def get_absolute_url(self):
        return reverse_lazy("bioblitz:occurrence_detail", kwargs={"pk": self.pk})

    def get_project_absolute_url(self):
        return reverse_lazy(
            "bioblitz:project_detail", kwargs={"pk": self.project_id.pk}
        )

    @property
    def popup_content(self):  # todo Me parece que lo importante es poner alguna foto
        popup = "<strong><span>Nombre científico: </span>{}</strong><br>".format(
            self.taxon_name
        )
        popup += "<span>Altura: </span>{}<br>".format(self.iconic_taxon_name)
        popup += (
            f"<span>Especie amenazada: </span>{'sí' if self.threatened else 'no'}<br>"
        )
        popup += f"<span>Usuário: </span>{self.user_login}<br>"
        popup += f"<span><a href={self.get_project_absolute_url()}>Detalles del proyecto</a></strong><br>"
        popup += f"<span><a href={self.get_absolute_url()}>Detalles de la occurrencia</a></strong><br>"
        return popup

    class Meta:
        verbose_name = "Especie observada"
        verbose_name_plural = "Especies observadas"
