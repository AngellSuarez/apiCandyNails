from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ..models.usuariosModel import Usuario, Cliente, Manicurista
from ..models.rolesModel import Rol
from ..serializers.usuariosSerializer import ClienteSerializer
from ..utils.email_utils import enviar_correo;

# Vista personalizada para login con JWT
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Obtener información básica del usuario para devolver junto con el token
        username = request.data.get('username')
        user = get_object_or_404(Usuario, username=username)
        
        # Añadir información básica del usuario a la respuesta
        response.data['user_id'] = user.id
        response.data['username'] = user.username
        response.data['nombre'] = user.nombre
        response.data['apellido'] = user.apellido
        response.data['rol'] = user.rol_id.nombre if user.rol_id else None
        
        # Determinar el tipo de usuario y añadir su ID específico
        try:
            if user.rol_id and user.rol_id.nombre.lower() == 'cliente':
                cliente = Cliente.objects.get(usuario=user)
                response.data['cliente_id'] = cliente.id
            elif user.rol_id and user.rol_id.nombre.lower() == 'manicurista':
                manicurista = Manicurista.objects.get(usuario=user)
                response.data['manicurista_id'] = manicurista.id
        except:
            pass
            
        return response

# Vista para registro de clientes
class RegistroClienteView(generics.CreateAPIView):
    serializer_class = ClienteSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        try:
            rol_cliente = Rol.objects.get(nombre__iexact='cliente')
            data = request.data.copy()  # ✅ Hacemos una copia mutable
            data['rol_id'] = rol_cliente.id
        except Rol.DoesNotExist:
            return Response(
                {"error": "No se pudo asignar el rol de cliente"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=data)  # ✅ Usamos `data` en lugar de `request.data`
        serializer.is_valid(raise_exception=True)
        cliente = serializer.save()

        # ✅ Enviar correo de confirmación después del registro
        asunto = "Bienvenido a CandyNails 💅"
        mensaje = f"Hola {cliente.usuario.nombre}, gracias por registrarte en CandyNails. 🎉"
        enviar_correo(cliente.usuario.correo, asunto, mensaje)

        # ✅ Generar tokens JWT para el usuario recién creado
        refresh = RefreshToken.for_user(cliente.usuario)
        
        return Response({
            'cliente': serializer.data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Registro completado con éxito, revisa tu correo 📩'
        }, status=status.HTTP_201_CREATED)
        
# Vista para cerrar sesión (invalidar token)
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Vista para verificar si el token es válido y devolver información del usuario
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
        'nombre': user.nombre,
        'apellido': user.apellido,
        'correo': user.correo,
        'rol': user.rol_id.nombre if user.rol_id else None,
    }
    
    # Añadir datos específicos según el rol
    try:
        if user.rol_id and user.rol_id.nombre.lower() == 'cliente':
            cliente = Cliente.objects.get(usuario=user)
            data['cliente_id'] = cliente.id
            data['tipo_documento'] = cliente.tipo_documento
            data['numero_documento'] = cliente.numero_documento
            data['celular'] = cliente.celular
        elif user.rol_id and user.rol_id.nombre.lower() == 'manicurista':
            manicurista = Manicurista.objects.get(usuario=user)
            data['manicurista_id'] = manicurista.id
            # Añadir campos específicos de manicurista si es necesario
    except:
        pass
    
    return Response(data)