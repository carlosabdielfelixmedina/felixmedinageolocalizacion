import json
from decimal import Decimal
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import geodesic
from .models import Biblioteca
from .serializers import BibliotecaSerializer


class BibliotecaListCreateView(generics.ListCreateAPIView):
    queryset = Biblioteca.objects.all()
    serializer_class = BibliotecaSerializer


class BibliotecaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Biblioteca.objects.all()
    serializer_class = BibliotecaSerializer


class BibliotecasCercanasView(APIView):
    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

        if lat is None or lng is None:
            return Response(
                {'error': 'Se requieren los parámetros lat y lng.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            return Response(
                {'error': 'Los parámetros lat y lng deben ser numéricos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        origen = (lat, lng)
        bibliotecas = Biblioteca.objects.exclude(latitud=None, longitud=None)

        resultados = []
        for b in bibliotecas:
            destino = (float(b.latitud), float(b.longitud))
            distancia_km = geodesic(origen, destino).km
            datos = BibliotecaSerializer(b).data
            datos['distancia_km'] = round(distancia_km, 3)
            resultados.append(datos)

        resultados.sort(key=lambda x: x['distancia_km'])
        return Response(resultados)


class MapaView(APIView):
    def get(self, request):
        bibliotecas = Biblioteca.objects.exclude(latitud=None, longitud=None)
        datos = []
        for b in bibliotecas:
            datos.append({
                'nombre': b.nombre,
                'direccion_completa': b.direccion_completa,
                'latitud': float(b.latitud),
                'longitud': float(b.longitud),
                'telefono': b.telefono,
                'horario': b.horario,
                'google_maps_url': b.google_maps_url,
            })
        return render(request, 'libros/mapa.html', {
            'bibliotecas_json': json.dumps(datos),
            'total': len(datos),
        })

