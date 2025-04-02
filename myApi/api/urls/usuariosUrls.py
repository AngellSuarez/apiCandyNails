from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.usuariosViews import UsuarioViewSet, ClienteViewSet, ManicuristaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'manicuristas', ManicuristaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]