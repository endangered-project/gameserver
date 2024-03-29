# Generated by Django 5.0.1 on 2024-03-11 02:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0014_imagecustomquestion_difficulty_level_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('score', models.IntegerField(default=0)),
                ('weight', models.JSONField(default=dict)),
                ('finished', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_true', models.BooleanField(default=False)),
                ('answered', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.game')),
                ('game_mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.gamemode')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.questionmodel')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_mode', models.CharField(max_length=100)),
                ('difficulty_level', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], max_length=100)),
                ('choice', models.TextField(blank=True, null=True)),
                ('answer', models.TextField(blank=True, null=True)),
                ('type', models.CharField(max_length=100)),
                ('full_json', models.JSONField(default=dict)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.questioncategory')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.questionmodel')),
            ],
        ),
    ]
