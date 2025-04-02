from django.urls import path,include;
from rest_framework.routers import DefaultRouter;
from ..views.rolesViews import RolViewSet, PermisoViewSet, PermisoRolViewSet;

router = DefaultRouter();
router.register(r'roles', RolViewSet);
router.register(r'permisos',PermisoViewSet);
router.register(r'permisos-roles',PermisoRolViewSet);

urlpatterns = [
    path('',include(router.urls)),
]