import re
from users.models import CustomUser
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "rol",
            "cargo",
            "password",
            "password2",
        )
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "rol": {"required": True},
            "cargo": {"required": True},
        }

    def _validate_name_length(self, value, field_name):
        """Helper function to validate name lengths."""
        if len(value) < 5:
            raise serializers.ValidationError(
                f"El {field_name} debe tener al menos 5 caracteres."
            )
        elif len(value) > 30:
            raise serializers.ValidationError(
                f"El {field_name} no debe superar los 30 caracteres."
            )
        return value

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(is_staff=False, **validated_data)
        return user

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden."}
            )
        return data

    def validate_username(self, value):
        return self._validate_name_length(value, "username")

    def validate_first_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError(
                "El first_name es obligatorio y no puede estar vacío."
            )
        return self._validate_name_length(value, "first_name")

    def validate_last_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError(
                "El last_name es obligatorio y no puede estar vacío."
            )
        return self._validate_name_length(value, "last_name")

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya está registrado.")
        # Consider adding a regex validation for email format here
        return value

    def validate_password(self, value):
        """
        Valida que la contraseña cumpla con los requisitos de seguridad.
        """
        if len(value) < 8 or len(value) > 20:
            raise serializers.ValidationError(
                "La contraseña debe tener entre 8 y 20 caracteres."
            )

        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un número."
            )

        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra."
            )

        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra mayúscula."
            )

        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos una letra minúscula."
            )

        if not re.findall("[@#$%^&+=]", value):
            raise serializers.ValidationError(
                "La contraseña debe contener al menos un carácter especial (ej. @, #, $, etc.)."
            )

        return value
