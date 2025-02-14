from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('predict/', views.predict_view, name='predict'),
    path('arduino/', views.arduino_data, name='arduino'),
]