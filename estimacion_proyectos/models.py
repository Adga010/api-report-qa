from django.db import models
import uuid
from proyectos.models import Proyecto  # Asegúrate de importar tu modelo Proyecto
from django.conf import settings  # Para obtener el modelo de usuario
from users.models import CustomUser


class EstimacionProyecto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    est_diseno_cp = models.DecimalField(max_digits=5, decimal_places=2)
    est_eje_cp = models.DecimalField(max_digits=5, decimal_places=2)
    eje_diseno = models.DecimalField(max_digits=5, decimal_places=2)
    eje_cp = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_estimacion = models.DateTimeField(auto_now_add=True)
    reportado = models.ForeignKey(
        CustomUser,
        related_name="estimaciones_realizadas",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.proyecto.project_name} - Estimación"
