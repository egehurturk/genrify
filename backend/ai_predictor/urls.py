from django.urls import path
from ai_predictor import views

urlpatterns = [
    path('api/classify', views.classify),
]