# Generated by Django 3.2 on 2021-06-03 13:20

from django.db import migrations, models
import django.db.models.deletion
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ("bioblitz", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bioblitzproject",
            options={
                "verbose_name": "Proyecto de BioBlitz",
                "verbose_name_plural": "Proyecto de BioBlitz",
            },
        ),
        migrations.AlterField(
            model_name="bioblitzproject",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.CreateModel(
            name="BioblitzOccurrence",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("obs_id", models.IntegerField(verbose_name="ID de la observación")),
                (
                    "quality_grade",
                    models.CharField(max_length=50, verbose_name="Calidad de ranking"),
                ),
                (
                    "created_at",
                    models.DateTimeField(verbose_name="Fecha de la observación"),
                ),
                ("uri", models.URLField(verbose_name="URL de la observación")),
                (
                    "name",
                    models.CharField(
                        max_length=300,
                        null=True,
                        verbose_name="Nombre cientifico de la especie",
                    ),
                ),
                (
                    "rank",
                    models.CharField(
                        max_length=50, null=True, verbose_name="Ranking taxonomico"
                    ),
                ),
                (
                    "iconic_taxon_name",
                    models.CharField(
                        max_length=50, null=True, verbose_name="Ranking taxonomico"
                    ),
                ),
                (
                    "endemic",
                    models.BooleanField(
                        default=False, verbose_name="Especie endémica?"
                    ),
                ),
                (
                    "threatened",
                    models.BooleanField(
                        default=False, verbose_name="Especie amenazada?"
                    ),
                ),
                (
                    "introduced",
                    models.BooleanField(
                        default=False, verbose_name="Especie introducida?"
                    ),
                ),
                (
                    "native",
                    models.BooleanField(default=False, verbose_name="Especie nativa?"),
                ),
                ("geom", djgeojson.fields.PointField(null=True)),
                ("user_id", models.IntegerField(verbose_name="ID del observador")),
                (
                    "user_login",
                    models.CharField(
                        max_length=50, verbose_name="Login del observador"
                    ),
                ),
                (
                    "user_name",
                    models.CharField(
                        max_length=100, null=True, verbose_name="Nombre del observador"
                    ),
                ),
                (
                    "project_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bioblitz.bioblitzproject",
                    ),
                ),
            ],
            options={
                "verbose_name": "Especie observada",
                "verbose_name_plural": "Especies observadas",
            },
        ),
    ]
