# models/__init__.py

# Modelos relacionados con roles y permisos
from .rolesModel import Rol, Permiso, Permiso_Rol

# Modelos relacionados con usuarios, clientes y manicuristas
from .usuariosModel import Usuario, Cliente, Manicurista

# Modelos relacionados con proveedores y ciudades
from .proveedoresModel import Proveedor, Ciudad

# Modelos relacionados con insumos y marcas
from .insumoModel import Insumo, Marca

# Modelos relacionados con compras y estados de compra
from .comprasModel import EstadoCompra, Compra, CompraInsumo

# Modelos relacionados con abastecimiento
from .abastecimientoModel import Abastecimiento, insumoAbastecimiento;

# Modelos relacionados con citas, ventas y servicios
from .citaventaModel import EstadoCita, CitaVenta, ServicioCita

# Modelos relacionados con liquidaciones y horarios
from .liqHorModel import Novedades, Liquidacion