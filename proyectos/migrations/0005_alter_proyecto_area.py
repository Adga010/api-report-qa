# Generated by Django 4.2.6 on 2023-12-03 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0004_alter_proyecto_actividad_alter_proyecto_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='area',
            field=models.CharField(choices=[('Axces', 'Axces'), ('Transversal', 'Transversal'), ('Gestion del Riesgo', 'Gestion del Riesgo'), ('Mercadeo', 'Mercadeo')], max_length=50),
        ),
    ]