from django.urls import path
from .views import BibliotecaListCreateView, BibliotecaDetailView, BibliotecasCercanasView

urlpatterns = [
    path('bibliotecas/', BibliotecaListCreateView.as_view(), name='biblioteca-list'),
    path('bibliotecas/cercanas/', BibliotecasCercanasView.as_view(), name='biblioteca-cercanas'),
    path('bibliotecas/<int:pk>/', BibliotecaDetailView.as_view(), name='biblioteca-detail'),
]
