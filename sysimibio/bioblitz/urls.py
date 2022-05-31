from django.urls import path

from sysimibio.bioblitz.views import (
    register_bioblitz_project,
    register_bioblitz_occurrences,
    list_bioblitz_occurrences,
    list_bioblitz_projects,
    bioblitz_occurrence_detail,
    project_detail,
    project_stats,
    proj_occs_geojson,
    bioblitz_events_stats,
    bioblitz_events_geojson,
    observation_detail_geojson,
)

app_name = "bioblitz"


urlpatterns = [
    path("", register_bioblitz_project, name="register_bioblitz_project"),
    path("project_list", list_bioblitz_projects, name="list_bioblitz_projects"),
    path("bioblitz_events_stats", bioblitz_events_stats, name="bioblitz_events_stats"),
    path("project_detail/<int:pk>/", project_detail, name="project_detail"),
    path(
        "get_occurrences/<int:project_id>/",
        register_bioblitz_occurrences,
        name="get_occurrences",
    ),
    path(
        "get_project_occurrence_geojson/<int:pk>/",
        proj_occs_geojson,
        name="project_occurrence_geojson",
    ),
    path(
        "bioblitz_events_occurrences_geojson/",
        bioblitz_events_geojson,
        name="bioblitz_events_geojson",
    ),
    path(
        "bioblitz_occurrence_detail_geojson/<int:pk>/",
        observation_detail_geojson,
        name="bioblitz_occurrence_geojson",
    ),
    path(
        "list_occurrences/<int:pk>/", list_bioblitz_occurrences, name="list_occurrences"
    ),
    path(
        "occurrence_detail/<int:pk>/",
        bioblitz_occurrence_detail,
        name="occurrence_detail",
    ),
    path("project_stats/<int:pk>/", project_stats, name="project_stats"),
]
