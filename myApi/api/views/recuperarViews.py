from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from ..models.usuariosModel import Usuario
from random import randint
from datetime import timedelta

from ..models.codigo_recuperacion import CodigoRecuperacion
from ..utils.email_utils import enviar_correo

class SolicitarCodigoRecuperacionView(APIView):
    def post(self, request):
        correo = request.data.get('correo')

        if not correo:
            return Response({"error": "Debe proporcionar un correo."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return Response({"error": "No se encontró un usuario con ese correo."}, status=status.HTTP_404_NOT_FOUND)

        # Generar código de 6 dígitos
        codigo = f"{randint(100000, 999999)}"
        expiracion = timezone.now() + timedelta(minutes=10)

        # Guardar o actualizar el código en la tabla
        CodigoRecuperacion.objects.update_or_create(
            usuario=usuario,
            defaults={
                'codigo': codigo,
                'creado_en': timezone.now(),
                'expiracion': expiracion
            }
        )

        asunto = "Código de recuperación de contraseña"
        mensaje = f"Tu código de recuperación es: {codigo}. Expira en 10 minutos."

        if enviar_correo(correo, asunto, mensaje):
            return Response({"mensaje": "Código enviado al correo."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Error al enviar el correo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConfirmarCodigoRecuperacionView(APIView):
    def post(self, request):
        correo = request.data.get('correo')
        codigo = request.data.get('codigo')
        nueva_password = request.data.get('nueva_password')

        if not all([correo, codigo, nueva_password]):
            return Response({"error": "Faltan datos requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(correo=correo)
            codigo_obj = CodigoRecuperacion.objects.get(usuario=usuario, codigo=codigo)
        except (Usuario.DoesNotExist, CodigoRecuperacion.DoesNotExist):
            return Response({"error": "Código inválido o usuario no encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if codigo_obj.expiracion < timezone.now():
            return Response({"error": "El código ha expirado."}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar la contraseña
        usuario.set_password(nueva_password)
        usuario.save()

        # Eliminar el código
        codigo_obj.delete()

        return Response({"mensaje": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
