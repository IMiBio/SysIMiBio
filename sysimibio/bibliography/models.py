from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import resolve_url as r
from geojson import Point

from sysimibio.bibliography.validators import (
    validate_isbn,
    validate_doi_prefix,
    validate_doi_slash,
)
from sysimibio.imibio_tree_ecological_data.validators import validate_lat, validate_lon


class Publication(models.Model):
    id = models.AutoField(primary_key=True)
    publication_year = models.CharField(
        "Año de publicación", max_length=4, blank=True, help_text="YYYY"
    )
    title = models.CharField("Título", max_length=255, blank=True)
    author = models.CharField("Autor", max_length=255, blank=True)
    DOI = models.CharField(
        "DOI",
        max_length=30,
        blank=True,
        validators=[validate_doi_prefix, validate_doi_slash],
    )
    ISBN = models.CharField(
        "ISBN",
        help_text="Ingresar ISBN sin guion ni puntos",
        max_length=13,
        blank=True,
        validators=[validate_isbn],
    )
    subject = models.CharField("Palabras clave o tema", max_length=200, blank=True)
    ORCID = models.URLField("ORCID (opcional)", max_length=200, blank=True)
    URL = models.URLField("URL (opcional)", max_length=200, blank=True)
    created_at = models.DateTimeField(verbose_name="Fecha creación", auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    last_modification_at = models.DateTimeField(
        verbose_name="Ultima modificación", auto_now=True
    )
    observations = models.TextField(verbose_name="Observaciones", blank=True)
    imibio = models.BooleanField(verbose_name="Participación IMIBIO ?", default=False)
    crossref = models.BooleanField(
        verbose_name="Tiene DOI/ISBN ?",
        help_text="Si tiene referencias con DOI O ISBN marcar.",
        default=True,
    )

    def __str__(self):
        return f"{self.author}, {self.publication_year} - {self.title}"

    def get_absolute_url(self):
        return r("bibliography:publication_detail", self.pk)


class SpeciesList(models.Model):
    scientific_name = models.CharField("Nombre científico", max_length=50)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    other_fields_json = models.JSONField(default=dict)

    def __str__(self):
        return self.scientific_name


class OccurrenceList(models.Model):
    scientific_name = models.CharField("Nombre científico", max_length=50, blank=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    latitude = models.FloatField("Latitud", validators=[validate_lat])
    longitude = models.FloatField("Longitud", validators=[validate_lon])
    other_fields_json = models.JSONField(default=dict)

    def get_publication_absolute_url(self):
        return r("bibliography:publication_detail", self.publication.pk)

    @property
    def geom(self):
        return Point((self.longitude, self.latitude))

    @property
    def popup_content(self):
        popup = f"<p><strong><span>Nombre científico: </span>{self.scientific_name}</strong></p>"
        popup += f"<span><a href={self.get_publication_absolute_url()}>Detalles de la publicación</a></strong><br>"
        return popup

    def __str__(self):
        return self.scientific_name
