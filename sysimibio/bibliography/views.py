from crossref.restful import Works
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, resolve_url as r
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django_filters.views import FilterView
from djgeojson.views import GeoJSONLayerView
from isbnlib import is_isbn13, meta
from sysimibio.bibliography.filters import (
    PublicationFilters,
    SpeciesListFilters,
    OccurrenceListFilters,
)
from sysimibio.bibliography.forms import (
    PublicationForm,
    UploadSpeciesListForm,
    UploadOccurrencesListForm,
)
from sysimibio.bibliography.models import Publication, SpeciesList, OccurrenceList


class PublicationUpdateClass(LoginRequiredMixin, UpdateView):
    model = Publication
    form_class = PublicationForm

    def get_success_url(self):
        objectid = self.kwargs["pk"]
        return r("bibliography:publication_detail", objectid)


PublicationUpdateView = PublicationUpdateClass.as_view()


class PublicationListClass(LoginRequiredMixin, FilterView):
    paginate_by = 15
    queryset = Publication.objects.all().order_by("-publication_year")
    filterset_class = PublicationFilters
    template_name = "bibliography/publication_list.html"


PublicationList = PublicationListClass.as_view()


class PublicationDetailClass(LoginRequiredMixin, DetailView):
    model = Publication

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the
        context["species_list"] = SpeciesList.objects.filter(
            publication=self.kwargs["pk"]
        )
        context["occurrence_list"] = OccurrenceList.objects.filter(
            publication=self.kwargs["pk"]
        )
        return context


PublicationDetail = PublicationDetailClass.as_view()


class PublicationCreateClass(LoginRequiredMixin, CreateView):
    model = Publication
    form_class = PublicationForm

    def form_valid(self, form):
        self.publication = form.save(commit=False)
        self.publication.created_by = self.request.user
        works = Works()
        if self.publication.DOI != "" and works.doi_exists(self.publication.DOI):
            paper_data_result = works.doi(self.publication.DOI)
            self.publication.publication_year = str(
                paper_data_result.get("created").get("date-parts")[0][0]
            )
            self.publication.title = paper_data_result.get("title")[0]
            self.publication.author = f"{paper_data_result.get('author')[0].get('given')},{paper_data_result.get('author')[0].get('family')}"
            sub = paper_data_result.get("subject", [self.publication.subject])
            self.publication.subject = ", ".join([str(elem) for elem in sub])
            self.publication.URL = paper_data_result.get("URL")

        elif self.publication.ISBN != "" and is_isbn13(self.publication.ISBN):
            book_data_result = meta(self.publication.ISBN)
            self.publication.publication_year = book_data_result.get("Year")
            self.publication.title = book_data_result.get("Title")
            self.publication.author = book_data_result.get("Authors")[0]

        elif self.publication.crossref and (
            self.publication.DOI or self.publication.ISBN
        ):
            messages.error(
                self.request,
                'DOI/ISBN no encontrado. Cargar datos y desmarcar el campo "tiene DOI/ISBN"',
            )
            return render(
                self.request, "bibliography/publication_form.html", {"form": form}
            )
        self.publication.save()
        messages.success(self.request, "Registro realizado con exito")

        return redirect("bibliography:publication_detail", pk=self.publication.pk)


PublicationCreateView = PublicationCreateClass.as_view()


def handle_uploaded_species_list_file(file, publication_pk):
    import pandas as pd

    df = pd.read_csv(file)
    assert (
        "scientific_name" in df.columns
    ), "Archivo .CSV Inválido.Debe tener scientific_name como primera columna"
    columns_sequence = [number for number in range(1, len(df.columns))]
    result = pd.DataFrame()
    result["scientific_name"] = df.scientific_name
    result["publication"] = Publication.objects.get(pk=publication_pk)
    result = result.join(
        pd.DataFrame(
            {"other_fields_json": df.iloc[:, columns_sequence].to_dict("records")}
        )
    )
    return result


