# Generated by Django 5.0.1 on 2024-03-15 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0017_alter_questionhistory_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamequestion',
            name='selected',
            field=models.TextField(blank=True, null=True),
        ),
    ]
