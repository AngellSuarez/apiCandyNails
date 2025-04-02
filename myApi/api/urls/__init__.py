from django.urls import path, include

urlpatterns = [
    path('citas/', include('api.urls.citaVentaUrls')),
    path('liquidaciones/', include('api.urls.liqNovUrls')),
    path('roles/', include('api.urls.rolesUrls')),
    path('usuarios/', include('api.urls.usuariosUrls')),
]