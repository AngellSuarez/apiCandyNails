from django.db import models;
from .usuariosModel import Manicurista;
from .insumoModel import Insumo;
class EstadoAbastecimiento(models.Model):
    estado = models.CharField(max_length=45,null=False);

class Abastecimiento(models.Model):
    fecha = models.DateField(null=False);
    manicurista_id = models.ForeignKey(Manicurista,on_delete=models.CASCADE);
    
    def __str__(self):
        return f"{self.fecha} - {self.cantidad} - {self.manicurista_id} - {self.insumo_id}";
    
class insumoAbastecimiento(models.Model):
    cantidad = models.IntegerField(null=False);
    insumo_id = models.ForeignKey(Insumo,on_delete=models.CASCADE);
    abastecimiento_id = models.ForeignKey(Abastecimiento,on_delete=models.CASCADE);
    estado_id = models.ForeignKey(EstadoAbastecimiento,on_delete=models.CASCADE);