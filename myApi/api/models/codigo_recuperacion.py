from django.db import models;
from django.utils import timezone;
from datetime import timedelta;
from .usuariosModel import Usuario;

class CodigoRecuperacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name ='codigos_recuperacion')
    codigo = models.CharField(max_length=6)
    creado_en = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField()
    
    def ha_expirado(self):
        return timezone.now() > self.expiracion
    
    def __str__(self):
        return f"Codigo para {self.usuario.username} ({'expirado' if self.ha_expirado() else 'activo'})"