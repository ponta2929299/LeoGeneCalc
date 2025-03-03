from django.urls import path
from . import views

urlpatterns = [
    path("", views.dominant_morph_view,name="calculate"),
    path("result/", views.result_view, name="result")
]