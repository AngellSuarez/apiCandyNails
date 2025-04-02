from django.db import models

#Roles
class Rol(models.Model):
    ESTADOS_CHOICES = (
        ("activo", "activo"),
        ("inactivo", "inactivo"),
    );
    
    nombre = models.CharField(max_length=60, null=False, default='no ingresado')
    descripcion = models.CharField("No hay descripcion",max_length=80,null=True)
    estado = models.CharField(max_length=8,choices=ESTADOS_CHOICES,default="activo")
    
    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - ({self.estado})" 

class Permiso(models.Model):
    
    modulo = models.CharField(max_length=45,null=False,default='')
    accion = models.CharField(max_length=45,null=False,default='')
    
    def __str__(self):
        return f"{self.modulo} - puede({self.accion})"
    
class Permiso_Rol(models.Model):
    rol_id = models.ForeignKey(Rol,on_delete=models.CASCADE,null=True)
    permiso_id = models.ForeignKey(Permiso,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return f"Rol {self.rol_id} - permiso {self.permiso_id}"
