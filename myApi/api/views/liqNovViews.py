from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.liqHorModel import Novedades, Liquidacion
from ..serializers.liquidacionHorarioSerializer import NovedadesSerializer, LiquidacionSerializer

class NovedadesViewSet(viewsets.ModelViewSet):
    serializer_class = NovedadesSerializer
    queryset = Novedades.objects.all()

    def get_queryset(self):
        manicurista_id = self.request.query_params.get('manicurista_id')
        if manicurista_id:
            return Novedades.objects.filter(manicurista_id=manicurista_id)
        return Novedades.objects.all()

class LiquidacionViewSet(viewsets.ModelViewSet):
    serializer_class = LiquidacionSerializer
    queryset = Liquidacion.objects.all()

    def get_queryset(self):
        manicurista_id = self.request.query_params.get('manicurista_id')
        if manicurista_id:
            return Liquidacion.objects.filter(manicurista_id=manicurista_id)
        return Liquidacion.objects.all()
