# Generated by Django 5.0.1 on 2024-02-07 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_gamemode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamemode',
            name='answer_mode',
        ),
        migrations.AddField(
            model_name='questionmodel',
            name='answer_mode',
            field=models.CharField(default='single_right', max_length=100),
            preserve_default=False,
        ),
    ]
