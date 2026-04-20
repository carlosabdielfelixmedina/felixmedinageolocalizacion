from django.urls import path
from .views import BibliotecaListCreateView, BibliotecaDetailView

urlpatterns = [
    path('bibliotecas/', BibliotecaListCreateView.as_view(), name='biblioteca-list'),
    path('bibliotecas/<int:pk>/', BibliotecaDetailView.as_view(), name='biblioteca-detail'),
]
