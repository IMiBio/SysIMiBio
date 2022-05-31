from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
from djgeojson.views import GeoJSONLayerView
from pyinaturalist.node_api import get_projects, get_observations

# Create your views here.
from sysimibio.bioblitz.forms import BioblitzModelForm
from sysimibio.bioblitz.models import BioblitzProject, BioblitzOccurrence


@login_required
def register_bioblitz_project(request):
    if request.method == "POST":
        form = BioblitzModelForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Formulário con error: revise todos los campos")
            return render(
                request, "bioblitz/project_registration_form.html", {"form": form}
            )

        elif form.cleaned_data.get("project_slug") in [
            val["project_slug"]
            for val in list(BioblitzProject.objects.all().values("project_slug"))
        ]:
            messages.error(request, "Proyecto ya cargado al sistema")
            return render(
                request, "bioblitz/project_registration_form.html", {"form": form}
            )

        else:
            bioblitz_project_data = get_projects(
                q=form.cleaned_data.get("project_slug"), member_id=1626810
            )
            if bioblitz_project_data.get("total_results") == 0:
                messages.error(
                    request, "Proyecto no encontrado. confirmar nombre del proyecto"
                )
                return render(
                    request, "bioblitz/project_registration_form.html", {"form": form}
                )

            project = BioblitzProject.objects.create(
                iconURL=bioblitz_project_data.get("results")[0].get("icon"),
                description=bioblitz_project_data.get("results")[0].get("description"),
                created_at=bioblitz_project_data.get("results")[0].get("created_at"),
                title=bioblitz_project_data.get("results")[0].get("title"),
                project_id=bioblitz_project_data.get("results")[0].get("id"),
                project_slug=bioblitz_project_data.get("results")[0].get("slug"),
                place_id=bioblitz_project_data.get("results")[0].get("place_id"),
                project_type=bioblitz_project_data.get("results")[0].get(
                    "project_type"
                ),
                manager_id=bioblitz_project_data.get("results")[0]
                .get("admins")[0]
                .get("user")
                .get("id"),
                manager_login=bioblitz_project_data.get("results")[0]
                .get("admins")[0]
                .get("user")
                .get("login"),
                manager_name=bioblitz_project_data.get("results")[0]
                .get("admins")[0]
                .get("user")
                .get("name"),
            )
            messages.success(request, "Proyecto registrado con exito")

            return HttpResponseRedirect(r("bioblitz:project_detail", project.pk))

    return render(
        request,
        "bioblitz/project_registration_form.html",
        {"form": BioblitzModelForm()},
    )


@login_required
def list_bioblitz_projects(request):
    ptojects = BioblitzProject.objects.all()
    return render(request, "bioblitz/projects_list.html", {"projects": ptojects})


@login_required
def project_detail(request, pk):
    try:
        project = BioblitzProject.objects.get(pk=pk)
        project_occurrences = BioblitzOccurrence.objects.filter(project_id__pk=pk)
        if not project_occurrences:
            messages.info(request, "Proyecto sin occurrencias")
        context = {"project": project, "occurences": project_occurrences}
    except BioblitzProject.DoesNotExist:
        raise Http404

    return render(request, "bioblitz/project_detail.html", context)


@login_required
def register_bioblitz_occurrences(request, project_id):
    try:
        project = BioblitzProject.objects.get(project_id=project_id)
        observations = get_observations(
            project_id=project_id, page="all"
        )  # todo consider user_agent https://pyinaturalist.readthedocs.io/en/v0.13.0/general_usage.html#user-agent
        total_obs = len(observations.get("results"))
        for obs in observations.get(
            "results"
        ):  # todo get a better way to map dict variables
            # print(obs.get("id"))
            project_id = project
            obs_id = obs.get("id")
            quality_grade = obs.get("quality_grade")
            created_at = obs.get("created_at")
            uri = obs.get("uri")
            geom = obs.get("geojson", "")
            # taxon
            if obs.get("taxon"):
                name = obs.get("taxon").get("name")
                rank = obs.get("taxon").get("rank")
                iconic_taxon_name = obs.get("taxon").get("iconic_taxon_name", "")
                endemic = obs.get("taxon").get("endemic")
                threatened = obs.get("taxon").get("threatened")
                introduced = obs.get("taxon").get("introduced")
                native = obs.get("taxon").get("native")
            else:
                name = ""
                rank = ""
                iconic_taxon_name = ""
                endemic = False
                threatened = False
                introduced = False
                native = False

            # user
            user_login = obs.get("user").get("login")
            user_name = obs.get("user").get("name")
            user_id = obs.get("user").get("id")

            BioblitzOccurrence.objects.create(
                project_id=project_id,
                obs_id=obs_id,
                quality_grade=quality_grade,
                created_at=created_at,
                uri=uri,
                taxon_name=name,
                taxon_rank=rank,
                iconic_taxon_name=iconic_taxon_name,
                endemic=endemic,
                threatened=threatened,
                introduced=introduced,
                native=native,
                geom=geom,
                user_id=user_id,
                user_name=user_name,
                user_login=user_login,
            )

        messages.success(request, f"{total_obs} observaciones cargadas con exito")
        return HttpResponseRedirect(r("bioblitz:list_occurrences", project.pk))

    except BioblitzProject.DoesNotExist:
        raise Http404


