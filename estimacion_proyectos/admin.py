from django.contrib import admin
from .models import EstimacionProyecto


class EstimacionProyectoAdmin(admin.ModelAdmin):
    list_display = (
        "proyecto",
        "est_diseno_cp",
        "est_eje_cp",
        "eje_diseno",
        "eje_cp",
        "fecha_estimacion",
        "reportado",
    )
    list_filter = ("proyecto", "fecha_estimacion", "reportado")
    search_fields = ("proyecto__nombre", "reportado__username")


admin.site.register(EstimacionProyecto, EstimacionProyectoAdmin)
