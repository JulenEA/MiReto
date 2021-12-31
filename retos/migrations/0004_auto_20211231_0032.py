# Generated by Django 3.1.7 on 2021-12-30 23:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('retos', '0003_auto_20211229_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='progreso',
            name='fecha_dia',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='progreso',
            name='fecha_mes',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='progreso',
            name='fecha',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
