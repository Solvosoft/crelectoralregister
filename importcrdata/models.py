from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Distelec(models.Model):
    codelec = models.CharField(max_length=6, primary_key=True)
    provincia = models.CharField(max_length=100)
    canton = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)

    def __str__(self):
        return "%s " % self.provincia

class PadronElectoral(models.Model):
    cedula = models.CharField(max_length=9,primary_key=True)
    codelec = models.ForeignKey(Distelec, on_delete=models.CASCADE)
    sexo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    fechacaduc = models.CharField(max_length=8)
    junta = models.CharField(max_length=5)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50)











