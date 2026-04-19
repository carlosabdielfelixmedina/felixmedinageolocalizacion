import googlemaps
from django.conf import settings
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)  # Logger para errores

class GoogleMapsService:
    """Servicio para interactuar con Google Maps API"""
    
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)  # Cliente de Google Maps
    
    @classmethod
    def geocodificar_direccion(cls, direccion):
        """
        Convierte dirección en coordenadas
        
        Args:
            direccion (str): Dirección completa
            
        Returns:
            dict: {'lat': float, 'lng': float, 'place_id': str}
        """
        try:
            service = cls()  # Instancia del servicio
            resultado = service.client.geocode(direccion)  # Llama a Geocoding API
            
            if resultado:  # Si encuentra resultados
                location = resultado[0]['geometry']['location']  # Obtiene ubicación
                place_id = resultado[0]['place_id']  # ID del lugar
                
                return {
                    'lat': Decimal(str(location['lat'])),  # Convierte a Decimal
                    'lng': Decimal(str(location['lng'])),  # Convierte a Decimal
                    'place_id': place_id,
                    'formatted_address': resultado[0]['formatted_address']  # Dirección formateada
                }
            
            return None  # No se encontró
            
        except Exception as e:
            logger.error(f"Error geocodificando: {e}")  # Registra error
            return None
    
    @classmethod
    def calcular_distancia(cls, origen, destino):
        """
        Calcula distancia entre dos puntos
        
        Args:
            origen (tuple): (lat, lng) del origen
            destino (tuple): (lat, lng) del destino
            
        Returns:
            dict: Información de distancia y duración
        """
        try:
            service = cls()
            resultado = service.client.distance_matrix(
                origins=[origen],  # Punto de inicio
                destinations=[destino],  # Punto de destino
                mode='driving',  # Modo: driving, walking, bicycling, transit
                language='es'  # Idioma español
            )
            
            if resultado['rows']:
                element = resultado['rows'][0]['elements'][0]
                
                if element['status'] == 'OK':
                    return {
                        'distancia_texto': element['distance']['text'],  # "15.2 km"
                        'distancia_metros': element['distance']['value'],  # 15200
                        'duracion_texto': element['duration']['text'],  # "25 mins"
                        'duracion_segundos': element['duration']['value']  # 1500
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error calculando distancia: {e}")
            return None