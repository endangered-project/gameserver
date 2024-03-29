# Generated by Django 5.0.1 on 2024-03-04 19:00

from django.db import migrations

from apps.utils import create_all_weighted


def create_all_question_weighted(apps, schema_editor):
    create_all_weighted()


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_usercategoryweight'),
    ]

    operations = [
        migrations.RunPython(create_all_question_weighted)
    ]
