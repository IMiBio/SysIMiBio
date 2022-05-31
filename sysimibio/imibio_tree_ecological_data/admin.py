from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from django.forms import CheckboxSelectMultiple
from django.db import models
from sysimibio.imibio_tree_ecological_data.forms import (
    FieldForm,
    PicturesForm,
    TreeForm,
    PermanentParcelForm,
    TreeMeasurementForm,
)
from sysimibio.imibio_tree_ecological_data.models import (
    FieldWork,
    Tree,
    Pictures,
    PermanentParcel,
    TreeMeasurement,
)


class PermanentParcelModelAdmin(admin.ModelAdmin):
    form = PermanentParcelForm
    model = PermanentParcel


class PicsInline(admin.TabularInline):
    form = PicturesForm
    model = Pictures


class TreeInline(admin.StackedInline):
    form = TreeForm
    model = Tree
    extra = 1
    inlines = [PicsInline]


class TreeMeasurementsInline(admin.TabularInline):
    model = TreeMeasurement
    extra = 1


class TreeModelAdmin(admin.ModelAdmin):
    form = TreeForm
    model = Tree
    extra = 1
    inlines = [TreeMeasurementsInline]
    list_display = (
        "tree_id",
        "specie",
    )
    # date_hierarchy = 'field.date'
    search_fields = ("specie",)
    list_filter = ("specie",)


class FieldWorkModelAdmin(admin.ModelAdmin):
    form = FieldForm
    inlines = [TreeInline]
    list_display = (
        "date",
        "coordinator",
        "start_time",
        "end_time",
        "parcel_id",
        "created_at",
        "last_modification_at",
    )
    date_hierarchy = "date"
    search_fields = ("date", "coordinator", "parcel_id")
    list_filter = ("date", "coordinator", "parcel_id")
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }


class TreeMeasurementAdmin(admin.ModelAdmin):
    model = TreeMeasurement
    form = TreeMeasurementForm
    list_display = ("tree",)
    # inlines = [TreeInline]


admin.site.register(PermanentParcel, LeafletGeoAdmin)
admin.site.register(FieldWork, FieldWorkModelAdmin)
admin.site.register(Pictures)
admin.site.register(Tree, TreeModelAdmin)
admin.site.register(TreeMeasurement, TreeMeasurementAdmin)
