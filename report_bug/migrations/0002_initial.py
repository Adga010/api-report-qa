# Generated by Django 4.2.6 on 2023-10-24 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('report_bug', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bugreport',
            name='REPORTADO',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportado', to=settings.AUTH_USER_MODEL),
        ),
    ]
