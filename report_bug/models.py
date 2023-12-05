from rest_framework import serializers
from django.db import models
import uuid
from users.models import CustomUser
from proyectos.models import Proyecto  # Asegúrate de importar tu modelo Proyecto


class BugReport(models.Model):
    # uuid_temp = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FECHA = models.DateField()
    STATUS_CHOICES = [("Pendiente", "Pendiente"), ("Finalizado", "Finalizado")]
    STATUS = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pendiente"
    )
    # PROJECT_NAME = models.CharField(max_length=255)
    PROJECT_NAME = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    BUG = models.TextField()
    CAUSAL_CHOICES = [
        ("Desarrollo", "Desarrollo"),
        ("Analisis", "Analisis"),
        ("Documentacion", "Documentacion"),
        ("Testing", "Testing"),
        ("Diseño", "Diseño"),
    ]
    AREA_CHOICES = [
        ("Axces", "Axces"),
        ("Transversal", "Transversal"),
        ("Gestion del Riesgo", "Gestion del Riesgo"),
        ("Mercadeo", "Mercadeo"),
    ]
    AREA = models.CharField(max_length=20, choices=AREA_CHOICES)
    CAUSAL = models.CharField(max_length=20, choices=CAUSAL_CHOICES)
    SEVERIDAD_CHOICES = [
        ("Funcional", "Funcional"),
        ("Presentacion", "Presentacion"),
        ("Bloqueante", "Bloqueante"),
    ]
    SEVERIDAD = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES)
    ENLACE = models.URLField()
    ENCARGADO = models.CharField(max_length=255)
    REPORTADO = models.ForeignKey(
        CustomUser, related_name="reportado", on_delete=models.CASCADE
    )


def __str__(self):
    return f"Report {self.id}: {self.PROJECT_NAME}"
