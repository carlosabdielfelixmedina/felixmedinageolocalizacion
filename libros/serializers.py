from rest_framework import serializers
from .models import Biblioteca


class BibliotecaSerializer(serializers.ModelSerializer):
    direccion_completa = serializers.ReadOnlyField()

    class Meta:
        model = Biblioteca
        fields = [
            'id',
            'nombre',
            'direccion',
            'ciudad',
            'pais',
            'latitud',
            'longitud',
            'place_id',
            'google_maps_url',
            'telefono',
            'horario',
            'direccion_completa',
        ]
