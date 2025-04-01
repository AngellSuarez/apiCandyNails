#liquidaciones y horarios pq si mkon

from django.db import models;
from .usuariosModel import Manicurista;

class Novedades(models.Model):
    manicurista_id = models.ForeignKey(Manicurista,on_delete=models.CASCADE,null=False);
    Fecha = models.DateField(null=False);
    HoraEntrada = models.TimeField(null=False);
    HoraSalida = models.TimeField(null=False);
    Motivo = models.TextField();
    
    def __str__(self):
        return f"{self.manicurista_id} - {self.Fecha} - {self.HoraEntrada} - {self.HoraSalida} - {self.Motivo}";
    
    
class Liquidacion(models.Model):
    manicurista_id = models.ForeignKey(Manicurista,on_delete=models.CASCADE,null=False);
    FechaInicial = models.DateField(null=False);
    TotalGenerado = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=0.00);
    Comision = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=0.00);
    Local = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=0.00);
    FechaFinal = models.DateField(null=False);