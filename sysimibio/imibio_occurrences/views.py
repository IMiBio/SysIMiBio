from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
from sysimibio.imibio_occurrences.forms import OccurrencesRegistrationForm
from sysimibio.imibio_occurrences.models import ImibioOccurrence


def registration(request):
    if request.method == "POST":
        return create(request)
    else:
        return new(request)


def create(request):
    form = OccurrencesRegistrationForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Formulário con error: revise todos los campos")
        return render(
            request, "occurrences/occurrences_registration_form.html", {"form": form}
        )
    occ = ImibioOccurrence.objects.create(**form.cleaned_data)
    messages.success(request, "Registro realizado con exito")

    return HttpResponseRedirect(r("imibio_occurrences:detail", occ.pk))


def new(request):
    return render(
        request,
        "occurrences/occurrences_registration_form.html",
        {"form": OccurrencesRegistrationForm()},
    )


def detail(request, pk):
    try:
        occurrence = ImibioOccurrence.objects.get(pk=pk)
    except ImibioOccurrence.DoesNotExist:
        raise Http404

    return render(
        request, "occurrences/occurrence_detail.html", {"occurrence": occurrence}
    )
