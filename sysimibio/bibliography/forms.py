from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from isbnlib import is_isbn10, to_isbn13

from sysimibio.bibliography.models import Publication, SpeciesList, OccurrenceList


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = "__all__"
        exclude = ("created_by",)

    def clean(self):
        cleaned_data = super().clean()
        doi = cleaned_data.get("DOI")
        isbn = cleaned_data.get("ISBN")
        crossref = cleaned_data.get("crossref")
        title = cleaned_data.get("title")
        author = cleaned_data.get("author")
        publication_year = cleaned_data.get("publication_year")

        if crossref and not doi and not isbn:
            raise ValidationError(
                "Ingresar DOI o ISBN. Si la publicacion no posee ninguno de los dos deshabilitar checkbox"
            )
        if not crossref and (not title or not author or not publication_year):
            raise ValidationError(
                "Si la publicacion no posee DOI ni ISBN, cargar Titulo, autor y año de publicacion"
            )

        return cleaned_data

    def clean_ISBN(self):
        isbn = self.cleaned_data.get("ISBN")
        if isbn:
            if is_isbn10(isbn):
                isbn = to_isbn13(isbn)
            if "-" in isbn:
                isbn = isbn.replace("-", "")
            if "." in isbn:
                isbn = isbn.replace(".", "")

        return isbn

    def clean_DOI(self):
        doi = self.cleaned_data.get("DOI")
        if doi.endswith("/"):
            doi = doi[:-1]
        return doi


class UploadSpeciesListForm(forms.ModelForm):
    species_list_spreadsheet = forms.FileField(
        validators=[FileExtensionValidator(["csv"])]
    )

    class Meta:
        model = SpeciesList
        exclude = (
            "scientific_name",
            "other_fields_json",
        )


class UploadOccurrencesListForm(forms.ModelForm):
    occurrences_list_spreadsheet = forms.FileField(
        validators=[FileExtensionValidator(["csv"])]
    )

    class Meta:
        model = OccurrenceList
        exclude = (
            "scientific_name",
            "latitude",
            "longitude",
            "other_fields_json",
        )
