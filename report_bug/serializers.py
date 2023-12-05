from rest_framework import serializers
from .models import BugReport, Proyecto


class BugReportSerializer(serializers.ModelSerializer):
    PROJECT_NAME = serializers.SlugRelatedField(
        slug_field="project_name", queryset=Proyecto.objects.all()
    )

    class Meta:
        model = BugReport
        fields = "__all__"


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
