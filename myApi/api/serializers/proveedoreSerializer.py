from rest_framework import serializers;
from ..models.proveedoresModel import Ciudad, Proveedor;

class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad;
        fields = '__all__';
        # fields = ['id', 'nombre'];
        
        def validate_nombre(self,nombre):
            if len(nombre)<3:
                raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres");
            if nombre.isdigit():
                raise serializers.ValidationError("El nombre no puede contener solo numeros");
            return nombre;
        
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor;
        fields = '__all__';
        
        def validate_tipo_documento(self,tipo_documento):
            tipo_documento_choices = [choice[0] for choice in Proveedor.TIPO_DOCUMENTO_CHOICES];
            if tipo_documento not in tipo_documento_choices:
                raise serializers.ValidationError("Tipo de documento no valido");
            if not tipo_documento:
                raise serializers.ValidationError("El tipo de documento es requerido");
            return tipo_documento;
        
        def validate_numero_documento(self,numero_documento):
            if Proveedor.objects.filter(numero_documento=numero_documento).exist():
                raise serializers.ValidationError("El numero de documento ya se encuentra registado");
            if not numero_documento:
                raise serializers.ValidationError("El numero de documento es requerido");
            return numero_documento;
        
        def validate_tipo_persona(self,tipo_persona):
            tipo_persona_choices = [choice[0] for choice in Proveedor.TIPO_PERSONA_CHOICES];
            
            if tipo_persona not in tipo_persona_choices:
                raise serializers.ValidationError(f"Tipo de persona no valido, las opciones validas son: {tipo_persona_choices}");
            if not tipo_persona:
                raise serializers.ValidationError("El tipo de persona es requerido");
            return tipo_persona;
        
        def validate_telefono(self,telefono):
            if Proveedor.objects.filter(telefono=telefono).exists():
                raise serializers.ValidationError("El telefono ya se encuentra registrado");
            if not telefono:
                raise serializers.ValidationError("El telefono es requerido");
            return telefono;
        
        def validate_email(self,email):
            if Proveedor.objects.filter(email=email).exists():
                raise serializers.ValidationError("El email ya se encuentra registado");
            if not email:
                raise serializers.ValidationError("El email es requerido");
            return email;
        
        def validate_ciudad(self,ciudad_id):
            try:
                Ciudad.objects.get(id=ciudad_id);
            except Ciudad.DoesNotExist:
                raise serializers.ValidationError("La ciudad no existe");
            return ciudad_id;