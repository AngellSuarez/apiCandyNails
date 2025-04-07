from rest_framework import serializers;
from datetime import date,time, timedelta;
from django.db import models;
from ..models.liqHorModel import Novedades, Liquidacion;
from ..models.usuariosModel import Manicurista;
from ..models.citaventaModel import CitaVenta;

class NovedadesSerializer(serializers.ModelSerializer):
    manicurista_id = serializers.PrimaryKeyRelatedField(queryset=Manicurista.objects.all())
    manicurista_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Novedades
        fields = [
            'id',
            'manicurista_id',
            'Fecha',
            'HoraEntrada',
            'HoraSalida',
            'Motivo',
            'manicurista_nombre',
        ]

    def get_manicurista_nombre(self, obj):
        return f"{obj.manicurista_id.nombre} {obj.manicurista_id.apellido}"

    def validate_Fecha(self, value):
        max_fecha = date.today() + timedelta(days=7)
        if value > max_fecha:
            raise serializers.ValidationError("La fecha no puede superar 7 días desde hoy.")
        return value

    def validate_HoraEntrada(self, value):
        if value < time(8, 0) or value > time(18, 0):
            raise serializers.ValidationError("La hora de entrada debe estar entre las 8:00 AM y las 6:00 PM.")
        return value

    def validate_HoraSalida(self, value):
        if value < time(8, 0) or value > time(18, 0):
            raise serializers.ValidationError("La hora de salida debe estar entre las 8:00 AM y las 6:00 PM.")
        return value

    def validate(self, data):
        hora_entrada = data.get("HoraEntrada")
        hora_salida = data.get("HoraSalida")
        if hora_entrada and hora_salida and hora_salida <= hora_entrada:
            raise serializers.ValidationError("La hora de salida debe ser posterior a la hora de entrada.")
        return data


class LiquidacionSerializer(serializers.ModelSerializer):
    manicurista_id = serializers.PrimaryKeyRelatedField(queryset=Manicurista.objects.all())
    manicurista_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Liquidacion
        fields = [
            'id',
            'manicurista_id',
            'FechaInicial',
            'FechaFinal',
            'TotalGenerado',
            'Comision',
            'Local',
            'manicurista_nombre',
        ]

    def get_manicurista_nombre(self, obj):
        return f"{obj.manicurista_id.nombre} {obj.manicurista_id.apellido}"

    def validate_manicurista_id(self, manicurista_id):
        if not manicurista_id:
            raise serializers.ValidationError("El manicurista es requerido")
        return manicurista_id

    def validate(self, data):
        manicurista = data.get('manicurista_id')
        fecha_inicial = data.get('FechaInicial')
        fecha_final = data.get('FechaFinal')

        if not (manicurista and fecha_inicial and fecha_final):
            raise serializers.ValidationError("Debe proporcionar manicurista, fecha inicial y fecha final")

        if fecha_final != date.today():
            raise serializers.ValidationError({
                "FechaFinal": "La fecha final debe ser la fecha actual"
            })

        if fecha_inicial != fecha_final - timedelta(days=5):
            raise serializers.ValidationError({
                "FechaInicial": f"La fecha inicial debe ser exactamente 5 días antes de la fecha final ({fecha_final - timedelta(days=5)})"
            })

        liquidaciones_existentes = Liquidacion.objects.filter(
            manicurista_id=manicurista,
            FechaInicial=fecha_inicial,
            FechaFinal=fecha_final
        )
        if liquidaciones_existentes.exists():
            raise serializers.ValidationError("Ya existe una liquidación para este rango de fechas")

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
