from rest_framework import serializers;
from ..models.usuariosModel import Usuario, Manicurista, Cliente;
from ..models.rolesModel import Rol;
from django.contrib.auth.password_validation import validate_password;

class UsuarioSerializer(serializers.ModelSerializer):
    rol_id = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all())
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'nombre', 'apellido', 'correo', 'estado', 'rol_id']
        # Hacer que la contraseña solo se pueda escribir y no leer
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate_rol_id(self, rol_id):
        #Verifica que el rol exista
        try:
            Rol.objects.get(id=rol_id.id)
        except Rol.DoesNotExist:
            raise serializers.ValidationError("El rol no existe")
        return rol_id
    
    def validate_estado(self, estado):
        #Valida que el estado sea uno de los permitidos
        estados_validos = [choice[0] for choice in Usuario.ESTADOS_CHOICES]
        if estado not in estados_validos:
            raise serializers.ValidationError(f"Estado no válido. Opciones permitidas: {estados_validos}")
        return estado
    
    def validate_password(self, password):
        #Valida la fortaleza de la contraseña
        if password:
            try:
                validate_password(password)
            except Exception as e:
                raise serializers.ValidationError(str(e))
        return password
    
    def create(self, validated_data):
        #Crea un nuevo usuario con contraseña encriptada
        password = validated_data.pop('password', None)
        # Crea la instancia pero no la guarda aún
        instance = Usuario(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        #Actualiza un usuario existente
        password = validated_data.pop('password', None)
        
        # Actualiza todos los campos excepto password
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Actualiza password solo si se proporcionó uno nuevo
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance
        
class ClienteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), write_only=True) #Agregado rol_id

    class Meta:
        model = Cliente
        fields = ['username','password','rol_id','nombre','apellido','tipo_documento','numero_documento','correo','celular','estado']

    #validar el estado
    def validate_estado(self, estado):
        estados_validos = [choice[0] for choice in Cliente.ESTADOS_CHOICES]
        if estado not in estados_validos:
            raise serializers.ValidationError(f"Estado no valido, las opciones son: {estados_validos}")
        return estado

    #validar el tipo de documento
    def validate_tipo_documento(self, tipo_documento):
        tipos_validos = [choice[0] for choice in Cliente.TIPO_DOCUMENTO_CHOICES]

        if tipo_documento not in tipos_validos:
            raise serializers.ValidationError(f"Tipo de documento no valido, las opciones son: {tipos_validos}")
        return tipo_documento

    # For ClienteSerializer
    def validate_numero_documento(self, numero_documento):
        # Get the current instance if we're updating
        instance = getattr(self, 'instance', None)
        
        # Check if this document number exists for anyone OTHER than the current instance
        if Cliente.objects.exclude(pk=instance.pk if instance else None).filter(numero_documento=numero_documento).exists():
            raise serializers.ValidationError("El numero de documento ya esta registrado")
        return numero_documento

    def validate_correo(self, correo):
        # Get the current instance if we're updating
        instance = getattr(self, 'instance', None)
        
        # If updating, exclude the current instance's email from uniqueness check
        usuario_id = None
        if instance and hasattr(instance, 'usuario'):
            usuario_id = instance.usuario.pk
            
        # Check if email exists in Cliente model (excluding current instance)
        if Cliente.objects.exclude(pk=instance.pk if instance else None).filter(correo=correo).exists():
            raise serializers.ValidationError("El correo inscrito ya existe")
            
        # Check if email exists in Usuario model (excluding current instance's usuario)
        if Usuario.objects.exclude(pk=usuario_id).filter(correo=correo).exists():
            raise serializers.ValidationError("El correo inscrito ya existe")
            
        return correo

    def validate_celular(self, celular):
        # Get the current instance if we're updating
        instance = getattr(self, 'instance', None)
        
        # If updating, exclude the current instance's phone from uniqueness check
        if Cliente.objects.exclude(pk=instance.pk if instance else None).filter(celular=celular).exists():
            raise serializers.ValidationError("El celular inscrito ya existe")
        return celular

    def validate_nombre(self, nombre):
        if not nombre:
            raise serializers.ValidationError("El nombre no puede estar en blanco")
        if len(nombre) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        if nombre.isdigit():
            raise serializers.ValidationError("El nombre no puede ser solo numeros")
        return nombre

    def validate_apellido(self, apellido):
        if not apellido:
            raise serializers.ValidationError("El apellido no puede estar en blanco")
        if len(apellido) < 3:
            raise serializers.ValidationError("El apellido debe tener al menos 3 caracteres")
        if apellido.isdigit():
            raise serializers.ValidationError("El apellido no puede ser solo numeros")
        return apellido

    def create(self, validated_data):
        # Extract fields that don't belong to Cliente model
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        rol_id = validated_data.pop('rol_id')
        
        # Extract email value to use for both Usuario and Cliente
        correo = validated_data.get('correo')
        nombre = validated_data.get('nombre', '')
        apellido = validated_data.get('apellido', '')
        
        # Create usuario with email
        usuario = Usuario.objects.create_user(
            username=username, 
            password=password, 
            rol_id=rol_id,
            correo=correo,
            nombre=nombre,
            apellido=apellido
        )
        
        # Now create the Cliente instance with the usuario relation
        cliente = Cliente.objects.create(usuario=usuario, **validated_data)
        return cliente
    
    def update(self, instance, validated_data):
        usuario = instance.usuario  # Relación OneToOne con Usuario
    
    # Campos de Usuario que podrían actualizarse desde el Cliente
        usuario_fields = ['nombre', 'apellido', 'correo']
        for field in usuario_fields:
            if field in validated_data:
                setattr(usuario, field, validated_data[field])
    
        usuario.save()

    # Actualizar campos propios de Cliente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
    
        instance.save()
        return instance

        
