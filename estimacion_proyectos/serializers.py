from rest_framework import serializers
from .models import EstimacionProyecto


class EstimacionProyectoSerializer(serializers.ModelSerializer):
    reportado = serializers.ReadOnlyField(source="reportado.username")

    class Meta:
        model = EstimacionProyecto
        fields = "__all__"

    def validate_proyecto(self, value):
        if EstimacionProyecto.objects.filter(proyecto=value).exists():
            raise serializers.ValidationError(
                "Ya existe una estimación para este proyecto."
            )
        return value

    def create(self, validated_data):
        validated_data["reportado"] = self.context["request"].user
        return EstimacionProyecto.objects.create(**validated_data)
