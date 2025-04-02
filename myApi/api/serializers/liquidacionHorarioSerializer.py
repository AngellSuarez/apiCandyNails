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
        models = Liquidacion;
        fields = '__all__';
        #fields= ['id','manicurista_id','FechaInicial','TotalGenerado','Comision','Local','FechaFinal']
        
        def validate_manicurista(self,manicurista_id):
            try:
                Manicurista.objects.get(id=manicurista_id);
            except Manicurista.DoesNotExist:
                raise serializers.ValidationError("El manicurista ingresado no existe")
            if not manicurista_id:
                raise serializers.ValidationError("El manicurista es requerido");
            return manicurista_id;
        
        def validate(self,data):
            manicurista_liquidado = Manicurista.objects.get(id=data['manicurista_id']);
            
            fecha_inicial = data.get('FechaInicial');
            fecha_final = data.get('FechaFinal');
            
            fecha_inicial_minima = fecha_final - timedelta(days=5); #5 dias antes de la fecha 
        
            #fecha final debe ser la fecha actual
            if fecha_final != date.today():
                raise serializers.ValidationError("La fecha final debe ser la fecha actual");
            
            #fecha final debe ser maximo 5 dias antes de la fecha final
            if fecha_inicial != fecha_inicial_minima:
                raise serializers.ValidationError("La fecha inicial debe ser maximo 5 días antes de la fecha actual");
            
            #validar que no exista una liquidacion en la fecha de los 5 dias
            liquidaciones_existentes = Liquidacion.objects.filter(
                manicurista_id = manicurista_liquidado,
                fecha_final_filtrada = fecha_final,
                fecha_inicial_filtrada = fecha_inicial,
            )
            
            if liquidaciones_existentes.exists():
                ultima_liquidacion = liquidaciones_existentes.order_by("-FechaFinal").first();
                raise serializers.ValidationError({
                    "Fecha inicial":f"Ya existe una liquidación para este rango de fechas, la fecha minima permitida es {ultima_liquidacion + timedelta(days=1)}"
                })
   
            #calcular la comision y el local
            citas_venta = CitaVenta.objects.filter(
                manicurista_id = manicurista_liquidado,
                fecha__gte = fecha_inicial,
                fecha__lte = fecha_final,
            );
            total_generado = sum(cita.Total for cita in citas_venta);
            comision = total_generado * 0.5;
            local = total_generado * 0.5;
            
            data['TotalGenerado'] = total_generado;
            data['Comision'] = comision;
            data['Local'] = local;
            
            return data;