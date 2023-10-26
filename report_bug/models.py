from django.db import models
import uuid
from users.models import CustomUser


class BugReport(models.Model):
    # uuid_temp = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FECHA = models.DateField()
    STATUS_CHOICES = [("pendiente", "Pendiente"), ("finalizado", "Finalizado")]
    STATUS = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pendiente"
    )
    PROJECT_NAME = models.CharField(max_length=255)
    BUG = models.TextField()
    CAUSAL_CHOICES = [
        ("desarrollo", "Desarrollo"),
        ("analisis", "Analisis"),
        ("documentacion", "Documentacion"),
        ("testing", "Testing"),
        ("diseño", "Diseño"),
    ]
    AREA_CHOICES = [
        ("axces", "AXCES"),
        ("gestion del riesgo", "Gestion Del Riesgo"),
        ("mercadeo", "Mercadeo"),
        ("transversal", "Transversal"),
    ]
    AREA = models.CharField(max_length=20, choices=AREA_CHOICES)
    CAUSAL = models.CharField(max_length=20, choices=CAUSAL_CHOICES)
    SEVERIDAD_CHOICES = [
        ("funcional", "Funcional"),
        ("presentacion", "Presentacion"),
        ("bloqueante", "Bloqueante"),
    ]
    SEVERIDAD = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES)
    ENLACE = models.URLField()
    ENCARGADO = models.CharField(max_length=255)
    REPORTADO = models.ForeignKey(
        CustomUser, related_name="reportado", on_delete=models.CASCADE
    )


def __str__(self):
    return f"Report {self.id}: {self.PROJECT_NAME}"
