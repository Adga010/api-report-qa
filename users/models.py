from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    ROL_CHOICES = (
        ('admin', 'Administrador'),
        ('user', 'Usuario'),
        # ... otros roles ...
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='user')
    cargo = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # uuid_temp = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
