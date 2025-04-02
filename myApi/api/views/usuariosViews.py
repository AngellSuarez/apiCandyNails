from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..models.usuariosModel import Usuario, Cliente, Manicurista
from ..serializers.usuariosSerializer import UsuarioSerializer, ClienteSerializer, ManicuristaSerializer

#usuarios
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    # Sobreescribimos el método destroy para cambiar el estado en lugar de eliminar
    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        usuario.estado = "inactivo"
        usuario.save()
        return Response({"message": "Usuario desactivado correctamente"}, status=status.HTTP_200_OK)
    
    # Acción personalizada para cambiar el estado
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        usuario = self.get_object()
        nuevo_estado = "activo" if usuario.estado == "inactivo" else "inactivo"
        usuario.estado = nuevo_estado
        usuario.save()
        serializer = self.get_serializer(usuario)
        return Response({"message": f"Estado del usuario cambiado a {nuevo_estado}", "data": serializer.data})
    
    # Filtrar usuarios por estado
    @action(detail=False, methods=['get'])
    def activos(self, request):
        usuarios_activos = Usuario.objects.filter(estado="activo")
        serializer = self.get_serializer(usuarios_activos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactivos(self, request):
        usuarios_inactivos = Usuario.objects.filter(estado="inactivo")
        serializer = self.get_serializer(usuarios_inactivos, many=True)
        return Response(serializer.data)
    
    # Filtrar usuarios por rol
    @action(detail=False, methods=['get'])
    def por_rol(self, request):
        rol_id = request.query_params.get('rol_id', None)
        if rol_id:
            usuarios = Usuario.objects.filter(rol_id=rol_id)
            serializer = self.get_serializer(usuarios, many=True)
            return Response(serializer.data)
        return Response({"error": "Debe especificar un rol_id"}, status=status.HTTP_400_BAD_REQUEST)

#cliente
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    # Sobreescribimos el método destroy para cambiar el estado en lugar de eliminar
    def destroy(self, request, *args, **kwargs):
        cliente = self.get_object()
        cliente.estado = "inactivo"
        cliente.save()
        return Response({"message": "Cliente desactivado correctamente"}, status=status.HTTP_200_OK)
    
    # Acción personalizada para cambiar el estado
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        cliente = self.get_object()
        nuevo_estado = "activo" if cliente.estado == "inactivo" else "inactivo"
        cliente.estado = nuevo_estado
        cliente.save()
        serializer = self.get_serializer(cliente)
        return Response({"message": f"Estado del cliente cambiado a {nuevo_estado}", "data": serializer.data})
    
    # Filtrar clientes por estado
    @action(detail=False, methods=['get'])
    def activos(self, request):
        clientes_activos = Cliente.objects.filter(estado="activo")
        serializer = self.get_serializer(clientes_activos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactivos(self, request):
        clientes_inactivos = Cliente.objects.filter(estado="inactivo")
        serializer = self.get_serializer(clientes_inactivos, many=True)
        return Response(serializer.data)
    
    # Buscar cliente por número de documento
    @action(detail=False, methods=['get'])
    def por_documento(self, request):
        numero = request.query_params.get('numero', None)
        tipo = request.query_params.get('tipo', None)
        
        if numero:
            query = {'numero_documento': numero}
            if tipo:
                query['tipo_documento'] = tipo
                
            clientes = Cliente.objects.filter(**query)
            serializer = self.get_serializer(clientes, many=True)
            return Response(serializer.data)
        return Response({"error": "Debe especificar un número de documento"}, status=status.HTTP_400_BAD_REQUEST)

#manicuristas
class ManicuristaViewSet(viewsets.ModelViewSet):
    queryset = Manicurista.objects.all()
    serializer_class = ManicuristaSerializer
    
    # Sobreescribimos el método destroy para cambiar el estado en lugar de eliminar
    def destroy(self, request, *args, **kwargs):
        manicurista = self.get_object()
        manicurista.estado = "inactivo"
        manicurista.save()
        return Response({"message": "Manicurista desactivado correctamente"}, status=status.HTTP_200_OK)
    
    # Acción personalizada para cambiar el estado
    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        manicurista = self.get_object()
        nuevo_estado = "activo" if manicurista.estado == "inactivo" else "inactivo"
        manicurista.estado = nuevo_estado
        manicurista.save()
        serializer = self.get_serializer(manicurista)
        return Response({"message": f"Estado del manicurista cambiado a {nuevo_estado}", "data": serializer.data})
    
    # Filtrar manicuristas por estado
    @action(detail=False, methods=['get'])
    def activos(self, request):
        manicuristas_activos = Manicurista.objects.filter(estado="activo")
        serializer = self.get_serializer(manicuristas_activos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactivos(self, request):
        manicuristas_inactivos = Manicurista.objects.filter(estado="inactivo")
        serializer = self.get_serializer(manicuristas_inactivos, many=True)
        return Response(serializer.data)
    
    # Buscar manicurista por número de documento
    @action(detail=False, methods=['get'])
    def por_documento(self, request):
        numero = request.query_params.get('numero', None)
        tipo = request.query_params.get('tipo', None)
        
        if numero:
            query = {'numero_documento': numero}
            if tipo:
                query['tipo_documento'] = tipo
                
            manicuristas = Manicurista.objects.filter(**query)
            serializer = self.get_serializer(manicuristas, many=True)
            return Response(serializer.data)
        return Response({"error": "Debe especificar un número de documento"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Filtrar manicuristas por fecha de contratación
    @action(detail=False, methods=['get'])
    def por_fecha_contratacion(self, request):
        desde = request.query_params.get('desde', None)
        hasta = request.query_params.get('hasta', None)
        
        query = {}
        if desde:
            query['fecha_contratacion__gte'] = desde
        if hasta:
            query['fecha_contratacion__lte'] = hasta
            
        if query:
            manicuristas = Manicurista.objects.filter(**query)
            serializer = self.get_serializer(manicuristas, many=True)
            return Response(serializer.data)
        return Response({"error": "Debe especificar al menos una fecha (desde o hasta)"}, status=status.HTTP_400_BAD_REQUEST)