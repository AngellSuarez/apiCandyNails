from django.contrib import admin

# Register your models here.
from .models.rolesModel import Rol,Permiso,Permiso_Rol;
from .models.usuariosModel import Usuario,Cliente,Manicurista;
from .models.citaventaModel import Servicio,CitaVenta,EstadoCita,ServicioCita;
from .models.liqHorModel import Liquidacion,Novedades;

admin.site.register(Rol)
admin.site.register(Permiso)
admin.site.register(Permiso_Rol)
admin.site.register(Manicurista)
admin.site.register(Cliente)
admin.site.register(Servicio)
admin.site.register(Usuario)
admin.site.register(CitaVenta)
admin.site.register(EstadoCita)
admin.site.register(ServicioCita)
admin.site.register(Novedades)
admin.site.register(Liquidacion)