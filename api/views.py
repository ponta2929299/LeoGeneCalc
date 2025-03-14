from django.shortcuts import render
from rest_framework import viewsets
from morph.models import Gene, Morph, ComboMorph
from .serializers import GeneSerializer, MorphSerializer, ComboMorphSerializer

class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer

class MorphViewSet(viewsets.ModelViewSet):
    queryset = Morph.objects.all()
    serializer_class = MorphSerializer

class ComboMorphViewSet(viewsets.ModelViewSet):
    queryset = ComboMorph.objects.all()
    serializer_class = ComboMorphSerializer

