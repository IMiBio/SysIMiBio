# Generated by Django 3.1.7 on 2021-03-30 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imibio_tree_ecological_data", "0012_auto_20210329_1339"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pictures",
            options={
                "verbose_name": "Fotografía",
                "verbose_name_plural": "Fotografías",
            },
        ),
        migrations.RemoveField(
            model_name="tree",
            name="photo",
        ),
        migrations.RemoveField(
            model_name="tree",
            name="tree_status",
        ),
        migrations.AlterField(
            model_name="tree",
            name="obs",
            field=models.TextField(blank=True, verbose_name="Observaciones"),
        ),
        migrations.AlterField(
            model_name="tree",
            name="specie",
            field=models.CharField(max_length=100, verbose_name="Nombre especie"),
        ),
    ]
