from django.db.models import Q
import django_filters
from sysimibio.imibio_tree_ecological_data.models import TreeMeasurement


class TreeMeasurementFilters(django_filters.FilterSet):
    q = django_filters.CharFilter(method="my_custom_filter", label="Definir filtro ")

    class Meta:
        model = TreeMeasurement
        fields = ["q"]

    def my_custom_filter(self, queryset, name, value):
        return TreeMeasurement.objects.filter(
            Q(field__parcel_id__name__icontains=value)
            | Q(field__parcel_id__coordinator__username__icontains=value)  # parcela
            | Q(field__parcel_id__municipality__icontains=value)  # parcela
            | Q(tree__tree_number__icontains=value)  # parcela
            | Q(tree__specie__icontains=value)  # arbol
            |  # arbol
            # Q(tree__tree_id__icontains=value) |  # arbol  # todo felipe
            Q(tree__created_at__icontains=value)
            | Q(dap__icontains=value)  # arbol
            | Q(dab__icontains=value)  # medidion
            | Q(tree_height__icontains=value)  # medidion
            | Q(phytosanitary_status__icontains=value)  # medidion
            | Q(sociological_classification__icontains=value)  # medidion
            | Q(obs__icontains=value)  # medidion
            | Q(created_at__icontains=value)  # medidion
        )  # medidion
