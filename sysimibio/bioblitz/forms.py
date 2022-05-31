from django.forms import ModelForm
from django.core.exceptions import ValidationError

from sysimibio.bioblitz.models import BioblitzProject


class BioblitzModelForm(ModelForm):
    class Meta:
        model = BioblitzProject
        fields = ["project_slug"]

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("project_slug") and not cleaned_data.get("project_id"):
            raise ValidationError("Informar nombre del proyecto o id")
