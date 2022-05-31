from django.contrib import admin
from sysimibio.imibio_occurrences.models import ImibioOccurrence


class ImibioOccurrenceModelAdmin(admin.ModelAdmin):
    list_display = (
        "scientificName",
        "decimalLatitude",
        "decimalLongitude",
        "has_latlong",
    )
    date_hierarchy = "created_at"
    search_fields = ("name", "created_at")

    def has_latlong(self, obj):
        return obj.decimalLatitude is not None and obj.decimalLongitude is not None

    has_latlong.short_description = "Posee georreferencia?"
    has_latlong.boolean = True
    exclude = ("geom",)


admin.site.register(ImibioOccurrence, ImibioOccurrenceModelAdmin)
