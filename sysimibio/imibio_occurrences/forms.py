from django import forms


class OccurrencesRegistrationForm(forms.Form):
    # occurrenceID = forms.CharField(required=True) # not necessary. it is created on insertion
    basisOfRecord = forms.CharField(required=True, label="Tipo de muestra")
    institutionCode = forms.CharField(required=True, label="Código de la Institución")
    collectionCode = forms.CharField(required=True, label="Código de la colección")
    catalogNumber = forms.CharField(required=True, label="Número de catálogo")
    scientificName = forms.CharField(required=True, label="Nombre científico")
    kingdom = forms.CharField(required=True)
    phylum = forms.CharField(required=True)
    clase = forms.CharField(required=True)
    order = forms.CharField(required=True)
    family = forms.CharField(required=True)
    genus = forms.CharField(required=True)
    specificEpithet = forms.CharField(required=False)
    taxonRank = forms.CharField(required=False)
    infraspecificEpithet = forms.CharField(required=False)
    identificationQualifier = forms.CharField(required=False)
    county = forms.CharField(required=True, label="País")
    stateProvince = forms.CharField(required=True, label="Província")
    locality = forms.CharField(required=True, label="Localidad")
    recordedBy = forms.CharField(required=False, label="Colectado por")
    recordNumber = forms.CharField(required=False, label="Número de colecta")
    decimalLatitude = forms.FloatField(required=False, label="Latitud")
    decimalLongitude = forms.FloatField(required=False, label="Longitud")
