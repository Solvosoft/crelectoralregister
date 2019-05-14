from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class PatronElectoral(models.Model):
    cedula = models.CharField(max_length=9)
    codele = models.CharField(max_length=6)
    sexo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    fechacaduc = models.CharField(max_length=8)
    junta = models.CharField(max_length=5)
    nombre = models.CharField(max_length=30)
    apellido1 = models.CharField(max_length=26)
    apellido2 = models.CharField(max_length=26)


class Distelec(models.Model):
    codele = models.CharField(max_length=6)
    provincia = models.CharField(max_length=26)
    canton = models.CharField(max_length=26)
    distrito = models.CharField(max_length=26)
