from django.contrib import admin
from django.utils.html import format_html
from .models import Biblioteca

@admin.register(Biblioteca)
class BibliotecaAdmin(admin.ModelAdmin):
    """Panel de administración para Bibliotecas"""
    
    # Campos a mostrar en la lista
    list_display = ['nombre', 'ciudad', 'pais', 'latitud', 'longitud', 'ver_en_mapa']
    
    # Filtros en la barra lateral
    list_filter = ['ciudad', 'pais']
    
    # Campos de búsqueda
    search_fields = ['nombre', 'direccion', 'ciudad']
    
    # Campos solo de lectura (no editables)
    readonly_fields = ['latitud', 'longitud', 'place_id', 'google_maps_url', 'ver_en_mapa']
    
    # Acción personalizada para geocodificar
    actions = ['geocodificar_seleccionadas']
    
    def ver_en_mapa(self, obj):
        """Muestra un enlace para abrir en Google Maps"""
        if obj.google_maps_url:
            return format_html(
                '<a href="{}" target="_blank" style="color: #11998e; font-weight: bold;">🗺️ Abrir en Google Maps</a>',
                obj.google_maps_url
            )
        return '-'
    
    ver_en_mapa.short_description = 'Ver en Mapa'
    
    def geocodificar_seleccionadas(self, request, queryset):
        """Geocodifica las bibliotecas seleccionadas"""
        contador = 0
        for biblioteca in queryset:
            if biblioteca.geocodificar():
                contador += 1
        
        self.message_user(request, f'{contador} bibliotecas geocodificadas exitosamente.')
    
    geocodificar_seleccionadas.short_description = "Geocodificar bibliotecas seleccionadas"