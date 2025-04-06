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
    serializer_class = CitaVentaSerializer

    def get_queryset(self):
        queryset = CitaVenta.objects.all()
        manicurista_id = self.request.query_params.get('manicurista_id')
        cliente_id = self.request.query_params.get('cliente_id')
        
        if manicurista_id is not None:
            queryset = queryset.filter(manicurista_id=manicurista_id)
        if cliente_id is not None:
            queryset = queryset.filter(cliente_id=cliente_id)
        
        return queryset

    def destroy(self, request, *args, **kwargs):
        cita_venta = self.get_object()
        estado_cancelado = EstadoCita.objects.get(estado='cancelada')
        cita_venta.estado = estado_cancelado
        cita_venta.save()
        return Response({"message": "Cita de venta cancelada correctamente"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        cita_venta = self.get_object()
        estado_pendiente = EstadoCita.objects.get(estado='pendiente')
        estado_terminada = EstadoCita.objects.get(estado='terminada')
        estado_reprogramada = EstadoCita.objects.get(estado='re programada')

        if cita_venta.estado == estado_pendiente:
            nuevo_estado = estado_terminada
        else:
            nuevo_estado = estado_reprogramada

        cita_venta.estado = nuevo_estado
        cita_venta.save()
        serializer = self.get_serializer(cita_venta)
        return Response({
            "message": f"Estado de la cita de venta cambiado a {nuevo_estado.estado}",
            "data": serializer.data
        })

class ServicioCitaViewSet(viewsets.ModelViewSet):
    queryset = ServicioCita.objects.all()
    serializer_class = ServicioCitaSerializer

    def create(self, request, *args, **kwargs):
        # Si es un solo objeto
        data = request.data.copy()
        if 'servicio_id' in data and 'subtotal' not in data:
            try:
                servicio_id = data['servicio_id']
                servicio = Servicio.objects.get(id=servicio_id)
                data['subtotal'] = servicio.precio
            except Servicio.DoesNotExist:
                pass
            except Exception as e:
                return Response(
                    {"error": f"Error al obtener precio del servicio: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], url_path='batch')
    def create_batch(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Se esperaba una lista de objetos"}, status=status.HTTP_400_BAD_REQUEST)

        created_items = []
        errors = []

        for entry in data:
            try:
                # Obtener precio si no viene incluido
                if 'servicio_id' in entry and 'subtotal' not in entry:
                    servicio_id = entry['servicio_id']
                    servicio = Servicio.objects.get(id=servicio_id)
                    entry['subtotal'] = servicio.precio

                serializer = self.get_serializer(data=entry)
                if serializer.is_valid():
                    serializer.save()
                    created_items.append(serializer.data)
                else:
                    errors.append(serializer.errors)
            except Exception as e:
                errors.append({"error": str(e)})

        if errors:
            return Response({"created": created_items, "errors": errors}, status=status.HTTP_207_MULTI_STATUS)
        return Response({"created": created_items}, status=status.HTTP_201_CREATED)
