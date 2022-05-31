from datetime import date

from django.core.exceptions import ValidationError


def validate_date(value):
    if value > date.today():
        raise ValidationError(
            "Fecha debe estar en el formato AAAA-MM-DD y debe ser menor o igual a la fecha de hoy",
            "Date in the future",
        )


def validate_temperature(temp):
    if temp < -5 or temp > 55:
        raise ValidationError(
            "Temperatura debe estar en un rango desde -5 hasta 55° Celsius",
            "Temperature out of the range",
        )


def validate_humidity(humedad):
    if humedad < 0 or humedad > 100:
        raise ValidationError(
            "Humedad debe estar en un rango desde 0 hasta 100%",
            "Humidity out of the range",
        )


def validate_lat(lat):
    if lat < -28.17 or lat > -25.48:
        raise ValidationError(
            "Latitud no corresponde a Misiones", "Latitude out of the range"
        )


def validate_lon(lon):
    if lon < -56.06 or lon > -53.62:
        raise ValidationError(
            "Longitud no corresponde a Misiones", "Longitude out of the range"
        )


def tree_height_validation(tree_height):
    if tree_height < 1.3:
        raise ValidationError(
            "Altura del árbol no puede ser menor a 1.3 metros", "Tree height too small"
        )


def tree_dap_validation(tree_dap):
    if tree_dap <= 10:
        raise ValidationError(
            "DAP del árbol debe ser mayor a 10 cm", "Tree DAP too small"
        )


def validate_dist_x(dist_x_value):
    if 0 > dist_x_value or dist_x_value > 10:
        raise ValidationError(
            "La distancia no puede ser menos que cero ni mayor que diez"
        )


def validate_dist_y(dist_y_value):
    if 0 > dist_y_value or dist_y_value > 10:
        raise ValidationError(
            "La distancia no puede ser menos que cero ni mayor que diez"
        )
