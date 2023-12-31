# Generated by Django 4.2.6 on 2023-12-01 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0003_remove_proyecto_project_name_proyecto_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='actividad',
            field=models.CharField(choices=[('Planeacion', 'Planeacion'), ('Estimacion', 'Estimacion'), ('Diseño', 'Diseño'), ('Ejecucion', 'Ejecucion'), ('Pendiente', 'Pendiente'), ('Finalizado', 'Finalizado')], max_length=50),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='project_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
