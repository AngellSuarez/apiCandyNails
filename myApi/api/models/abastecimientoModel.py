from django.db import models;
from .usuariosModel import Manicurista;
from .insumoModel import Insumo;
class Abastecimiento(models.Model):
    fecha = models.DateField(null=False)
    manicurista_id = models.ForeignKey(Manicurista,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.fecha} - {self.cantidad} - {self.manicurista_id} - {self.insumo_id}";
    
class insumoAbastecimiento(models.Model):
    insumo_id = models.ForeignKey(Insumo,on_delete=models.CASCADE)
    abastecimiento_id = models.ForeignKey(Abastecimiento,on_delete=models.CASCADE)
    estado = models.CharField(max_length=30,null=False,default="Uso")