@login_required
def list_bioblitz_occurrences(request, pk):
    observations = BioblitzOccurrence.objects.filter(project_id__pk=pk)
    context = {"observations": observations, "project_pk": pk}
    return render(request, "bioblitz/occurrences_list.html", context)


@login_required
def bioblitz_occurrence_detail(request, pk):
    try:
        observation = BioblitzOccurrence.objects.get(pk=pk)
    except BioblitzProject.DoesNotExist:
        raise Http404
    return render(
        request, "bioblitz/occurrence_detail.html", {"observation": observation}
    )


@login_required
def project_stats(request, pk):
    # Observations
    labelsObsQGrade = []
    dataObsQGrade = []
    labelsObsRank = []
    dataObsRank = []
    labelsObsITName = []
    dataObsITName = []
    labelsObsUser = []
    dataObsUser = []

    # Species
    labelsSppQGrade = []
    dataSppQGrade = []
    labelsSppRank = []
    dataSppRank = []
    labelsSppITName = []
    dataSppITName = []
    labelsSppUser = []
    dataSppUser = []

    # return object
    data = dict()
    labels = dict()

    # Observation
    # quality grade
    querysetGrade = (
        BioblitzOccurrence.objects.filter(project_id__pk=pk)
        .values("quality_grade")
        .annotate(Count("obs_id"))
        .order_by("-obs_id__count")[:10]
    )
    for QGrade in querysetGrade:
        labelsObsQGrade.append(QGrade.get("quality_grade"))
        dataObsQGrade.append(QGrade.get("obs_id__count"))

    data["ObsQGrade"] = dataObsQGrade
    labels["ObsQGrade"] = labelsObsQGrade

    # Rank
    querysetRank = (
        BioblitzOccurrence.objects.filter(project_id__pk=pk)
        .values("taxon_rank")
        .annotate(Count("obs_id"))
        .order_by("-obs_id__count")[:10]
    )
    for rank in querysetRank:
        labelsObsRank.append(rank.get("taxon_rank"))
        dataObsRank.append(rank.get("obs_id__count"))

    data["ObsRank"] = dataObsRank
    labels["ObsRank"] = labelsObsRank

    # ITName
    querysetITName = (
        BioblitzOccurrence.objects.filter(project_id__pk=pk)
        .values("iconic_taxon_name")
        .annotate(Count("obs_id"))
        .order_by("-obs_id__count")[:10]
    )
    for ITName in querysetITName:
        labelsObsITName.append(ITName.get("iconic_taxon_name"))
        dataObsITName.append(ITName.get("obs_id__count"))

    data["ObsITName"] = dataObsITName
    labels["ObsITName"] = labelsObsITName

    # User_id
    querysetUser = (
        BioblitzOccurrence.objects.filter(project_id__pk=pk)
        .values("user_login")
        .annotate(Count("obs_id"))
        .order_by("-obs_id__count")[:10]
    )
    for user in querysetUser:
        labelsObsUser.append(user.get("user_login"))
        dataObsUser.append(user.get("obs_id__count"))

    data["ObsUser"] = dataObsUser
    labels["ObsUser"] = labelsObsUser

    # species
    # quality grade
    querysetGradeSpp = (
        BioblitzOccurrence.objects.filter(project_id__pk=pk)
        .values("quality_grade")
        .annotate(Count("taxon_name", distinct=True))
        .order_by("-taxon_name__count")[:10]
    )
    for QGradeSpp in querysetGradeSpp:
        labelsSppQGrade.append(QGradeSpp.get("quality_grade"))
        dataSppQGrade.append(QGradeSpp.get("taxon_name__count"))

    data["SppQGrade"] = dataSppQGrade
    labels["SppQGrade"] = labelsSppQGrade

    # Rank
    querysetRankSpp = (
        BioblitzOccurrence.objects.filter(project_id__pk=pk)
        .values("taxon_rank")
        .annotate(Count("taxon_name", distinct=True))
        .order_by("-taxon_name__count")[:10]
    )
    for rankSpp in querysetRankSpp:
        labelsSppRank.append(rankSpp.get("taxon_rank"))
        dataSppRank.append(rankSpp.get("taxon_name__count"))

    data["SppRank"] = dataSppRank
    labels["SppRank"] = labelsSppRank

    # ITName
    querysetITNameSpp = (
        BioblitzOccurrence.objects.filter(project_id__pk=pk)
        .values("iconic_taxon_name")
        .annotate(Count("taxon_name", distinct=True))
        .order_by("-taxon_name__count")[:9]
    )
    for ITNameSpp in querysetITNameSpp:
        labelsSppITName.append(ITNameSpp.get("iconic_taxon_name"))
        dataSppITName.append(ITNameSpp.get("taxon_name__count"))

    data["SppITName"] = dataSppITName
    labels["SppITName"] = labelsSppITName

    # User_id
    querysetUserSpp = (
        BioblitzOccurrence.objects.filter(project_id__pk=pk)
        .values("user_login")
        .annotate(Count("taxon_name", distinct=True))
        .order_by("-taxon_name__count")[:10]
    )
    for userSpp in querysetUserSpp:
        labelsSppUser.append(userSpp.get("user_login"))
        dataSppUser.append(userSpp.get("taxon_name__count"))

    data["SppUser"] = dataSppUser
    labels["SppUser"] = labelsSppUser

    project_slug = BioblitzOccurrence.objects.filter(project_id__pk=pk)[
        0
    ].project_id.project_slug
    project_id = BioblitzOccurrence.objects.filter(project_id__pk=pk)[
        0
    ].project_id.project_id
    return render(
        request,
        "bioblitz/project_stats.html",
        {
            "labels": labels,
            "data": data,
            "project_pk": pk,
            "project_name": project_slug,
            "project_id": project_id,
        },
    )


