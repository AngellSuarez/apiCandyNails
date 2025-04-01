from django.db import models;
from .usuariosModel import Manicurista, Cliente;

class EstadoCita(models.Model):
    Estado = models.CharField(max_length=40,null=False);
    
    def __str__(self): 
        return self.Estado;
    
class Servicio(models.Model):
    ESTADOS_CHOICES = (
        ("activo", "activo"),
        ("inactivo", "inactivo"),
    );
    
    nombre = models.CharField(max_length=40,null=False);
    descripcion = models.TextField();
    precio = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=0.00);
    estado = models.CharField(max_length=40,null=False,choices=ESTADOS_CHOICES,default="activo");
    url_imagen = models.CharField(max_length=200,null=True,blank=True);
    
    def __str__(self):
        return f"{self.nombre} - {self.precio}";
    
class CitaVenta(models.Model):
    estado_id = models.ForeignKey(EstadoCita,on_delete=models.CASCADE,null=False);
    manicurista_id = models.ForeignKey(Manicurista,on_delete=models.CASCADE,null=False);
    cliente_id = models.ForeignKey(Cliente,on_delete=models.CASCADE,null=False);
    Fecha = models.DateField(null=False);
    Hora = models.TimeField(null=False);
    Descripcion = models.TextField();
    Total = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=0.00);
    
    def __str__(self):
        return f"{self.estado_id} - {self.manicurista_id} - {self.cliente_id} - {self.Fecha}- {self.Hora} - {self.Descripcion} - {self.Total}";
    
class ServicioCita(models.Model):
    cita_id = models.ForeignKey(CitaVenta,on_delete=models.CASCADE,null=False);
    servicio_id = models.ForeignKey(Servicio,on_delete=models.CASCADE,null=False);
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=0.00);
    
    def __str__(self):
        return f"{self.cita_id} - {self.servicio_id} - {self.subtotal}";