#importacion de los serialzadores en orden de importancia (mentira es el orden en q los fui haciendo )

#roles-pernisos-permisoRol
from .rolesSerializer import RolSerializer,PermisoSerializer, PermisoRolSerializer;

#usuarios-cliente-manicurista
from .usuariosSerializer import UsuarioSerializer,ClienteSerializer,ManicuristaSerializer;

#insumos-marca
from .insumoSerializer import MarcaSerializer,InsumoSerializer;

#proveedores-ciudad
from .proveedoreSerializer import CiudadSerializer,ProveedorSerializer;

#cita venta-estado cita - servicio -servicio cita
from .citaVentaSerializer import CitaVentaSerializer, EstadoCitaSerializer, ServicioSerializer, ServicioCitaSerializer;

#abastecimientos 

#compras

#liquidaciones y novedades