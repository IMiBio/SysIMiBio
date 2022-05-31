from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django_filters.views import FilterView
from djgeojson.views import GeoJSONLayerView

from sysimibio.imibio_tree_ecological_data.filters import TreeMeasurementFilters
from sysimibio.imibio_tree_ecological_data.forms import (
    TreeForm,
    FieldForm,
    PermanentParcelForm,
    TreeMeasurementForm,
)
from sysimibio.imibio_tree_ecological_data.models import (
    FieldWork,
    Tree,
    PermanentParcel,
    TreeMeasurement,
)


class PlotCreateView(LoginRequiredMixin, CreateView):
    model = PermanentParcel
    form_class = PermanentParcelForm

    def post(self, request, *args, **kwargs):
        form = PermanentParcelForm(request.POST)
        if form.is_valid():
            self.object.save()
            return redirect("imibio_tree_ecological_data:plot_detail", self.object.pk)
        else:
            return render(
                self.request,
                "imibio_tree_ecological_data/permanentparcel_form.html",
                {"form": form},
            )


PlotCreateView = PlotCreateView.as_view()


class PlotEditView(LoginRequiredMixin, UpdateView):
    model = PermanentParcel
    form_class = PermanentParcelForm

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        parcel = get_object_or_404(PermanentParcel, pk=pk)
        form = PermanentParcelForm(request.POST, instance=parcel)
        if form.is_valid():
            form.save()
            return redirect("imibio_tree_ecological_data:plot_detail", pk)
        else:
            return render(
                self.request,
                "imibio_tree_ecological_data/permanentparcel_form.html",
                {"form": form},
            )


PlotEditView = PlotEditView.as_view()


class PlotListView(LoginRequiredMixin, ListView):
    model = PermanentParcel


PlotListView = PlotListView.as_view()


class PlotDetailView(LoginRequiredMixin, DetailView):
    model = PermanentParcel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["field_list"] = FieldWork.objects.filter(parcel_id=self.kwargs["pk"])
        context["measurement_list"] = TreeMeasurement.objects.filter(
            tree__field__parcel_id=self.kwargs["pk"]
        )
        context["tree_list"] = Tree.objects.filter(field__parcel_id=self.kwargs["pk"])
        return context


PlotDetailView = PlotDetailView.as_view()


class PlotDetailGeoJson(GeoJSONLayerView):
    model = PermanentParcel
    properties = ("popup_content",)

    def get_queryset(self):
        self.plot = super().get_queryset()
        return self.plot.filter(pk=self.kwargs["pk"])


PlotDetailGeoJson = PlotDetailGeoJson.as_view()


class PlotDetailTreesGeoJson(GeoJSONLayerView):
    model = Tree
    properties = ("popup_content",)

    def get_queryset(self):
        self.tree = super().get_queryset()
        return self.tree.filter(field__parcel_id=self.kwargs["pk"])


PlotDetailTreesGeoJson = PlotDetailTreesGeoJson.as_view()


class FieldWorkCreateView(LoginRequiredMixin, CreateView):
    model = FieldWork
    form_class = FieldForm


FieldWorkCreateView = FieldWorkCreateView.as_view()


class FieldWorkEditView(LoginRequiredMixin, UpdateView):
    model = FieldWork
    form_class = FieldForm


FieldWorkEditView = FieldWorkEditView.as_view()


class FieldWorkListView(LoginRequiredMixin, ListView):
    model = FieldWork


FieldWorkListView = FieldWorkListView.as_view()


class FieldWorkDetailView(LoginRequiredMixin, DetailView):
    model = FieldWork

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["measurement_list"] = TreeMeasurement.objects.filter(
            tree__field__pk=self.kwargs["pk"]
        )
        context["tree_list"] = Tree.objects.filter(field__pk=self.kwargs["pk"])
        return context


FieldWorkDetailView = FieldWorkDetailView.as_view()


class FieldWorkDetailTreesGeoJson(GeoJSONLayerView):
    model = Tree
    properties = ("popup_content",)

    def get_queryset(self):
        self.tree = super().get_queryset()
        return self.tree.filter(field__pk=self.kwargs["pk"])


FieldWorkDetailTreesGeoJson = FieldWorkDetailTreesGeoJson.as_view()


class TreeCreateView(LoginRequiredMixin, CreateView):
    model = Tree
    form_class = TreeForm


TreeCreateView = TreeCreateView.as_view()


class TreeEditView(LoginRequiredMixin, UpdateView):
    model = Tree
    form_class = TreeForm


TreeEditView = TreeEditView.as_view()


class TreeListView(LoginRequiredMixin, ListView):
    model = Tree


TreeListView = TreeListView.as_view()


class TreeDetailView(LoginRequiredMixin, DetailView):
    model = Tree

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["measurement_list"] = TreeMeasurement.objects.filter(
            tree__pk=self.kwargs["pk"]
        )
        return context


TreeDetailView = TreeDetailView.as_view()


class TreeDetailGeoJson(GeoJSONLayerView):
    model = Tree
    properties = ("popup_content",)

    def get_queryset(self):
        self.tree = super().get_queryset()
        return self.tree.filter(pk=self.kwargs["pk"])


TreeDetailGeoJson = TreeDetailGeoJson.as_view()


class TreeMeasurementCreateView(LoginRequiredMixin, CreateView):
    model = TreeMeasurement
    form_class = TreeMeasurementForm


TreeMeasurementCreateView = TreeMeasurementCreateView.as_view()


class TreeMeasurementEditView(LoginRequiredMixin, UpdateView):
    model = TreeMeasurement
    form_class = TreeMeasurementForm


TreeMeasurementEditView = TreeMeasurementEditView.as_view()


class TreeMeasurementListView(LoginRequiredMixin, FilterView):
    model = TreeMeasurement
    queryset = TreeMeasurement.objects.all().order_by("-created_at")
    filterset_class = TreeMeasurementFilters
    template_name = "imibio_tree_ecological_data/treemeasurement_list.html"


TreeMeasurementListView = TreeMeasurementListView.as_view()


class TreeMeasurementDetailView(LoginRequiredMixin, DetailView):
    model = TreeMeasurement


TreeMeasurementDetailView = TreeMeasurementDetailView.as_view()


class TreesGeoJson(GeoJSONLayerView):
    model = Tree
    properties = ("popup_content",)


trees_geojson = TreesGeoJson.as_view()
