from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.citaVentaVIew import EstadoCitaViewSet, ServicioViewSet, CitaVentaViewSet, ServicioCitaViewSet

router = DefaultRouter()
router.register(r'estados-cita', EstadoCitaViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'citas-venta', CitaVentaViewSet)
router.register(r'servicios-cita', ServicioCitaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]