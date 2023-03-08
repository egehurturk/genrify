from django.urls import path
from ai_predictor import views

urlpatterns = [
    path('api/', views.inference),
    path('api/list', views._list_songs),
    path('api/classify', views.classify),
]