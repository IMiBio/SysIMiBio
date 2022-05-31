from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import HiddenInput
from leaflet.forms.widgets import LeafletWidget

from sysimibio.imibio_tree_ecological_data.models import (
    Tree,
    FieldWork,
    Pictures,
    PermanentParcel,
    TreeMeasurement,
)


class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = "__all__"
        widgets = {
            "geom": HiddenInput(),
        }

    def clean(
        self,
    ):  # todo buscar una forma de generar la latitud a partir de la distancia
        cleaned_data = super().clean()
        # lon = cleaned_data.get('longitude')
        # lat = cleaned_data.get('latitude')
        # if all((lon, lat)):
        #     cleaned_data["geom"] = Point((lon, lat))
        #     if not cleaned_data["geom"].is_valid:
        #         raise ValidationError("Geometria inválida")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("field", css_class="form-group col-md-4 mb-0"),
                Column("subplot", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("tree_number", css_class="form-group col-md-4 mb-0"),
                Column("specie", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("latitude", css_class="form-group col-md-4 mb-0"),
                Column("longitude", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("obs", css_class="form-group col-md-8 mb-0"),
                css_class="form-row",
            ),
            Submit("submit", "Guardar", css_class="btn btn-success"),
        )


class FieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("date", css_class="form-group col-md-4 mb-0"),
                Column("start_time", css_class="form-group col-md-4 mb-0"),
                Column("end_time", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("temperature", css_class="form-group col-md-6 mb-0"),
                Column("humidity", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("coordinator", css_class="form-group col-md-6 mb-0"),
                Column("parcel_id", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("staff", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Submit("submit", "Guardar", css_class="btn btn-success"),
        )

    class Meta:
        model = FieldWork
        fields = "__all__"

    staff = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Acompañantes",
        required=False,
        help_text="-Tildar solamente acompañantes sin responsable.",
    )

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        coordinator = cleaned_data.get("coordinator")
        staff = cleaned_data.get("staff", "")
        if coordinator in staff:
            raise ValidationError(
                "Porfavor desmarque coordinador del campo acompañantes"
            )
        elif (start_time and end_time) and start_time > end_time:
            raise ValidationError("Hora de inicio debe ser menor que hora final")
        coordinator_staff_date_instance = FieldWork.objects.filter(
            Q(date=date, coordinator=coordinator)
            | Q(date=date, staff__in=staff)
            | Q(date=date, coordinator__in=staff)
            | Q(date=date, staff=coordinator)
        )
        coordinator_staff_date_instance = coordinator_staff_date_instance.filter(
            Q(start_time__lte=start_time) & Q(end_time__gte=start_time)
            | Q(start_time__lte=end_time) & Q(end_time__gte=end_time)
            | Q(start_time__gte=start_time) & Q(end_time__lte=end_time)
        )

        if self.instance.pk:
            coordinator_staff_date_instance = coordinator_staff_date_instance.exclude(
                pk=self.instance.pk
            )

        if coordinator_staff_date_instance:
            raise ValidationError(
                "Staff o coordinador ya registrados en otro campo en el mismo dia y hora"
            )

        return cleaned_data


class PicturesForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = "__all__"


PLOT_CHOICES = (
    ("Fiscal", "Fiscal"),
    ("Privado", "Privado"),
)


class PermanentParcelForm(forms.ModelForm):
    class Meta:
        model = PermanentParcel
        exclude = ("created_at",)
        widgets = {
            "geom": LeafletWidget(),
        }

    def clean(self):
        cleaned_data = super().clean()
        cadastral_parcel = cleaned_data.get("cadastral_parcel")
        plot_type = cleaned_data.get("plot_type")
        if len(plot_type) > len(cadastral_parcel.split(",")):
            raise ValidationError(
                "La cantidad de Nomenclaturas catastrales no esta compatible con la cantidad de Plot_types. Favor revisar;"
            )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-6 mb-0"),
                Column("coordinator", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("province", css_class="form-group col-md-6 mb-0"),
                Column("municipality", css_class="form-group col-md-4 mb-0"),
                Column("locality", css_class="form-group col-md-2 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("cadastral_parcel", css_class="form-group col-md-6 mb-0"),
                Column("plot_type", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("geom", css_class="form-group col-md-6 mb-0"),
                Column(
                    Row("latitude", css_class="form-group col-md-4 mb-0"),
                    Row("longitude", css_class="form-group col-md-4 mb-0"),
                ),
                css_class="form-row",
            ),
            Row(
                Column("obs", css_class="form-group col-md-8 mb-0"),
                css_class="form-row",
            ),
            Submit("submit", "Guardar", css_class="btn btn-success"),
        )


liana_types = (
    ("Solo en Fuste", "Solo en Fuste"),
    ("Fuste y copa menor al 50%", "Fuste y copa menor al 50%"),
    ("Fuste y copa mayor al 50%", "Fuste y copa mayor al 50%"),
)


class TreeMeasurementForm(forms.ModelForm):
    class Meta:
        model = TreeMeasurement
        exclude = ("picture",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("tree", css_class="form-group col-md-8 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("dap", css_class="form-group col-md-2 mb-0"),
                Column("dab", css_class="form-group col-md-2 mb-0"),
                Column("tree_height", css_class="form-group col-md-2 mb-0"),
                Column("liana_cover", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("phytosanitary_status", css_class="form-group col-md-4 mb-0"),
                Column(
                    "sociological_classification", css_class="form-group col-md-4 mb-0"
                ),
                css_class="form-row",
            ),
            Row(
                Column("obs", css_class="form-group col-md-8 mb-0"),
                css_class="form-row",
            ),
            Submit("submit", "Guardar", css_class="btn btn-success"),
        )
