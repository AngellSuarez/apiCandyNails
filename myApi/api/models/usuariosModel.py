from django.db import models
from django.contrib.auth.models import AbstractUser
from .rolesModel import Rol;

class Usuario(AbstractUser):
    ESTADOS_CHOICES = (
        ("activo", "activo"),
        ("inactivo", "inactivo"),
    )

    nombre = models.CharField("nombre", max_length=30, null=False)
    apellido = models.CharField("apellido", max_length=30, null=False)
    correo = models.EmailField("correo", max_length=60, null=False, unique=True)
    estado = models.CharField(max_length=8, choices=ESTADOS_CHOICES, default="activo")
    rol_id = models.ForeignKey(Rol, on_delete=models.CASCADE)  # Usamos string para evitar dependencia circular

    def __str__(self):
        return self.username

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="api_usuario_groups",
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="api_usuario_user_permissions",
        related_query_name="usuario",
    )

class Cliente(models.Model):
    ESTADOS_CHOICES = (
        ("activo", "activo"),
        ("inactivo", "inactivo"),
    )

    TIPO_DOCUMENTO_CHOICES = (
        ("CC", "cedula de ciudadania"),
        ("CE", "cedula de extranjeria"),
        ("TI", "tarjeta de identidad"),
        ("RC", "registro civil"),
        ("PA", "pasaporte"),
    )

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    apellido = models.CharField(max_length=30, null=False)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES, null=False)
    numero_documento = models.CharField(max_length=15, null=False)
    correo = models.EmailField(max_length=40, null=False)
    celular = models.CharField(max_length=13, null=False)
    estado = models.CharField(max_length=8, choices=ESTADOS_CHOICES, default="activo")

    def __str__(self):
        return f"{self.nombre} - {self.apellido} - {self.correo} - ({self.estado})"

class Manicurista(models.Model):
    ESTADOS_CHOICES = (
        ("activo", "activo"),
        ("inactivo", "inactivo"),
    )

    TIPO_DOCUMENTO_CHOICES = (
        ("CC", "cedula de ciudadania"),
        ("CE", "cedula de extranjeria"),
        ("TI", "tarjeta de identidad"),
        ("RC", "registro civil"),
        ("PA", "pasaporte"),
    )

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    apellido = models.CharField(max_length=30, null=False)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES, null=False)
    numero_documento = models.CharField(max_length=15, null=False)
    correo = models.EmailField(max_length=60, null=False)
    celular = models.CharField(max_length=13, null=False)
    estado = models.CharField(max_length=8, choices=ESTADOS_CHOICES, default="activo")
    fecha_nacimiento = models.DateField(null=False)
    fecha_contratacion = models.DateField(null=False)

    def __str__(self):
        return f"{self.nombre} - {self.apellido} - {self.correo} - ({self.estado})"