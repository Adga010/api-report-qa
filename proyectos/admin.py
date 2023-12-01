from django.contrib import admin
from .models import Proyecto


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = (
        "project_name",
        "area",
        "tipo",
        "desarrollador",
        "funcional",
        "fecha_creacion",
        "actividad",
    )
    list_filter = ("area", "tipo", "actividad")
    search_fields = ("project_name", "desarrollador", "funcional")
