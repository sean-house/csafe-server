from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('checkin/', views.checkin, name='checkin'),
]
