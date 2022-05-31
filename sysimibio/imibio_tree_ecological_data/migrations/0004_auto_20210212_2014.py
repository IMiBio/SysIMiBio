# Generated by Django 3.1.3 on 2021-02-12 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imibio_tree_ecological_data", "0003_auto_20210212_1950"),
    ]

    operations = [
        migrations.AddField(
            model_name="treeecologicaldata",
            name="last_modification_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Ultima modificación"
            ),
        ),
        migrations.AlterField(
            model_name="treeecologicaldata",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Fecha creación"
            ),
        ),
    ]