def handle_uploaded_ocurrences_list_file(file, publication_pk):
    import pandas as pd

    df = pd.read_csv(file)
    assert (
        "scientific_name" in df.columns
    ), "Archivo .csv Inválido.Falta columna scientific_name"
    assert "latitude" in df.columns, "Archivo .csv Inválido.Falta columna latitude"
    assert "longitude" in df.columns, "Archivo .csv Inválido.Falta columna longitude"
    columns_sequence = [number for number in range(3, len(df.columns))]
    result = pd.DataFrame()
    result["scientific_name"] = df.scientific_name
    result["latitude"] = df.latitude
    result["longitude"] = df.longitude
    result["publication"] = Publication.objects.get(pk=publication_pk)
    result = result.join(
        pd.DataFrame(
            {"other_fields_json": df.iloc[:, columns_sequence].to_dict("records")}
        )
    )
    return result


class SpeciesListCreateClass(LoginRequiredMixin, CreateView):
    model = Publication
    form_class = UploadSpeciesListForm

    def post(self, request, *args, **kwargs):
        form = UploadSpeciesListForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = (request.FILES["species_list_spreadsheet"],)
            publication_pk = request.POST["publication"]
            try:

                df = handle_uploaded_species_list_file(
                    file=uploaded_file[0], publication_pk=publication_pk
                )
                SpeciesList.objects.bulk_create(
                    SpeciesList(**vals) for vals in df.to_dict("records")
                )
            except AssertionError as e:
                messages.error(self.request, e)
                return render(
                    request, "bibliography/specieslist_form.html", {"form": form}
                )
            return HttpResponseRedirect(
                r("bibliography:publication_detail", publication_pk)
            )
        else:
            return render(request, "bibliography/specieslist_form.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = UploadSpeciesListForm()
        pk = self.kwargs.get(self.pk_url_kwarg)
        form.fields["publication"].queryset = Publication.objects.filter(pk=pk)
        return render(request, "bibliography/specieslist_form.html", {"form": form})


SpeciesListCreateView = SpeciesListCreateClass.as_view()


class SpeciesListUpdateClass(LoginRequiredMixin, UpdateView):
    model = Publication
    form_class = UploadSpeciesListForm

    def post(self, request, *args, **kwargs):
        form = UploadSpeciesListForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = (request.FILES["species_list_spreadsheet"],)
            publication_pk = request.POST["publication"]
            species_to_update = SpeciesList.objects.filter(publication=publication_pk)
            try:
                df = handle_uploaded_species_list_file(
                    file=uploaded_file[0], publication_pk=publication_pk
                )
                dict_list = [row for row in df.to_dict("records")]
                for index, obj in enumerate(list(species_to_update)):
                    dato = dict_list[index]
                    for key, value in dato.items():
                        setattr(obj, key, value)
                SpeciesList.objects.bulk_update(
                    species_to_update, ["scientific_name", "other_fields_json"]
                )
            except AssertionError as e:
                messages.error(self.request, e)
                return render(
                    request, "bibliography/specieslist_form.html", {"form": form}
                )
            return HttpResponseRedirect(
                r("bibliography:publication_detail", publication_pk)
            )
        else:
            return render(request, "bibliography/specieslist_form.html", {"form": form})

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        form = UploadSpeciesListForm()
        form.fields["publication"].queryset = Publication.objects.filter(pk=pk)
        return render(request, "bibliography/specieslist_form.html", {"form": form})


SpeciesListUpdateView = SpeciesListUpdateClass.as_view()


class OccurrenceListCreateClass(LoginRequiredMixin, CreateView):
    model = Publication
    form_class = UploadOccurrencesListForm

    def post(self, request, *args, **kwargs):
        form = UploadOccurrencesListForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = (request.FILES["occurrences_list_spreadsheet"],)
            publication_pk = request.POST["publication"]
            try:
                df = handle_uploaded_ocurrences_list_file(
                    file=uploaded_file[0], publication_pk=publication_pk
                )
                OccurrenceList.objects.bulk_create(
                    OccurrenceList(**vals) for vals in df.to_dict("records")
                )
            except AssertionError as e:
                messages.error(self.request, e)
                return render(
                    request, "bibliography/occurrenceslist_form.html", {"form": form}
                )
            return HttpResponseRedirect(
                r("bibliography:publication_detail", publication_pk)
            )
        else:
            return render(
                request, "bibliography/occurrenceslist_form.html", {"form": form}
            )

    def get(self, request, *args, **kwargs):
        form = UploadOccurrencesListForm()
        pk = self.kwargs.get(self.pk_url_kwarg)
        form.fields["publication"].queryset = Publication.objects.filter(pk=pk)
        return render(request, "bibliography/occurrenceslist_form.html", {"form": form})


OccurrenceListCreateView = OccurrenceListCreateClass.as_view()


class OccurrenceListUpdateClass(LoginRequiredMixin, UpdateView):
    model = Publication
    form_class = UploadOccurrencesListForm

    def post(self, request, *args, **kwargs):
        form = UploadOccurrencesListForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = (request.FILES["occurrences_list_spreadsheet"],)
            publication_pk = request.POST["publication"]
            occurrences_to_update = OccurrenceList.objects.filter(
                publication=publication_pk
            )
            try:
                df = handle_uploaded_ocurrences_list_file(
                    file=uploaded_file[0], publication_pk=publication_pk
                )
                dict_list = [row for row in df.to_dict("records")]
                for index, obj in enumerate(list(occurrences_to_update)):
                    dato = dict_list[index]
                    for key, value in dato.items():
                        setattr(obj, key, value)
                OccurrenceList.objects.bulk_update(
                    occurrences_to_update,
                    ["scientific_name", "latitude", "longitude", "other_fields_json"],
                )
            except AssertionError as e:
                messages.error(self.request, e)
                return render(
                    request, "bibliography/occurrenceslist_form.html", {"form": form}
                )
            return HttpResponseRedirect(
                r("bibliography:publication_detail", publication_pk)
            )
        else:
            return render(
                request, "bibliography/occurrenceslist_form.html", {"form": form}
            )

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        form = UploadOccurrencesListForm()
        form.fields["publication"].queryset = Publication.objects.filter(pk=pk)
        return render(request, "bibliography/occurrenceslist_form.html", {"form": form})


OccurrenceListUpdateView = OccurrenceListUpdateClass.as_view()


class PublicationOccurrenceListGeoJsonClass(LoginRequiredMixin, GeoJSONLayerView):
    model = OccurrenceList
    properties = ("popup_content",)

    def get_queryset(self, **kwargs):
        self.obs = super().get_queryset()
        return self.obs.filter(publication=self.kwargs["pk"])


PublicationOccurrenceListGeoJsonView = PublicationOccurrenceListGeoJsonClass.as_view()


class AllPublicationOccurrenceListGeoJsonClass(LoginRequiredMixin, GeoJSONLayerView):
    model = OccurrenceList
    properties = ("popup_content",)


AllPublicationOccurrenceListGeoJsonView = (
    AllPublicationOccurrenceListGeoJsonClass.as_view()
)


class map_all_publication_occurrences(LoginRequiredMixin, ListView):
    model = Publication
    template_name = "bibliography/occurrencelist_map.html"


AllPublicationOccurrencesMap = map_all_publication_occurrences.as_view()


class list_all_publication_occurrenceslist(LoginRequiredMixin, FilterView):
    paginate_by = 15
    template_name = "bibliography/occurrencelist_list.html"
    filterset_class = OccurrenceListFilters
    ordering = ["-publication__created_at"]


ListAllPublicationOccurrences = list_all_publication_occurrenceslist.as_view()


class list_all_publication_specieslist(LoginRequiredMixin, FilterView):
    paginate_by = 15
    ordering = ["-publication__created_at"]
    template_name = "bibliography/specieslist_list.html"
    filterset_class = SpeciesListFilters


ListAllPublicationSpecies = list_all_publication_specieslist.as_view()