##manicuristas
class ManicuristaSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), write_only=True) #rol_id solo para escritura

    class Meta:
        model = Manicurista
        fields = ['username', 'password', 'nombre', 'apellido', 'tipo_documento', 'numero_documento', 'correo', 'celular', 'estado', 'fecha_nacimiento', 'fecha_contratacion', 'rol_id']

    def validate_estado(self, estado):
        estados_validos = [choice[0] for choice in Manicurista.ESTADOS_CHOICES]
        if estado not in estados_validos:
            raise serializers.ValidationError(f"Estado no valido, las opciones son: {estados_validos}")
        return estado

    def validate_tipo_documento(self, tipo):
        tipos_validos = [choice[0] for choice in Manicurista.TIPO_DOCUMENTO_CHOICES]
        if tipo not in tipos_validos:
            raise serializers.ValidationError(f"Tipo de documento no valido, las opciones son: {tipos_validos}")
        if not tipo:
            raise serializers.ValidationError("El tipo no puede estar vacio")
        return tipo

    def validate_numero_documento(self, numero_documento):
        # Get the current instance if we're updating
        instance = getattr(self, 'instance', None)
        
        # If updating, exclude the current instance from uniqueness check
        if Manicurista.objects.exclude(pk=instance.pk if instance else None).filter(numero_documento=numero_documento).exists():
            raise serializers.ValidationError("El numero de documento ya existe")
        if not numero_documento:
            raise serializers.ValidationError("El numero de documento no puede estar vacio")
        return numero_documento

    def validate_correo(self, correo):
        # Get the current instance if we're updating
        instance = getattr(self, 'instance', None)
        
        # If updating, exclude the current instance's email from uniqueness check
        usuario_id = None
        if instance and hasattr(instance, 'usuario'):
            usuario_id = instance.usuario.pk
            
        if Usuario.objects.exclude(pk=usuario_id).filter(correo=correo).exists():
            raise serializers.ValidationError("El correo ya existe")
        if not correo:
            raise serializers.ValidationError("El correo no puede estar vacio")
        return correo

    def validate_celular(self, celular):
        # Get the current instance if we're updating
        instance = getattr(self, 'instance', None)
        
        # If updating, exclude the current instance's phone from uniqueness check
        if Manicurista.objects.exclude(pk=instance.pk if instance else None).filter(celular=celular).exists():
            raise serializers.ValidationError("El celular ya esta registrado")
        return celular

    def validate_nombre(self, nombre):
        if not nombre:
            raise serializers.ValidationError("El nombre no puede estar en blanco")
        if len(nombre) < 3:
            raise serializers.ValidationError("El nombre no puede tener menos de 3 letras")
        if nombre.isdigit():
            raise serializers.ValidationError("El nombre no puede ser solo numeros")
        return nombre

    def validate_apellido(self, apellido):
        if not apellido:
            raise serializers.ValidationError("El apellido no puede estar vacio")
        if len(apellido) < 3:
            raise serializers.ValidationError("El apellido no puede tener menos de 3 letras")
        if apellido.isdigit():
            raise serializers.ValidationError("El apellido no puede ser solo numeros")
        return apellido

    def validate(self, data):
        # This method validates fields that depend on each other
        if 'fecha_contratacion' in data and 'fecha_nacimiento' in data:
            if data['fecha_contratacion'] < data['fecha_nacimiento']:
                raise serializers.ValidationError("La fecha de contrato no debe ser menor a la fecha de nacimiento")
        return data

    def create(self, validated_data):
        # Extract fields that don't belong to Manicurista model
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        rol_id = validated_data.pop('rol_id')
        
        # Extract common fields to use for both Usuario and Manicurista
        correo = validated_data.get('correo')
        nombre = validated_data.get('nombre', '')
        apellido = validated_data.get('apellido', '')
        
        # Create usuario with extracted data
        usuario = Usuario.objects.create_user(
            username=username, 
            password=password, 
            rol_id=rol_id,
            correo=correo,
            nombre=nombre,
            apellido=apellido
        )
        
        # Now create the Manicurista instance with the usuario relation
        manicurista = Manicurista.objects.create(usuario=usuario, **validated_data)
        return manicurista
    
    def update(self, instance, validated_data):
        usuario = instance.usuario

        usuario_fields = ['nombre', 'apellido', 'correo']
        for field in usuario_fields:
            if field in validated_data:
                setattr(usuario, field, validated_data[field])
    
        usuario.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
    
        instance.save()
        return instance
