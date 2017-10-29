from django.db import models
from django.contrib.auth.models import AbstractUser

TIPO_PERSONA_CHOICES = (
    ('Estudiante', 'Estudiante'),
    ('Docente', 'Docente'),
    ('Administrativo', 'Administrativo')
)

class Persona(AbstractUser):
    tipo = models.CharField(max_length=15, choices=TIPO_PERSONA_CHOICES)
    ci = models.CharField(max_length=50)
