from rest_framework import serializers;
from datetime import date,time, timedelta;
from django.db import models;
from ..models.liqHorModel import Novedades, Liquidacion;
from ..models.usuariosModel import Manicurista;
from ..models.citaventaModel import CitaVenta;

class NovedadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novedades
        fields = '__all__'

    # Validar la fecha
    def validate_Fecha(self, value):
        max_fecha = date.today() + timedelta(days=7)
        if value > max_fecha:
            raise serializers.ValidationError("La fecha no puede superar 7 días desde hoy.")
        return value

    # Validar la hora de entrada
    def validate_HoraEntrada(self, value):
        hora_entrada_minima = time(8, 0)  # 8:00 AM
        hora_salida_maxima = time(18, 0)  # 6:00 PM
        
        if value < hora_entrada_minima or value > hora_salida_maxima:
            raise serializers.ValidationError("La hora de entrada debe estar entre las 8:00 AM y las 6:00 PM.")
        
        return value

    # Validar la hora de salida
    def validate_HoraSalida(self, value):
        hora_entrada_minima = time(8, 0)  # 8:00 AM
        hora_salida_maxima = time(18, 0)  # 6:00 PM
        
        if value < hora_entrada_minima or value > hora_salida_maxima:
            raise serializers.ValidationError("La hora de salida debe estar entre las 8:00 AM y las 6:00 PM.")
        
        return value

    # Validar que la hora de salida sea después de la entrada
    def validate(self, data):
        hora_entrada = data.get("HoraEntrada")
        hora_salida = data.get("HoraSalida")

        if hora_entrada and hora_salida:
            if hora_salida <= hora_entrada:
                raise serializers.ValidationError("La hora de salida debe ser posterior a la hora de entrada.")
        
        return data

class LiquidacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liquidacion
        fields = '__all__'

    def validate_manicurista_id(self, manicurista_id):
        if not manicurista_id:
            raise serializers.ValidationError("El manicurista es requerido")
        try:
            Manicurista.objects.get(id=manicurista_id.id)
        except Manicurista.DoesNotExist:
            raise serializers.ValidationError("El manicurista ingresado no existe")
        return manicurista_id

    def validate(self, data):
        manicurista = data.get('manicurista_id')
        fecha_inicial = data.get('FechaInicial')
        fecha_final = data.get('FechaFinal')

        if not (manicurista and fecha_inicial and fecha_final):
            raise serializers.ValidationError("Debe proporcionar manicurista, fecha inicial y fecha final")

        # Validar que la fecha final sea hoy
        if fecha_final != date.today():
            raise serializers.ValidationError({
                "FechaFinal": "La fecha final debe ser la fecha actual"
            })

        # Validar que la fecha inicial sea exactamente 5 días antes
        if fecha_inicial != fecha_final - timedelta(days=5):
            raise serializers.ValidationError({
                "FechaInicial": f"La fecha inicial debe ser exactamente 5 días antes de la fecha final ({fecha_final - timedelta(days=5)})"
            })

        # Verificar que no exista ya una liquidación en ese rango de fechas
        liquidaciones_existentes = Liquidacion.objects.filter(
            manicurista_id=manicurista,
            FechaInicial=fecha_inicial,
            FechaFinal=fecha_final
        )
        if liquidaciones_existentes.exists():
            raise serializers.ValidationError("Ya existe una liquidación para este rango de fechas")

        # Calcular el total generado en ese rango por el manicurista
        citas_venta = CitaVenta.objects.filter(
            manicurista_id=manicurista,
            Fecha__gte=fecha_inicial,
            Fecha__lte=fecha_final
        )

        total_generado = sum(cita.Total for cita in citas_venta)
        data['TotalGenerado'] = total_generado
        data['Comision'] = total_generado * 0.5
        data['Local'] = total_generado * 0.5

        return data