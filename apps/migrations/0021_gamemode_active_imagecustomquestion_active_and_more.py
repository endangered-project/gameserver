# Generated by Django 5.0.1 on 2024-03-30 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0020_gamequestion_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamemode',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='imagecustomquestion',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='questionmodel',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='textcustomquestion',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
