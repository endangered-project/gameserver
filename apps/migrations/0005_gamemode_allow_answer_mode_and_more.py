# Generated by Django 5.0.1 on 2024-02-07 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_remove_gamemode_answer_mode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamemode',
            name='allow_answer_mode',
            field=models.CharField(choices=[('single_right', 'Single (1 right answer, others are wrong)'), ('text', 'Text (User input text)')], default='single_right', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='questionmodel',
            name='answer_mode',
            field=models.CharField(choices=[('single_right', 'Single (1 right answer, others are wrong)'), ('text', 'Text (User input text)')], max_length=100),
        ),
    ]