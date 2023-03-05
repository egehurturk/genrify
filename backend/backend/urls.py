from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ai_predictor.urls')),
]
