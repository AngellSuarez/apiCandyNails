from rest_framework import serializers;
from ..models.rolesModel import Rol, Permiso, Permiso_Rol;

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol;
        fields = '__all__';
        
        def validate_nombre(self, nombre):
            if not nombre:
                raise serializers.ValidationError("El nombre no puede estar vacio");
            if len(nombre) <3:
                raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres");
            if nombre.isdigit():
                raise serializers.ValidationError("El nombre no puede ser solo numeros");
            return nombre;
        
        def validate_descripcion(self, descripcion):
            if len(descripcion) <3:
                raise serializers.ValidationError("La descripcion debe tener al menos 3 caracteres");
            if descripcion.isdigit():
                raise serializers.ValidationError("La descripcion no puede ser solo numeros");
            return descripcion;
        
        def validate_estado(self, estado):
            if not estado:
                raise serializers.ValidationError("El estado no puede estar vacio");
            return estado;

class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso;
        fields = '__all__';
        
        def validate_modulo(self, modulo):
            if not modulo:
                raise serializers.ValidationError("El nombre no puede estar vacio");
            if len(modulo) <3:
                raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres");
            if modulo.isdigit():
                raise serializers.ValidationError("El nombre no puede ser solo numeros");
            return modulo;
        
        def validate_accion(self, accion):
            if not accion:
                raise serializers.ValidationError("El nombre no puede estar vacio");
            if len(accion) <3:
                raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres");
            if accion.isdigit():
                raise serializers.ValidationError("El nombre no puede ser solo numeros");
            return accion;
        
class PermisoRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso_Rol;
        fields = '__all__';
        
        def validate(self,data):
            rol_id = data.get('rol_id');
            permiso_id = data.get('permiso_id');
            
            if not Rol.objects.filter(id=rol_id).exists():
                raise serializers.ValidationError("El rol no existe");
            if not Permiso.objects.filter(id=permiso_id).exists():
                raise serializers.ValidationError("El permiso no existe");
            
            return data;