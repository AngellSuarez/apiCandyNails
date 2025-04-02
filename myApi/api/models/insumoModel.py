from django.db import models;

class  Marca(models.Model):
    nombre = models.CharField(max_length=40,null=False)
    
    def __str__(self):
        return self.nombre;
    
class Insumo(models.Model):
    ESTADOS_CHOICES = (
        ("activo", "activo"),
        ("inactivo", "inactivo"),
        ("agotado", "agotado")
    );
    
    nombre = models.CharField(max_length=40,null=False)
    cantidad = models.IntegerField(null=False,default=0)
    marca_id = models.ForeignKey(Marca,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} - {self.cantidad} - {self.marca_id}";