@login_required
def bioblitz_events_stats(request):
    # Observations
    labelsObsAmount = []
    dataObsAmount = []

    # Species
    labelsSppAmount = []
    dataSppAmount = []

    # return object
    data = dict()
    labels = dict()

    # Observation
    querysetObsAmount = (
        BioblitzOccurrence.objects.values("project_id__title")
        .annotate(Count("obs_id"))
        .order_by("-obs_id__count")[:10]
    )
    for proj in querysetObsAmount:
        labelsObsAmount.append(proj.get("project_id__title"))
        dataObsAmount.append(proj.get("obs_id__count"))

    data["ObsAmount"] = dataObsAmount
    labels["ObsAmount"] = labelsObsAmount

    # species
    querysetSppAmount = (
        BioblitzOccurrence.objects.values("project_id__title")
        .annotate(Count("taxon_name", distinct=True))
        .order_by("-taxon_name__count")[:10]
    )
    for proj in querysetSppAmount:
        labelsSppAmount.append(proj.get("project_id__title"))
        dataSppAmount.append(proj.get("taxon_name__count"))

    data["SppAmount"] = dataSppAmount
    labels["SppAmount"] = labelsSppAmount

    return render(
        request, "bioblitz/bioblitz_events_stats.html", {"labels": labels, "data": data}
    )


class BioblitzEventsObservationsGeoJSON(GeoJSONLayerView):
    model = BioblitzOccurrence
    properties = ("popup_content",)

    def get_queryset(self):
        context = BioblitzOccurrence.objects.all()
        return context


class BioblitzProjectObservationsGeoJSON(GeoJSONLayerView):
    model = BioblitzOccurrence
    properties = ("popup_content",)

    def get_queryset(self, **kwargs):
        self.obs = super().get_queryset()
        return self.obs.filter(project_id=self.kwargs["pk"])


class BioblitzObservationGeoJSON(GeoJSONLayerView):
    model = BioblitzOccurrence
    properties = ("popup_content",)

    def get_queryset(self, **kwargs):
        self.obs = super().get_queryset()
        return self.obs.filter(pk=self.kwargs["pk"])


bioblitz_events_geojson = BioblitzEventsObservationsGeoJSON.as_view()
proj_occs_geojson = BioblitzProjectObservationsGeoJSON.as_view()
observation_detail_geojson = BioblitzObservationGeoJSON.as_view()
