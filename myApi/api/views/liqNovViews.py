from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.liqHorModel import Novedades, Liquidacion
from ..serializers.liquidacionHorarioSerializer import NovedadesSerializer, LiquidacionSerializer

class NovedadesViewSet(viewsets.ModelViewSet):
    queryset = Novedades.objects.all()
    serializer_class = NovedadesSerializer

class LiquidacionViewSet(viewsets.ModelViewSet):
    queryset = Liquidacion.objects.all()
    serializer_class = LiquidacionSerializer