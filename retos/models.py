from django.conf import settings
from django.db import models
from datetime import date
import datetime

# Create your models here.
class Reto(models.Model):
    nombre = models.CharField(max_length=50)
    objetivo = models.IntegerField()
    unidad = models.CharField(max_length=15)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)


    class Meta:
        db_table = "reto"

    def __str__(self):
        return self.nombre


class Progreso(models.Model):
    reto = models.ForeignKey(Reto, models.CASCADE)
    cantidad = models.FloatField()
    fecha = models.DateTimeField()
    fecha_dia = models.DateField()
    fecha_mes = models.DateField()
    


    class Meta:
        db_table = "progreso"

    def save(self, *args, **kwargs):
        self.fecha = datetime.datetime.now()
        self.fecha_dia = date.today()
        self.fecha_mes = date.today().replace(day=1)
        super(Progreso, self).save(*args, **kwargs)
