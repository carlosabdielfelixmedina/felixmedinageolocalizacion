from rest_framework import generics
from .models import Biblioteca
from .serializers import BibliotecaSerializer


class BibliotecaListCreateView(generics.ListCreateAPIView):
    queryset = Biblioteca.objects.all()
    serializer_class = BibliotecaSerializer


class BibliotecaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Biblioteca.objects.all()
    serializer_class = BibliotecaSerializer

