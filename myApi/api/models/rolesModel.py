from django.db import models

#Roles
class Rol(models.Model):
    ESTADOS_CHOICES = (
        ("activo", "activo"),
        ("inactivo", "inactivo"),
    );
    
    nombre = models.CharField(max_length=60, null=False),
    descripcion = models.CharField("No hay descripcion",max_length=80,null=True),
    estado = models.CharField(max_length=8,choices=ESTADOS_CHOICES,default="activo")
    
    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - ({self.estado})" 

class Permiso(models.Model):
    
    nombre = models.CharField(max_length=45,null=False),
    modulo = models.CharField(max_length=45,null=False),
    accion = models.CharField(max_length=45,null=False),
    
    def __str__(self):
        return f"{self.nombre} - {self.modulo} - puede({self.accion})"
    
class Permiso_Rol(models.Model):
    rol_id = models.ForeignKey(Rol,on_delete=models.CASCADE,),
    permiso_id = models.ForeignKey(Permiso,on_delete=models.CASCADE),
    
    def __str__(self):
        return f"Rol {self.rol_id} - permiso {self.permiso_id}"
