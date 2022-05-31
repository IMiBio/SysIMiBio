from django.db.models import Q
import django_filters
from sysimibio.bibliography.models import Publication, SpeciesList, OccurrenceList


class PublicationFilters(django_filters.FilterSet):
    q = django_filters.CharFilter(method="my_custom_filter", label="Definir filtro ")

    class Meta:
        model = Publication
        fields = ["q"]

    def my_custom_filter(self, queryset, name, value):
        return Publication.objects.filter(
            Q(title__icontains=value)
            | Q(author__icontains=value)
            | Q(subject__icontains=value)
            | Q(observations__icontains=value)
            | Q(ISBN__icontains=value)
            | Q(DOI__icontains=value)
            | Q(ORCID__icontains=value)
        )


class SpeciesListFilters(django_filters.FilterSet):
    scientific_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Filtrar por nombre científico "
    )

    class Meta:
        model = SpeciesList
        fields = ["scientific_name"]


class OccurrenceListFilters(django_filters.FilterSet):
    scientific_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Filtrar por nombre científico "
    )

    class Meta:
        model = OccurrenceList
        fields = ["scientific_name"]
