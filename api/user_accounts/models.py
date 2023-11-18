from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class KAMIUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = (
            "-updated_at",
            "-created_at",
        )

    def __str__(self):
        return self.first_name + " " + self.last_name
