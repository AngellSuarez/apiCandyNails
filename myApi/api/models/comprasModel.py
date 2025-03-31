from django.db import models;
from .proveedoresModel import Proveedor;
from .insumoModel import Insumo;

class EstadoCompra(models.Model):
    Estado = models.CharField(max_length=40,null=False);
    
    def __str__(self):
        return self.Estado;
    
class Compra(models.Model):
    fechaIngreso = models.DateField(null=False),
    fechaCompra = models.DateField(null=False),
    total = models.DecimalField(null=False,default=0),
    IVA = models.DecimalField(max_digits=10,decimal_places=2,default=0.19),
    estadoCompra_id = models.ForeignKey(EstadoCompra,on_delete=models.CASCADE);
    proveedor_id = models.ForeignKey(Proveedor,on_delete=models.CASCADE);
    
    def __str__(self):
        return f"{self.fechaIngreso} - {self.fechaCompra} - {self.total} - {self.IVA} - {self.estadoCompra_id} - {self.proveedor_id}";
    
class CompraInsumo(models.Model):
    
    cantidad = models.IntegerField(null=False),
    precioUnitario = models.DecimalField(null=False),
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,null=False),
    compra_id = models.ForeignKey(Compra,on_delete=models.CASCADE);
    insumo_id = models.ForeignKey(Insumo,on_delete=models.CASCADE);
    
    def __str__(self):
        return f"{self.cantidad} - {self.precioUnitario} - {self.subtotal} - {self.compra_id} - {self.insumo_id}";