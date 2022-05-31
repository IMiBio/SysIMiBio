from django.urls import path

from sysimibio.imibio_occurrences.views import registration, detail

app_name = "imibio_occurrences"

urlpatterns = [
    path("", registration, name="new"),
    path("<int:pk>/", detail, name="detail"),
]
