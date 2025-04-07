from rest_framework import serializers
from ..models.codigo_recuperacion import CodigoRecuperacion
from ..models.usuariosModel import Usuario
from django.contrib.auth.password_validation import validate_password
from django.utils import timeszone

class ConfirmacionCodigoSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    codigo = serializers.CharField(max_length=6)
    nueva_contraseña = serializers.CharField(write_only = True)
    
    def validate(self, data):
        correo = data.get('correo')
        codigo = data.get('codigo')
        password = data.get('nueva_password')
        
        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado.")
        
        try:
            registro = CodigoRecuperacion.objects.get(usuario=usuario, codigo=codigo)
        except CodigoRecuperacion.DoesNotExist:
            raise serializers.ValidationError("Codigo invalido") 
        
        if registro.ha_expirado():
            raise serializers.ValidationError("El codigo ha expirado.")
        
        #validar contraseña
        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({"password":list(e.messages)})
        
        #usuario en validated_data
        data['usuario'] = usuario
        data['registro'] = registro
        return data