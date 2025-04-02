from rest_framework import viewsets, status, permissions;
from rest_framework.response import Response;
from rest_framework.decorators import action;
from rest_framework.permissions import AllowAny;

#serializers y modelos
from ..models.rolesModel import Rol,Permiso,Permiso_Rol;
from ..serializers.rolesSerializer import RolSerializer,PermisoSerializer,PermisoRolSerializer;

#codigo
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all();
    serializer_class = RolSerializer;
    permission_classes = [AllowAny];
    
    #ncambiar estado
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self,request,pk=None):
        rol = self.get_object();
        nuevo_estado = "activo" if rol.estado == "inactivo" else "inactivo";
        rol.estado = nuevo_estado;
        rol.save();
        serializer = self.get_serializer(rol)
        return Response({"message":f"El estado del rol cambio a {nuevo_estado} correctamente","data":serializer.data});
    
    #cambiar el eliminar (destroy en django para inactivo)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object();
        instance.estado = "inactivo";
        instance.save()
        return Response({"message":"Rol desactivado correctamente"}, status=status.HTTP_200_OK);
    
    #filtrar roles por estado
    @action(detail=False,methods=['get'])
    def activos(self,request):
        roles_activos = Rol.objects.filter(estado="activo");
        serializer = self.get_serializer(roles_activos, many=True);
        return Response(serializer.data);
    
    @action(detail=False,methods=["get"])
    def inactivos(self,request):
        roles_inactivos = Rol.objects.filter(estado="inactivo");
        serializer = self.get_serializer(roles_inactivos, many=True);
        return Response(serializer.data);
    
#permisos
class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all();
    serializer_class = PermisoSerializer;
    permission_classes = [AllowAny];
    
    #conseguir por metodo
    @action(detail=False,methods=['get'])
    def por_modulo(self,request):
        modulo = request.query_params.get('modulo',None);
        if modulo:
            permisos = Permiso.objects.filter(modulo=modulo);
            serializer = self.get_serializer(permisos);
            return Response(serializer.data);
        return Response({"error":"Debe especificar un modulo"},status=status.HTTP_400_BAD_REQUEST)
    
#permiso-rol
class PermisoRolViewSet(viewsets.ModelViewSet):
    queryset = Permiso_Rol.objects.all()
    serializer_class = PermisoRolSerializer
    permission_classes = [AllowAny]
    
    # Obtener todos los permisos de un rol específico
    @action(detail=False, methods=['get'])
    def permisos_por_rol(self, request):
        rol_id = request.query_params.get('rol_id', None)
        if rol_id:
            permisos_roles = Permiso_Rol.objects.filter(rol_id=rol_id)
            serializer = self.get_serializer(permisos_roles, many=True)
            return Response(serializer.data)
        return Response({"error": "Debe especificar un rol_id"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Obtener todos los roles con un permiso específico
    @action(detail=False, methods=['get'])
    def roles_por_permiso(self, request):
        permiso_id = request.query_params.get('permiso_id', None)
        if permiso_id:
            permisos_roles = Permiso_Rol.objects.filter(permiso_id=permiso_id)
            serializer = self.get_serializer(permisos_roles, many=True)
            return Response(serializer.data)
        return Response({"error": "Debe especificar un permiso_id"}, status=status.HTTP_400_BAD_REQUEST)