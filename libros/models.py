from django.db import models
from decimal import Decimal

class Biblioteca(models.Model):
    """Modelo para bibliotecas con ubicación geográfica"""
    
    nombre = models.CharField(max_length=200)  # Nombre de la biblioteca
    direccion = models.CharField(max_length=300)  # Dirección postal
    ciudad = models.CharField(max_length=100)  # Ciudad
    pais = models.CharField(max_length=100, default='México')  # País
    
    # Coordenadas geográficas (se llenan automáticamente)
    latitud = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True
    )  # Latitud con 7 decimales de precisión
    
    longitud = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True
    )  # Longitud con 7 decimales de precisión
    
    # Datos adicionales de Google Maps
    place_id = models.CharField(max_length=200, blank=True)  # ID único de Google
    google_maps_url = models.URLField(blank=True)  # URL de Google Maps
    
    telefono = models.CharField(max_length=20, blank=True)  # Teléfono
    horario = models.TextField(blank=True)  # Horario de atención
    
    class Meta:
        verbose_name = 'Biblioteca'
        verbose_name_plural = 'Bibliotecas'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    @property
    def direccion_completa(self):
        """Retorna dirección formateada"""
        return f"{self.direccion}, {self.ciudad}, {self.pais}"  # Dirección completa
    
    def generar_google_maps_url(self):
        """
        Genera URL de Google Maps basada en las coordenadas
        
        Formatos disponibles:
        1. Con Place ID (más preciso): https://www.google.com/maps/place/?q=place_id:ChIJ...
        2. Con coordenadas: https://www.google.com/maps?q=lat,lng
        3. Con búsqueda: https://www.google.com/maps/search/?api=1&query=nombre+direccion
        """
        if self.place_id:
            # Opción 1: Usar Place ID (más preciso)
            return f"https://www.google.com/maps/place/?q=place_id:{self.place_id}"
        elif self.latitud and self.longitud:
            # Opción 2: Usar coordenadas
            return f"https://www.google.com/maps?q={self.latitud},{self.longitud}"
        else:
            # Opción 3: Búsqueda por texto
            import urllib.parse
            query = urllib.parse.quote(self.direccion_completa)
            return f"https://www.google.com/maps/search/?api=1&query={query}"
    
    def geocodificar(self):
        """Obtiene coordenadas de la dirección"""
        from .services import GoogleMapsService
        
        resultado = GoogleMapsService.geocodificar_direccion(self.direccion_completa)
        
        if resultado:
            self.latitud = resultado['lat']  # Guarda latitud
            self.longitud = resultado['lng']  # Guarda longitud
            self.place_id = resultado.get('place_id', '')  # Guarda Place ID
            self.google_maps_url = self.generar_google_maps_url()  # ⭐ Genera URL automáticamente
            self.save()  # Guarda en la base de datos
            return True
        return False