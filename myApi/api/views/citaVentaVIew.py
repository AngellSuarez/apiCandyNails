from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.citaventaModel import EstadoCita, Servicio, CitaVenta, ServicioCita
from ..serializers.citaVentaSerializer import EstadoCitaSerializer, ServicioSerializer, CitaVentaSerializer, ServicioCitaSerializer

class EstadoCitaViewSet(viewsets.ModelViewSet):
    queryset = EstadoCita.objects.all()
    serializer_class = EstadoCitaSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

    def destroy(self, request, *args, **kwargs):
        servicio = self.get_object()
        servicio.estado = "inactivo"
        servicio.save()
        return Response({"message": "Servicio desactivado correctamente"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        servicio = self.get_object()
        nuevo_estado = "activo" if servicio.estado == "inactivo" else "inactivo"
        servicio.estado = nuevo_estado
        servicio.save()
        serializer = self.get_serializer(servicio)
        return Response({"message": f"Estado del servicio cambiado a {nuevo_estado}", "data": serializer.data})

class CitaVentaViewSet(viewsets.ModelViewSet):
    queryset = CitaVenta.objects.all()
    serializer_class = CitaVentaSerializer

    def destroy(self, request, *args, **kwargs):
        cita_venta = self.get_object()
        # Asumiendo que tienes un campo 'estado' en el modelo CitaVenta
        # y que tienes un estado 'cancelada' o similar.
        cita_venta.estado_id = EstadoCita.objects.get(Estado='cancelada') #Se debe cambiar el estado por el de cancelada.
        cita_venta.save()
        return Response({"message": "Cita de venta cancelada correctamente"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        cita_venta = self.get_object()
        nuevo_estado = EstadoCita.objects.get(Estado = "aprobada") if cita_venta.estado_id == EstadoCita.objects.get(Estado = "pendiente") else EstadoCita.objects.get(Estado = "pendiente")
        cita_venta.estado_id = nuevo_estado
        cita_venta.save()
        serializer = self.get_serializer(cita_venta)
        return Response({"message": f"Estado de la cita de venta cambiado a {nuevo_estado}", "data": serializer.data})

class ServicioCitaViewSet(viewsets.ModelViewSet):
    queryset = ServicioCita.objects.all()
    serializer_class = ServicioCitaSerializer