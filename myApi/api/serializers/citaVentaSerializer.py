from rest_framework import serializers
from django.db import models
from datetime import date, time
from ..models.citaventaModel import EstadoCita, Servicio, CitaVenta, ServicioCita
from ..models.usuariosModel import Manicurista, Cliente

class EstadoCitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCita
        fields = '__all__'
        
    def validate_Estado(self, Estado):
        if not Estado:
            raise serializers.ValidationError("El estado es requerido")
        if len(Estado) < 3:
            raise serializers.ValidationError("El estado debe tener al menos 3 caracteres")
        if Estado.isdigit():
            raise serializers.ValidationError("El estado no puede contener solo numeros")
        return Estado

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'
        
    def validate_nombre(self, nombre):
        if not nombre:
            raise serializers.ValidationError("El nombre es requerido")
        if len(nombre) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres")
        if nombre.isdigit():
            raise serializers.ValidationError("El nombre no puede contener solo numeros")
        return nombre
        
    def validate_precio(self, precio):
        if precio < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        if not precio:
            raise serializers.ValidationError("El precio es requerido")
        return precio
        
    def validate_estado(self, estado):
        estado_choices = [choice[0] for choice in Servicio.ESTADOS_CHOICES]
        if estado not in estado_choices:
            raise serializers.ValidationError(f"Estado no valido, las opciones validas son: {estado_choices}")
        if not estado:
            raise serializers.ValidationError("El estado es requerido")
        return estado

class CitaVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitaVenta
        fields = '__all__'
        
    def validate_manicurista_id(self, manicurista_id):
        try:
            Manicurista.objects.get(usuario=manicurista_id)
        except Manicurista.DoesNotExist:
            raise serializers.ValidationError("El manicurista no existe")
        if not manicurista_id:
            raise serializers.ValidationError("El manicurista es requerido")
        return manicurista_id
        
    def validate_cliente_id(self, cliente_id):
        try:
            Cliente.objects.get(usuario=cliente_id)
        except Cliente.DoesNotExist:
            raise serializers.ValidationError("El cliente no existe")
        if not cliente_id:
            raise serializers.ValidationError("El cliente es requerido")
        return cliente_id
        
    def validate_Total(self, total):
        if total < 0:
            raise serializers.ValidationError("El total no puede ser negativo")
        if not total:
            raise serializers.ValidationError("El total es requerido")
        return total
        
    def validate(self, data):
        # Validación de fecha
        if 'Fecha' in data:
            if data['Fecha'] < date.today():
                raise serializers.ValidationError({"Fecha": "La fecha no puede ser menor a la fecha actual"})
                
        # Validación de hora
        if 'Hora' in data:
            hora_apertura = time(8, 0)
            hora_cierre = time(18, 0)
            if data['Hora'] < hora_apertura or data['Hora'] > hora_cierre:
                raise serializers.ValidationError({"Hora": "La hora debe estar entre las 8:00 y las 18:00"})
                
        # Verificar si el manicurista se encuentra disponible
        if all(k in data for k in ('manicurista_id', 'Fecha', 'Hora')):
            citas_existentes = CitaVenta.objects.filter(
                manicurista_id=data['manicurista_id'],
                Fecha=data['Fecha'],
                Hora=data['Hora'], 
            )
            if self.instance:
                citas_existentes = citas_existentes.exclude(id=self.instance.id)
                
            if citas_existentes.exists():
                raise serializers.ValidationError({
                    "non_field_errors": "El manicurista ya tiene una cita agendada para esa fecha y hora"
                })
        return data

class ServicioCitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioCita
        fields = '__all__'
        
    def validate_cita_id(self, cita_id):
        try:
            CitaVenta.objects.get(id=cita_id.id)
        except CitaVenta.DoesNotExist:
            raise serializers.ValidationError("La cita no existe")
        if not cita_id:
            raise serializers.ValidationError("La cita es requerida")
        return cita_id
        
    def validate_servicio_id(self, servicio_id):
        try:
            Servicio.objects.get(id=servicio_id.id)
        except Servicio.DoesNotExist:
            raise serializers.ValidationError("El servicio no existe")
        if not servicio_id:
            raise serializers.ValidationError("El servicio es requerido")
        return servicio_id
        
    def validate_subtotal(self, subtotal):
        if subtotal < 0:
            raise serializers.ValidationError("El subtotal no puede ser negativo")
        if not subtotal:
            raise serializers.ValidationError("El subtotal es requerido")
        return subtotal
        
    def validate(self, data):
        # Validar que el servicio no este ya en la cita
        if 'cita_id' in data and 'servicio_id' in data:
            # Eliminar la instancia actual de la consulta al momento de actualizar
            query_existente = ServicioCita.objects.filter(
                cita_id=data['cita_id'],
                servicio_id=data['servicio_id'],
            )
            if self.instance:
                query_existente = query_existente.exclude(id=self.instance.id)
                
            if query_existente.exists():
                raise serializers.ValidationError({
                    "non_field_errors": "El servicio ya se encuentra registrado en la cita"
                })
        return data 
            
    def create(self, validated_data):
        servicioCita = super().create(validated_data)
        self._actualizar_total_cita(servicioCita.cita_id)
        return servicioCita
        
    def update(self, instance, validated_data):
        servicioCita = super().update(instance, validated_data)
        self._actualizar_total_cita(servicioCita.cita_id)
        return servicioCita
        
    def _actualizar_total_cita(self, cita):
        nuevo_total = ServicioCita.objects.filter(cita_id=cita).aggregate(
            total=models.Sum('subtotal')  
        )['total'] or 0  
        cita.Total = nuevo_total
        cita.save()