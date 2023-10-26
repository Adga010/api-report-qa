from rest_framework import serializers
from .models import BugReport

class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = "__all__"

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
