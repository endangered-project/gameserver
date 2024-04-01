# Generated by Django 5.0.1 on 2024-03-06 18:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_create_user_category_weight'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCustomQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('choices', models.TextField()),
                ('answer', models.TextField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.questioncategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TextCustomQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('choices', models.TextField()),
                ('answer', models.TextField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='apps.questioncategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
