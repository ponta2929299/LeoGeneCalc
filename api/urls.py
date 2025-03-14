from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeneViewSet, MorphViewSet, ComboMorphViewSet

router = DefaultRouter()
router.register(r'genes', GeneViewSet)
router.register(r'morphs', MorphViewSet)
router.register(r'combo-morphs', ComboMorphViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]