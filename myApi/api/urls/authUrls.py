from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from ..views.usuariosViews import UsuarioViewSet, ClienteViewSet, ManicuristaViewSet
from ..views.authViews import LoginView, RegistroClienteView, LogoutView, user_info

from ..views.recuperarViews import SolicitarCodigoRecuperacionView, ConfirmarCodigoRecuperacionView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Auth URLs
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistroClienteView.as_view(), name='register_cliente'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', user_info, name='user_info'),
    path('password/reset-request/',SolicitarCodigoRecuperacionView.as_view(),name='reset_request'),
    path('password/reset-confirm/',ConfirmarCodigoRecuperacionView.as_view(),name='reset_confirm')
]
