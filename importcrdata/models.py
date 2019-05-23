from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class PadronElectoral(models.Model):
    cedula = models.CharField(max_length=9)
    codele = models.CharField(max_length=6)
    sexo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    fechacaduc = models.CharField(max_length=8)
    junta = models.CharField(max_length=5)
    nombre_completo = models.CharField(max_length=90)

    class Meta:
        ordering = ['id']

class Distelec(models.Model):
    codele = models.CharField(max_length=6)
    provincia = models.CharField(max_length=26)
    canton = models.CharField(max_length=26)
    distrito = models.CharField(max_length=26)


