from django.db import models
import uuid
from users.models import CustomUser


class Proyecto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=255, unique=True)
    AREA_CHOICES = [
        ("Axces", "Axces"),
        ("Transversal", "Transversal"),
        ("Gestion del Riesgo", "Gestion del Riesgo"),
        ("Mercadeo", "Mercadeo"),
    ]
    area = models.CharField(max_length=50, choices=AREA_CHOICES)
    TIPO_CHOICES = [
        ("Fore", "Fore"),
        ("Reca", "Reca"),
    ]
    tipo = models.CharField(max_length=4, choices=TIPO_CHOICES)
    enlace_tw = models.URLField(max_length=200)
    desarrollador = models.CharField(max_length=255)
    funcional = models.CharField(max_length=255)
    fecha_entrega_qa = models.DateField()
    fecha_estimada_liberacion = models.DateField()
    fecha_creacion = models.DateField(auto_now_add=True)
    ACTIVIDAD_CHOICES = [
        ("Planeacion", "Planeacion"),
        ("Estimacion", "Estimacion"),
        ("Diseño", "Diseño"),
        ("Ejecucion", "Ejecucion"),
        ("Pendiente", "Pendiente"),
        ("Finalizado", "Finalizado"),
    ]
    actividad = models.CharField(max_length=50, choices=ACTIVIDAD_CHOICES)
    reportado = models.ForeignKey(
        CustomUser, related_name="proyectos_reportados", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.project_name
