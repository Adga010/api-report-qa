from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Proyecto

User = get_user_model()


class ProyectoSerializer(serializers.ModelSerializer):
    reportado = serializers.ReadOnlyField(source="reportado.username")

    class Meta:
        model = Proyecto
        fields = "__all__"

    def validate_project_name(self, value):
        if Proyecto.objects.filter(project_name__iexact=value).exists():
            raise serializers.ValidationError("Un proyecto con este nombre ya existe.")
        return value

    def validate_fecha_entrega_qa(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "La fecha de entrega para QA no puede ser menor al dia calendario."
            )
        return value

    def validate_fecha_estimada_liberacion(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "La fecha estimada de liberación no puede ser menor al dia calendario."
            )
        return value

    def validate(self, attrs):
        if "fecha_entrega_qa" in attrs and "fecha_estimada_liberacion" in attrs:
            if attrs["fecha_estimada_liberacion"] < attrs["fecha_entrega_qa"]:
                raise serializers.ValidationError(
                    {
                        "fecha_estimada_liberacion": "La fecha estimada de liberación no puede ser menor a la fecha de entrega para QA."
                    }
                )
        return attrs