from django.db import models;

class Ciudad (models.Model):
    nombre = models.CharField(max_length=30,null=False)
    
    def __str__(self):
        return self.nombre;
    
class Proveedor(models.Model):
    TIPO_PERSONA_CHOICES = (
        ("NATURAL", "NATURAL"),
        ("JURIDICA", "JURIDICA"),
    );
    
    TIPO_DOCUMENTO_CHOICES = (
        ("NIT", "NIT"),
        ("CC", "cedula de ciudadania"),
    );
    
    nombre = models.CharField(max_length=60,null=False)
    tipo_persona = models.CharField(max_length=8,choices=TIPO_PERSONA_CHOICES,null=False)
    tipo_documento = models.CharField(max_length=3,choices=TIPO_DOCUMENTO_CHOICES,null=False)
    numero_documento = models.CharField(max_length=15,null=False)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=60)
    direccion = models.CharField(max_length=60)
    ciudad_id = models.ForeignKey(Ciudad,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} - {self.tipo_persona} - {self.tipo_documento} - {self.numero_documento} - {self.telefono} - {self.email} - {self.direccion} - {self.ciudad_id}";