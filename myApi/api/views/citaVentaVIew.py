from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.citaventaModel import EstadoCita, Servicio, CitaVenta, ServicioCita
from ..serializers.citaVentaSerializer import EstadoCitaSerializer, ServicioSerializer, CitaVentaSerializer, ServicioCitaSerializer
from ..models.usuariosModel import Cliente, Manicurista, Usuario
from ..utils.email_utils import enviar_correo

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
    queryset = CitaVenta.objects.all()

    def get_queryset(self):
        queryset = CitaVenta.objects.all()
        manicurista_id = self.request.query_params.get('manicurista_id')
        cliente_id = self.request.query_params.get('cliente_id')
        if manicurista_id is not None:
            queryset = queryset.filter(manicurista_id=manicurista_id)
        if cliente_id is not None:
            queryset = queryset.filter(cliente_id=cliente_id)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            cita = serializer.save()

            # Obtener los datos necesarios para el correo
            cliente = Cliente.objects.get(pk=cita.cliente_id)
            manicurista = Manicurista.objects.get(pk=cita.manicurista_id)  # Asumiendo que manicurista es un Usuario

            # Preparar el contenido del correo
            asunto = "Confirmación de Cita - Servicio de Manicura"
            mensaje = f"""
Estimado/a {cliente.nombre} {cliente.apellido},

Su cita ha sido programada exitosamente.

Detalles de la cita:
- Fecha: {cita.Fecha}
- Hora: {cita.Hora}
- Manicurista: {manicurista.nombre if hasattr(manicurista, 'nombre') else "Su profesional asignado"}
- Descripción: {cita.Descripcion}
- Total: ${cita.Total}

Le esperamos en nuestra ubicación. Si necesita modificar o cancelar su cita, por favor contáctenos con anticipación.

¡Gracias por confiar en nuestros servicios!
            """

            # Enviar el correo
            enviar_correo(cliente.correo, asunto, mensaje)

            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    "message": "Cita creada correctamente y notificación enviada al cliente",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Cliente.DoesNotExist:
            return Response(
                {"error": "No se encontró información del cliente para enviar la notificación."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": f"Error al crear la cita: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            cita_venta = self.get_object()
            estado_cancelado = EstadoCita.objects.get(Estado='cancelada')
            cita_venta.estado_id = estado_cancelado  # Asume que estado_id almacena el ID del estado
            cita_venta.save()

            # Obtener el cliente para enviar el correo
            cliente = Cliente.objects.get(pk=cita_venta.cliente_id)

            # Preparar el contenido del correo
            asunto = "Cancelación de cita - Servicio de Manicura"
            mensaje = f"""
Estimado/a {cliente.nombre} {cliente.apellido},

Le informamos que su cita programada para el {cita_venta.Fecha} a las {cita_venta.Hora} ha sido cancelada.

Si tiene alguna pregunta o desea reprogramar, por favor contáctenos.

Gracias por su comprensión.
            """

            # Enviar el correo
            enviar_correo(cliente.correo, asunto, mensaje)

            return Response(
                {"message": "Cita de venta cancelada correctamente y notificación enviada al cliente"},
                status=status.HTTP_200_OK
            )
        except EstadoCita.DoesNotExist:
            return Response(
                {"error": "El estado 'cancelada' no existe."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Cliente.DoesNotExist:
            return Response(
                {"error": "No se encontró información del cliente para enviar la notificación."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": f"Error al cancelar la cita: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    
    def get_queryset(self):
        cita_id = self.request.query_params.get('cita_id')
        if cita_id:
            return ServicioCita.objects.filter(cita_id=cita_id)
        return ServicioCita.objects.all()

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
