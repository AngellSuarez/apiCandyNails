from rest_framework import serializers;
from datetime import date,time, timedelta;
from django.db import models;
from ..models.liqHorModel import Novedades, Liquidacion;
from ..models.usuariosModel import Manicurista;
from ..models.citaventaModel import CitaVenta;

class NovedadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novedades;
        fields = '__all__'
        #fields = ['id','Fecha','HoraEntrada','HoraSalida'];
        
        def validate_manicurista_id(self,manicurista_id):
            try:
                Manicurista.objects.get(id=manicurista_id);
            except Manicurista.DoesNotExist:
                raise serializers.ValidationError("El manicurista no existe");
            if not manicurista_id:
                raise serializers.ValidationError("El manicurista es requerido");
            return manicurista_id;
        
        #validar fechas
        def validate_fecha(self,data):
            if 'Fecha' in data:
                max_fecha = date.today() + timedelta(days=7);
                if data['Fecha'] < max_fecha:
                    raise serializers.ValidationError("La fecha no puede superar 7 días desde hoy")
            
            #ver si hay mas de una novedad con esa fecha para el manicurista
            if all(k in data for k in ('manicurista_id','Fecha')):
                novedades_existentes = Novedades.objects.filter(
                    manicurista_id = data['manicurista_id'],
                    Fecha = data['Fecha'],
                );
                if self.intance:
                    novedades_existentes = novedades_existentes.exclude(id=self.instance.id);
                if novedades_existentes.exists():
                    raise serializers.ValidationError({"non_filed_errors": "El manicurista ya tiene una novedad en esa fecha"});
            return data
        
        #validate horas
        def validate_hora(self,data):
            hora_entrada_minima = time(8,0); #8 am
            hora_salida_maxima = time(18,0) #6pm
            
            if 'HoraEntrada' in data:
                if data['HoraEntrada'] < hora_entrada_minima or data['HoraEntrada'] > hora_salida_maxima:
                    raise serializers.ValidationError({"Hora: " "La hora de entrada debe ser entre las 8:00am y las 6:00pm"});
            
            if 'HoraSalida' in data:
                if data['HoraSalida'] < hora_entrada_minima or data['HoraSalida'] > hora_salida_maxima:
                    raise serializers.ValidationError({"Hora: " "La hora de salida debe estar entre las 8:00am y las 6:00pm"});
            return data;

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