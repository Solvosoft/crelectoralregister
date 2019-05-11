from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Padron_electoral(models.Model):
    cedula = models.CharField(max_length=9)
    codelec = models.CharField(max_length=6)
    sexo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    fecha_caducidad = models.CharField(max_length=8)
    junta = models.CharField(max_length=5)
    nombre = models.CharField(max_length=30)
    primer_apellido = models.CharField(max_length=26)
    segundo_apellido = models.CharField(max_length=26)


class Distelec(models.Model):
    codele = models.CharField(max_length=6)
    provincia = models.CharField(max_length=10)
    canton = models.CharField(max_length=20)
    distrito = models.CharField(max_length=34)

