from django.db import models

# Create your models here.


class Teorema(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    formula_latex = models.CharField(max_length=200)

    def __clstr__(self):
        return self.nombre
