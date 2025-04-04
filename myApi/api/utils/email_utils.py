from django.core.mail import send_mail
from django.conf import settings

def enviar_correo(destinatario, asunto, mensaje):
    """
    Función para enviar correos electrónicos.
    """
    try:
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[destinatario],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False
